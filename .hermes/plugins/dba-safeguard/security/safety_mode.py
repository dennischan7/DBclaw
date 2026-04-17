"""五档人机协同模式 — 动态安全模式切换。

五档模式:
  ULTRA_CONSERVATIVE (极度保守) — 仅自动放行L0，任何写操作强制人工审批
  MODERATE (适度，默认)         — 放行L0/L1，L2+强制人工确认并审核回滚脚本
  AGGRESSIVE (激进，开发/测试)  — 放行L0/L1/L2，仅拦截L3/L4破坏性操作
  MADMAN (疯子)                — 全量放行L0-L4，需管理员密码开启
  READONLY_AUDIT (只读审计)    — 强制锁定只读连接，纯诊断无写入权限

核心约束:
  - 模式只影响审批策略，不影响风险评估(风险等级始终客观计算)
  - 疯子模式需管理员密码验证
  - 只读审计模式从连接层强制锁定
  - 管理员可锁定模式，防止被下级用户切换
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("dba_safeguard.security.safety_mode")


# ============================================================
# Safety Mode Enum
# ============================================================

class SafetyMode(IntEnum):
    """五档人机协同安全模式。"""
    READONLY_AUDIT = 0       # 只读审计 — 最严格
    ULTRA_CONSERVATIVE = 1   # 极度保守
    MODERATE = 2             # 适度 (默认)
    AGGRESSIVE = 3           # 激进 (开发/测试)
    MADMAN = 4               # 疯子 — 最宽松, 需管理员密码

    @property
    def display_name(self) -> str:
        _names = {
            0: "只读审计模式",
            1: "极度保守模式",
            2: "适度模式",
            3: "激进模式",
            4: "疯子模式",
        }
        return _names[self.value]

    @property
    def description(self) -> str:
        _desc = {
            0: "强制锁定只读连接，纯诊断无写入权限",
            1: "仅自动放行L0，任何写操作强制人工审批",
            2: "放行L0/L1，L2及以上强制人工确认并审核回滚脚本",
            3: "放行L0/L1/L2，仅拦截L3/L4破坏性操作",
            4: "全量放行L0-L4，无阻断自动执行（需管理员密码）",
        }
        return _desc[self.value]


# ============================================================
# Mode ↔ Auto-approve threshold mapping
# ============================================================

# 每个模式下，≤ 此等级自动放行，> 此等级需人工审批
# READONLY_AUDIT: -1 (无任何自动放行)
# MADMAN: 4 (全量放行)
MODE_AUTO_APPROVE_THRESHOLD: Dict[SafetyMode, int] = {
    SafetyMode.READONLY_AUDIT: -1,       # 无写操作放行
    SafetyMode.ULTRA_CONSERVATIVE: 0,    # 仅L0自动放行
    SafetyMode.MODERATE: 1,              # L0/L1自动放行
    SafetyMode.AGGRESSIVE: 2,            # L0/L1/L2自动放行
    SafetyMode.MADMAN: 4,                # 全量自动放行
}

# 只读审计模式下连接强制只读
READONLY_MODES = frozenset({SafetyMode.READONLY_AUDIT})

# 需要回滚脚本审核的最低等级 (按模式)
MODE_REQUIRE_ROLLBACK_ABOVE: Dict[SafetyMode, int] = {
    SafetyMode.READONLY_AUDIT: -1,       # N/A — 无写操作
    SafetyMode.ULTRA_CONSERVATIVE: 0,    # L1+需回滚
    SafetyMode.MODERATE: 1,              # L2+需回滚
    SafetyMode.AGGRESSIVE: 2,            # L3+需回滚
    SafetyMode.MADMAN: 99,               # 不需要回滚审核
}


# ============================================================
# Password Hashing
# ============================================================

def _hash_password(password: str) -> str:
    """SHA-256 hash for admin password (加盐)."""
    salt = "dba-safeguard-admin-salt-v1"
    return hashlib.sha256(f"{salt}:{password}".encode()).hexdigest()


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify password against stored hash."""
    return _hash_password(password) == stored_hash


# ============================================================
# Persistence
# ============================================================

_DB_PATH: Optional[Path] = None


def set_safety_mode_db_path(path: Path) -> None:
    """Override DB path (for testing)."""
    global _DB_PATH
    _DB_PATH = path


