"""审批流程管理器 — 创建/通过/驳回/修改后执行 + 审计留痕。

核心流程:
  1. 高危操作触发审批 → create_approval_request()
  2. 审批信息包含: SQL, 风险等级, 校验结果, 回滚脚本
  3. 审批操作: approve / reject / modify_and_approve
  4. 所有审批操作不可篡改，永久审计留痕
  5. 未通过审批的任务绝对禁止执行
  6. 审批环节禁止修改原始SQL的风险等级

设计约束:
  - 单人审批，无超时
  - 审批记录永久留存，不可修改/删除
  - 生成 SSE 兼容事件供前端推送
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.security.approval_manager")


# ============================================================
# Approval Status
# ============================================================

class ApprovalStatus(str, Enum):
    PENDING = "pending"        # 等待审批
    APPROVED = "approved"      # 已通过
    REJECTED = "rejected"      # 已驳回
    MODIFIED = "modified"      # 修改后执行


# ============================================================
# SSE Event Types
# ============================================================

class ApprovalEventType(str, Enum):
    """SSE事件类型，前端订阅。"""
    APPROVAL_REQUESTED = "approval_requested"
    APPROVAL_APPROVED = "approval_approved"
    APPROVAL_REJECTED = "approval_rejected"
    APPROVAL_MODIFIED = "approval_modified"


# ============================================================
# Data Models
# ============================================================

@dataclass
class ApprovalRequest:
    """审批请求。"""
    request_id: str
    task_id: str
    sql: str
    risk_level: int
    risk_label: str
    operation_type: str
    instance_name: str
    dialect: str
    tables_affected: List[str]
    validation_summary: str
    rollback_sql: str
    created_by: str
    status: ApprovalStatus = ApprovalStatus.PENDING
    reviewer: str = ""
    review_comment: str = ""
    modified_sql: str = ""
    created_at: str = ""
    reviewed_at: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "request_id": self.request_id,
            "task_id": self.task_id,
            "sql": self.sql,
            "risk_level": self.risk_level,
            "risk_label": self.risk_label,
            "operation_type": self.operation_type,
            "instance_name": self.instance_name,
            "dialect": self.dialect,
            "tables_affected": self.tables_affected,
            "validation_summary": self.validation_summary,
            "rollback_sql": self.rollback_sql,
            "created_by": self.created_by,
            "status": self.status.value,
            "reviewer": self.reviewer,
            "review_comment": self.review_comment,
            "modified_sql": self.modified_sql,
            "created_at": self.created_at,
            "reviewed_at": self.reviewed_at,
        }

    def to_sse_event(self, event_type: ApprovalEventType) -> Dict[str, Any]:
        """Generate SSE-compatible event data."""
        return {
            "event": event_type.value,
            "data": {
                "request_id": self.request_id,
                "task_id": self.task_id,
                "sql": self.sql[:500],
                "risk_level": self.risk_level,
                "risk_label": self.risk_label,
                "operation_type": self.operation_type,
                "instance_name": self.instance_name,
                "tables_affected": self.tables_affected,
                "validation_summary": self.validation_summary[:300],
                "rollback_sql": self.rollback_sql[:500],
                "status": self.status.value,
                "reviewer": self.reviewer,
                "review_comment": self.review_comment,
                "created_at": self.created_at,
                "reviewed_at": self.reviewed_at,
            },
        }


# ============================================================
# Persistence
# ============================================================

_DB_PATH: Optional[Path] = None
_event_listeners: List[Callable] = []


def set_approval_db_path(path: Path) -> None:
    """Override DB path (for testing)."""
    global _DB_PATH
    _DB_PATH = path


def _get_db_path() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    return Path(__file__).parent.parent / "data" / "approval.db"


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
        CREATE TABLE IF NOT EXISTS approval_requests (
            request_id       TEXT PRIMARY KEY,
            task_id          TEXT NOT NULL,
            sql_text         TEXT NOT NULL,
            risk_level       INTEGER NOT NULL,
            risk_label       TEXT NOT NULL DEFAULT '',
            operation_type   TEXT NOT NULL DEFAULT '',
            instance_name    TEXT NOT NULL DEFAULT '',
            dialect          TEXT NOT NULL DEFAULT 'postgresql',
            tables_affected  TEXT NOT NULL DEFAULT '[]',
            validation_summary TEXT NOT NULL DEFAULT '',
            rollback_sql     TEXT NOT NULL DEFAULT '',
            created_by       TEXT NOT NULL DEFAULT 'system',
            status           TEXT NOT NULL DEFAULT 'pending',
            reviewer         TEXT NOT NULL DEFAULT '',
            review_comment   TEXT NOT NULL DEFAULT '',
            modified_sql     TEXT NOT NULL DEFAULT '',
            created_at       TEXT NOT NULL DEFAULT (datetime('now')),
            reviewed_at      TEXT NOT NULL DEFAULT ''
        );

        -- 审计表: 不可修改不可删除, 永久留存
        CREATE TABLE IF NOT EXISTS approval_audit (
            audit_id    INTEGER PRIMARY KEY AUTOINCREMENT,
            request_id  TEXT NOT NULL,
            action      TEXT NOT NULL,
            actor       TEXT NOT NULL DEFAULT '',
            detail      TEXT NOT NULL DEFAULT '',
            created_at  TEXT NOT NULL DEFAULT (datetime('now'))
        );

        CREATE INDEX IF NOT EXISTS idx_approval_status
            ON approval_requests(status);
        CREATE INDEX IF NOT EXISTS idx_approval_task
            ON approval_requests(task_id);
        CREATE INDEX IF NOT EXISTS idx_audit_request
            ON approval_audit(request_id);
    """)
    conn.commit()


