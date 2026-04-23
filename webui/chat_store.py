"""Chat conversation persistence — SQLite storage.

Tables:
  conversations — one row per chat session (id, title, timestamps, instance)
  chat_messages — ordered messages within a conversation (role, content, metadata)
  chat_messages_fts — FTS5 virtual table for full-text search across messages
"""

from __future__ import annotations

from datetime import date, datetime, time as dt_time
from decimal import Decimal
import json
import logging
import os
import sqlite3
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_webui.chat_store")

_DB_PATH = Path(__file__).parent / "chat_history.db"
_conn: Optional[sqlite3.Connection] = None


def _to_jsonable(value: Any) -> Any:
    """Recursively normalize values so task snapshots can be stored as JSON."""
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, (datetime, date, dt_time)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, dict):
        return {str(key): _to_jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_to_jsonable(item) for item in value]
    if hasattr(value, "isoformat"):
        try:
            return value.isoformat()
        except Exception:
            pass
    if hasattr(value, "value") and not callable(getattr(value, "value")):
        try:
            return _to_jsonable(value.value)
        except Exception:
            pass
    if hasattr(value, "_asdict"):
        try:
            return _to_jsonable(value._asdict())
        except Exception:
            pass
    if hasattr(value, "__dict__"):
        try:
            return _to_jsonable(vars(value))
        except Exception:
            pass
    return str(value)


# ---------------------------------------------------------------------------
# Connection
# ---------------------------------------------------------------------------

def _get_conn() -> sqlite3.Connection:
    global _conn
    if _conn is None:
        _conn = sqlite3.connect(str(_DB_PATH), check_same_thread=False)
        _conn.row_factory = sqlite3.Row
        _conn.execute("PRAGMA journal_mode=WAL")
        _conn.execute("PRAGMA foreign_keys=ON")
        _init_schema(_conn)
    return _conn


