"""L4 业务图谱与用户建模 — 企业业务血缘关系、业务字典、用户操作习惯。

核心内容:
  - 业务血缘字典: 跨表字段映射关系、表关联关系
  - 业务状态码释义: 业务字段的枚举值、状态含义
  - 业务规则: 企业专属的业务逻辑、数据规范
  - 用户建模: 用户的操作习惯、偏好的SQL风格、风险模式选择

安全约束:
  - 业务图谱的修改必须经过管理员审批(admin_only)
  - 禁止AI自动修改业务图谱
  - 禁止存储用户的敏感信息/密码
  - 所有对话前预加载，全程生效

支持从企业数据字典手动导入业务图谱 (import_data_dictionary)
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.memory.l4_business_graph")

_DB_PATH: Optional[Path] = None
_CONN: Optional[sqlite3.Connection] = None


def set_graph_db_path(path: Path) -> None:
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
        _DB_PATH = data_dir / "business_graph.db"

    _CONN = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    _CONN.execute("PRAGMA journal_mode=WAL")
    _CONN.executescript(_SCHEMA_SQL)
    return _CONN


_SCHEMA_SQL = """
-- 业务血缘关系: 表间字段映射
CREATE TABLE IF NOT EXISTS table_relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_table TEXT NOT NULL,
    source_column TEXT NOT NULL,
    target_table TEXT NOT NULL,
    target_column TEXT NOT NULL,
    relation_type TEXT DEFAULT 'fk',
    description TEXT DEFAULT '',
    instance_name TEXT DEFAULT '',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    created_by TEXT DEFAULT 'admin'
);

CREATE INDEX IF NOT EXISTS idx_rel_source ON table_relations(source_table, source_column);
CREATE INDEX IF NOT EXISTS idx_rel_target ON table_relations(target_table, target_column);

-- 业务字典: 字段含义、枚举值释义
CREATE TABLE IF NOT EXISTS business_dictionary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    column_name TEXT NOT NULL,
    business_name TEXT DEFAULT '',
    description TEXT DEFAULT '',
    enum_values TEXT DEFAULT '',
    data_rules TEXT DEFAULT '',
    instance_name TEXT DEFAULT '',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    created_by TEXT DEFAULT 'admin'
);

CREATE INDEX IF NOT EXISTS idx_dict_table ON business_dictionary(table_name);
CREATE INDEX IF NOT EXISTS idx_dict_column ON business_dictionary(table_name, column_name);

-- 业务规则: 企业数据约束规则
CREATE TABLE IF NOT EXISTS business_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rule_name TEXT NOT NULL,
    rule_type TEXT NOT NULL,
    target_table TEXT DEFAULT '',
    target_column TEXT DEFAULT '',
    condition TEXT NOT NULL,
    description TEXT DEFAULT '',
    severity TEXT DEFAULT 'warning',
    enabled INTEGER DEFAULT 1,
    instance_name TEXT DEFAULT '',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    created_by TEXT DEFAULT 'admin'
);

CREATE INDEX IF NOT EXISTS idx_rule_table ON business_rules(target_table);
CREATE INDEX IF NOT EXISTS idx_rule_type ON business_rules(rule_type);

-- 用户画像
CREATE TABLE IF NOT EXISTS user_profiles (
    user_id TEXT PRIMARY KEY,
    preferred_dialect TEXT DEFAULT '',
    preferred_instance TEXT DEFAULT '',
    risk_mode TEXT DEFAULT 'moderate',
    sql_style TEXT DEFAULT '',
    common_tables TEXT DEFAULT '',
    operation_stats TEXT DEFAULT '',
    last_active REAL DEFAULT 0,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);

