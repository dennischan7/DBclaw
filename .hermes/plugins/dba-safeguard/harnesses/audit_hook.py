"""审计钩子 — post_tool_call 钩子，自动记录所有DBA工具调用的审计日志。

在每个DBA工具执行完成后自动写入审计日志，无需工具自身关心审计逻辑。
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("dba_safeguard.harnesses.audit_hook")

# DBA tool names that should be audited
AUDITABLE_TOOLS = {
    "db_connect", "db_disconnect", "db_execute",
    "sql_validate", "explain_analyze", "metadata_read",
    "rollback_generate", "audit_query", "library_search",
}


def post_tool_call_hook(
    tool_name: str = "",
    args: Optional[Dict[str, Any]] = None,
    result: Any = None,
    task_id: str = "",
    session_id: str = "",
    tool_call_id: str = "",
    **kwargs,
) -> None:
    """Hermes post_tool_call hook for audit logging.

    Automatically records every DBA tool call to the audit database.

    Hermes passes: tool_name, args, result, task_id, session_id, tool_call_id.
    """
    if tool_name not in AUDITABLE_TOOLS:
        return

    tool_args = args or {}
    tool_result = result

    try:
        from ..tools.audit_logger import log_audit_event

        # Parse tool result
        result_str = str(tool_result) if tool_result else ""
        error_message = ""
        execution_time = 0

        try:
            result_data = json.loads(result_str) if isinstance(tool_result, str) else {}
            error_message = result_data.get("error") or ""
            execution_time = result_data.get("execution_time_ms") or 0
        except (json.JSONDecodeError, AttributeError):
            pass

        # Determine operation and risk from tool args
        sql = tool_args.get("sql", "")
        instance = tool_args.get("instance_name", "")
        dialect = tool_args.get("dialect", "")
        risk_level = tool_args.get("risk_level", 0)

        session_id = kwargs.get("session_id", "")

        log_audit_event(
            session_id=session_id,
            instance_name=instance,
            dialect=dialect,
            operation_type=tool_name,
            risk_level=risk_level if tool_name == "db_execute" else 0,
            risk_label=tool_args.get("risk_label", ""),
            original_sql=sql[:2000] if sql else "",
            validation_result="",
            approval_status="approved" if tool_args.get("approved") else "N/A",
            execution_result=result_str[:2000],
            execution_time_ms=execution_time,
            rollback_sql=tool_args.get("rollback_sql", "")[:2000],
            error_message=error_message[:500],
        )

        logger.debug("Audit logged: %s on %s", tool_name, instance or "N/A")

    except Exception as e:
        # Audit logging should never block tool execution
        logger.warning("Audit logging failed for %s: %s", tool_name, e)
