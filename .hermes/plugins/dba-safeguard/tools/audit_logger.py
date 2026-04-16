"""审计日志工具 — 全链路操作记录，所有数据库操作全程留痕。

安全约束:
  - Append-only: 禁止修改/删除已生成的审计日志
  - 审计日志永久留存
  - 支持按时间/用户/风险等级/数据库/操作类型检索
  - 支持批量导出CSV
"""

from __future__ import annotations

import csv
import io
import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.tools.audit_logger")

# ---------------------------------------------------------------------------
# Audit Database
# ---------------------------------------------------------------------------

_AUDIT_DB_PATH: Optional[Path] = None
_AUDIT_CONN: Optional[sqlite3.Connection] = None


def set_audit_db_path(path: Path) -> None:
    """Override the audit database path (for testing)."""
    global _AUDIT_DB_PATH, _AUDIT_CONN
    if _AUDIT_CONN is not None:
        _AUDIT_CONN.close()
        _AUDIT_CONN = None
    _AUDIT_DB_PATH = path

AUDIT_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp REAL NOT NULL,
    session_id TEXT,
    user_id TEXT DEFAULT 'default',
    instance_name TEXT,
    dialect TEXT,
    operation_type TEXT,
    risk_level INTEGER DEFAULT 0,
    risk_label TEXT,
    original_sql TEXT,
    validation_result TEXT,
    approval_status TEXT DEFAULT 'N/A',
    execution_result TEXT,
    execution_time_ms INTEGER DEFAULT 0,
    rollback_sql TEXT,
    error_message TEXT,
    extra_data TEXT
);

CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_log(timestamp);
CREATE INDEX IF NOT EXISTS idx_audit_risk ON audit_log(risk_level);
CREATE INDEX IF NOT EXISTS idx_audit_instance ON audit_log(instance_name);
CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_log(user_id);
"""


def _get_audit_db() -> sqlite3.Connection:
    global _AUDIT_CONN, _AUDIT_DB_PATH
    if _AUDIT_CONN is not None:
        return _AUDIT_CONN

    if _AUDIT_DB_PATH is None:
        artifacts_dir = Path(__file__).parent.parent.parent.parent.parent / "artifacts" / "audit"
        artifacts_dir.mkdir(parents=True, exist_ok=True)
        _AUDIT_DB_PATH = artifacts_dir / "audit.db"

    _AUDIT_CONN = sqlite3.connect(str(_AUDIT_DB_PATH), check_same_thread=False)
    _AUDIT_CONN.execute("PRAGMA journal_mode=WAL")
    _AUDIT_CONN.executescript(AUDIT_SCHEMA_SQL)
    return _AUDIT_CONN


def log_audit_event(
    session_id: str = "",
    user_id: str = "default",
    instance_name: str = "",
    dialect: str = "",
    operation_type: str = "",
    risk_level: int = 0,
    risk_label: str = "",
    original_sql: str = "",
    validation_result: str = "",
    approval_status: str = "N/A",
    execution_result: str = "",
    execution_time_ms: int = 0,
    rollback_sql: str = "",
    error_message: str = "",
    extra_data: str = "",
) -> int:
    """Append an audit log entry. Returns the row ID."""
    db = _get_audit_db()
    cursor = db.execute(
        """INSERT INTO audit_log
        (timestamp, session_id, user_id, instance_name, dialect,
         operation_type, risk_level, risk_label, original_sql,
         validation_result, approval_status, execution_result,
         execution_time_ms, rollback_sql, error_message, extra_data)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (
            time.time(), session_id, user_id, instance_name, dialect,
            operation_type, risk_level, risk_label, original_sql,
            validation_result, approval_status, execution_result,
            execution_time_ms, rollback_sql, error_message, extra_data,
        ),
    )
    db.commit()
    return cursor.lastrowid


def query_audit_logs(
    start_time: float = 0,
    end_time: float = 0,
    user_id: str = "",
    instance_name: str = "",
    risk_level: Optional[int] = None,
    operation_type: str = "",
    limit: int = 100,
) -> List[Dict]:
    """Query audit logs with filters."""
    db = _get_audit_db()
    conditions = []
    params = []

    if start_time > 0:
        conditions.append("timestamp >= ?")
        params.append(start_time)
    if end_time > 0:
        conditions.append("timestamp <= ?")
        params.append(end_time)
    if user_id:
        conditions.append("user_id = ?")
        params.append(user_id)
    if instance_name:
        conditions.append("instance_name = ?")
        params.append(instance_name)
    if risk_level is not None:
        conditions.append("risk_level = ?")
        params.append(risk_level)
    if operation_type:
        conditions.append("operation_type = ?")
        params.append(operation_type)

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    sql = f"SELECT * FROM audit_log {where} ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    db.row_factory = sqlite3.Row
    rows = db.execute(sql, params).fetchall()
    db.row_factory = None
    return [dict(r) for r in rows]


def export_audit_csv(logs: List[Dict]) -> str:
    """Export audit logs as CSV string."""
    if not logs:
        return ""
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=logs[0].keys())
    writer.writeheader()
    writer.writerows(logs)
    return output.getvalue()


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_audit_query(args: dict, task_id: str = "", **kwargs) -> str:
    logs = query_audit_logs(
        start_time=args.get("start_time", 0),
        end_time=args.get("end_time", 0),
        user_id=args.get("user_id", ""),
        instance_name=args.get("instance_name", ""),
        risk_level=args.get("risk_level"),
        operation_type=args.get("operation_type", ""),
        limit=args.get("limit", 100),
    )

    if args.get("export_csv", False):
        csv_data = export_audit_csv(logs)
        return json.dumps({"format": "csv", "data": csv_data, "count": len(logs)})

    return json.dumps({"logs": logs, "count": len(logs)}, ensure_ascii=False, default=str)


AUDIT_QUERY_SCHEMA = {
    "name": "audit_query",
    "description": (
        "查询DBA审计日志。支持按时间、用户、数据库实例、风险等级、操作类型筛选。"
        "支持导出CSV格式。审计日志永久留存，不可修改删除。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "start_time": {"type": "number", "description": "起始时间戳(Unix)"},
            "end_time": {"type": "number", "description": "结束时间戳(Unix)"},
            "user_id": {"type": "string", "description": "用户ID"},
            "instance_name": {"type": "string", "description": "数据库实例名称"},
            "risk_level": {"type": "integer", "description": "风险等级(0-4)"},
            "operation_type": {"type": "string", "description": "操作类型"},
            "limit": {"type": "integer", "description": "返回条数(默认100)", "default": 100},
            "export_csv": {"type": "boolean", "description": "是否导出CSV格式"},
        },
        "required": [],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="audit_query",
        toolset="dba-safeguard",
        schema=AUDIT_QUERY_SCHEMA["parameters"],
        handler=handle_audit_query,
        description=AUDIT_QUERY_SCHEMA["description"],
        emoji="📝",
    )