def _init_schema(conn: sqlite3.Connection):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS conversations (
            id          TEXT PRIMARY KEY,
            title       TEXT NOT NULL DEFAULT '',
            instance_name TEXT NOT NULL DEFAULT 'pg_test',
            created_at  REAL NOT NULL,
            updated_at  REAL NOT NULL,
            message_count INTEGER NOT NULL DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS chat_messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role            TEXT NOT NULL,
            content         TEXT NOT NULL,
            intent          TEXT DEFAULT NULL,
            risk_level      INTEGER DEFAULT NULL,
            task_snapshot   TEXT DEFAULT NULL,
            created_at      REAL NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_messages_conv
            ON chat_messages(conversation_id, created_at);

        -- FTS5 for search (content-less, refers back to chat_messages)
        CREATE VIRTUAL TABLE IF NOT EXISTS chat_messages_fts USING fts5(
            content,
            content=chat_messages,
            content_rowid=id
        );

        -- Triggers to keep FTS in sync
        CREATE TRIGGER IF NOT EXISTS trg_fts_insert AFTER INSERT ON chat_messages BEGIN
            INSERT INTO chat_messages_fts(rowid, content) VALUES (new.id, new.content);
        END;

        CREATE TRIGGER IF NOT EXISTS trg_fts_delete AFTER DELETE ON chat_messages BEGIN
            INSERT INTO chat_messages_fts(chat_messages_fts, rowid, content)
                VALUES('delete', old.id, old.content);
        END;
    """)
    conn.commit()


# ---------------------------------------------------------------------------
# Conversations CRUD
# ---------------------------------------------------------------------------

def create_conversation(
    title: str = "",
    instance_name: str = "pg_test",
) -> Dict[str, Any]:
    """Create a new conversation and return its metadata."""
    conn = _get_conn()
    conv_id = uuid.uuid4().hex[:16]
    now = time.time()
    conn.execute(
        "INSERT INTO conversations (id, title, instance_name, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (conv_id, title, instance_name, now, now),
    )
    conn.commit()
    return {
        "id": conv_id,
        "title": title,
        "instance_name": instance_name,
        "created_at": now,
        "updated_at": now,
        "message_count": 0,
    }


def list_conversations(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Return conversations ordered by most recent activity."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT id, title, instance_name, created_at, updated_at, message_count "
        "FROM conversations ORDER BY updated_at DESC LIMIT ? OFFSET ?",
        (limit, offset),
    ).fetchall()
    return [dict(r) for r in rows]


def get_conversation(conv_id: str) -> Optional[Dict[str, Any]]:
    """Return single conversation metadata."""
    conn = _get_conn()
    row = conn.execute(
        "SELECT id, title, instance_name, created_at, updated_at, message_count "
        "FROM conversations WHERE id = ?",
        (conv_id,),
    ).fetchone()
    return dict(row) if row else None


def delete_conversation(conv_id: str) -> bool:
    """Delete a conversation and all its messages (CASCADE)."""
    conn = _get_conn()
    cur = conn.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
    conn.commit()
    return cur.rowcount > 0


def update_conversation_title(conv_id: str, title: str):
    """Update conversation title."""
    conn = _get_conn()
    conn.execute(
        "UPDATE conversations SET title = ? WHERE id = ?",
        (title, conv_id),
    )
    conn.commit()


# ---------------------------------------------------------------------------
# Messages
# ---------------------------------------------------------------------------

def save_message(
    conversation_id: str,
    role: str,
    content: str,
    intent: str = None,
    risk_level: int = None,
    task_snapshot: dict = None,
) -> int:
    """Save a message and update conversation metadata. Returns message id."""
    conn = _get_conn()
    now = time.time()
    task_json = json.dumps(_to_jsonable(task_snapshot), ensure_ascii=False) if task_snapshot else None

    cur = conn.execute(
        "INSERT INTO chat_messages "
        "(conversation_id, role, content, intent, risk_level, task_snapshot, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (conversation_id, role, content, intent, risk_level, task_json, now),
    )
    # Update conversation counters
    conn.execute(
        "UPDATE conversations SET updated_at = ?, message_count = message_count + 1 "
        "WHERE id = ?",
        (now, conversation_id),
    )
    conn.commit()
    return cur.lastrowid


def get_messages(
    conversation_id: str,
    limit: int = 100,
    offset: int = 0,
) -> List[Dict[str, Any]]:
    """Return messages for a conversation, oldest first."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT id, role, content, intent, risk_level, task_snapshot, created_at "
        "FROM chat_messages WHERE conversation_id = ? "
        "ORDER BY created_at ASC LIMIT ? OFFSET ?",
        (conversation_id, limit, offset),
    ).fetchall()
    result = []
    for r in rows:
        msg = dict(r)
        if msg.get("task_snapshot"):
            try:
                msg["task_snapshot"] = json.loads(msg["task_snapshot"])
            except (json.JSONDecodeError, TypeError):
                pass
        result.append(msg)
    return result


def get_history_for_llm(conversation_id: str, max_messages: int = 20) -> List[Dict[str, str]]:
    """Return recent messages in OpenAI chat format for LLM context."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT role, content FROM chat_messages "
        "WHERE conversation_id = ? ORDER BY created_at DESC LIMIT ?",
        (conversation_id, max_messages),
    ).fetchall()
    # Reverse to chronological order
    return [{"role": r["role"], "content": r["content"]} for r in reversed(rows)]


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def search_conversations(query: str, limit: int = 20) -> List[Dict[str, Any]]:
    """Full-text search across all messages, return matching conversations."""
    conn = _get_conn()
    rows = conn.execute(
        "SELECT DISTINCT c.id, c.title, c.instance_name, c.created_at, "
        "c.updated_at, c.message_count "
        "FROM chat_messages_fts fts "
        "JOIN chat_messages m ON m.id = fts.rowid "
        "JOIN conversations c ON c.id = m.conversation_id "
        "WHERE chat_messages_fts MATCH ? "
        "ORDER BY c.updated_at DESC LIMIT ?",
        (query, limit),
    ).fetchall()
    return [dict(r) for r in rows]
