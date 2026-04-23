"""安全执行器 — 审批通过的SQL执行入口。

安全约束:
  - 仅审批通过的操作可进入执行
  - L2+操作必须先生成回滚脚本
  - 使用管理员连接执行写操作
  - 事务封装: L1+ 操作在显式事务中执行，异常自动回滚
  - 执行前/后自动记录审计日志
  - 执行超时控制 (默认60s)
  - L2+ UPDATE/DELETE 执行前自动快照受影响行
"""

from __future__ import annotations

import json
import logging
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.tools.safe_executor")

DEFAULT_EXECUTION_TIMEOUT = 60  # seconds
DEFAULT_RESULT_PAGE_SIZE = 100
RESULT_CACHE_TTL_SECONDS = 600

_RESULT_CACHE: Dict[str, Dict[str, Any]] = {}
_RESULT_CACHE_LOCK = threading.Lock()


def _row_to_list(row: Any) -> List[Any]:
    return list(row)


def _close_result_cache_entry(entry: Dict[str, Any]) -> None:
    result = entry.get("result")
    connection = entry.get("connection")
    try:
        if result is not None:
            result.close()
    except Exception:
        pass
    try:
        if connection is not None:
            connection.close()
    except Exception:
        pass
    entry["result"] = None
    entry["connection"] = None


def _prune_expired_result_cache(now: Optional[float] = None) -> None:
    now = now or time.time()
    expired_ids: List[str] = []
    with _RESULT_CACHE_LOCK:
        for result_set_id, entry in _RESULT_CACHE.items():
            if now - entry.get("created_at", now) > RESULT_CACHE_TTL_SECONDS:
                expired_ids.append(result_set_id)
        for result_set_id in expired_ids:
            entry = _RESULT_CACHE.pop(result_set_id, None)
            if entry is not None:
                _close_result_cache_entry(entry)


def bind_result_cache_owner(
    result_set_id: str,
    *,
    conversation_id: str = "",
    user_id: str = "",
) -> bool:
    if not result_set_id:
        return False
    _prune_expired_result_cache()
    with _RESULT_CACHE_LOCK:
        entry = _RESULT_CACHE.get(result_set_id)
        if entry is None:
            return False
        if conversation_id:
            entry["conversation_id"] = conversation_id
        if user_id:
            entry["user_id"] = user_id
        return True


def _entry_has_more(entry: Dict[str, Any], next_offset: int) -> bool:
    if entry.get("loaded_count", 0) > next_offset:
        return True
    return not entry.get("exhausted", True)


def fetch_result_page(
    result_set_id: str,
    *,
    offset: int = 0,
    limit: int = DEFAULT_RESULT_PAGE_SIZE,
    conversation_id: str = "",
    user_id: str = "",
) -> Dict[str, Any]:
    _prune_expired_result_cache()
    limit = max(1, min(int(limit), DEFAULT_RESULT_PAGE_SIZE))
    offset = max(0, int(offset))

    with _RESULT_CACHE_LOCK:
        entry = _RESULT_CACHE.get(result_set_id)

    if entry is None:
        return {"error": "结果集不存在或已过期"}

    entry_conversation_id = entry.get("conversation_id") or ""
    entry_user_id = entry.get("user_id") or ""
    if conversation_id and entry_conversation_id and conversation_id != entry_conversation_id:
        return {"error": "无权访问该结果集"}
    if user_id and entry_user_id and user_id != entry_user_id:
        return {"error": "无权访问该结果集"}

    with entry["lock"]:
        pages = entry["pages"]
        page_rows = pages.get(offset)
        if page_rows is None:
            if offset != entry.get("loaded_count", 0):
                return {"error": "结果集仅支持顺序加载下一批数据"}

            if entry.get("exhausted", False):
                return {
                    "result_set_id": result_set_id,
                    "columns": entry.get("columns", []),
                    "rows": [],
                    "offset": offset,
                    "limit": limit,
                    "loaded_count": entry.get("loaded_count", 0),
                    "page_size": entry.get("page_size", DEFAULT_RESULT_PAGE_SIZE),
                    "has_more": False,
                }

            page_rows = []
            buffered_rows = entry["buffered_rows"]
            while buffered_rows and len(page_rows) < limit:
                page_rows.append(buffered_rows.pop(0))

            while len(page_rows) < limit and not entry.get("exhausted", False):
                result = entry.get("result")
                if result is None:
                    entry["exhausted"] = True
                    break
                fetched = result.fetchmany(limit - len(page_rows))
                if not fetched:
                    entry["exhausted"] = True
                    _close_result_cache_entry(entry)
                    break
                page_rows.extend(_row_to_list(row) for row in fetched)

            if page_rows:
                pages[offset] = page_rows
                entry["loaded_count"] = max(entry.get("loaded_count", 0), offset + len(page_rows))

            if not entry.get("exhausted", False) and not entry["buffered_rows"]:
                result = entry.get("result")
                if result is None:
                    entry["exhausted"] = True
                else:
                    peek = result.fetchmany(1)
                    if peek:
                        entry["buffered_rows"].extend(_row_to_list(row) for row in peek)
                    else:
                        entry["exhausted"] = True
                        _close_result_cache_entry(entry)

        next_offset = offset + len(page_rows)
        payload: Dict[str, Any] = {
            "result_set_id": result_set_id,
            "columns": entry.get("columns", []),
            "rows": page_rows,
            "offset": offset,
            "limit": limit,
            "loaded_count": entry.get("loaded_count", 0),
            "page_size": entry.get("page_size", DEFAULT_RESULT_PAGE_SIZE),
            "has_more": _entry_has_more(entry, next_offset),
        }
        if entry.get("exhausted", False):
            payload["total_rows"] = entry.get("loaded_count", 0)
        return payload


