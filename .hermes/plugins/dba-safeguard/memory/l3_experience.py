"""L3 运维经验记忆 — 自动沉淀成功SQL范式、故障排查方案、避坑指南。

核心规则:
  - 仅沉淀成功完成的任务经验，失败任务不自动沉淀
  - 经验沉淀必须经过用户确认才能入库 (require_confirmation=True)
  - 禁止修改已归档的经验版本，仅可新增版本
  - 向量化存储: 使用SQLite FTS5做全文索引 (Hermes原生方案)
  - 智能召回: 同类任务启动时自动匹配历史经验

Experience lifecycle:
  任务成功 → distill_experience() → 生成pending条目 →
  用户确认 confirm_experience() → 正式入库 → search时可被召回
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.memory.l3_experience")

_DB_PATH: Optional[Path] = None
_CONN: Optional[sqlite3.Connection] = None


def set_experience_db_path(path: Path) -> None:
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
        _DB_PATH = data_dir / "experience.db"

    _CONN = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    _CONN.execute("PRAGMA journal_mode=WAL")
    _CONN.executescript(_SCHEMA_SQL)
    return _CONN


_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS experiences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL,
    version INTEGER DEFAULT 1,

    -- 分类与标识
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    summary TEXT DEFAULT '',

    -- DBA元数据
    db_type TEXT DEFAULT '',
    dialect TEXT DEFAULT '',
    operation_type TEXT DEFAULT '',
    risk_level INTEGER DEFAULT 0,
    sql_pattern TEXT DEFAULT '',

    -- 标签与检索
    tags TEXT DEFAULT '',
    source_task_id TEXT DEFAULT '',
    source_session_id TEXT DEFAULT '',

    -- 状态管理
    status TEXT DEFAULT 'pending',
    confirmed_at REAL DEFAULT 0,
    confirmed_by TEXT DEFAULT '',
    enabled INTEGER DEFAULT 1,

    -- 版本管理 (同一experience_group_id的多个版本)
    experience_group_id TEXT DEFAULT '',
    parent_version_id INTEGER DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_exp_category ON experiences(category);
CREATE INDEX IF NOT EXISTS idx_exp_status ON experiences(status);
CREATE INDEX IF NOT EXISTS idx_exp_db_type ON experiences(db_type);
CREATE INDEX IF NOT EXISTS idx_exp_enabled ON experiences(enabled);
CREATE INDEX IF NOT EXISTS idx_exp_group ON experiences(experience_group_id);

CREATE VIRTUAL TABLE IF NOT EXISTS experience_fts USING fts5(
    title, content, summary, tags, sql_pattern,
    content='experiences', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS exp_ai AFTER INSERT ON experiences BEGIN
    INSERT INTO experience_fts(rowid, title, content, summary, tags, sql_pattern)
    VALUES (new.id, new.title, new.content, new.summary, new.tags, new.sql_pattern);
END;

CREATE TRIGGER IF NOT EXISTS exp_ad AFTER DELETE ON experiences BEGIN
    INSERT INTO experience_fts(experience_fts, rowid, title, content, summary, tags, sql_pattern)
    VALUES ('delete', old.id, old.title, old.content, old.summary, old.tags, old.sql_pattern);
END;
"""

# ---------------------------------------------------------------------------
# Categories
# ---------------------------------------------------------------------------

EXPERIENCE_CATEGORIES = {
    "sql_pattern": "成功SQL范式",
    "optimization": "性能优化经验",
    "troubleshooting": "故障排查方案",
    "pitfall": "避坑指南",
    "best_practice": "最佳实践",
    "ddl_workflow": "DDL变更流程",
    "health_check": "巡检经验",
}


# ---------------------------------------------------------------------------
# Experience Distillation
# ---------------------------------------------------------------------------

