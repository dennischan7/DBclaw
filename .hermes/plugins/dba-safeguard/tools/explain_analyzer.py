"""执行计划校验工具 — 拉取EXPLAIN执行计划识别性能风险。

安全约束:
  - 仅使用只读连接执行 EXPLAIN
  - 绝对不修改任何数据
  - 仅做性能风险识别，不做语法校验
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict

logger = logging.getLogger("dba_safeguard.tools.explain_analyzer")

# Default thresholds
DEFAULT_ROW_THRESHOLD = 1000


def analyze_explain(
    sql: str,
    instance_name: str,
    dialect: str = "mysql",
    row_threshold: int = DEFAULT_ROW_THRESHOLD,
) -> Dict[str, Any]:
    """Execute EXPLAIN and analyze the execution plan.

    Returns:
        {
            "plan": str,           # Raw EXPLAIN output
            "risks": [str],        # Identified performance risks
            "suggestions": [str],  # Optimization suggestions
            "should_block": bool,  # Whether to block execution
            "estimated_rows": int, # Estimated rows affected
        }
    """
    result = {
        "plan": "",
        "risks": [],
        "suggestions": [],
        "should_block": False,
        "estimated_rows": 0,
    }

    try:
        from .db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine(instance_name)

        # Build EXPLAIN statement based on dialect
        explain_sql = _build_explain_sql(sql, dialect)

        with engine.connect() as conn:
            rows = conn.execute(text(explain_sql)).fetchall()
            result["plan"] = _format_plan(rows, dialect)

            # Analyze the plan for risks
            risks, suggestions, total_rows = _analyze_plan_rows(rows, dialect, row_threshold)
            result["risks"] = risks
            result["suggestions"] = suggestions
            result["estimated_rows"] = total_rows
            result["should_block"] = len(risks) > 0

    except Exception as e:
        result["risks"].append(f"执行计划获取失败: {e}")
        logger.warning("EXPLAIN failed for instance %s: %s", instance_name, e)

    return result


def _build_explain_sql(sql: str, dialect: str) -> str:
    """Build EXPLAIN statement for the target dialect."""
    dialect = dialect.lower()
    if dialect == "mysql":
        return f"EXPLAIN {sql}"
    elif dialect in ("postgresql", "postgres"):
        return f"EXPLAIN (ANALYZE false, COSTS true, FORMAT TEXT) {sql}"
    elif dialect == "oracle":
        return f"EXPLAIN PLAN FOR {sql}"
    elif dialect == "sqlserver":
        # SQL Server uses SET SHOWPLAN_TEXT ON
        return f"SET SHOWPLAN_TEXT ON; {sql}; SET SHOWPLAN_TEXT OFF"
    return f"EXPLAIN {sql}"


def _format_plan(rows, dialect: str) -> str:
    """Format EXPLAIN output into readable text."""
    lines = []
    for row in rows:
        lines.append(" | ".join(str(col) for col in row))
    return "\n".join(lines)


def _analyze_plan_rows(rows, dialect: str, threshold: int):
    """Analyze EXPLAIN rows for performance risks."""
    risks = []
    suggestions = []
    total_rows = 0

    for row in rows:
        row_dict = dict(row._mapping) if hasattr(row, "_mapping") else {}
        row_str = str(row).upper()

        # Check for full table scan
        if "ALL" in row_str or "FULL TABLE SCAN" in row_str or "SEQ SCAN" in row_str:
            table = row_dict.get("table", "unknown")
            risks.append(f"全表扫描检测: 表 {table}")
            suggestions.append(f"建议为表 {table} 添加合适的索引")

        # Check row count estimate
        estimated = row_dict.get("rows", 0) or row_dict.get("Rows", 0)
        if isinstance(estimated, (int, float)):
            total_rows += int(estimated)

        # Check for no index usage
        if "NO INDEX" in row_str or "USING FILESORT" in row_str:
            suggestions.append("检测到未使用索引或使用文件排序,建议优化查询或添加索引")

    if total_rows > threshold:
        risks.append(f"预估扫描行数 {total_rows} 超过阈值 {threshold}")
        suggestions.append(f"预估扫描行数过大，建议添加WHERE条件或索引缩小范围")

    return risks, suggestions, total_rows


# ---------------------------------------------------------------------------
# Tool Handler
# ---------------------------------------------------------------------------

def handle_explain_analyze(args: dict, task_id: str = "", **kwargs) -> str:
    sql = args.get("sql", "")
    instance = args.get("instance_name", "")
    dialect = args.get("dialect", "mysql")
    threshold = args.get("row_threshold", DEFAULT_ROW_THRESHOLD)

    if not sql.strip():
        return json.dumps({"error": "sql参数不能为空"})
    if not instance:
        return json.dumps({"error": "instance_name参数不能为空"})

    result = analyze_explain(sql, instance, dialect, threshold)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

EXPLAIN_SCHEMA = {
    "name": "explain_analyze",
    "description": (
        "对SQL执行EXPLAIN获取执行计划，识别全表扫描、无索引JOIN、超阈值扫描行数等性能风险。"
        "仅使用只读连接，不会修改任何数据。在sql_validate语法校验通过后调用。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sql": {"type": "string", "description": "要分析执行计划的SQL语句"},
            "instance_name": {"type": "string", "description": "数据库实例名称"},
            "dialect": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "sqlserver"],
                "description": "数据库方言",
            },
            "row_threshold": {
                "type": "integer",
                "description": "扫描行数告警阈值(默认1000)",
                "default": 1000,
            },
        },
        "required": ["sql", "instance_name", "dialect"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="explain_analyze",
        toolset="dba-safeguard",
        schema=EXPLAIN_SCHEMA["parameters"],
        handler=handle_explain_analyze,
        description=EXPLAIN_SCHEMA["description"],
        emoji="📊",
    )