def _build_result_preview(
    rs: Any,
    conn: Any,
    *,
    task_id: str,
    session_id: str,
    user_id: str,
) -> Dict[str, Any]:
    columns = list(rs.keys()) if hasattr(rs, "keys") else []
    preview_rows = [_row_to_list(row) for row in rs.fetchmany(DEFAULT_RESULT_PAGE_SIZE)]
    buffered_rows = [_row_to_list(row) for row in rs.fetchmany(1)]
    has_more = bool(buffered_rows)

    data: Dict[str, Any] = {
        "columns": columns,
        "rows": preview_rows,
        "page_size": DEFAULT_RESULT_PAGE_SIZE,
        "loaded_count": len(preview_rows),
        "has_more": has_more,
        "preview_limited": has_more,
    }

    if not has_more:
        data["total_rows"] = len(preview_rows)
        try:
            rs.close()
        finally:
            conn.close()
        return data

    result_set_id = task_id or f"result_{uuid.uuid4().hex}"
    entry = {
        "created_at": time.time(),
        "result": rs,
        "connection": conn,
        "columns": columns,
        "page_size": DEFAULT_RESULT_PAGE_SIZE,
        "pages": {0: preview_rows},
        "loaded_count": len(preview_rows),
        "buffered_rows": buffered_rows,
        "exhausted": False,
        "session_id": session_id,
        "user_id": user_id,
        "conversation_id": "",
        "lock": threading.Lock(),
    }
    with _RESULT_CACHE_LOCK:
        old_entry = _RESULT_CACHE.pop(result_set_id, None)
        if old_entry is not None:
            _close_result_cache_entry(old_entry)
        _RESULT_CACHE[result_set_id] = entry

    data["result_set_id"] = result_set_id
    return data