def distill_experience(
    task_result: Dict[str, Any],
    *,
    require_confirmation: bool = True,
) -> Optional[int]:
    """Distill a successful task into a structured experience entry.

    Only processes tasks that completed successfully.
    Creates a 'pending' entry that requires user confirmation by default.

    Args:
        task_result: Dict from DBATask.to_dict() with pipeline results.
        require_confirmation: If True (default), entry starts as 'pending'.

    Returns:
        Experience ID if created, None if task is not eligible.
    """
    # Only distill successful tasks
    stages = task_result.get("stages", [])
    if not stages:
        return None

    # Check if pipeline completed (has audit stage or execute stage passed)
    completed = any(
        s.get("stage") == "audit" and s.get("status") == "passed"
        for s in stages
    )
    execute_passed = any(
        s.get("stage") == "execute" and s.get("status") == "passed"
        for s in stages
    )
    if not completed and not execute_passed:
        return None

    # Build experience from task data
    sql = task_result.get("sql", "")
    risk_level = task_result.get("risk_level", 0)
    dialect = task_result.get("dialect", "")

    category = _classify_experience(task_result)
    title = _generate_title(task_result)
    content = _generate_content(task_result)
    summary = _generate_summary(task_result)
    sql_pattern = _extract_sql_pattern(sql)

    status = "pending" if require_confirmation else "confirmed"

    exp_id = _save_experience(
        category=category,
        title=title,
        content=content,
        summary=summary,
        db_type=dialect,
        dialect=dialect,
        operation_type=task_result.get("current_stage", ""),
        risk_level=risk_level,
        sql_pattern=sql_pattern,
        tags=f"{category},{dialect},L{risk_level}",
        source_task_id=task_result.get("task_id", ""),
        status=status,
    )

    logger.info(
        "Distilled experience #%d from task %s (status=%s, category=%s)",
        exp_id, task_result.get("task_id", ""), status, category,
    )
    return exp_id


def _classify_experience(task: Dict) -> str:
    """Classify experience category from task data."""
    sql = task.get("sql", "").upper()
    risk = task.get("risk_level", 0)

    if any(kw in sql for kw in ["ALTER", "CREATE INDEX", "DROP INDEX"]):
        return "ddl_workflow"
    if risk >= 2:
        return "pitfall"
    if any(kw in sql for kw in ["EXPLAIN", "ANALYZE"]):
        return "optimization"
    if "SELECT" in sql and ("JOIN" in sql or "WINDOW" in sql or "WITH" in sql):
        return "sql_pattern"
    return "best_practice"


def _generate_title(task: Dict) -> str:
    """Generate a concise title for the experience."""
    sql = task.get("sql", "")
    risk = task.get("risk_level", 0)
    dialect = task.get("dialect", "unknown")

    # Extract operation type
    sql_upper = sql.strip().upper()
    for op in ["SELECT", "INSERT", "UPDATE", "DELETE", "ALTER TABLE",
               "CREATE INDEX", "CREATE TABLE", "DROP"]:
        if sql_upper.startswith(op):
            return f"[L{risk}] {dialect} {op} 成功执行范式"

    return f"[L{risk}] {dialect} 操作经验"


def _generate_content(task: Dict) -> str:
    """Generate structured Markdown content for the experience."""
    lines = []
    sql = task.get("sql", "")
    dialect = task.get("dialect", "")
    risk = task.get("risk_level", 0)

    lines.append(f"## 操作概要\n")
    lines.append(f"- **数据库方言**: {dialect}")
    lines.append(f"- **风险等级**: L{risk}")
    lines.append(f"- **SQL语句**:\n```sql\n{sql}\n```\n")

    # Add stage results summary
    stages = task.get("stages", [])
    if stages:
        lines.append("## 流水线执行结果\n")
        for s in stages:
            status_icon = {"passed": "✅", "failed": "❌", "skipped": "⏭️",
                           "blocked": "🚫"}.get(s.get("status", ""), "❓")
            duration = s.get("duration_ms", 0)
            lines.append(f"- {status_icon} **{s['stage']}** ({duration}ms)")

    if task.get("rollback_sql"):
        lines.append(f"\n## 回滚脚本\n```sql\n{task['rollback_sql']}\n```")

    return "\n".join(lines)


