"""回滚脚本生成工具。

基于SQL语法树与元数据生成对应回滚脚本。
L2及以上风险操作必须生成回滚脚本才能进入审批环节。

安全约束:
  - 仅生成回滚脚本，不自动执行
  - 生成的回滚SQL也需经过语法校验
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List

logger = logging.getLogger("dba_safeguard.tools.rollback_generator")


def generate_rollback(
    sql: str,
    dialect: str = "mysql",
    table_metadata: str = "",
) -> Dict[str, Any]:
    """Generate a rollback script for the given SQL."""
    result = {
        "rollback_sql": "",
        "description": "",
        "warnings": [],
        "can_rollback": True,
    }

    sql_upper = sql.strip().upper()

    try:
        import sqlglot
        parsed = sqlglot.parse(sql, dialect=dialect.lower())
        if not parsed or parsed[0] is None:
            result["can_rollback"] = False
            result["warnings"].append("无法解析SQL，无法生成回滚脚本")
            return result

        stmt = parsed[0]
        result = _generate_for_statement(stmt, sql, dialect, table_metadata)

    except ImportError:
        result["can_rollback"] = False
        result["warnings"].append("sqlglot未安装，无法生成回滚脚本")
    except Exception as e:
        result["can_rollback"] = False
        result["warnings"].append(f"回滚脚本生成失败: {e}")

    return result


def _generate_for_statement(stmt, original_sql: str, dialect: str, metadata: str) -> Dict:
    """Generate rollback based on statement type."""
    import sqlglot.expressions as exp

    result = {
        "rollback_sql": "",
        "description": "",
        "warnings": [],
        "can_rollback": True,
    }

    if isinstance(stmt, exp.Drop):
        result["can_rollback"] = False
        result["warnings"].append(
            "DROP操作的回滚需要完整的对象重建DDL。"
            "建议在执行前备份表结构和数据。"
        )
        result["description"] = "DROP操作不可简单回滚，需从备份恢复"
        if metadata:
            result["rollback_sql"] = f"-- 从备份恢复:\n-- {metadata[:500]}"
        return result

    if isinstance(stmt, exp.Insert):
        # Rollback: DELETE the inserted rows
        tables = [t.name for t in stmt.find_all(exp.Table)]
        table_name = tables[0] if tables else "unknown_table"
        result["rollback_sql"] = (
            f"-- 回滚INSERT操作:\n"
            f"-- 需要根据实际插入的数据确定WHERE条件\n"
            f"DELETE FROM {table_name} WHERE <插入数据的唯一标识条件>;"
        )
        result["description"] = f"删除插入到 {table_name} 的数据"
        result["warnings"].append("需要确认具体的WHERE条件以精确回滚")
        return result

    if isinstance(stmt, exp.Update):
        tables = [t.name for t in stmt.find_all(exp.Table)]
        table_name = tables[0] if tables else "unknown_table"
        result["rollback_sql"] = (
            f"-- 回滚UPDATE操作:\n"
            f"-- 需要在执行前记录被更新行的原始值\n"
            f"-- UPDATE {table_name} SET <原始列值> WHERE <相同条件>;"
        )
        result["description"] = f"恢复 {table_name} 被更新行的原始值"
        result["warnings"].append("UPDATE回滚需要执行前快照，建议先SELECT备份原始数据")
        return result

    if isinstance(stmt, exp.Delete):
        tables = [t.name for t in stmt.find_all(exp.Table)]
        table_name = tables[0] if tables else "unknown_table"
        result["rollback_sql"] = (
            f"-- 回滚DELETE操作:\n"
            f"-- 需要在执行前备份将被删除的数据\n"
            f"-- INSERT INTO {table_name} SELECT * FROM <备份表> WHERE <条件>;"
        )
        result["description"] = f"恢复 {table_name} 被删除的数据"
        result["warnings"].append("DELETE回滚需要执行前备份数据，建议先SELECT INTO备份")
        return result

    if isinstance(stmt, exp.Alter):
        result["rollback_sql"] = f"-- 回滚ALTER操作:\n-- 需要人工分析具体变更并编写反向DDL"
        result["description"] = "ALTER操作需要手动编写反向DDL"
        return result

    # For TRUNCATE and other unsupported
    sql_upper = original_sql.strip().upper()
    if sql_upper.startswith("TRUNCATE"):
        result["can_rollback"] = False
        result["warnings"].append("TRUNCATE操作不可简单回滚，需从备份恢复全表数据")
        result["description"] = "TRUNCATE不可逆，需从备份恢复"
    else:
        result["can_rollback"] = False
        result["warnings"].append(f"不支持为该类型SQL生成回滚脚本")

    return result


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_rollback_generate(args: dict, task_id: str = "", **kwargs) -> str:
    sql = args.get("sql", "")
    dialect = args.get("dialect", "mysql")
    metadata = args.get("table_metadata", "")

    if not sql.strip():
        return json.dumps({"error": "sql参数不能为空"})

    result = generate_rollback(sql, dialect, metadata)
    return json.dumps(result, ensure_ascii=False, indent=2)


ROLLBACK_SCHEMA = {
    "name": "rollback_generate",
    "description": (
        "为DML/DDL操作自动生成对应的回滚脚本。"
        "L2及以上风险操作必须生成回滚脚本才能进入审批环节。"
        "仅生成脚本，不自动执行。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "sql": {"type": "string", "description": "原始SQL语句"},
            "dialect": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "sqlserver"],
                "description": "数据库方言",
            },
            "table_metadata": {
                "type": "string",
                "description": "表结构元数据（可选，用于生成更精确的回滚脚本）",
            },
        },
        "required": ["sql", "dialect"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="rollback_generate",
        toolset="dba-safeguard",
        schema=ROLLBACK_SCHEMA["parameters"],
        handler=handle_rollback_generate,
        description=ROLLBACK_SCHEMA["description"],
        emoji="⏪",
    )