# ============================================================
# Event Listener (for SSE push)
# ============================================================

def register_event_listener(listener: Callable[[Dict[str, Any]], None]) -> None:
    """Register a listener for approval events (SSE push)."""
    _event_listeners.append(listener)


def clear_event_listeners() -> None:
    """Clear all event listeners."""
    _event_listeners.clear()


def _emit_event(event: Dict[str, Any]) -> None:
    """Emit event to all registered listeners."""
    for listener in _event_listeners:
        try:
            listener(event)
        except Exception as e:
            logger.warning("Event listener error: %s", e)


# ============================================================
# Approval Request CRUD
# ============================================================

def create_approval_request(
    task_id: str,
    sql: str,
    risk_level: int,
    risk_label: str = "",
    operation_type: str = "",
    instance_name: str = "",
    dialect: str = "postgresql",
    tables_affected: Optional[List[str]] = None,
    validation_summary: str = "",
    rollback_sql: str = "",
    created_by: str = "system",
) -> ApprovalRequest:
    """Create a new approval request.

    Returns:
        ApprovalRequest with request_id
    """
    request_id = f"apr-{uuid.uuid4().hex[:12]}"
    tables = tables_affected or []

    conn = _get_conn()
    try:
        conn.execute(
            "INSERT INTO approval_requests "
            "(request_id, task_id, sql_text, risk_level, risk_label, operation_type, "
            "instance_name, dialect, tables_affected, validation_summary, "
            "rollback_sql, created_by) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (request_id, task_id, sql, risk_level, risk_label, operation_type,
             instance_name, dialect, json.dumps(tables), validation_summary,
             rollback_sql, created_by),
        )
        # Audit trail
        conn.execute(
            "INSERT INTO approval_audit (request_id, action, actor, detail) "
            "VALUES (?, 'created', ?, ?)",
            (request_id, created_by, f"审批请求创建: L{risk_level} {operation_type}"),
        )
        conn.commit()

        request = _load_request(conn, request_id)
    finally:
        conn.close()

    # Emit SSE event
    if request:
        _emit_event(request.to_sse_event(ApprovalEventType.APPROVAL_REQUESTED))

    return request