def _generate_summary(task: Dict) -> str:
    """Generate a one-line summary."""
    sql = task.get("sql", "")[:100]
    return f"L{task.get('risk_level', 0)} {task.get('dialect', '')} - {sql}"


def _extract_sql_pattern(sql: str) -> str:
    """Extract a normalized SQL pattern for matching similar operations."""
    if not sql:
        return ""
    # Normalize: remove literals, keep structure
    import re
    pattern = sql.strip()
    # Replace string literals
    pattern = re.sub(r"'[^']*'", "'?'", pattern)
    # Replace numeric literals
    pattern = re.sub(r"\b\d+\b", "?", pattern)
    # Collapse whitespace
    pattern = re.sub(r"\s+", " ", pattern)
    return pattern[:500]


# ---------------------------------------------------------------------------
# CRUD Operations
# ---------------------------------------------------------------------------

def _save_experience(**kwargs) -> int:
    """Internal save. Returns row ID."""
    db = _get_db()
    now = time.time()
    cursor = db.execute(
        """INSERT INTO experiences
        (created_at, updated_at, category, title, content, summary,
         db_type, dialect, operation_type, risk_level, sql_pattern,
         tags, source_task_id, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            now, now,
            kwargs.get("category", ""),
            kwargs.get("title", ""),
            kwargs.get("content", ""),
            kwargs.get("summary", ""),
            kwargs.get("db_type", ""),
            kwargs.get("dialect", ""),
            kwargs.get("operation_type", ""),
            kwargs.get("risk_level", 0),
            kwargs.get("sql_pattern", ""),
            kwargs.get("tags", ""),
            kwargs.get("source_task_id", ""),
            kwargs.get("status", "pending"),
        ),
    )
    db.commit()
    return cursor.lastrowid


def confirm_experience(experience_id: int, confirmed_by: str = "user") -> bool:
    """Confirm a pending experience entry. Required for it to be searchable.

    Returns True if confirmed, False if not found or already confirmed.
    """
    db = _get_db()
    cursor = db.execute(
        """UPDATE experiences
        SET status = 'confirmed', confirmed_at = ?, confirmed_by = ?, updated_at = ?
        WHERE id = ? AND status = 'pending'""",
        (time.time(), confirmed_by, time.time(), experience_id),
    )
    db.commit()
    if cursor.rowcount > 0:
        logger.info("Experience #%d confirmed by %s", experience_id, confirmed_by)
        return True
    return False


def reject_experience(experience_id: int) -> bool:
    """Reject a pending experience. Marks as 'rejected'."""
    db = _get_db()
    cursor = db.execute(
        "UPDATE experiences SET status = 'rejected', updated_at = ? WHERE id = ? AND status = 'pending'",
        (time.time(), experience_id),
    )
    db.commit()
    return cursor.rowcount > 0


def toggle_experience(experience_id: int, enabled: bool) -> bool:
    """Enable or disable an experience."""
    db = _get_db()
    cursor = db.execute(
        "UPDATE experiences SET enabled = ?, updated_at = ? WHERE id = ?",
        (1 if enabled else 0, time.time(), experience_id),
    )
    db.commit()
    return cursor.rowcount > 0


def get_experience(experience_id: int) -> Optional[Dict[str, Any]]:
    """Get a single experience by ID."""
    db = _get_db()
    row = db.execute("SELECT * FROM experiences WHERE id = ?", (experience_id,)).fetchone()
    if not row:
        return None
    return _row_to_dict(row)


def list_experiences(
    *,
    status: str = "",
    category: str = "",
    db_type: str = "",
    enabled_only: bool = True,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """List experiences with filters."""
    db = _get_db()
    conditions = []
    params: list = []

    if status:
        conditions.append("status = ?")
        params.append(status)
    if category:
        conditions.append("category = ?")
        params.append(category)
    if db_type:
        conditions.append("db_type = ?")
        params.append(db_type)
    if enabled_only:
        conditions.append("enabled = 1")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    rows = db.execute(
        f"SELECT * FROM experiences {where} ORDER BY updated_at DESC LIMIT ?",
        params + [limit],
    ).fetchall()
    return [_row_to_dict(r) for r in rows]


def get_pending_experiences(limit: int = 20) -> List[Dict[str, Any]]:
    """Get experiences awaiting user confirmation."""
    return list_experiences(status="pending", enabled_only=False, limit=limit)


# ---------------------------------------------------------------------------
# Search & Recall
# ---------------------------------------------------------------------------

def search_experiences(
    query: str,
    *,
    category: str = "",
    db_type: str = "",
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Full-text search in confirmed & enabled experiences.

    Only returns confirmed+enabled experiences for LLM context injection.
    """
    db = _get_db()
    conditions = ["e.status = 'confirmed'", "e.enabled = 1"]
    params: list = []

    if category:
        conditions.append("e.category = ?")
        params.append(category)
    if db_type:
        conditions.append("e.db_type = ?")
        params.append(db_type)

    where = " AND ".join(conditions)

    try:
        rows = db.execute(
            f"""SELECT e.* FROM experiences e
            JOIN experience_fts ON e.id = experience_fts.rowid
            WHERE experience_fts MATCH ? AND {where}
            ORDER BY rank LIMIT ?""",
            [query] + params + [limit],
        ).fetchall()
        return [_row_to_dict(r) for r in rows]
    except Exception as e:
        logger.warning("Experience FTS search failed: %s", e)
        return []


def recall_for_task(
    sql: str = "",
    operation_type: str = "",
    db_type: str = "",
    limit: int = 3,
) -> List[Dict[str, Any]]:
    """Recall relevant experiences for a new task.

    Used during pipeline preflight to inject historical context.
    """
    parts = []
    if sql:
        pattern = _extract_sql_pattern(sql)
        if pattern:
            parts.append(pattern[:200])
    if operation_type:
        parts.append(operation_type)

    if not parts:
        return []

    query = " OR ".join(parts)
    return search_experiences(query, db_type=db_type, limit=limit)


# ---------------------------------------------------------------------------
# Version Management
# ---------------------------------------------------------------------------

def create_new_version(
    experience_id: int,
    new_content: str,
    new_summary: str = "",
) -> Optional[int]:
    """Create a new version of an existing experience.

    The old version is preserved unchanged. A new row is created
    with parent_version_id pointing to the old one.
    """
    original = get_experience(experience_id)
    if not original:
        return None

    db = _get_db()
    group_id = original.get("experience_group_id") or str(experience_id)
    old_version = original.get("version", 1)
    now = time.time()

    cursor = db.execute(
        """INSERT INTO experiences
        (created_at, updated_at, version, category, title, content, summary,
         db_type, dialect, operation_type, risk_level, sql_pattern,
         tags, source_task_id, status, confirmed_at, confirmed_by, enabled,
         experience_group_id, parent_version_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending', 0, '', 1, ?, ?)""",
        (
            now, now, old_version + 1,
            original["category"], original["title"], new_content,
            new_summary or original.get("summary", ""),
            original.get("db_type", ""), original.get("dialect", ""),
            original.get("operation_type", ""), original.get("risk_level", 0),
            original.get("sql_pattern", ""), original.get("tags", ""),
            original.get("source_task_id", ""),
            group_id, experience_id,
        ),
    )
    db.commit()
    return cursor.lastrowid


def get_version_history(experience_group_id: str) -> List[Dict[str, Any]]:
    """Get all versions of an experience group."""
    db = _get_db()
    rows = db.execute(
        "SELECT * FROM experiences WHERE experience_group_id = ? ORDER BY version ASC",
        (experience_group_id,),
    ).fetchall()
    return [_row_to_dict(r) for r in rows]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_COLUMNS = [
    "id", "created_at", "updated_at", "version",
    "category", "title", "content", "summary",
    "db_type", "dialect", "operation_type", "risk_level", "sql_pattern",
    "tags", "source_task_id", "source_session_id",
    "status", "confirmed_at", "confirmed_by", "enabled",
    "experience_group_id", "parent_version_id",
]


def _row_to_dict(row) -> Dict[str, Any]:
    return dict(zip(_COLUMNS, row))