def execute_sql(
    sql: str,
    instance_name: str,
    dialect: str = "mysql",
    *,
    risk_level: int = 0,
    approved: bool = False,
    rollback_sql: str = "",
    task_id: str = "",
    session_id: str = "",
    user_id: str = "default",
    timeout: int = DEFAULT_EXECUTION_TIMEOUT,
    snapshot: bool = True,
) -> Dict[str, Any]:
    """Execute an approved SQL statement safely.

    Flow:
      1. Safety gate checks
      2. Audit log: record attempt
      3. For L2+ UPDATE/DELETE: snapshot affected rows (if snapshot=True)
      4. Execute in transaction with timeout
      5. Audit log: record result
    """
    result: Dict[str, Any] = {
        "success": False,
        "data": None,
        "rows_affected": 0,
        "execution_time_ms": 0,
        "error": None,
        "snapshot_rows": None,
    }

    # ---- Safety gates ----
    if risk_level >= 2 and not rollback_sql:
        result["error"] = "L2及以上风险操作必须提供回滚脚本"
        _audit_execution(session_id, user_id, instance_name, dialect, sql,
                         risk_level, "rejected", result, rollback_sql)
        return result

    if risk_level >= 1 and not approved:
        result["error"] = "写操作需要审批通过后才能执行"
        _audit_execution(session_id, user_id, instance_name, dialect, sql,
                         risk_level, "rejected", result, rollback_sql)
        return result

    try:
        from .db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()

        # L0 → readonly engine; L1+ → admin engine
        if risk_level == 0:
            engine = mgr.get_readonly_engine(instance_name)
        else:
            engine = mgr.get_admin_engine(instance_name)

        start = time.time()

        if risk_level >= 1:
            with engine.connect() as conn:
                # Set statement timeout
                _set_statement_timeout(conn, dialect, timeout)

                # L2+ UPDATE/DELETE: snapshot affected rows before execution
                if snapshot and risk_level >= 2:
                    snapshot_data = _snapshot_affected_rows(conn, sql, dialect)
                    if snapshot_data is not None:
                        result["snapshot_rows"] = snapshot_data

                # Explicit transaction for write operations
                # SQLAlchemy 2.x: use conn.begin() as context manager
                # If autobegin is active, commit/rollback the implicit txn first
                try:
                    trans = conn.begin()
                except Exception:
                    # Already in a transaction (autobegin) — use it directly
                    trans = None
                try:
                    rs = conn.execute(text(sql))
                    if rs.returns_rows:
                        rows = rs.fetchall()
                        columns = list(rs.keys()) if hasattr(rs, "keys") else []
                        result["data"] = {
                            "columns": columns,
                            "rows": [_row_to_list(r) for r in rows[:1000]],
                            "total_rows": len(rows),
                        }
                        if len(rows) > 1000:
                            result["data"]["truncated"] = True
                    else:
                        result["rows_affected"] = rs.rowcount
                    if trans is not None:
                        trans.commit()
                    else:
                        conn.commit()
                except Exception:
                    if trans is not None:
                        trans.rollback()
                    else:
                        conn.rollback()
                    raise
        else:
            conn = engine.connect()
            try:
                _set_statement_timeout(conn, dialect, timeout)
                rs = conn.execute(text(sql))
                if rs.returns_rows:
                    result["data"] = _build_result_preview(
                        rs,
                        conn,
                        task_id=task_id,
                        session_id=session_id,
                        user_id=user_id,
                    )
                    conn = None
                else:
                    result["rows_affected"] = rs.rowcount
            finally:
                if conn is not None:
                    conn.close()

        result["execution_time_ms"] = int((time.time() - start) * 1000)
        result["success"] = True

        # Audit: success
        _audit_execution(session_id, user_id, instance_name, dialect, sql,
                         risk_level, "approved", result, rollback_sql)

    except Exception as e:
        result["error"] = str(e)
        result["execution_time_ms"] = int((time.time() - start) * 1000) if 'start' in dir() else 0
        logger.error("SQL execution failed on %s: %s", instance_name, e)

        # Audit: failure
        _audit_execution(session_id, user_id, instance_name, dialect, sql,
                         risk_level, "error", result, rollback_sql, error_message=str(e))

    return result


def _set_statement_timeout(conn, dialect: str, timeout: int) -> None:
    """Set per-statement execution timeout on the connection."""
    from sqlalchemy import text
    timeout_ms = timeout * 1000
    try:
        if dialect in ("postgresql", "postgres"):
            conn.execute(text(f"SET statement_timeout = {timeout_ms}"))
        elif dialect == "mysql":
            conn.execute(text(f"SET max_execution_time = {timeout_ms}"))
        # Oracle/SQL Server: timeout set via connection args, not per-statement
    except Exception as e:
        logger.debug("Could not set statement timeout for %s: %s", dialect, e)


