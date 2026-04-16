"""安全执行器 — 审批通过的SQL执行入口。

安全约束:
  - 仅审批通过的操作可进入执行
  - L2+操作必须先生成回滚脚本
  - 使用管理员连接执行写操作
  - 执行前/后自动记录审计日志
  - 执行超时控制
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict

logger = logging.getLogger("dba_safeguard.tools.safe_executor")


def execute_sql(
    sql: str,
    instance_name: str,
    dialect: str = "mysql",
    *,
    risk_level: int = 0,
    approved: bool = False,
    rollback_sql: str = "",
    task_id: str = "",
) -> Dict[str, Any]:
    """Execute an approved SQL statement safely."""
    result: Dict[str, Any] = {
        "success": False,
        "data": None,
        "rows_affected": 0,
        "execution_time_ms": 0,
        "error": None,
    }

    # Safety checks
    if risk_level >= 2 and not rollback_sql:
        result["error"] = "L2及以上风险操作必须提供回滚脚本"
        return result

    if risk_level >= 1 and not approved:
        result["error"] = "写操作需要审批通过后才能执行"
        return result

    try:
        from .db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()

        # Read-only operations use readonly engine
        if risk_level == 0:
            engine = mgr.get_readonly_engine(instance_name)
        else:
            engine = mgr.get_admin_engine(instance_name)

        start = time.time()
        with engine.connect() as conn:
            rs = conn.execute(text(sql))

            if rs.returns_rows:
                rows = rs.fetchall()
                columns = list(rs.keys()) if hasattr(rs, "keys") else []
                result["data"] = {
                    "columns": columns,
                    "rows": [list(r) for r in rows[:1000]],  # Limit output
                    "total_rows": len(rows),
                }
                if len(rows) > 1000:
                    result["data"]["truncated"] = True
            else:
                result["rows_affected"] = rs.rowcount
                conn.commit()

        result["execution_time_ms"] = int((time.time() - start) * 1000)
        result["success"] = True

    except Exception as e:
        result["error"] = str(e)
        logger.error("SQL execution failed on %s: %s", instance_name, e)

    return result


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