def _get_db_path() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    return Path(__file__).parent.parent / "data" / "safety_mode.db"


def _get_conn() -> sqlite3.Connection:
    db_path = _get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    _init_tables(conn)
    return conn


def _init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS mode_state (
            key         TEXT PRIMARY KEY,
            value       TEXT NOT NULL,
            updated_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS mode_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            old_mode    INTEGER NOT NULL,
            new_mode    INTEGER NOT NULL,
            changed_by  TEXT NOT NULL DEFAULT 'system',
            reason      TEXT NOT NULL DEFAULT '',
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS admin_password (
            id          INTEGER PRIMARY KEY CHECK (id = 1),
            password_hash TEXT NOT NULL,
            set_at      TEXT NOT NULL DEFAULT (datetime('now')),
            set_by      TEXT NOT NULL DEFAULT 'admin'
        );
    """)
    conn.commit()


# ============================================================
# Mode State Management
# ============================================================

def get_current_mode() -> SafetyMode:
    """Get current safety mode. Defaults to MODERATE."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT value FROM mode_state WHERE key='current_mode'"
        ).fetchone()
        if row:
            return SafetyMode(int(row["value"]))
        return SafetyMode.MODERATE
    except (ValueError, Exception):
        return SafetyMode.MODERATE
    finally:
        conn.close()


def is_mode_locked() -> bool:
    """Check if mode is locked by admin."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT value FROM mode_state WHERE key='mode_locked'"
        ).fetchone()
        return row is not None and row["value"] == "1"
    finally:
        conn.close()


def get_mode_lock_info() -> Optional[Dict[str, str]]:
    """Get lock info if mode is locked."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT value FROM mode_state WHERE key='locked_by'"
        ).fetchone()
        if row:
            return {"locked_by": row["value"]}
        return None
    finally:
        conn.close()


def switch_mode(
    new_mode: SafetyMode,
    changed_by: str = "user",
    admin_password: Optional[str] = None,
    reason: str = "",
) -> Dict[str, Any]:
    """Switch safety mode.

    Args:
        new_mode: Target safety mode
        changed_by: User performing the switch
        admin_password: Required for MADMAN mode
        reason: Reason for switch

    Returns:
        dict with success/error info
    """
    # Check lock
    if is_mode_locked() and changed_by != "admin":
        return {
            "success": False,
            "error": "安全模式已被管理员锁定，不可切换",
        }

    old_mode = get_current_mode()

    # MADMAN mode requires admin password
    if new_mode == SafetyMode.MADMAN:
        if not admin_password:
            return {
                "success": False,
                "error": "切换到疯子模式需要管理员密码",
            }
        if not verify_admin_password(admin_password):
            return {
                "success": False,
                "error": "管理员密码错误",
            }

    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO mode_state (key, value) VALUES ('current_mode', ?)",
            (str(new_mode.value),),
        )
        conn.execute(
            "INSERT INTO mode_history (old_mode, new_mode, changed_by, reason) VALUES (?, ?, ?, ?)",
            (old_mode.value, new_mode.value, changed_by, reason),
        )
        conn.commit()

        logger.info(
            "Safety mode switched: %s → %s by %s (%s)",
            old_mode.display_name, new_mode.display_name, changed_by, reason,
        )

        return {
            "success": True,
            "old_mode": old_mode.value,
            "new_mode": new_mode.value,
            "old_mode_name": old_mode.display_name,
            "new_mode_name": new_mode.display_name,
        }
    finally:
        conn.close()


