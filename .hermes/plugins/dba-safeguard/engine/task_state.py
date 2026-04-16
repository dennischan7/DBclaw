"""任务状态管理 — 断点续跑与状态持久化。

核心能力:
  - 全流程状态持久化到SQLite
  - 任务中断后可从断点恢复
  - 支持查询历史任务状态
  - 自动清理过期任务状态 (默认7天)
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.engine.task_state")

# State DB location
_state_db_path: Optional[Path] = None
_STATE_DB_NAME = "task_state.db"
STATE_EXPIRY_DAYS = 7


# ============================================================
# DB Setup
# ============================================================

def set_state_db_path(path: Path) -> None:
    """Override state DB path (for testing)."""
    global _state_db_path
    _state_db_path = path


def _get_state_db_path() -> Path:
    if _state_db_path:
        return _state_db_path
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    return data_dir / _STATE_DB_NAME


def _get_conn() -> sqlite3.Connection:
    db_path = _get_state_db_path()
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.row_factory = sqlite3.Row
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            sql TEXT NOT NULL,
            instance_name TEXT NOT NULL,
            dialect TEXT NOT NULL DEFAULT 'postgresql',
            user_id TEXT DEFAULT 'default',
            session_id TEXT DEFAULT '',
            user_message TEXT DEFAULT '',
            risk_level INTEGER DEFAULT 0,
            risk_label TEXT DEFAULT '',
            rollback_sql TEXT DEFAULT '',
            approved INTEGER DEFAULT 0,
            current_stage TEXT DEFAULT 'intent_classify',
            rewrite_count INTEGER DEFAULT 0,
            intent_json TEXT DEFAULT '{}',
            validation_json TEXT DEFAULT '{}',
            explain_json TEXT DEFAULT '{}',
            execution_json TEXT DEFAULT '{}',
            status TEXT DEFAULT 'running',
            created_at REAL NOT NULL,
            updated_at REAL NOT NULL,
            completed_at REAL DEFAULT NULL
        );

        CREATE TABLE IF NOT EXISTS task_stages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL REFERENCES tasks(task_id),
            stage TEXT NOT NULL,
            status TEXT NOT NULL,
            data_json TEXT DEFAULT '{}',
            error TEXT DEFAULT '',
            duration_ms INTEGER DEFAULT 0,
            created_at REAL NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_session ON tasks(session_id);
        CREATE INDEX IF NOT EXISTS idx_stages_task ON task_stages(task_id);
    """)


# ============================================================
# Save / Load Task
# ============================================================