def approve_request(
    request_id: str,
    reviewer: str,
    comment: str = "",
) -> Dict[str, Any]:
    """Approve a pending request.

    Returns:
        dict with success/error, request data
    """
    conn = _get_conn()
    try:
        request = _load_request(conn, request_id)
        if not request:
            return {"success": False, "error": f"审批请求 {request_id} 不存在"}
        if request.status != ApprovalStatus.PENDING:
            return {
                "success": False,
                "error": f"审批请求状态为 {request.status.value}，不可审批",
            }

        conn.execute(
            "UPDATE approval_requests SET status='approved', reviewer=?, "
            "review_comment=?, reviewed_at=datetime('now') WHERE request_id=?",
            (reviewer, comment, request_id),
        )
        conn.execute(
            "INSERT INTO approval_audit (request_id, action, actor, detail) "
            "VALUES (?, 'approved', ?, ?)",
            (request_id, reviewer, f"审批通过: {comment}"),
        )
        conn.commit()

        updated = _load_request(conn, request_id)
        if updated:
            _emit_event(updated.to_sse_event(ApprovalEventType.APPROVAL_APPROVED))

        return {"success": True, "request": updated.to_dict() if updated else None}
    finally:
        conn.close()


def reject_request(
    request_id: str,
    reviewer: str,
    comment: str = "",
) -> Dict[str, Any]:
    """Reject a pending request. Comment is required.

    Returns:
        dict with success/error
    """
    if not comment.strip():
        return {"success": False, "error": "驳回审批必须填写原因"}

    conn = _get_conn()
    try:
        request = _load_request(conn, request_id)
        if not request:
            return {"success": False, "error": f"审批请求 {request_id} 不存在"}
        if request.status != ApprovalStatus.PENDING:
            return {
                "success": False,
                "error": f"审批请求状态为 {request.status.value}，不可驳回",
            }

        conn.execute(
            "UPDATE approval_requests SET status='rejected', reviewer=?, "
            "review_comment=?, reviewed_at=datetime('now') WHERE request_id=?",
            (reviewer, comment, request_id),
        )
        conn.execute(
            "INSERT INTO approval_audit (request_id, action, actor, detail) "
            "VALUES (?, 'rejected', ?, ?)",
            (request_id, reviewer, f"审批驳回: {comment}"),
        )
        conn.commit()

        updated = _load_request(conn, request_id)
        if updated:
            _emit_event(updated.to_sse_event(ApprovalEventType.APPROVAL_REJECTED))

        return {"success": True, "request": updated.to_dict() if updated else None}
    finally:
        conn.close()


def modify_and_approve(
    request_id: str,
    reviewer: str,
    modified_sql: str,
    comment: str = "",
) -> Dict[str, Any]:
    """Approve with modified SQL.

    The modified SQL replaces the original for execution, but:
      - Original SQL is preserved in audit trail
      - Risk level is NOT re-assessed (禁止审批环节修改风险等级)
      - Modified SQL is recorded separately
    """
    if not modified_sql.strip():
        return {"success": False, "error": "修改后的SQL不能为空"}

    conn = _get_conn()
    try:
        request = _load_request(conn, request_id)
        if not request:
            return {"success": False, "error": f"审批请求 {request_id} 不存在"}
        if request.status != ApprovalStatus.PENDING:
            return {
                "success": False,
                "error": f"审批请求状态为 {request.status.value}，不可修改",
            }

        conn.execute(
            "UPDATE approval_requests SET status='modified', reviewer=?, "
            "review_comment=?, modified_sql=?, reviewed_at=datetime('now') "
            "WHERE request_id=?",
            (reviewer, comment, modified_sql, request_id),
        )
        conn.execute(
            "INSERT INTO approval_audit (request_id, action, actor, detail) "
            "VALUES (?, 'modified', ?, ?)",
            (request_id, reviewer,
             f"修改后执行: 原SQL保留, 修改SQL={modified_sql[:200]}; {comment}"),
        )
        conn.commit()

        updated = _load_request(conn, request_id)
        if updated:
            _emit_event(updated.to_sse_event(ApprovalEventType.APPROVAL_MODIFIED))

        return {"success": True, "request": updated.to_dict() if updated else None}
    finally:
        conn.close()


# ============================================================
# Query
# ============================================================

def get_request(request_id: str) -> Optional[ApprovalRequest]:
    """Get a single approval request."""
    conn = _get_conn()
    try:
        return _load_request(conn, request_id)
    finally:
        conn.close()