CREATE VIRTUAL TABLE IF NOT EXISTS dict_fts USING fts5(
    business_name, description, enum_values,
    content='business_dictionary', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS dict_ai AFTER INSERT ON business_dictionary BEGIN
    INSERT INTO dict_fts(rowid, business_name, description, enum_values)
    VALUES (new.id, new.business_name, new.description, new.enum_values);
END;

CREATE TRIGGER IF NOT EXISTS dict_ad AFTER DELETE ON business_dictionary BEGIN
    INSERT INTO dict_fts(dict_fts, rowid, business_name, description, enum_values)
    VALUES ('delete', old.id, old.business_name, old.description, old.enum_values);
END;
"""


# ===========================================================================
# Table Relations (Business Lineage)
# ===========================================================================

def add_table_relation(
    source_table: str,
    source_column: str,
    target_table: str,
    target_column: str,
    *,
    relation_type: str = "fk",
    description: str = "",
    instance_name: str = "",
    created_by: str = "admin",
) -> int:
    """Add a table-to-table column relation. Returns row ID."""
    db = _get_db()
    now = time.time()
    cursor = db.execute(
        """INSERT INTO table_relations
        (source_table, source_column, target_table, target_column,
         relation_type, description, instance_name, created_at, updated_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (source_table, source_column, target_table, target_column,
         relation_type, description, instance_name, now, now, created_by),
    )
    db.commit()
    return cursor.lastrowid


def get_table_relations(
    table_name: str,
    *,
    direction: str = "both",
    instance_name: str = "",
) -> List[Dict[str, Any]]:
    """Get relations for a table.

    Args:
        direction: "source" (outgoing), "target" (incoming), or "both".
    """
    db = _get_db()
    results = []

    instance_filter = "AND instance_name = ?" if instance_name else ""
    params_base = [instance_name] if instance_name else []

    if direction in ("source", "both"):
        rows = db.execute(
            f"""SELECT * FROM table_relations
            WHERE source_table = ? {instance_filter}""",
            [table_name] + params_base,
        ).fetchall()
        results.extend(_rel_rows_to_dicts(rows))

    if direction in ("target", "both"):
        rows = db.execute(
            f"""SELECT * FROM table_relations
            WHERE target_table = ? {instance_filter}""",
            [table_name] + params_base,
        ).fetchall()
        results.extend(_rel_rows_to_dicts(rows))

    return results


def get_column_lineage(table_name: str, column_name: str) -> List[Dict[str, Any]]:
    """Trace lineage for a specific column across tables."""
    db = _get_db()
    rows = db.execute(
        """SELECT * FROM table_relations
        WHERE (source_table = ? AND source_column = ?)
           OR (target_table = ? AND target_column = ?)""",
        (table_name, column_name, table_name, column_name),
    ).fetchall()
    return _rel_rows_to_dicts(rows)


# ===========================================================================
# Business Dictionary
# ===========================================================================

def add_dictionary_entry(
    table_name: str,
    column_name: str,
    *,
    business_name: str = "",
    description: str = "",
    enum_values: str = "",
    data_rules: str = "",
    instance_name: str = "",
    created_by: str = "admin",
) -> int:
    """Add or update a business dictionary entry. Returns row ID."""
    db = _get_db()
    now = time.time()

    # Check if entry exists (upsert by table_name + column_name + instance_name)
    existing = db.execute(
        "SELECT id FROM business_dictionary WHERE table_name = ? AND column_name = ? AND instance_name = ?",
        (table_name, column_name, instance_name),
    ).fetchone()

    if existing:
        db.execute(
            """UPDATE business_dictionary
            SET business_name = ?, description = ?, enum_values = ?,
                data_rules = ?, updated_at = ?, created_by = ?
            WHERE id = ?""",
            (business_name, description, enum_values, data_rules, now, created_by, existing[0]),
        )
        db.commit()
        return existing[0]

    cursor = db.execute(
        """INSERT INTO business_dictionary
        (table_name, column_name, business_name, description, enum_values,
         data_rules, instance_name, created_at, updated_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (table_name, column_name, business_name, description, enum_values,
         data_rules, instance_name, now, now, created_by),
    )
    db.commit()
    return cursor.lastrowid


def get_dictionary(
    table_name: str,
    column_name: str = "",
    *,
    instance_name: str = "",
) -> List[Dict[str, Any]]:
    """Get business dictionary entries for a table (optionally a specific column)."""
    db = _get_db()
    conditions = ["table_name = ?"]
    params: list = [table_name]

    if column_name:
        conditions.append("column_name = ?")
        params.append(column_name)
    if instance_name:
        conditions.append("instance_name = ?")
        params.append(instance_name)

    where = " AND ".join(conditions)
    rows = db.execute(
        f"SELECT * FROM business_dictionary WHERE {where} ORDER BY column_name",
        params,
    ).fetchall()
    return _dict_rows_to_dicts(rows)


def search_dictionary(query: str, limit: int = 10) -> List[Dict[str, Any]]:
    """Full-text search in business dictionary."""
    db = _get_db()
    try:
        rows = db.execute(
            """SELECT bd.* FROM business_dictionary bd
            JOIN dict_fts ON bd.id = dict_fts.rowid
            WHERE dict_fts MATCH ?
            ORDER BY rank LIMIT ?""",
            (query, limit),
        ).fetchall()
        return _dict_rows_to_dicts(rows)
    except Exception as e:
        logger.warning("Dictionary FTS search failed: %s", e)
        return []


# ===========================================================================
# Business Rules
# ===========================================================================

def add_business_rule(
    rule_name: str,
    rule_type: str,
    condition: str,
    *,
    target_table: str = "",
    target_column: str = "",
    description: str = "",
    severity: str = "warning",
    instance_name: str = "",
    created_by: str = "admin",
) -> int:
    """Add a business rule. Returns row ID.

    rule_type examples: "not_null", "range_check", "enum_check",
                        "cross_table", "naming_convention"
    """
    db = _get_db()
    now = time.time()
    cursor = db.execute(
        """INSERT INTO business_rules
        (rule_name, rule_type, target_table, target_column, condition,
         description, severity, instance_name, created_at, updated_at, created_by)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (rule_name, rule_type, target_table, target_column, condition,
         description, severity, instance_name, now, now, created_by),
    )
    db.commit()
    return cursor.lastrowid


def get_rules_for_table(table_name: str, *, enabled_only: bool = True) -> List[Dict[str, Any]]:
    """Get business rules applicable to a table."""
    db = _get_db()
    enabled_clause = "AND enabled = 1" if enabled_only else ""
    rows = db.execute(
        f"""SELECT * FROM business_rules
        WHERE (target_table = ? OR target_table = '') {enabled_clause}
        ORDER BY severity DESC""",
        (table_name,),
    ).fetchall()
    return _rule_rows_to_dicts(rows)


def check_rules(table_name: str, column_name: str = "",
                value: str = "") -> List[Dict[str, Any]]:
    """Check business rules for a table/column/value. Returns violated rules."""
    rules = get_rules_for_table(table_name)
    violations = []

    for rule in rules:
        # Skip if column doesn't match
        if rule.get("target_column") and column_name:
            if rule["target_column"] != column_name:
                continue

        condition = rule.get("condition", "")
        violated = False

        if rule["rule_type"] == "not_null" and not value:
            violated = True
        elif rule["rule_type"] == "enum_check" and value:
            allowed = [v.strip() for v in condition.split(",")]
            if value not in allowed:
                violated = True
        elif rule["rule_type"] == "range_check" and value:
            try:
                parts = condition.split(",")
                if len(parts) == 2:
                    low, high = float(parts[0]), float(parts[1])
                    if not (low <= float(value) <= high):
                        violated = True
            except (ValueError, TypeError):
                pass

        if violated:
            violations.append(rule)

    return violations


# ===========================================================================
# User Profiling
# ===========================================================================

def update_user_profile(
    user_id: str,
    *,
    preferred_dialect: str = "",
    preferred_instance: str = "",
    risk_mode: str = "",
    sql_style: str = "",
    common_tables: str = "",
    operation_stats: str = "",
) -> None:
    """Update user profile. Creates if not exist."""
    db = _get_db()
    now = time.time()

    existing = db.execute(
        "SELECT user_id FROM user_profiles WHERE user_id = ?", (user_id,)
    ).fetchone()

    if existing:
        updates = ["updated_at = ?", "last_active = ?"]
        params: list = [now, now]
        if preferred_dialect:
            updates.append("preferred_dialect = ?")
            params.append(preferred_dialect)
        if preferred_instance:
            updates.append("preferred_instance = ?")
            params.append(preferred_instance)
        if risk_mode:
            updates.append("risk_mode = ?")
            params.append(risk_mode)
        if sql_style:
            updates.append("sql_style = ?")
            params.append(sql_style)
        if common_tables:
            updates.append("common_tables = ?")
            params.append(common_tables)
        if operation_stats:
            updates.append("operation_stats = ?")
            params.append(operation_stats)

        db.execute(
            f"UPDATE user_profiles SET {', '.join(updates)} WHERE user_id = ?",
            params + [user_id],
        )
    else:
        db.execute(
            """INSERT INTO user_profiles
            (user_id, preferred_dialect, preferred_instance, risk_mode,
             sql_style, common_tables, operation_stats, last_active,
             created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (user_id, preferred_dialect, preferred_instance,
             risk_mode or "moderate", sql_style, common_tables,
             operation_stats, now, now, now),
        )
    db.commit()


def get_user_profile(user_id: str) -> Optional[Dict[str, Any]]:
    """Get user profile."""
    db = _get_db()
    row = db.execute(
        "SELECT * FROM user_profiles WHERE user_id = ?", (user_id,)
    ).fetchone()
    if not row:
        return None
    cols = [
        "user_id", "preferred_dialect", "preferred_instance", "risk_mode",
        "sql_style", "common_tables", "operation_stats", "last_active",
        "created_at", "updated_at",
    ]
    return dict(zip(cols, row))


def record_user_operation(user_id: str, operation_type: str, dialect: str = "") -> None:
    """Record a user operation for profiling (increments stats)."""
    profile = get_user_profile(user_id)
    stats: Dict[str, int] = {}
    if profile and profile.get("operation_stats"):
        try:
            stats = json.loads(profile["operation_stats"])
        except (json.JSONDecodeError, TypeError):
            pass

    stats[operation_type] = stats.get(operation_type, 0) + 1
    update_user_profile(
        user_id,
        operation_stats=json.dumps(stats, ensure_ascii=False),
        preferred_dialect=dialect or "",
    )


# ===========================================================================
# Data Dictionary Import
# ===========================================================================

def import_data_dictionary(
    entries: List[Dict[str, str]],
    *,
    instance_name: str = "",
    created_by: str = "admin",
) -> int:
    """Batch import business dictionary entries from enterprise data dictionary.

    Each entry should have: table_name, column_name, and optionally:
    business_name, description, enum_values, data_rules.

    Returns count of imported entries.
    """
    count = 0
    for entry in entries:
        table_name = entry.get("table_name", "")
        column_name = entry.get("column_name", "")
        if not table_name or not column_name:
            continue
        add_dictionary_entry(
            table_name=table_name,
            column_name=column_name,
            business_name=entry.get("business_name", ""),
            description=entry.get("description", ""),
            enum_values=entry.get("enum_values", ""),
            data_rules=entry.get("data_rules", ""),
            instance_name=instance_name,
            created_by=created_by,
        )
        count += 1

    logger.info("Imported %d dictionary entries (instance=%s)", count, instance_name)
    return count


# ===========================================================================
# Context Generation (for LLM injection)
# ===========================================================================

def get_graph_context(
    tables: List[str],
    user_id: str = "",
    instance_name: str = "",
) -> str:
    """Build business graph context for LLM injection.

    Called before each LLM interaction to provide business knowledge.
    """
    parts = []

    # Table relations
    for table in tables[:10]:  # cap at 10 tables
        relations = get_table_relations(table, instance_name=instance_name)
        if relations:
            lines = [f"### {table} 关联关系"]
            for rel in relations[:10]:
                lines.append(
                    f"- {rel['source_table']}.{rel['source_column']} "
                    f"→ {rel['target_table']}.{rel['target_column']} "
                    f"({rel['relation_type']})"
                )
            parts.append("\n".join(lines))

    # Business dictionary for referenced tables
    for table in tables[:5]:
        entries = get_dictionary(table, instance_name=instance_name)
        if entries:
            lines = [f"### {table} 业务字段"]
            for e in entries[:20]:
                line = f"- **{e['column_name']}**"
                if e.get("business_name"):
                    line += f" ({e['business_name']})"
                if e.get("description"):
                    line += f": {e['description']}"
                if e.get("enum_values"):
                    line += f" [枚举: {e['enum_values']}]"
                lines.append(line)
            parts.append("\n".join(lines))

    # Business rules for referenced tables
    all_rules = []
    for table in tables[:5]:
        all_rules.extend(get_rules_for_table(table))
    if all_rules:
        lines = ["### 适用的业务规则"]
        for rule in all_rules[:10]:
            severity_icon = {"error": "🔴", "warning": "🟡", "info": "🔵"}.get(
                rule.get("severity", ""), "⚪"
            )
            lines.append(
                f"- {severity_icon} **{rule['rule_name']}**: {rule.get('description', rule['condition'])}"
            )
        parts.append("\n".join(lines))

    # User profile
    if user_id:
        profile = get_user_profile(user_id)
        if profile:
            lines = ["### 用户偏好"]
            if profile.get("preferred_dialect"):
                lines.append(f"- 默认方言: {profile['preferred_dialect']}")
            if profile.get("risk_mode"):
                lines.append(f"- 安全模式: {profile['risk_mode']}")
            if profile.get("sql_style"):
                lines.append(f"- SQL风格: {profile['sql_style']}")
            if len(lines) > 1:
                parts.append("\n".join(lines))

    if not parts:
        return ""

    return "## 业务图谱上下文\n\n" + "\n\n".join(parts)


# ===========================================================================
# Helpers
# ===========================================================================

_REL_COLUMNS = [
    "id", "source_table", "source_column", "target_table", "target_column",
    "relation_type", "description", "instance_name", "created_at", "updated_at",
    "created_by",
]

_DICT_COLUMNS = [
    "id", "table_name", "column_name", "business_name", "description",
    "enum_values", "data_rules", "instance_name", "created_at", "updated_at",
    "created_by",
]

_RULE_COLUMNS = [
    "id", "rule_name", "rule_type", "target_table", "target_column",
    "condition", "description", "severity", "enabled", "instance_name",
    "created_at", "updated_at", "created_by",
]


def _rel_rows_to_dicts(rows) -> List[Dict[str, Any]]:
    return [dict(zip(_REL_COLUMNS, r)) for r in rows]


def _dict_rows_to_dicts(rows) -> List[Dict[str, Any]]:
    return [dict(zip(_DICT_COLUMNS, r)) for r in rows]


def _rule_rows_to_dicts(rows) -> List[Dict[str, Any]]:
    return [dict(zip(_RULE_COLUMNS, r)) for r in rows]
