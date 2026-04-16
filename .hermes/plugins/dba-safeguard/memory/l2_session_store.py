"""L2 情景会话记忆 — 全量历史会话记录，支持DBA专属标签和跨会话检索。

核心能力:
  - 复用Hermes SQLite+FTS5全文检索体系
  - DBA专属标签: db_type, operation_type, risk_level, instance_name
  - 支持按标签、数据库实例、时间范围精准检索
  - 仅逻辑删除，禁止物理删除
  - 30天自动归档周期
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.memory.l2_session_store")

ARCHIVE_DAYS = 30
_DB_PATH: Optional[Path] = None
_CONN: Optional[sqlite3.Connection] = None


def set_session_db_path(path: Path) -> None:
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
        _DB_PATH = data_dir / "session_memory.db"

    _CONN = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
    _CONN.execute("PRAGMA journal_mode=WAL")
    _CONN.executescript(_SCHEMA_SQL)
    return _CONN


_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS session_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    timestamp REAL NOT NULL,
    role TEXT NOT NULL,
    content TEXT NOT NULL,

    -- DBA专属标签
    db_type TEXT DEFAULT '',
    db_version TEXT DEFAULT '',
    instance_name TEXT DEFAULT '',
    operation_type TEXT DEFAULT '',
    risk_level INTEGER DEFAULT -1,
    intent_label TEXT DEFAULT '',
    sql_text TEXT DEFAULT '',

    -- 管理字段
    archived INTEGER DEFAULT 0,
    tags TEXT DEFAULT '',
    extra_data TEXT DEFAULT '',

    -- L1快照 (会话结束时归档)
    workspace_snapshot TEXT DEFAULT ''
);

CREATE INDEX IF NOT EXISTS idx_session_id ON session_records(session_id);
CREATE INDEX IF NOT EXISTS idx_timestamp ON session_records(timestamp);
CREATE INDEX IF NOT EXISTS idx_db_type ON session_records(db_type);
CREATE INDEX IF NOT EXISTS idx_risk_level ON session_records(risk_level);
CREATE INDEX IF NOT EXISTS idx_instance ON session_records(instance_name);
CREATE INDEX IF NOT EXISTS idx_archived ON session_records(archived);

CREATE VIRTUAL TABLE IF NOT EXISTS session_fts USING fts5(
    content, sql_text, tags, intent_label,
    content='session_records', content_rowid='id'
);

CREATE TRIGGER IF NOT EXISTS session_ai AFTER INSERT ON session_records BEGIN
    INSERT INTO session_fts(rowid, content, sql_text, tags, intent_label)
    VALUES (new.id, new.content, new.sql_text, new.tags, new.intent_label);
END;

CREATE TRIGGER IF NOT EXISTS session_ad AFTER DELETE ON session_records BEGIN
    INSERT INTO session_fts(session_fts, rowid, content, sql_text, tags, intent_label)
    VALUES ('delete', old.id, old.content, old.sql_text, old.tags, old.intent_label);
END;
"""


# ---------------------------------------------------------------------------
# Record Operations
# ---------------------------------------------------------------------------

