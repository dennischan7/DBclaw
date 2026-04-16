"""回滚脚本生成工具。

基于SQL语法树与元数据生成对应回滚脚本。
L2及以上风险操作必须生成回滚脚本才能进入审批环节。

安全约束:
  - 仅生成回滚脚本，不自动执行
  - 生成的回滚SQL也需经过语法校验
  - ALTER回滚基于元数据精确生成反向DDL
"""

from __future__ import annotations

import json
import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.tools.rollback_generator")


def generate_rollback(
    sql: str,
    dialect: str = "mysql",
    table_metadata: str = "",
    instance_name: str = "",
) -> Dict[str, Any]:
    """Generate a rollback script for the given SQL.

    If instance_name is provided and the SQL is ALTER TABLE, the generator
    will read live metadata to produce a precise reverse DDL.
    """
    result = {
        "rollback_sql": "",
        "description": "",
        "warnings": [],
        "can_rollback": True,
    }

    try:
        import sqlglot

        sg_dialect = {"mysql": "mysql", "postgresql": "postgres",
                      "postgres": "postgres", "oracle": "oracle",
                      "sqlserver": "tsql"}.get(dialect.lower(), dialect.lower())

        parsed = sqlglot.parse(sql, dialect=sg_dialect)
        if not parsed or parsed[0] is None:
            result["can_rollback"] = False
            result["warnings"].append("无法解析SQL，无法生成回滚脚本")
            return result

        stmt = parsed[0]
        result = _generate_for_statement(stmt, sql, dialect, table_metadata, instance_name)

        # Validate the generated rollback SQL syntax
        if result["rollback_sql"] and not result["rollback_sql"].startswith("--"):
            _validate_rollback_sql(result, dialect, sg_dialect)

    except ImportError:
        result["can_rollback"] = False
        result["warnings"].append("sqlglot未安装，无法生成回滚脚本")
    except Exception as e:
        result["can_rollback"] = False
        result["warnings"].append(f"回滚脚本生成失败: {e}")

    return result


def _validate_rollback_sql(result: Dict, dialect: str, sg_dialect: str) -> None:
    """Validate the generated rollback SQL for syntax correctness."""
    import sqlglot
    from sqlglot import errors as sg_errors

    rollback = result["rollback_sql"]
    # Strip comment lines for validation
    clean_lines = [ln for ln in rollback.split("\n") if not ln.strip().startswith("--")]
    clean_sql = "\n".join(clean_lines).strip()
    if not clean_sql:
        return

    try:
        sqlglot.parse(clean_sql, dialect=sg_dialect)
    except sg_errors.ParseError as e:
        result["warnings"].append(f"回滚脚本语法校验警告: {e}")


def _generate_for_statement(
    stmt,
    original_sql: str,
    dialect: str,
    metadata: str,
    instance_name: str = "",
) -> Dict:
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
        # If we have metadata (DDL), include it as recovery reference
        if metadata:
            result["rollback_sql"] = f"-- 从备份恢复:\n{metadata}"
        elif instance_name:
            ddl = _fetch_table_ddl(stmt, dialect, instance_name)
            if ddl:
                result["rollback_sql"] = f"-- 重建DDL (执行前备份):\n{ddl}"
                result["can_rollback"] = True
                result["description"] = "DROP操作回滚: 使用执行前备份的DDL重建"
        return result

    if isinstance(stmt, exp.Insert):
        tables = [t.name for t in stmt.find_all(exp.Table)]
        table_name = tables[0] if tables else "unknown_table"

        # Try to extract specific column values for precise rollback
        values_sql = _extract_insert_values(stmt, table_name, dialect)
        if values_sql:
            result["rollback_sql"] = values_sql
        else:
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
            f"-- 执行前已自动快照受影响行，可从快照恢复原始值\n"
            f"-- UPDATE {table_name} SET <原始列值> WHERE <相同条件>;"
        )
        result["description"] = f"恢复 {table_name} 被更新行的原始值"
        result["warnings"].append("UPDATE回滚依赖执行前快照，safe_executor已自动记录")
        return result

    if isinstance(stmt, exp.Delete):
        tables = [t.name for t in stmt.find_all(exp.Table)]
        table_name = tables[0] if tables else "unknown_table"
        result["rollback_sql"] = (
            f"-- 回滚DELETE操作:\n"
            f"-- 执行前已自动快照受影响行，可从快照恢复\n"
            f"-- INSERT INTO {table_name} SELECT * FROM <快照数据>;"
        )
        result["description"] = f"恢复 {table_name} 被删除的数据"
        result["warnings"].append("DELETE回滚依赖执行前快照，safe_executor已自动记录")
        return result

    if isinstance(stmt, exp.Alter):
        alter_rollback = _generate_alter_rollback(stmt, original_sql, dialect, instance_name)
        if alter_rollback:
            return alter_rollback
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


