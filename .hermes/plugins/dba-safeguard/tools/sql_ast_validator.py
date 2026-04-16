"""AST语法解析工具 — 基于sqlglot的离线SQL校验。

核心能力:
  - SQL语法正确性校验
  - 多数据库方言适配（Oracle/MySQL/PostgreSQL/Hive/SQL Server）
  - 操作类型识别与L0-L4风险等级映射
  - 语法树解析与结构化输出

安全约束:
  - 仅做语法层面校验，不执行任何SQL
  - 不修改原始SQL，仅做解析
  - 校验失败后AI可自动重写，最多3轮
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("dba_safeguard.tools.sql_ast_validator")

# Dialect mapping: our config names → sqlglot dialect names
DIALECT_MAP = {
    "mysql": "mysql",
    "postgresql": "postgres",
    "postgres": "postgres",
    "oracle": "oracle",
    "sqlserver": "tsql",
    "hive": "hive",
}

# Risk level classification based on SQL operation type
RISK_CLASSIFICATION = {
    # L0 — Read-only, no data modification
    "SELECT": 0, "SHOW": 0, "DESCRIBE": 0, "DESC": 0, "EXPLAIN": 0,
    "USE": 0, "SET": 0,
    # L1 — Low-risk single row DML
    # (actual L1 vs L2 determined by WHERE clause analysis)
    "INSERT": 1,
    # L2 — Medium-risk batch DML / structure extension
    "UPDATE": 2, "DELETE": 2, "MERGE": 2,
    "CREATE INDEX": 2, "CREATE UNIQUE INDEX": 2,
    "ALTER TABLE ADD": 2,
    # L3 — High-risk structure destruction
    "ALTER TABLE DROP": 3, "ALTER TABLE MODIFY": 3, "ALTER TABLE ALTER": 3,
    "ALTER TABLE RENAME": 3, "DROP INDEX": 3, "TRUNCATE": 3, "TRUNCATE TABLE": 3,
    # L4 — Catastrophic operations
    "DROP TABLE": 4, "DROP DATABASE": 4, "DROP SCHEMA": 4,
    "DROP VIEW": 4, "DROP PROCEDURE": 4, "DROP FUNCTION": 4,
}

RISK_LABELS = {
    0: "L0_READONLY",
    1: "L1_LOW_DML",
    2: "L2_MEDIUM_BATCH",
    3: "L3_HIGH_DESTRUCTIVE",
    4: "L4_CATASTROPHIC",
}


def validate_sql(
    sql: str,
    dialect: str = "mysql",
    *,
    check_no_where: bool = True,
) -> Dict[str, Any]:
    """Validate SQL using sqlglot AST parser.

    Returns:
        {
            "valid": bool,
            "errors": [{"message": str, "line": int}],
            "warnings": [str],
            "risk_level": int (0-4),
            "risk_label": str,
            "operation_type": str,
            "tables": [str],
            "suggestions": [str],
        }
    """
    result = {
        "valid": True,
        "errors": [],
        "warnings": [],
        "risk_level": 0,
        "risk_label": "L0_READONLY",
        "operation_type": "UNKNOWN",
        "tables": [],
        "suggestions": [],
    }

    sg_dialect = DIALECT_MAP.get(dialect.lower(), dialect.lower())

    try:
        import sqlglot
        from sqlglot import errors as sg_errors

        # Parse the SQL
        try:
            parsed = sqlglot.parse(sql, dialect=sg_dialect)
        except sg_errors.ParseError as e:
            result["valid"] = False
            result["errors"].append({"message": str(e), "line": 0})
            result["suggestions"].append(f"SQL语法错误，请检查 {sg_dialect} 方言语法")
            return result

        if not parsed or parsed[0] is None:
            result["valid"] = False
            result["errors"].append({"message": "无法解析SQL语句", "line": 0})
            return result

        stmt = parsed[0]

        # Identify operation type
        operation = _identify_operation(stmt)
        result["operation_type"] = operation

        # Extract table names
        tables = _extract_tables(stmt)
        result["tables"] = tables

        # Classify risk level
        risk = _classify_risk(stmt, operation, sql)
        result["risk_level"] = risk
        result["risk_label"] = RISK_LABELS.get(risk, f"L{risk}_UNKNOWN")

        # Warn on dangerous patterns
        if check_no_where:
            warnings = _check_dangerous_patterns(stmt, operation, sql)
            result["warnings"] = warnings
            # Escalate risk if DELETE/UPDATE without WHERE
            if operation in ("DELETE", "UPDATE") and any("无WHERE" in w for w in warnings):
                result["risk_level"] = 4
                result["risk_label"] = "L4_CATASTROPHIC"
                result["suggestions"].append("DELETE/UPDATE语句缺少WHERE条件，极其危险！请添加WHERE条件限制影响范围。")

        # Try transpile to validate dialect compatibility
        try:
            sqlglot.transpile(sql, read=sg_dialect, write=sg_dialect)
        except Exception as e:
            result["warnings"].append(f"方言兼容性警告: {e}")

    except ImportError:
        result["valid"] = False
        result["errors"].append({"message": "sqlglot未安装，无法进行SQL校验", "line": 0})

    return result


def _identify_operation(stmt) -> str:
    """Identify the SQL operation type from AST."""
    import sqlglot.expressions as exp

    type_map = {
        exp.Select: "SELECT",
        exp.Insert: "INSERT",
        exp.Update: "UPDATE",
        exp.Delete: "DELETE",
        exp.Create: "CREATE",
        exp.Drop: "DROP",
        exp.Alter: "ALTER",
    }
    for expr_type, name in type_map.items():
        if isinstance(stmt, expr_type):
            if name == "DROP":
                kind = getattr(stmt, "kind", "")
                if kind:
                    return f"DROP {kind.upper()}"
            if name == "CREATE":
                kind = getattr(stmt, "kind", "")
                if kind:
                    return f"CREATE {kind.upper()}"
            if name == "ALTER":
                kind = getattr(stmt, "kind", "")
                prefix = f"ALTER {kind.upper()}" if kind else "ALTER"
                # Determine sub-action: ADD, DROP, MODIFY, RENAME, ALTER
                actions = stmt.args.get("actions", [])
                for action in (actions if isinstance(actions, list) else [actions]):
                    if action is None:
                        continue
                    action_sql = action.sql().upper().strip()
                    for sub_op in ("DROP", "RENAME", "MODIFY", "ALTER", "ADD"):
                        if action_sql.startswith(sub_op):
                            return f"{prefix} {sub_op}"
                return prefix
            return name

    # Fallback: check SQL text
    sql_upper = stmt.sql().upper().strip()
    for keyword in ("TRUNCATE", "MERGE", "EXPLAIN", "DESCRIBE", "SHOW", "USE", "SET"):
        if sql_upper.startswith(keyword):
            return keyword
    return "UNKNOWN"


def _extract_tables(stmt) -> List[str]:
    """Extract table names from AST."""
    import sqlglot.expressions as exp

    tables = []
    for table in stmt.find_all(exp.Table):
        name = table.name
        if name:
            db = table.db
            tables.append(f"{db}.{name}" if db else name)
    return list(set(tables))


def _classify_risk(stmt, operation: str, sql: str) -> int:
    """Classify risk level based on operation and context."""
    # Check exact match first
    if operation in RISK_CLASSIFICATION:
        return RISK_CLASSIFICATION[operation]

    # Check prefix matches (e.g., "ALTER TABLE ADD" → L2)
    for pattern, level in sorted(RISK_CLASSIFICATION.items(), key=lambda x: -len(x[0])):
        if operation.startswith(pattern):
            return level

    # Default to L2 for unknown write operations
    sql_upper = sql.upper().strip()
    if any(kw in sql_upper for kw in ("INSERT", "UPDATE", "DELETE", "ALTER", "DROP", "TRUNCATE")):
        return 2
    return 0


def _check_dangerous_patterns(stmt, operation: str, sql: str) -> List[str]:
    """Check for dangerous SQL patterns."""
    import sqlglot.expressions as exp

    warnings = []

    # DELETE/UPDATE without WHERE
    if operation in ("DELETE", "UPDATE"):
        has_where = bool(list(stmt.find_all(exp.Where)))
        if not has_where:
            warnings.append(f"{operation}语句无WHERE条件 — 将影响全表数据！")

    # SELECT * (mild warning)
    if operation == "SELECT":
        sql_upper = sql.upper()
        if "SELECT *" in sql_upper or "SELECT  *" in sql_upper:
            warnings.append("使用了SELECT * — 建议明确指定需要的列")

    return warnings


# ---------------------------------------------------------------------------
# Tool Handler
# ---------------------------------------------------------------------------

def handle_sql_validate(args: dict, task_id: str = "", **kwargs) -> str:
    """Handle sql_validate tool call."""
    sql = args.get("sql", "")
    dialect = args.get("dialect", "mysql")

    if not sql.strip():
        return json.dumps({"error": "sql参数不能为空"})

    result = validate_sql(sql, dialect)
    return json.dumps(result, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Tool Registration
# ---------------------------------------------------------------------------

SQL_VALIDATE_SCHEMA = {
    "name": "sql_validate",
    "description": (
        "对SQL语句进行离线语法校验和风险分级。基于AST解析，识别语法错误、"
        "方言不兼容、危险模式（如DELETE无WHERE），并映射L0-L4风险等级。"
        "在执行任何SQL之前必须先调用此工具进行校验。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sql": {
                "type": "string",
                "description": "要校验的SQL语句",
            },
            "dialect": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "sqlserver", "hive"],
                "description": "目标数据库方言",
            },
        },
        "required": ["sql", "dialect"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="sql_validate",
        toolset="dba-safeguard",
        schema=SQL_VALIDATE_SCHEMA["parameters"],
        handler=handle_sql_validate,
        description=SQL_VALIDATE_SCHEMA["description"],
        emoji="🔍",
    )