def save_session_record(
    session_id: str,
    role: str,
    content: str,
    *,
    db_type: str = "",
    db_version: str = "",
    instance_name: str = "",
    operation_type: str = "",
    risk_level: int = -1,
    intent_label: str = "",
    sql_text: str = "",
    tags: str = "",
    extra_data: str = "",
    workspace_snapshot: str = "",
) -> int:
    """Save a session record with DBA tags. Returns row ID."""
    db = _get_db()
    cursor = db.execute(
        """INSERT INTO session_records
        (session_id, timestamp, role, content,
         db_type, db_version, instance_name, operation_type,
         risk_level, intent_label, sql_text, tags, extra_data, workspace_snapshot)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            session_id, time.time(), role, content,
            db_type, db_version, instance_name, operation_type,
            risk_level, intent_label, sql_text, tags, extra_data, workspace_snapshot,
        ),
    )
    db.commit()
    return cursor.lastrowid


def get_session_records(
    session_id: str,
    limit: int = 100,
    include_archived: bool = False,
) -> List[Dict[str, Any]]:
    """Get records for a specific session."""
    db = _get_db()
    archived_clause = "" if include_archived else "AND archived = 0"
    rows = db.execute(
        f"""SELECT * FROM session_records
        WHERE session_id = ? {archived_clause}
        ORDER BY timestamp ASC LIMIT ?""",
        (session_id, limit),
    ).fetchall()
    return _rows_to_dicts(db, rows)


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_sessions(
    query: str,
    *,
    db_type: str = "",
    instance_name: str = "",
    risk_level: Optional[int] = None,
    operation_type: str = "",
    start_time: float = 0,
    end_time: float = 0,
    limit: int = 20,
) -> List[Dict[str, Any]]:
    """Full-text + tag-filtered search across all sessions."""
    db = _get_db()
    conditions = ["archived = 0"]
    params: list = []

    if db_type:
        conditions.append("sr.db_type = ?")
        params.append(db_type)
    if instance_name:
        conditions.append("sr.instance_name = ?")
        params.append(instance_name)
    if risk_level is not None:
        conditions.append("sr.risk_level = ?")
        params.append(risk_level)
    if operation_type:
        conditions.append("sr.operation_type = ?")
        params.append(operation_type)
    if start_time > 0:
        conditions.append("sr.timestamp >= ?")
        params.append(start_time)
    if end_time > 0:
        conditions.append("sr.timestamp <= ?")
        params.append(end_time)

    where = " AND ".join(conditions) if conditions else "1=1"

    if query:
        # FTS5 search with tag filters
        sql = f"""
            SELECT sr.* FROM session_records sr
            JOIN session_fts ON sr.id = session_fts.rowid
            WHERE session_fts MATCH ? AND {where}
            ORDER BY rank LIMIT ?
        """
        params = [query] + params + [limit]
    else:
        # Tag-only filter (no FTS)
        sql = f"""
            SELECT * FROM session_records sr
            WHERE {where}
            ORDER BY timestamp DESC LIMIT ?
        """
        params.append(limit)

    try:
        rows = db.execute(sql, params).fetchall()
        return _rows_to_dicts(db, rows)
    except Exception as e:
        logger.warning("Session search failed: %s", e)
        return []


def search_similar_operations(
    sql_text: str = "",
    operation_type: str = "",
    db_type: str = "",
    limit: int = 5,
) -> List[Dict[str, Any]]:
    """Find similar past operations for context enrichment."""
    parts = []
    if sql_text:
        # Extract key terms from SQL
        for kw in ["SELECT", "INSERT", "UPDATE", "DELETE", "ALTER", "CREATE", "DROP"]:
            if kw in sql_text.upper():
                parts.append(kw)
    if operation_type:
        parts.append(operation_type)

    if not parts:
        return []

    query = " OR ".join(parts)
    return search_sessions(query, db_type=db_type, limit=limit)


# ---------------------------------------------------------------------------
# Session Summary
# ---------------------------------------------------------------------------

def get_session_summary(session_id: str) -> Dict[str, Any]:
    """Generate a summary of a session for archival/display."""
    records = get_session_records(session_id, limit=1000)
    if not records:
        return {"session_id": session_id, "record_count": 0}

    ops = [r for r in records if r.get("operation_type")]
    risk_levels = [r["risk_level"] for r in records if r.get("risk_level", -1) >= 0]
    db_types = list({r["db_type"] for r in records if r.get("db_type")})
    instances = list({r["instance_name"] for r in records if r.get("instance_name")})

    return {
        "session_id": session_id,
        "record_count": len(records),
        "operation_count": len(ops),
        "db_types": db_types,
        "instances": instances,
        "max_risk_level": max(risk_levels) if risk_levels else -1,
        "start_time": records[0]["timestamp"],
        "end_time": records[-1]["timestamp"],
    }


# ---------------------------------------------------------------------------
# Archival
# ---------------------------------------------------------------------------

def archive_old_sessions(days: int = ARCHIVE_DAYS) -> int:
    """Mark records older than `days` as archived. Returns affected count."""
    db = _get_db()
    cutoff = time.time() - (days * 86400)
    cursor = db.execute(
        "UPDATE session_records SET archived = 1 WHERE timestamp < ? AND archived = 0",
        (cutoff,),
    )
    db.commit()
    count = cursor.rowcount
    if count:
        logger.info("Archived %d session records older than %d days", count, days)
    return count


def get_active_session_ids(limit: int = 50) -> List[str]:
    """Get distinct active (non-archived) session IDs, most recent first."""
    db = _get_db()
    rows = db.execute(
        """SELECT DISTINCT session_id FROM session_records
        WHERE archived = 0
        ORDER BY MAX(timestamp) OVER (PARTITION BY session_id) DESC
        LIMIT ?""",
        (limit,),
    ).fetchall()
    return [r[0] for r in rows]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rows_to_dicts(db: sqlite3.Connection, rows: list) -> List[Dict[str, Any]]:
    """Convert raw rows to dicts using column names."""
    if not rows:
        return []
    col_names = [
        "id", "session_id", "timestamp", "role", "content",
        "db_type", "db_version", "instance_name", "operation_type",
        "risk_level", "intent_label", "sql_text", "archived",
        "tags", "extra_data", "workspace_snapshot",
    ]
    return [dict(zip(col_names, row)) for row in rows]
