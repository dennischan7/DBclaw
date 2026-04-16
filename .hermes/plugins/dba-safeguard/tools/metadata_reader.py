"""元数据读取工具 — 安全读取库表结构、字段属性、索引信息。

安全约束:
  - 仅使用只读连接
  - 仅读取系统表/information_schema
  - 禁止读取业务数据
  - 结果缓存1小时TTL
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Optional

logger = logging.getLogger("dba_safeguard.tools.metadata_reader")

# Simple in-memory cache with TTL
_cache: Dict[str, tuple] = {}  # key -> (data, timestamp)
CACHE_TTL = 3600  # 1 hour


def _cache_get(key: str) -> Optional[Any]:
    if key in _cache:
        data, ts = _cache[key]
        if time.time() - ts < CACHE_TTL:
            return data
        del _cache[key]
    return None


def _cache_set(key: str, data: Any) -> None:
    _cache[key] = (data, time.time())


def read_metadata(
    instance_name: str,
    dialect: str,
    database: str = "",
    table: str = "",
    info_type: str = "tables",
) -> Dict[str, Any]:
    """Read database metadata.

    info_type: "tables" | "columns" | "indexes" | "ddl"
    """
    cache_key = f"{instance_name}:{database}:{table}:{info_type}"
    cached = _cache_get(cache_key)
    if cached is not None:
        return cached

    result: Dict[str, Any] = {"data": "", "format": "markdown"}

    try:
        from .db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine(instance_name)

        with engine.connect() as conn:
            if info_type == "tables":
                result["data"] = _read_tables(conn, dialect, database)
            elif info_type == "columns":
                result["data"] = _read_columns(conn, dialect, database, table)
            elif info_type == "indexes":
                result["data"] = _read_indexes(conn, dialect, database, table)
            elif info_type == "ddl":
                result["data"] = _read_ddl(conn, dialect, database, table)
            else:
                result["data"] = f"不支持的info_type: {info_type}"

        _cache_set(cache_key, result)

    except Exception as e:
        result["data"] = f"元数据读取失败: {e}"
        logger.warning("Metadata read failed for %s: %s", instance_name, e)

    return result


def _read_tables(conn, dialect: str, database: str) -> str:
    from sqlalchemy import text
    if dialect in ("mysql",):
        rows = conn.execute(text(
            "SELECT TABLE_NAME, TABLE_ROWS, TABLE_COMMENT "
            "FROM information_schema.TABLES "
            f"WHERE TABLE_SCHEMA = :db"
        ), {"db": database}).fetchall()
        lines = ["| 表名 | 行数 | 注释 |", "|---|---|---|"]
        for r in rows:
            lines.append(f"| {r[0]} | {r[1]} | {r[2]} |")
        return "\n".join(lines)
    elif dialect in ("postgresql", "postgres"):
        rows = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = :schema"
        ), {"schema": database or "public"}).fetchall()
        return "\n".join(f"- {r[0]}" for r in rows)
    return "该数据库方言暂不支持tables查询"


def _read_columns(conn, dialect: str, database: str, table: str) -> str:
    from sqlalchemy import text
    if dialect in ("mysql",):
        rows = conn.execute(text(
            "SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_COMMENT "
            "FROM information_schema.COLUMNS "
            "WHERE TABLE_SCHEMA = :db AND TABLE_NAME = :tbl "
            "ORDER BY ORDINAL_POSITION"
        ), {"db": database, "tbl": table}).fetchall()
        lines = ["| 列名 | 类型 | 可空 | 默认值 | 注释 |", "|---|---|---|---|---|"]
        for r in rows:
            lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} | {r[4]} |")
        return "\n".join(lines)
    elif dialect in ("postgresql", "postgres"):
        schema = database or "public"
        rows = conn.execute(text(
            "SELECT c.column_name, c.data_type, c.is_nullable, c.column_default, "
            "COALESCE(pgd.description, '') AS column_comment "
            "FROM information_schema.columns c "
            "LEFT JOIN pg_catalog.pg_statio_all_tables st "
            "  ON st.schemaname = c.table_schema AND st.relname = c.table_name "
            "LEFT JOIN pg_catalog.pg_description pgd "
            "  ON pgd.objoid = st.relid AND pgd.objsubid = c.ordinal_position "
            "WHERE c.table_schema = :schema AND c.table_name = :tbl "
            "ORDER BY c.ordinal_position"
        ), {"schema": schema, "tbl": table}).fetchall()
        lines = ["| 列名 | 类型 | 可空 | 默认值 | 注释 |", "|---|---|---|---|---|"]
        for r in rows:
            lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {r[3] or ''} | {r[4]} |")
        return "\n".join(lines)
    return "该数据库方言暂不支持columns查询"


def _read_indexes(conn, dialect: str, database: str, table: str) -> str:
    from sqlalchemy import text
    if dialect in ("mysql",):
        rows = conn.execute(text(
            "SHOW INDEX FROM " + f"`{database}`.`{table}`"
        )).fetchall()
        lines = ["| 索引名 | 列名 | 唯一 | 类型 |", "|---|---|---|---|"]
        for r in rows:
            lines.append(f"| {r[2]} | {r[4]} | {'否' if r[1] else '是'} | {r[10]} |")
        return "\n".join(lines)
    elif dialect in ("postgresql", "postgres"):
        schema = database or "public"
        rows = conn.execute(text(
            "SELECT indexname, indexdef "
            "FROM pg_indexes "
            "WHERE schemaname = :schema AND tablename = :tbl "
            "ORDER BY indexname"
        ), {"schema": schema, "tbl": table}).fetchall()
        lines = ["| 索引名 | 定义 |", "|---|---|"]
        for r in rows:
            lines.append(f"| {r[0]} | {r[1]} |")
        return "\n".join(lines)
    return "该数据库方言暂不支持indexes查询"


def _read_ddl(conn, dialect: str, database: str, table: str) -> str:
    from sqlalchemy import text
    if dialect in ("mysql",):
        rows = conn.execute(text(f"SHOW CREATE TABLE `{database}`.`{table}`")).fetchall()
        if rows:
            return rows[0][1]
    elif dialect in ("postgresql", "postgres"):
        schema = database or "public"
        # Reconstruct DDL from information_schema (PG has no SHOW CREATE TABLE)
        cols = conn.execute(text(
            "SELECT column_name, data_type, character_maximum_length, "
            "is_nullable, column_default "
            "FROM information_schema.columns "
            "WHERE table_schema = :schema AND table_name = :tbl "
            "ORDER BY ordinal_position"
        ), {"schema": schema, "tbl": table}).fetchall()
        if not cols:
            return f"表 {schema}.{table} 不存在或无列信息"
        ddl_lines = [f'CREATE TABLE "{schema}"."{table}" (']
        col_defs = []
        for c in cols:
            col_name, data_type, max_len, nullable, default = c
            type_str = data_type
            if max_len:
                type_str = f"{data_type}({max_len})"
            parts = [f'  "{col_name}" {type_str}']
            if nullable == "NO":
                parts.append("NOT NULL")
            if default:
                parts.append(f"DEFAULT {default}")
            col_defs.append(" ".join(parts))
        # Add primary key constraint
        pk = conn.execute(text(
            "SELECT kcu.column_name "
            "FROM information_schema.table_constraints tc "
            "JOIN information_schema.key_column_usage kcu "
            "  ON tc.constraint_name = kcu.constraint_name "
            "  AND tc.table_schema = kcu.table_schema "
            "WHERE tc.constraint_type = 'PRIMARY KEY' "
            "  AND tc.table_schema = :schema AND tc.table_name = :tbl "
            "ORDER BY kcu.ordinal_position"
        ), {"schema": schema, "tbl": table}).fetchall()
        if pk:
            pk_cols = ", ".join(f'"{r[0]}"' for r in pk)
            col_defs.append(f"  PRIMARY KEY ({pk_cols})")
        ddl_lines.append(",\n".join(col_defs))
        ddl_lines.append(");")
        return "\n".join(ddl_lines)
    return "该数据库方言暂不支持DDL查询"


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_metadata_read(args: dict, task_id: str = "", **kwargs) -> str:
    instance = args.get("instance_name", "")
    dialect = args.get("dialect", "mysql")
    database = args.get("database", "")
    table = args.get("table", "")
    info_type = args.get("info_type", "tables")

    if not instance:
        return json.dumps({"error": "instance_name参数不能为空"})

    result = read_metadata(instance, dialect, database, table, info_type)
    return json.dumps(result, ensure_ascii=False)


METADATA_SCHEMA = {
    "name": "metadata_read",
    "description": (
        "安全读取数据库元数据：库表列表、表结构字段、索引信息、DDL。"
        "仅使用只读连接，不会读取业务数据。结果缓存1小时。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "instance_name": {"type": "string", "description": "数据库实例名称"},
            "dialect": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "sqlserver"],
                "description": "数据库方言",
            },
            "database": {"type": "string", "description": "数据库/Schema名称"},
            "table": {"type": "string", "description": "表名（查columns/indexes/ddl时必填）"},
            "info_type": {
                "type": "string",
                "enum": ["tables", "columns", "indexes", "ddl"],
                "description": "要读取的元数据类型",
            },
        },
        "required": ["instance_name", "dialect", "info_type"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="metadata_read",
        toolset="dba-safeguard",
        schema=METADATA_SCHEMA["parameters"],
        handler=handle_metadata_read,
        description=METADATA_SCHEMA["description"],
        emoji="📋",
    )