def save_task(task) -> None:
    """Save a DBATask to the state database.

    Accepts a DBATask dataclass from dba_loop.py.
    """
    now = time.time()
    conn = _get_conn()
    try:
        # Determine status
        try:
            from .dba_loop import StageStatus
        except ImportError:
            from engine.dba_loop import StageStatus
        has_failure = any(
            s.status == StageStatus.FAILED for s in task.stage_results
        )
        has_blocked = any(
            s.status == StageStatus.BLOCKED for s in task.stage_results
        )
        all_passed = all(
            s.status in (StageStatus.PASSED, StageStatus.SKIPPED)
            for s in task.stage_results
        ) and len(task.stage_results) > 0

        if has_failure:
            status = "failed"
        elif has_blocked:
            status = "blocked"
        elif all_passed:
            status = "completed"
        else:
            status = "running"

        completed_at = now if status in ("completed", "failed") else None

        conn.execute("""
            INSERT INTO tasks (
                task_id, sql, instance_name, dialect, user_id, session_id,
                user_message, risk_level, risk_label, rollback_sql, approved,
                current_stage, rewrite_count, intent_json, validation_json,
                explain_json, execution_json, status, created_at, updated_at,
                completed_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(task_id) DO UPDATE SET
                risk_level=excluded.risk_level,
                risk_label=excluded.risk_label,
                rollback_sql=excluded.rollback_sql,
                approved=excluded.approved,
                current_stage=excluded.current_stage,
                rewrite_count=excluded.rewrite_count,
                intent_json=excluded.intent_json,
                validation_json=excluded.validation_json,
                explain_json=excluded.explain_json,
                execution_json=excluded.execution_json,
                status=excluded.status,
                updated_at=excluded.updated_at,
                completed_at=excluded.completed_at
        """, (
            task.task_id, task.sql, task.instance_name, task.dialect,
            task.user_id, task.session_id, task.user_message,
            task.risk_level, task.risk_label, task.rollback_sql,
            1 if task.approved else 0, task.current_stage.value,
            task.rewrite_count,
            json.dumps(task.intent, ensure_ascii=False, default=str),
            json.dumps(task.validation, ensure_ascii=False, default=str),
            json.dumps(task.explain_result, ensure_ascii=False, default=str),
            json.dumps(task.execution_result, ensure_ascii=False, default=str),
            status, now, now, completed_at,
        ))

        # Save stage results
        for sr in task.stage_results:
            conn.execute("""
                INSERT INTO task_stages (task_id, stage, status, data_json, error, duration_ms, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                task.task_id, sr.stage.value, sr.status.value,
                json.dumps(sr.data, ensure_ascii=False, default=str),
                sr.error, sr.duration_ms, now,
            ))

        conn.commit()
    finally:
        conn.close()


def load_task(task_id: str):
    """Load a DBATask from the state database.

    Returns a DBATask ready for pipeline resumption, or None if not found.
    """
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT * FROM tasks WHERE task_id = ?", (task_id,)
        ).fetchone()
        if not row:
            return None

        try:
            from .dba_loop import DBATask, PipelineStage, StepResult, StageStatus
        except ImportError:
            from engine.dba_loop import DBATask, PipelineStage, StepResult, StageStatus

        task = DBATask(
            task_id=row["task_id"],
            sql=row["sql"],
            instance_name=row["instance_name"],
            dialect=row["dialect"],
            user_id=row["user_id"],
            session_id=row["session_id"],
            user_message=row["user_message"],
            risk_level=row["risk_level"],
            risk_label=row["risk_label"],
            rollback_sql=row["rollback_sql"],
            approved=bool(row["approved"]),
            rewrite_count=row["rewrite_count"],
        )

        # Restore complex fields
        task.intent = json.loads(row["intent_json"] or "{}")
        task.validation = json.loads(row["validation_json"] or "{}")
        task.explain_result = json.loads(row["explain_json"] or "{}")
        task.execution_result = json.loads(row["execution_json"] or "{}")
        task.current_stage = PipelineStage(row["current_stage"])

        # Restore stage results
        stage_rows = conn.execute(
            "SELECT * FROM task_stages WHERE task_id = ? ORDER BY id",
            (task_id,),
        ).fetchall()
        for sr in stage_rows:
            task.stage_results.append(StepResult(
                stage=PipelineStage(sr["stage"]),
                status=StageStatus(sr["status"]),
                data=json.loads(sr["data_json"] or "{}"),
                error=sr["error"] or "",
                duration_ms=sr["duration_ms"],
            ))

        return task
    finally:
        conn.close()


# ============================================================
# Query & Management
# ============================================================

def list_tasks(
    status: Optional[str] = None,
    session_id: Optional[str] = None,
    limit: int = 50,
) -> List[Dict[str, Any]]:
    """List tasks filtered by status/session."""
    conn = _get_conn()
    try:
        query = "SELECT task_id, sql, instance_name, dialect, risk_level, risk_label, status, current_stage, created_at, updated_at FROM tasks"
        params: list = []
        conditions = []

        if status:
            conditions.append("status = ?")
            params.append(status)
        if session_id:
            conditions.append("session_id = ?")
            params.append(session_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY updated_at DESC LIMIT ?"
        params.append(limit)

        rows = conn.execute(query, params).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_task_status(task_id: str) -> Optional[Dict[str, Any]]:
    """Get current status of a task."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT task_id, status, current_stage, risk_level, risk_label, rewrite_count, created_at, updated_at FROM tasks WHERE task_id = ?",
            (task_id,),
        ).fetchone()
        if not row:
            return None

        stages = conn.execute(
            "SELECT stage, status, error, duration_ms FROM task_stages WHERE task_id = ? ORDER BY id",
            (task_id,),
        ).fetchall()

        result = dict(row)
        result["stages"] = [dict(s) for s in stages]
        return result
    finally:
        conn.close()


def approve_task(task_id: str) -> bool:
    """Mark a blocked task as approved, allowing pipeline resumption."""
    conn = _get_conn()
    try:
        cursor = conn.execute(
            "UPDATE tasks SET approved = 1, status = 'running', updated_at = ? WHERE task_id = ? AND status = 'blocked'",
            (time.time(), task_id),
        )
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def cleanup_expired(days: int = STATE_EXPIRY_DAYS) -> int:
    """Remove tasks older than `days` days."""
    conn = _get_conn()
    try:
        cutoff = time.time() - (days * 86400)
        # Delete stages first (FK)
        conn.execute(
            "DELETE FROM task_stages WHERE task_id IN (SELECT task_id FROM tasks WHERE updated_at < ?)",
            (cutoff,),
        )
        cursor = conn.execute(
            "DELETE FROM tasks WHERE updated_at < ?", (cutoff,),
        )
        conn.commit()
        return cursor.rowcount
    finally:
        conn.close()
