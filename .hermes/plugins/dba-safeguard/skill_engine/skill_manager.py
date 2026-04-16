"""DBA技能库管理器 — 统一技能生命周期管理。

核心能力:
  - 6.1 DBA内置技能库注册与元数据管理
  - 6.4 技能权限管控 (admin/developer/readonly 三级角色)
  - 版本管理 (保留所有历史版本，支持回滚)
  - 启用/禁用开关
  - 使用统计追踪
  - 为 skill_generator 和 skill_optimizer 提供持久化后端

角色权限:
  - ADMIN: 所有技能可用，可修改内置技能
  - DEVELOPER: L0-L3 相关技能可用
  - READONLY: 仅查询类技能可用 (risk_level=0)

数据库表:
  - skills: 技能注册 (名称/分类/风险/来源/权限/状态)
  - skill_versions: 版本历史
  - skill_executions: 执行记录
  - skill_drafts: 待确认的生成草案
  - skill_patches: 待确认的优化补丁
"""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
import time
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.skill_engine.skill_manager")


# ============================================================
# User Role
# ============================================================

class UserRole(IntEnum):
    READONLY = 0
    DEVELOPER = 1
    ADMIN = 2


_ROLE_MAP = {
    "readonly": UserRole.READONLY,
    "developer": UserRole.DEVELOPER,
    "admin": UserRole.ADMIN,
}


def parse_role(role_str: str) -> UserRole:
    """Parse role string to UserRole enum."""
    return _ROLE_MAP.get(role_str.lower(), UserRole.READONLY)


# ============================================================
# Built-in Skills Metadata
# ============================================================

_BUILTIN_SKILLS = [
    {
        "name": "dba-sql-safe",
        "display_name": "SQL安全生成与优化",
        "description": "安全地生成SQL语句，确保语法正确、方言兼容、风险可控",
        "category": "query",
        "risk_level": 0,
        "min_role": "readonly",
        "file_name": "sql-safe-generation.md",
    },
    {
        "name": "dba-ddl-change",
        "display_name": "DDL变更全流程执行",
        "description": "安全执行数据库结构变更，确保回滚可行、影响可控",
        "category": "ddl",
        "risk_level": 2,
        "min_role": "developer",
        "file_name": "ddl-change-workflow.md",
    },
    {
        "name": "dba-health-check",
        "display_name": "数据库健康巡检",
        "description": "对数据库实例执行健康检查，识别性能瓶颈和配置问题",
        "category": "health",
        "risk_level": 0,
        "min_role": "readonly",
        "file_name": "health-check.md",
    },
    {
        "name": "dba-index-optimize",
        "display_name": "索引优化建议",
        "description": "分析查询执行计划，识别缺失索引或冗余索引，给出优化建议",
        "category": "optimize",
        "risk_level": 1,
        "min_role": "developer",
        "file_name": "index-optimization.md",
    },
    {
        "name": "dba-troubleshoot",
        "display_name": "故障排查根因分析",
        "description": "诊断和解决数据库常见故障，包括死锁、慢查询、连接耗尽等",
        "category": "troubleshoot",
        "risk_level": 0,
        "min_role": "readonly",
        "file_name": "troubleshooting.md",
    },
]


# ============================================================
# Database Singleton
# ============================================================

_DB_PATH: Optional[Path] = None
_CONN: Optional[sqlite3.Connection] = None


def set_skill_db_path(path: Path) -> None:
    """Override DB path for testing."""
    global _DB_PATH, _CONN
    if _CONN is not None:
        _CONN.close()
        _CONN = None
    _DB_PATH = path


def _get_db() -> sqlite3.Connection:
    global _CONN, _DB_PATH
    if _CONN is not None:
        return _CONN

    if _DB_PATH is None:
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        _DB_PATH = data_dir / "skill_manager.db"

    _CONN = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    _CONN.execute("PRAGMA journal_mode=WAL")
    _CONN.row_factory = sqlite3.Row
    _init_tables(_CONN)
    _register_builtins(_CONN)
    return _CONN