def _extract_insert_values(stmt, table_name: str, dialect: str) -> Optional[str]:
    """Try to extract column/value pairs from INSERT for a precise DELETE rollback."""
    import sqlglot.expressions as exp

    # Get columns from INSERT schema (they are Identifier nodes, not Column)
    schema = stmt.find(exp.Schema)
    if not schema:
        return None

    columns = [e.name for e in schema.expressions if hasattr(e, "name")]
    if not columns:
        return None

    # Get first row of values
    values_list = list(stmt.find_all(exp.Tuple))
    if not values_list:
        return None

    first_values = values_list[0]
    literals = [lit.sql() for lit in first_values.expressions]

    if len(columns) != len(literals):
        return None

    conditions = " AND ".join(f"{col} = {val}" for col, val in zip(columns, literals))
    return f"DELETE FROM {table_name} WHERE {conditions};"


def _generate_alter_rollback(
    stmt,
    original_sql: str,
    dialect: str,
    instance_name: str,
) -> Optional[Dict]:
    """Generate a precise reverse DDL for ALTER TABLE operations."""
    import sqlglot.expressions as exp

    tables = [t.name for t in stmt.find_all(exp.Table)]
    table_name = tables[0] if tables else None
    if not table_name:
        return None

    actions = stmt.args.get("actions", [])
    if not actions:
        return None

    actions_list = actions if isinstance(actions, list) else [actions]

    result = {
        "rollback_sql": "",
        "description": "",
        "warnings": [],
        "can_rollback": True,
    }

    for action in actions_list:
        if action is None:
            continue

        if isinstance(action, exp.ColumnDef):
            # ADD COLUMN → sqlglot represents as ColumnDef (no "ADD" prefix in sql)
            col_name = action.this.name if action.this else None
            if col_name:
                result["rollback_sql"] = f"ALTER TABLE {table_name} DROP COLUMN {col_name};"
                result["description"] = f"删除新增的列 {col_name}"
            else:
                result["rollback_sql"] = f"-- ALTER TABLE {table_name} DROP COLUMN <新增的列名>;"
                result["warnings"].append("无法自动提取列名，需手动确认")

        elif isinstance(action, exp.Drop):
            # DROP COLUMN → reverse is ADD COLUMN (need metadata for column definition)
            col_name = _extract_column_name_from_action(action, "DROP")
            col_def = _fetch_column_definition(table_name, col_name, dialect, instance_name) if col_name and instance_name else None
            if col_def:
                result["rollback_sql"] = f"ALTER TABLE {table_name} ADD COLUMN {col_def};"
                result["description"] = f"重新添加被删除的列 {col_name}"
            else:
                result["rollback_sql"] = f"-- ALTER TABLE {table_name} ADD COLUMN {col_name or '<列名>'} <原始列定义>;"
                result["warnings"].append("DROP COLUMN回滚需要原始列定义，建议在执行前获取元数据")
                if not col_def and instance_name:
                    result["warnings"].append("无法从数据库获取列定义，列可能不存在或连接失败")

        elif isinstance(action, exp.RenameColumn):
            # RENAME COLUMN old TO new → reverse swap
            old_col = action.this.name if action.this else None
            new_col = action.expression.name if action.expression else None
            if old_col and new_col:
                result["rollback_sql"] = f"ALTER TABLE {table_name} RENAME COLUMN {new_col} TO {old_col};"
                result["description"] = f"将列 {new_col} 重命名回 {old_col}"
            else:
                result["rollback_sql"] = f"-- 反向RENAME需要交换新旧名称"
                result["warnings"].append("请手动确认RENAME的新旧名称并交换")

        elif isinstance(action, (exp.AlterColumn,)):
            # MODIFY / ALTER COLUMN
            col_name = action.this.name if action.this else None
            col_def = _fetch_column_definition(table_name, col_name, dialect, instance_name) if col_name and instance_name else None
            if col_def:
                if dialect in ("postgresql", "postgres"):
                    result["rollback_sql"] = f"-- 恢复列定义:\n-- ALTER TABLE {table_name} ALTER COLUMN {col_def};"
                else:
                    result["rollback_sql"] = f"ALTER TABLE {table_name} MODIFY COLUMN {col_def};"
                result["description"] = f"恢复列 {col_name} 的原始定义"
            else:
                result["rollback_sql"] = f"-- ALTER TABLE {table_name} MODIFY COLUMN {col_name or '<列名>'} <原始定义>;"
                result["warnings"].append("需要原始列定义来生成精确回滚")

        else:
            # Fallback: try string-based detection for other action types
            action_sql = action.sql().upper().strip()
            if action_sql.startswith("ADD"):
                col_name = _extract_column_name_from_action(action, "ADD")
                if col_name:
                    result["rollback_sql"] = f"ALTER TABLE {table_name} DROP COLUMN {col_name};"
                    result["description"] = f"删除新增的列 {col_name}"
                else:
                    return None
            else:
                return None  # Unsupported ALTER action

    return result if result["rollback_sql"] else None