def get_pending_requests(limit: int = 50) -> List[ApprovalRequest]:
    """Get all pending approval requests."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT * FROM approval_requests WHERE status='pending' "
            "ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
        return [_row_to_request(r) for r in rows]
    finally:
        conn.close()


def get_request_history(
    task_id: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = 50,
) -> List[ApprovalRequest]:
    """Get approval request history with optional filters."""
    conn = _get_conn()
    try:
        query = "SELECT * FROM approval_requests WHERE 1=1"
        params: List[Any] = []
        if task_id:
            query += " AND task_id=?"
            params.append(task_id)
        if status:
            query += " AND status=?"
            params.append(status)
        query += " ORDER BY created_at DESC LIMIT ?"
        params.append(limit)
        rows = conn.execute(query, params).fetchall()
        return [_row_to_request(r) for r in rows]
    finally:
        conn.close()


def get_audit_trail(request_id: str) -> List[Dict[str, Any]]:
    """Get immutable audit trail for a request."""
    conn = _get_conn()
    try:
        rows = conn.execute(
            "SELECT audit_id, request_id, action, actor, detail, created_at "
            "FROM approval_audit WHERE request_id=? ORDER BY audit_id ASC",
            (request_id,),
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def is_approved(request_id: str) -> bool:
    """Check if a request has been approved (approved or modified)."""
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT status FROM approval_requests WHERE request_id=?",
            (request_id,),
        ).fetchone()
        return row is not None and row["status"] in ("approved", "modified")
    finally:
        conn.close()


def get_effective_sql(request_id: str) -> Optional[str]:
    """Get the SQL that should actually be executed.

    Returns modified_sql if status=modified, else original sql.
    """
    conn = _get_conn()
    try:
        row = conn.execute(
            "SELECT sql_text, modified_sql, status FROM approval_requests WHERE request_id=?",
            (request_id,),
        ).fetchone()
        if not row:
            return None
        if row["status"] == "modified" and row["modified_sql"]:
            return row["modified_sql"]
        return row["sql_text"]
    finally:
        conn.close()


# ============================================================
# Stats
# ============================================================

def get_approval_stats() -> Dict[str, Any]:
    """Get approval statistics."""
    conn = _get_conn()
    try:
        total = conn.execute("SELECT COUNT(*) as c FROM approval_requests").fetchone()["c"]
        pending = conn.execute(
            "SELECT COUNT(*) as c FROM approval_requests WHERE status='pending'"
        ).fetchone()["c"]
        approved = conn.execute(
            "SELECT COUNT(*) as c FROM approval_requests WHERE status='approved'"
        ).fetchone()["c"]
        rejected = conn.execute(
            "SELECT COUNT(*) as c FROM approval_requests WHERE status='rejected'"
        ).fetchone()["c"]
        modified = conn.execute(
            "SELECT COUNT(*) as c FROM approval_requests WHERE status='modified'"
        ).fetchone()["c"]

        # Risk distribution
        risk_dist = {}
        for row in conn.execute(
            "SELECT risk_level, COUNT(*) as c FROM approval_requests GROUP BY risk_level"
        ).fetchall():
            risk_dist[f"L{row['risk_level']}"] = row["c"]

        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
            "modified": modified,
            "risk_distribution": risk_dist,
        }
    finally:
        conn.close()


# ============================================================
# Internal Helpers
# ============================================================

def _load_request(conn: sqlite3.Connection, request_id: str) -> Optional[ApprovalRequest]:
    row = conn.execute(
        "SELECT * FROM approval_requests WHERE request_id=?",
        (request_id,),
    ).fetchone()
    if not row:
        return None
    return _row_to_request(row)


def _row_to_request(row: sqlite3.Row) -> ApprovalRequest:
    tables = []
    try:
        tables = json.loads(row["tables_affected"])
    except (json.JSONDecodeError, TypeError):
        pass
    return ApprovalRequest(
        request_id=row["request_id"],
        task_id=row["task_id"],
        sql=row["sql_text"],
        risk_level=row["risk_level"],
        risk_label=row["risk_label"],
        operation_type=row["operation_type"],
        instance_name=row["instance_name"],
        dialect=row["dialect"],
        tables_affected=tables,
        validation_summary=row["validation_summary"],
        rollback_sql=row["rollback_sql"],
        created_by=row["created_by"],
        status=ApprovalStatus(row["status"]),
        reviewer=row["reviewer"],
        review_comment=row["review_comment"],
        modified_sql=row["modified_sql"],
        created_at=row["created_at"],
        reviewed_at=row["reviewed_at"],
    )