def _snapshot_affected_rows(conn, sql: str, dialect: str) -> Optional[Dict]:
    """For UPDATE/DELETE, snapshot rows that will be affected.

    Converts the DML to a SELECT with the same WHERE clause to capture
    the rows before modification. Returns None if not applicable.
    """
    sql_upper = sql.strip().upper()
    if not (sql_upper.startswith("UPDATE") or sql_upper.startswith("DELETE")):
        return None

    try:
        import sqlglot
        import sqlglot.expressions as exp
        from sqlalchemy import text

        sg_dialect = {"mysql": "mysql", "postgresql": "postgres",
                      "postgres": "postgres", "oracle": "oracle",
                      "sqlserver": "tsql"}.get(dialect.lower(), dialect.lower())

        parsed = sqlglot.parse(sql, dialect=sg_dialect)
        if not parsed or parsed[0] is None:
            return None

        stmt = parsed[0]
        tables = [t.name for t in stmt.find_all(exp.Table)]
        if not tables:
            return None

        table_name = tables[0]
        where_clauses = list(stmt.find_all(exp.Where))
        where_sql = where_clauses[0].sql(dialect=sg_dialect) if where_clauses else ""

        snapshot_sql = f"SELECT * FROM {table_name} {where_sql} LIMIT 100"
        rows = conn.execute(text(snapshot_sql)).fetchall()
        if not rows:
            return {"table": table_name, "count": 0, "rows": []}

        keys = rows[0]._fields if hasattr(rows[0], "_fields") else list(range(len(rows[0])))
        return {
            "table": table_name,
            "count": len(rows),
            "columns": list(keys) if isinstance(keys, (list, tuple)) else [str(k) for k in keys],
            "rows": [list(r) for r in rows[:100]],
            "truncated": len(rows) >= 100,
        }
    except Exception as e:
        logger.debug("Snapshot failed: %s", e)
        return None


def _audit_execution(
    session_id: str,
    user_id: str,
    instance_name: str,
    dialect: str,
    sql: str,
    risk_level: int,
    approval_status: str,
    result: Dict,
    rollback_sql: str,
    error_message: str = "",
) -> None:
    """Record this execution in the audit log."""
    try:
        from .audit_logger import log_audit_event
        from .sql_ast_validator import validate_sql, RISK_LABELS

        validation = validate_sql(sql, dialect)
        log_audit_event(
            session_id=session_id,
            user_id=user_id,
            instance_name=instance_name,
            dialect=dialect,
            operation_type=validation.get("operation_type", "UNKNOWN"),
            risk_level=risk_level,
            risk_label=RISK_LABELS.get(risk_level, f"L{risk_level}"),
            original_sql=sql,
            validation_result=json.dumps({"valid": validation["valid"]}, ensure_ascii=False),
            approval_status=approval_status,
            execution_result="success" if result.get("success") else "failed",
            execution_time_ms=result.get("execution_time_ms", 0),
            rollback_sql=rollback_sql,
            error_message=error_message or result.get("error", ""),
        )
    except Exception as e:
        logger.warning("Audit logging failed: %s", e)


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_db_execute(args: dict, task_id: str = "", **kwargs) -> str:
    sql = args.get("sql", "")
    instance = args.get("instance_name", "")
    dialect = args.get("dialect", "mysql")
    risk_level = args.get("risk_level", 0)
    approved = args.get("approved", False)
    rollback_sql = args.get("rollback_sql", "")

    if not sql.strip():
        return json.dumps({"error": "sql参数不能为空"})
    if not instance:
        return json.dumps({"error": "instance_name参数不能为空"})

    result = execute_sql(
        sql, instance, dialect,
        risk_level=risk_level,
        approved=approved,
        rollback_sql=rollback_sql,
        task_id=task_id,
    )
    return json.dumps(result, ensure_ascii=False, default=str)


DB_EXECUTE_SCHEMA = {
    "name": "db_execute",
    "description": (
        "执行经过校验和审批的SQL语句。L0只读操作直接执行，"
        "L1及以上需要approved=true，L2及以上需要提供rollback_sql。"
        "这是唯一的SQL执行入口。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sql": {"type": "string", "description": "要执行的SQL语句"},
            "instance_name": {"type": "string", "description": "数据库实例名称"},
            "dialect": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "sqlserver"],
                "description": "数据库方言",
            },
            "risk_level": {
                "type": "integer",
                "description": "风险等级(0-4)，由sql_validate工具确定",
                "enum": [0, 1, 2, 3, 4],
            },
            "approved": {
                "type": "boolean",
                "description": "是否已通过人工审批，L1+操作必须为true",
            },
            "rollback_sql": {
                "type": "string",
                "description": "回滚脚本，L2+操作必须提供",
            },
        },
        "required": ["sql", "instance_name", "dialect", "risk_level"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="db_execute",
        toolset="dba-safeguard",
        schema=DB_EXECUTE_SCHEMA["parameters"],
        handler=handle_db_execute,
        description=DB_EXECUTE_SCHEMA["description"],
        emoji="▶️",
    )