def _extract_column_name_from_action(action, prefix: str) -> Optional[str]:
    """Extract the column name from an ALTER TABLE action."""
    import sqlglot.expressions as exp
    # Try to find Column expression
    columns = list(action.find_all(exp.Column))
    if columns:
        return columns[0].name

    # Fallback: parse from SQL text
    action_sql = action.sql().strip()
    parts = action_sql.split()
    # "DROP COLUMN col_name" or "ADD col_name ..."
    for i, p in enumerate(parts):
        if p.upper() == "COLUMN" and i + 1 < len(parts):
            return parts[i + 1].strip('`"[]')
        if p.upper() == prefix and i + 1 < len(parts):
            next_part = parts[i + 1]
            if next_part.upper() != "COLUMN" and not next_part.startswith("("):
                return next_part.strip('`"[]')
    return None


def _fetch_column_definition(
    table_name: str,
    col_name: Optional[str],
    dialect: str,
    instance_name: str,
) -> Optional[str]:
    """Fetch the current column definition from the live database metadata."""
    if not col_name or not instance_name:
        return None
    try:
        from .db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine(instance_name)

        with engine.connect() as conn:
            if dialect in ("postgresql", "postgres"):
                row = conn.execute(text(
                    "SELECT column_name, data_type, character_maximum_length, "
                    "is_nullable, column_default "
                    "FROM information_schema.columns "
                    "WHERE table_name = :tbl AND column_name = :col"
                ), {"tbl": table_name, "col": col_name}).fetchone()
                if row:
                    col_n, dtype, max_len, nullable, default = row
                    type_str = f"{dtype}({max_len})" if max_len else dtype
                    parts = [f'"{col_n}" {type_str}']
                    if nullable == "NO":
                        parts.append("NOT NULL")
                    if default:
                        parts.append(f"DEFAULT {default}")
                    return " ".join(parts)
            elif dialect == "mysql":
                row = conn.execute(text(
                    "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT "
                    "FROM information_schema.COLUMNS "
                    "WHERE TABLE_NAME = :tbl AND COLUMN_NAME = :col"
                ), {"tbl": table_name, "col": col_name}).fetchone()
                if row:
                    col_n, col_type, nullable, default = row
                    parts = [f"`{col_n}` {col_type}"]
                    if nullable == "NO":
                        parts.append("NOT NULL")
                    if default:
                        parts.append(f"DEFAULT '{default}'")
                    return " ".join(parts)
    except Exception as e:
        logger.debug("Failed to fetch column definition: %s", e)
    return None


def _fetch_table_ddl(stmt, dialect: str, instance_name: str) -> Optional[str]:
    """Fetch the full table DDL for DROP rollback."""
    import sqlglot.expressions as exp
    tables = [t.name for t in stmt.find_all(exp.Table)]
    if not tables:
        return None
    try:
        from .metadata_reader import read_metadata
        result = read_metadata(instance_name, dialect, database="public", table=tables[0], info_type="ddl")
        return result.get("data") if "CREATE TABLE" in result.get("data", "") else None
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_rollback_generate(args: dict, task_id: str = "", **kwargs) -> str:
    sql = args.get("sql", "")
    dialect = args.get("dialect", "mysql")
    metadata = args.get("table_metadata", "")
    instance_name = args.get("instance_name", "")

    if not sql.strip():
        return json.dumps({"error": "sql参数不能为空"})

    result = generate_rollback(sql, dialect, metadata, instance_name)
    return json.dumps(result, ensure_ascii=False, indent=2)


ROLLBACK_SCHEMA = {
    "name": "rollback_generate",
    "description": (
        "为DML/DDL操作自动生成对应的回滚脚本。"
        "L2及以上风险操作必须生成回滚脚本才能进入审批环节。"
        "仅生成脚本，不自动执行。若提供instance_name，ALTER操作可基于元数据生成精确反向DDL。"
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
            "instance_name": {
                "type": "string",
                "description": "数据库实例名称（可选，用于获取元数据生成精确回滚）",
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