def _get_skills_dir() -> Path:
    """Get the built-in skills markdown directory."""
    return Path(__file__).parent.parent / "skills"


def _get_generated_dir() -> Path:
    """Get the directory for generated skill files.

    In test mode (custom DB path), uses DB path's parent to keep
    generated files alongside the test database.
    """
    if _DB_PATH:
        gen_dir = _DB_PATH.parent / "generated_skills"
    else:
        gen_dir = Path(__file__).parent.parent / "data" / "generated_skills"
    gen_dir.mkdir(parents=True, exist_ok=True)
    return gen_dir


# ============================================================
# Schema
# ============================================================

def _init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS skills (
            name TEXT PRIMARY KEY,
            display_name TEXT NOT NULL,
            description TEXT DEFAULT '',
            category TEXT DEFAULT 'general',
            risk_level INTEGER DEFAULT 0,
            source TEXT DEFAULT 'builtin',
            file_name TEXT DEFAULT '',
            enabled INTEGER DEFAULT 1,
            min_role TEXT DEFAULT 'readonly',
            current_version TEXT DEFAULT '1.0.0',
            created_at REAL,
            updated_at REAL
        );

        CREATE TABLE IF NOT EXISTS skill_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            version TEXT NOT NULL,
            content_hash TEXT NOT NULL,
            change_summary TEXT DEFAULT '',
            author TEXT DEFAULT 'system',
            created_at REAL,
            UNIQUE(skill_name, version)
        );

        CREATE TABLE IF NOT EXISTS skill_executions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            skill_name TEXT NOT NULL,
            task_id TEXT DEFAULT '',
            success INTEGER DEFAULT 0,
            duration_ms INTEGER DEFAULT 0,
            error_message TEXT DEFAULT '',
            created_at REAL
        );

        CREATE TABLE IF NOT EXISTS skill_drafts (
            draft_id TEXT PRIMARY KEY,
            skill_name TEXT NOT NULL,
            content TEXT NOT NULL,
            trigger_reason TEXT DEFAULT '',
            experience_ids TEXT DEFAULT '[]',
            status TEXT DEFAULT 'pending',
            created_at REAL,
            reviewed_at REAL
        );

        CREATE TABLE IF NOT EXISTS skill_patches (
            patch_id TEXT PRIMARY KEY,
            skill_name TEXT NOT NULL,
            old_version TEXT NOT NULL,
            new_content TEXT NOT NULL,
            change_summary TEXT NOT NULL,
            improvements TEXT DEFAULT '{}',
            status TEXT DEFAULT 'pending',
            created_at REAL,
            reviewed_at REAL
        );
    """)


def _register_builtins(conn: sqlite3.Connection) -> None:
    """Register built-in skills if not already present."""
    now = time.time()
    for skill in _BUILTIN_SKILLS:
        conn.execute("""
            INSERT OR IGNORE INTO skills
            (name, display_name, description, category, risk_level,
             source, file_name, enabled, min_role, current_version,
             created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'builtin', ?, 1, ?, '1.0.0', ?, ?)
        """, (
            skill["name"], skill["display_name"], skill["description"],
            skill["category"], skill["risk_level"], skill["file_name"],
            skill["min_role"], now, now,
        ))
    conn.commit()


# ============================================================
# Discovery & Listing
# ============================================================

def list_skills(
    user_role: UserRole = UserRole.ADMIN,
    include_disabled: bool = False,
) -> List[Dict[str, Any]]:
    """List skills filtered by role and enabled status."""
    db = _get_db()
    query = "SELECT * FROM skills"
    if not include_disabled:
        query += " WHERE enabled = 1"
    query += " ORDER BY category, risk_level, name"

    rows = db.execute(query).fetchall()
    result = []
    for row in rows:
        skill = dict(row)
        min_role = parse_role(skill.get("min_role", "readonly"))
        if user_role >= min_role:
            result.append(skill)
    return result


def get_skill(name: str) -> Optional[Dict[str, Any]]:
    """Get skill metadata by name."""
    db = _get_db()
    row = db.execute("SELECT * FROM skills WHERE name = ?", (name,)).fetchone()
    return dict(row) if row else None


def get_skill_content(name: str) -> Optional[str]:
    """Read skill markdown content from file."""
    skill = get_skill(name)
    if not skill:
        return None

    file_name = skill.get("file_name", "")
    if not file_name:
        return None

    if skill["source"] == "builtin":
        path = _get_skills_dir() / file_name
    else:
        path = _get_generated_dir() / file_name

    if path.exists():
        return path.read_text(encoding="utf-8")
    return None


# ============================================================
# Permission Checking
# ============================================================

def check_permission(user_role: UserRole, skill_name: str) -> bool:
    """Check if a user role can use a skill."""
    skill = get_skill(skill_name)
    if not skill:
        return False
    if not skill.get("enabled", True):
        return False
    min_role = parse_role(skill.get("min_role", "readonly"))
    return user_role >= min_role


def get_allowed_skills(user_role: UserRole) -> List[Dict[str, Any]]:
    """Get all skills accessible to a role."""
    return list_skills(user_role=user_role, include_disabled=False)


# ============================================================
# Enable / Disable
# ============================================================

def enable_skill(name: str) -> bool:
    """Enable a skill."""
    db = _get_db()
    cur = db.execute(
        "UPDATE skills SET enabled = 1, updated_at = ? WHERE name = ?",
        (time.time(), name),
    )
    db.commit()
    return cur.rowcount > 0


def disable_skill(name: str) -> bool:
    """Disable a skill. Disabled skills cannot be invoked by AI."""
    db = _get_db()
    cur = db.execute(
        "UPDATE skills SET enabled = 0, updated_at = ? WHERE name = ?",
        (time.time(), name),
    )
    db.commit()
    return cur.rowcount > 0


# ============================================================
# Version Management
# ============================================================

def save_version(
    skill_name: str,
    content: str,
    version: str,
    change_summary: str = "",
    author: str = "system",
) -> bool:
    """Save a new version of a skill. Returns False on duplicate."""
    db = _get_db()
    content_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
    try:
        db.execute("""
            INSERT INTO skill_versions
            (skill_name, version, content_hash, change_summary, author, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (skill_name, version, content_hash, change_summary, author, time.time()))
        db.execute(
            "UPDATE skills SET current_version = ?, updated_at = ? WHERE name = ?",
            (version, time.time(), skill_name),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def get_versions(skill_name: str) -> List[Dict[str, Any]]:
    """Get all versions of a skill, newest first."""
    db = _get_db()
    rows = db.execute("""
        SELECT * FROM skill_versions
        WHERE skill_name = ? ORDER BY created_at DESC
    """, (skill_name,)).fetchall()
    return [dict(r) for r in rows]


def get_latest_version(skill_name: str) -> Optional[str]:
    """Get the current version string of a skill."""
    skill = get_skill(skill_name)
    return skill.get("current_version") if skill else None


def rollback_version(skill_name: str, version: str) -> bool:
    """Rollback a skill to a previous version."""
    db = _get_db()
    row = db.execute(
        "SELECT content_hash FROM skill_versions WHERE skill_name = ? AND version = ?",
        (skill_name, version),
    ).fetchone()
    if not row:
        return False
    db.execute(
        "UPDATE skills SET current_version = ?, updated_at = ? WHERE name = ?",
        (version, time.time(), skill_name),
    )
    db.commit()
    return True


# ============================================================
# Execution Tracking
# ============================================================

def record_execution(
    skill_name: str,
    task_id: str = "",
    success: bool = True,
    duration_ms: int = 0,
    error: str = "",
) -> None:
    """Record a skill execution result."""
    db = _get_db()
    db.execute("""
        INSERT INTO skill_executions
        (skill_name, task_id, success, duration_ms, error_message, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (skill_name, task_id, int(success), duration_ms, error, time.time()))
    db.commit()


def get_execution_stats(skill_name: str) -> Dict[str, Any]:
    """Get aggregated execution statistics for a skill."""
    db = _get_db()
    row = db.execute("""
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN success = 1 THEN 1 ELSE 0 END) AS successes,
            AVG(duration_ms) AS avg_duration_ms,
            MAX(created_at) AS last_used
        FROM skill_executions WHERE skill_name = ?
    """, (skill_name,)).fetchone()

    if not row or row["total"] == 0:
        return {
            "total": 0, "successes": 0, "success_rate": 0.0,
            "avg_duration_ms": 0, "last_used": None,
        }

    return {
        "total": row["total"],
        "successes": row["successes"],
        "success_rate": row["successes"] / row["total"] if row["total"] else 0,
        "avg_duration_ms": int(row["avg_duration_ms"] or 0),
        "last_used": row["last_used"],
    }


# ============================================================
# Draft Management (for skill_generator)
# ============================================================

def save_draft(
    draft_id: str,
    skill_name: str,
    content: str,
    trigger_reason: str = "",
    experience_ids: Optional[List[str]] = None,
) -> None:
    """Save a generated skill draft as pending."""
    db = _get_db()
    db.execute("""
        INSERT OR REPLACE INTO skill_drafts
        (draft_id, skill_name, content, trigger_reason, experience_ids, status, created_at)
        VALUES (?, ?, ?, ?, ?, 'pending', ?)
    """, (
        draft_id, skill_name, content, trigger_reason,
        json.dumps(experience_ids or []), time.time(),
    ))
    db.commit()


def get_pending_drafts() -> List[Dict[str, Any]]:
    """Get all pending skill drafts awaiting confirmation."""
    db = _get_db()
    rows = db.execute(
        "SELECT * FROM skill_drafts WHERE status = 'pending' ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def get_draft(draft_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific draft by ID."""
    db = _get_db()
    row = db.execute(
        "SELECT * FROM skill_drafts WHERE draft_id = ?", (draft_id,)
    ).fetchone()
    return dict(row) if row else None


def confirm_draft(draft_id: str) -> bool:
    """Confirm a pending draft: install skill + save version + write file."""
    db = _get_db()
    draft = get_draft(draft_id)
    if not draft or draft["status"] != "pending":
        return False

    now = time.time()
    skill_name = draft["skill_name"]
    file_name = f"{skill_name}.md"

    # Install the skill
    db.execute("""
        INSERT OR REPLACE INTO skills
        (name, display_name, description, category, risk_level,
         source, file_name, enabled, min_role, current_version,
         created_at, updated_at)
        VALUES (?, ?, ?, 'general', 1, 'generated', ?, 1, 'developer', '1.0.0', ?, ?)
    """, (
        skill_name, skill_name,
        f"Auto-generated: {draft['trigger_reason']}",
        file_name, now, now,
    ))

    # Save content to file
    gen_dir = _get_generated_dir()
    (gen_dir / file_name).write_text(draft["content"], encoding="utf-8")

    # Save version
    content_hash = hashlib.sha256(draft["content"].encode()).hexdigest()[:16]
    db.execute("""
        INSERT OR IGNORE INTO skill_versions
        (skill_name, version, content_hash, change_summary, author, created_at)
        VALUES (?, '1.0.0', ?, ?, 'generator', ?)
    """, (skill_name, content_hash, draft["trigger_reason"], now))

    # Update draft status
    db.execute(
        "UPDATE skill_drafts SET status = 'confirmed', reviewed_at = ? WHERE draft_id = ?",
        (now, draft_id),
    )
    db.commit()
    return True


def reject_draft(draft_id: str) -> bool:
    """Reject a pending draft."""
    db = _get_db()
    cur = db.execute(
        "UPDATE skill_drafts SET status = 'rejected', reviewed_at = ? "
        "WHERE draft_id = ? AND status = 'pending'",
        (time.time(), draft_id),
    )
    db.commit()
    return cur.rowcount > 0


# ============================================================
# Patch Management (for skill_optimizer)
# ============================================================

def save_patch(
    patch_id: str,
    skill_name: str,
    old_version: str,
    new_content: str,
    change_summary: str,
    improvements: Optional[Dict] = None,
) -> None:
    """Save an optimization patch as pending."""
    db = _get_db()
    db.execute("""
        INSERT OR REPLACE INTO skill_patches
        (patch_id, skill_name, old_version, new_content, change_summary,
         improvements, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, 'pending', ?)
    """, (
        patch_id, skill_name, old_version, new_content, change_summary,
        json.dumps(improvements or {}), time.time(),
    ))
    db.commit()


def get_pending_patches() -> List[Dict[str, Any]]:
    """Get all pending optimization patches."""
    db = _get_db()
    rows = db.execute(
        "SELECT * FROM skill_patches WHERE status = 'pending' ORDER BY created_at DESC"
    ).fetchall()
    return [dict(r) for r in rows]


def get_patch(patch_id: str) -> Optional[Dict[str, Any]]:
    """Get a specific patch by ID."""
    db = _get_db()
    row = db.execute(
        "SELECT * FROM skill_patches WHERE patch_id = ?", (patch_id,)
    ).fetchone()
    return dict(row) if row else None


def confirm_patch(patch_id: str) -> bool:
    """Confirm a pending patch: update skill version + write file."""
    db = _get_db()
    patch = get_patch(patch_id)
    if not patch or patch["status"] != "pending":
        return False

    now = time.time()
    skill_name = patch["skill_name"]

    # Determine new version (increment patch number)
    old_ver = patch["old_version"]
    parts = old_ver.split(".")
    new_ver = f"{parts[0]}.{parts[1]}.{int(parts[2]) + 1}"

    # Save new content to file (for generated skills)
    skill = get_skill(skill_name)
    if skill and skill["source"] == "generated" and skill.get("file_name"):
        gen_dir = _get_generated_dir()
        (gen_dir / skill["file_name"]).write_text(
            patch["new_content"], encoding="utf-8"
        )

    # Save version
    content_hash = hashlib.sha256(patch["new_content"].encode()).hexdigest()[:16]
    db.execute("""
        INSERT OR IGNORE INTO skill_versions
        (skill_name, version, content_hash, change_summary, author, created_at)
        VALUES (?, ?, ?, ?, 'optimizer', ?)
    """, (skill_name, new_ver, content_hash, patch["change_summary"], now))

    # Update skill version
    db.execute(
        "UPDATE skills SET current_version = ?, updated_at = ? WHERE name = ?",
        (new_ver, now, skill_name),
    )

    # Update patch status
    db.execute(
        "UPDATE skill_patches SET status = 'confirmed', reviewed_at = ? WHERE patch_id = ?",
        (now, patch_id),
    )
    db.commit()
    return True


def reject_patch(patch_id: str) -> bool:
    """Reject a pending patch."""
    db = _get_db()
    cur = db.execute(
        "UPDATE skill_patches SET status = 'rejected', reviewed_at = ? "
        "WHERE patch_id = ? AND status = 'pending'",
        (time.time(), patch_id),
    )
    db.commit()
    return cur.rowcount > 0


# ============================================================
# Register New Skill (used by generator and external imports)
# ============================================================

def register_skill(
    name: str,
    display_name: str,
    description: str = "",
    category: str = "general",
    risk_level: int = 1,
    min_role: str = "developer",
    file_name: str = "",
    source: str = "generated",
) -> bool:
    """Register a new skill. Returns False if name already exists."""
    db = _get_db()
    now = time.time()
    try:
        db.execute("""
            INSERT INTO skills
            (name, display_name, description, category, risk_level,
             source, file_name, enabled, min_role, current_version,
             created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, '1.0.0', ?, ?)
        """, (
            name, display_name, description, category, risk_level,
            source, file_name, min_role, now, now,
        ))
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
