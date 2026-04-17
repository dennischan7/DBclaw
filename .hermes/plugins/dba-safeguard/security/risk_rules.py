"""L0-L4 风险分级引擎 — 可配置规则 + 硬编码兜底。

核心设计:
  1. 从 hitl_matrix.yaml 加载可配置的分级规则
  2. 硬编码兜底规则 (HARDCODED_ESCALATIONS) 无法被配置覆盖
  3. 风险只能被提升，不能被降低 (单调递增原则)
  4. 支持自定义规则扩展 (custom_rules 表)
"""

from __future__ import annotations

import json
import logging
import re
import sqlite3
from dataclasses import dataclass, field
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.security.risk_rules")

# ============================================================
# Risk Level Enum
# ============================================================


class RiskLevel(IntEnum):
    """SQL操作风险等级 — 只能提升不能降低。"""
    L0_READONLY = 0        # 无损只读: SELECT, SHOW, DESCRIBE, EXPLAIN
    L1_LOW_DML = 1         # 低危单行DML: 单行INSERT, 有WHERE的小范围UPDATE/DELETE
    L2_MEDIUM_BATCH = 2    # 中危结构扩展: 批量DML, CREATE INDEX, ALTER TABLE ADD
    L3_HIGH_DESTRUCTIVE = 3  # 高危结构破坏: ALTER DROP/MODIFY, DROP INDEX, TRUNCATE
    L4_CATASTROPHIC = 4    # 灾难级: DROP TABLE/DATABASE, DELETE无WHERE

    @property
    def label(self) -> str:
        return self.name

    @property
    def description(self) -> str:
        _desc = {
            0: "无损只读",
            1: "低危单行DML",
            2: "中危结构扩展",
            3: "高危结构破坏",
            4: "灾难级操作",
        }
        return _desc.get(self.value, "未知")


# ============================================================
# Hardcoded Escalation Rules (不可覆盖)
# ============================================================

# 这些规则是安全兜底，配置文件无法降低其等级
HARDCODED_ESCALATIONS: List[Dict[str, Any]] = [
    {
        "id": "HC-001",
        "name": "DELETE无WHERE强制L4",
        "pattern": r"(?i)^\s*DELETE\s+FROM\s+\S+\s*$",
        "check_type": "no_where",
        "operation": "DELETE",
        "target_level": RiskLevel.L4_CATASTROPHIC,
        "reason": "DELETE无WHERE条件将删除全表数据",
    },
    {
        "id": "HC-002",
        "name": "UPDATE无WHERE强制L4",
        "pattern": r"(?i)^\s*UPDATE\s+\S+\s+SET\s+.+",
        "check_type": "no_where",
        "operation": "UPDATE",
        "target_level": RiskLevel.L4_CATASTROPHIC,
        "reason": "UPDATE无WHERE条件将修改全表数据",
    },
    {
        "id": "HC-003",
        "name": "DROP DATABASE强制L4",
        "pattern": r"(?i)^\s*DROP\s+DATABASE",
        "check_type": "regex",
        "target_level": RiskLevel.L4_CATASTROPHIC,
        "reason": "DROP DATABASE是灾难性操作",
    },
    {
        "id": "HC-004",
        "name": "DROP TABLE强制L4",
        "pattern": r"(?i)^\s*DROP\s+TABLE",
        "check_type": "regex",
        "target_level": RiskLevel.L4_CATASTROPHIC,
        "reason": "DROP TABLE将永久删除表及数据",
    },
    {
        "id": "HC-005",
        "name": "TRUNCATE最低L3",
        "pattern": r"(?i)^\s*TRUNCATE",
        "check_type": "regex",
        "target_level": RiskLevel.L3_HIGH_DESTRUCTIVE,
        "reason": "TRUNCATE将清空全表数据",
    },
]

# ============================================================
# Base Risk Classification (默认基线, 可被配置覆盖)
# ============================================================

BASE_RISK_CLASSIFICATION: Dict[str, int] = {
    # L0 — 只读
    "SELECT": 0, "SHOW": 0, "DESCRIBE": 0, "EXPLAIN": 0, "USE": 0, "SET": 0,
    # L1 — 低危DML
    "INSERT": 1,
    # L2 — 中危
    "UPDATE": 2, "DELETE": 2, "MERGE": 2, "CREATE INDEX": 2, "ALTER TABLE ADD": 2,
    # L3 — 高危
    "ALTER TABLE DROP": 3, "ALTER TABLE MODIFY": 3, "ALTER TABLE ALTER": 3,
    "ALTER TABLE RENAME": 3, "DROP INDEX": 3, "TRUNCATE": 3,
    # L4 — 灾难
    "DROP TABLE": 4, "DROP DATABASE": 4, "DROP SCHEMA": 4,
    "DROP VIEW": 4, "DROP PROCEDURE": 4, "DROP FUNCTION": 4,
}