def lock_mode(locked_by: str = "admin") -> bool:
    """Lock current mode (admin only)."""
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO mode_state (key, value) VALUES ('mode_locked', '1')"
        )
        conn.execute(
            "INSERT OR REPLACE INTO mode_state (key, value) VALUES ('locked_by', ?)",
            (locked_by,),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def unlock_mode() -> bool:
    """Unlock mode (admin only)."""
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM mode_state WHERE key='mode_locked'")
        conn.execute("DELETE FROM mode_state WHERE key='locked_by'")
        conn.commit()
        return True
    finally:
        conn.close()


# ============================================================
# Admin Password Management
# ============================================================

def set_admin_password(password: str, set_by: str = "admin") -> bool:
    """Set or update admin password (for MADMAN mode)."""
    if len(password) < 6:
        return False
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO admin_password (id, password_hash, set_by) "
            "VALUES (1, ?, ?)",
            (_hash_password(password), set_by),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def verify_admin_password(password: str) -> bool:
    """Verify admin password."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT password_hash FROM admin_password WHERE id=1"
        ).fetchone()
        if not row:
            return False
        return _verify_password(password, row["password_hash"])
    finally:
        conn.close()


def has_admin_password() -> bool:
    """Check if admin password has been set."""
    conn = _get_conn()
    try:
        row = conn.execute("SELECT 1 FROM admin_password WHERE id=1").fetchone()
        return row is not None
    finally:
        conn.close()


# ============================================================
# Mode Decision Engine
# ============================================================

def should_auto_approve(risk_level: int) -> bool:
    """Check if a given risk level should auto-approve under current mode."""
    mode = get_current_mode()
    threshold = MODE_AUTO_APPROVE_THRESHOLD.get(mode, 1)
    return risk_level <= threshold


def should_block_write(risk_level: int) -> bool:
    """Check if write should be completely blocked (READONLY_AUDIT)."""
    mode = get_current_mode()
    if mode in READONLY_MODES and risk_level > 0:
        return True
    return False


def requires_rollback_review(risk_level: int) -> bool:
    """Check if rollback script review is required."""
    mode = get_current_mode()
    threshold = MODE_REQUIRE_ROLLBACK_ABOVE.get(mode, 1)
    return risk_level > threshold


def get_approval_decision(risk_level: int) -> Dict[str, Any]:
    """Get the full approval decision for a given risk level.

    Returns:
        dict with:
          - action: "auto_approve" | "human_confirm" | "force_block" | "readonly_block"
          - require_approval: bool
          - require_rollback: bool
          - mode: current mode name
          - reason: explanation
    """
    mode = get_current_mode()
    threshold = MODE_AUTO_APPROVE_THRESHOLD.get(mode, 1)
    rollback_threshold = MODE_REQUIRE_ROLLBACK_ABOVE.get(mode, 1)

    # READONLY_AUDIT: block all writes
    if mode in READONLY_MODES and risk_level > 0:
        return {
            "action": "readonly_block",
            "require_approval": False,
            "require_rollback": False,
            "mode": mode.display_name,
            "reason": f"只读审计模式下禁止任何写操作 (L{risk_level})",
        }

    # Auto-approve within threshold
    if risk_level <= threshold:
        action = "auto_approve" if risk_level == 0 else "notify_approve"
        return {
            "action": action,
            "require_approval": False,
            "require_rollback": risk_level > rollback_threshold,
            "mode": mode.display_name,
            "reason": f"{mode.display_name}下L{risk_level}自动放行",
        }

    # Above threshold: human confirm or force block
    if risk_level >= 3:
        return {
            "action": "force_block",
            "require_approval": True,
            "require_rollback": True,
            "mode": mode.display_name,
            "reason": f"{mode.display_name}下L{risk_level}强制阻断，需管理员审批",
        }

    return {
        "action": "human_confirm",
        "require_approval": True,
        "require_rollback": risk_level > rollback_threshold,
        "mode": mode.display_name,
        "reason": f"{mode.display_name}下L{risk_level}需人工确认",
    }


def get_mode_history(limit: int = 20) -> List[Dict[str, Any]]:
    """Get mode switch history."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT id, old_mode, new_mode, changed_by, reason, created_at "
            "FROM mode_history ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        results = []
        for r in rows:
            results.append({
                "id": r["id"],
                "old_mode": SafetyMode(r["old_mode"]).display_name,
                "new_mode": SafetyMode(r["new_mode"]).display_name,
                "changed_by": r["changed_by"],
                "reason": r["reason"],
                "created_at": r["created_at"],
            })
        return results
    finally:
        conn.close()


def list_modes() -> List[Dict[str, Any]]:
    """List all available safety modes."""
    current = get_current_mode()
    return [
        {
            "mode": m.value,
            "name": m.display_name,
            "description": m.description,
            "active": m == current,
            "auto_approve_threshold": MODE_AUTO_APPROVE_THRESHOLD[m],
        }
        for m in SafetyMode
    ]