# ============================================================
# Custom Rules DB
# ============================================================

_DB_PATH: Optional[Path] = None


def set_risk_rules_db_path(path: Path) -> None:
    """Override DB path (for testing)."""
    global _DB_PATH
    _DB_PATH = path


def _get_db_path() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    return Path(__file__).parent.parent / "data" / "risk_rules.db"


def _get_conn() -> sqlite3.Connection:
    db_path = _get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    _init_tables(conn)
    return conn


def _init_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS custom_rules (
            rule_id     TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            pattern     TEXT NOT NULL,
            check_type  TEXT NOT NULL DEFAULT 'regex',
            target_level INTEGER NOT NULL,
            reason      TEXT NOT NULL DEFAULT '',
            enabled     INTEGER NOT NULL DEFAULT 1,
            priority    INTEGER NOT NULL DEFAULT 100,
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            created_by  TEXT NOT NULL DEFAULT 'system'
        );

        CREATE TABLE IF NOT EXISTS risk_overrides (
            override_id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation   TEXT NOT NULL,
            base_level  INTEGER NOT NULL,
            reason      TEXT NOT NULL DEFAULT '',
            created_at  TEXT NOT NULL DEFAULT (datetime('now')),
            created_by  TEXT NOT NULL DEFAULT 'admin'
        );
    """)
    conn.commit()


# ============================================================
# Risk Classification Engine
# ============================================================

@dataclass
class RiskAssessment:
    """风险评估结果。"""
    risk_level: int
    risk_label: str
    base_level: int            # AST基线等级
    escalation_reasons: List[str] = field(default_factory=list)
    hardcoded_hit: bool = False  # 是否命中硬编码兜底
    custom_rules_hit: List[str] = field(default_factory=list)
    final_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "risk_label": self.risk_label,
            "base_level": self.base_level,
            "escalation_reasons": self.escalation_reasons,
            "hardcoded_hit": self.hardcoded_hit,
            "custom_rules_hit": self.custom_rules_hit,
            "final_reason": self.final_reason,
        }


def assess_risk(
    sql: str,
    operation: str = "",
    ast_risk_level: int = 0,
    explain_warnings: Optional[List[str]] = None,
    rows_affected: int = 0,
    environment: str = "development",
) -> RiskAssessment:
    """Assess risk level with configurable rules + hardcoded fallbacks.

    Args:
        sql: SQL statement text
        operation: Detected operation type (e.g. "DELETE", "ALTER TABLE DROP")
        ast_risk_level: Risk level from AST validator
        explain_warnings: Warnings from EXPLAIN analysis
        rows_affected: Estimated affected rows
        environment: "production" or "development"

    Returns:
        RiskAssessment with final risk level (monotonically non-decreasing)
    """
    assessment = RiskAssessment(
        risk_level=ast_risk_level,
        risk_label=_level_label(ast_risk_level),
        base_level=ast_risk_level,
    )

    # --- Phase 1: Custom rules from DB ---
    _apply_custom_rules(sql, assessment)

    # --- Phase 2: Configurable escalation rules ---
    _apply_configurable_escalations(
        sql, operation, assessment, rows_affected, environment,
    )

    # --- Phase 3: Hardcoded fallbacks (最高优先级, 不可降级) ---
    _apply_hardcoded_escalations(sql, assessment)

    # Clamp
    assessment.risk_level = min(assessment.risk_level, 4)
    assessment.risk_label = _level_label(assessment.risk_level)
    assessment.final_reason = "; ".join(assessment.escalation_reasons) if assessment.escalation_reasons else "AST基线分级"

    return assessment


def _apply_custom_rules(sql: str, assessment: RiskAssessment) -> None:
    """Apply user-defined custom rules from DB."""
    try:
        conn = _get_conn()
        rows = conn.execute(
            "SELECT rule_id, name, pattern, check_type, target_level, reason "
            "FROM custom_rules WHERE enabled=1 ORDER BY priority ASC"
        ).fetchall()
        conn.close()
    except Exception as e:
        logger.debug("Custom rules DB error: %s", e)
        return

    for row in rows:
        try:
            if row["check_type"] == "regex" and re.search(row["pattern"], sql, re.IGNORECASE):
                if row["target_level"] > assessment.risk_level:
                    assessment.risk_level = row["target_level"]
                    assessment.custom_rules_hit.append(row["rule_id"])
                    assessment.escalation_reasons.append(
                        f"自定义规则[{row['rule_id']}]: {row['reason']}"
                    )
        except re.error:
            logger.warning("Invalid regex in custom rule %s", row["rule_id"])


def _apply_configurable_escalations(
    sql: str,
    operation: str,
    assessment: RiskAssessment,
    rows_affected: int,
    environment: str,
) -> None:
    """Apply escalation rules from hitl_matrix.yaml."""
    try:
        from ..harnesses.risk_interceptor import load_hitl_matrix
    except ImportError:
        from harnesses.risk_interceptor import load_hitl_matrix

    matrix = load_hitl_matrix()
    escalation_rules = matrix.get("escalation_rules", [])

    # Row threshold escalation
    levels = matrix.get("risk_levels", {})
    current_cfg = levels.get(assessment.risk_level, {})
    threshold = current_cfg.get("row_threshold", 0)
    if threshold and rows_affected > threshold:
        new_level = min(assessment.risk_level + 1, 4)
        if new_level > assessment.risk_level:
            assessment.escalation_reasons.append(
                f"影响行数({rows_affected})超过阈值({threshold})"
            )
            assessment.risk_level = new_level

    # Production environment escalation
    if environment == "production":
        new_level = min(assessment.risk_level + 1, 4)
        if new_level > assessment.risk_level:
            assessment.escalation_reasons.append("生产环境操作自动提升一级")
            assessment.risk_level = new_level


def _apply_hardcoded_escalations(sql: str, assessment: RiskAssessment) -> None:
    """Apply hardcoded safety rules — cannot be overridden by config."""
    sql_normalized = sql.strip()
    for rule in HARDCODED_ESCALATIONS:
        if rule["check_type"] == "no_where":
            # Check for operation without WHERE clause
            op = rule["operation"]
            if re.match(rf"(?i)^\s*{op}\b", sql_normalized):
                if not re.search(r"(?i)\bWHERE\b", sql_normalized):
                    target = rule["target_level"]
                    if target > assessment.risk_level:
                        assessment.risk_level = target
                        assessment.hardcoded_hit = True
                        assessment.escalation_reasons.append(
                            f"硬编码兜底[{rule['id']}]: {rule['reason']}"
                        )
        elif rule["check_type"] == "regex":
            if re.search(rule["pattern"], sql_normalized, re.IGNORECASE):
                target = rule["target_level"]
                if target > assessment.risk_level:
                    assessment.risk_level = target
                    assessment.hardcoded_hit = True
                    assessment.escalation_reasons.append(
                        f"硬编码兜底[{rule['id']}]: {rule['reason']}"
                    )


def _level_label(level: int) -> str:
    """Return human-readable label for risk level."""
    try:
        return RiskLevel(level).label
    except ValueError:
        return f"L{level}_UNKNOWN"


# ============================================================
# Custom Rule Management (admin API)
# ============================================================

def add_custom_rule(
    rule_id: str,
    name: str,
    pattern: str,
    target_level: int,
    reason: str = "",
    check_type: str = "regex",
    priority: int = 100,
    created_by: str = "admin",
) -> bool:
    """Add a custom risk rule."""
    if target_level < 0 or target_level > 4:
        return False
    # Validate regex
    if check_type == "regex":
        try:
            re.compile(pattern)
        except re.error:
            return False
    conn = _get_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO custom_rules "
            "(rule_id, name, pattern, check_type, target_level, reason, priority, created_by) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (rule_id, name, pattern, check_type, target_level, reason, priority, created_by),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def remove_custom_rule(rule_id: str) -> bool:
    """Remove a custom risk rule."""
    conn = _get_conn()
    try:
        cur = conn.execute("DELETE FROM custom_rules WHERE rule_id=?", (rule_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()


def list_custom_rules() -> List[Dict[str, Any]]:
    """List all custom rules."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT rule_id, name, pattern, check_type, target_level, reason, "
            "enabled, priority, created_at, created_by FROM custom_rules ORDER BY priority"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_risk_level_config() -> Dict[int, Dict[str, Any]]:
    """Return the full risk level configuration (from HITL matrix)."""
    try:
        from ..harnesses.risk_interceptor import load_hitl_matrix
    except ImportError:
        from harnesses.risk_interceptor import load_hitl_matrix

    matrix = load_hitl_matrix()
    return matrix.get("risk_levels", {})
