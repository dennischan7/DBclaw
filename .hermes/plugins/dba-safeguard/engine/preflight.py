"""任务预检模块 — 执行前前置检查。

在SQL进入校验流水线之前完成:
  1. 数据库连接可用性检查
  2. 目标表是否存在
  3. 当前连接权限是否满足
  4. 元数据预读取

预检不通过 → 直接终止，不进入方案生成环节。
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.engine.preflight")


# ============================================================
# Public API
# ============================================================

def run_preflight(
    sql: str,
    instance_name: str,
    dialect: str = "postgresql",
    *,
    skip_connection: bool = False,
    skip_table_check: bool = False,
) -> Dict[str, Any]:
    """Run all preflight checks.

    Returns:
        {
          "passed": bool,
          "checks": [{"name": str, "passed": bool, "message": str, "data": Any}],
          "failures": [{"name": str, "message": str}],
          "metadata": {...}  # pre-fetched for downstream stages
        }
    """
    checks: List[Dict[str, Any]] = []
    failures: List[Dict[str, str]] = []
    metadata: Dict[str, Any] = {}

    # 1. Connection check
    if not skip_connection:
        conn_result = _check_connection(instance_name, dialect)
        checks.append(conn_result)
        if not conn_result["passed"]:
            failures.append({"name": conn_result["name"],
                            "message": conn_result["message"]})

    # 2. Table existence check
    if not skip_table_check and not failures:
        tables = _extract_tables(sql, dialect)
        if tables:
            table_result = _check_tables_exist(instance_name, dialect, tables)
            checks.append(table_result)
            if not table_result["passed"]:
                failures.append({"name": table_result["name"],
                                "message": table_result["message"]})
            else:
                metadata["tables"] = table_result.get("data", {}).get("found", [])

    # 3. Permission check (based on SQL operation type)
    if not failures:
        perm_result = _check_permissions(sql, dialect)
        checks.append(perm_result)
        if not perm_result["passed"]:
            failures.append({"name": perm_result["name"],
                            "message": perm_result["message"]})

    # 4. Pre-fetch metadata for downstream stages (non-blocking)
    if not failures:
        meta_result = _prefetch_metadata(instance_name, dialect, sql)
        checks.append(meta_result)
        if meta_result.get("data"):
            metadata.update(meta_result["data"])

    return {
        "passed": len(failures) == 0,
        "checks": checks,
        "failures": failures,
        "metadata": metadata,
    }


# ============================================================
# Individual Checks
# ============================================================

def _check_connection(instance_name: str, dialect: str) -> Dict[str, Any]:
    """Check database connectivity."""
    name = "connection_check"
    try:
        try:
            from ..tools.db_connector import get_connection_manager
        except ImportError:
            from tools.db_connector import get_connection_manager
        from sqlalchemy import text

        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine(instance_name)

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))

        return {
            "name": name,
            "passed": True,
            "message": f"连接到 {instance_name} 成功",
            "data": {"instance": instance_name, "dialect": dialect},
        }
    except Exception as e:
        return {
            "name": name,
            "passed": False,
            "message": f"连接失败: {instance_name} — {e}",
            "data": None,
        }


def _check_tables_exist(
    instance_name: str,
    dialect: str,
    tables: List[str],
) -> Dict[str, Any]:
    """Check if referenced tables exist in the database."""
    name = "table_existence_check"

    # Skip check for DDL CREATE since the table may not exist yet
    if not tables:
        return {"name": name, "passed": True, "message": "无表引用",
                "data": {"found": [], "missing": []}}

    try:
        try:
            from ..tools.db_connector import get_connection_manager
        except ImportError:
            from tools.db_connector import get_connection_manager
        from sqlalchemy import text, inspect

        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine(instance_name)

        with engine.connect() as conn:
            inspector = inspect(engine)
            existing = set(inspector.get_table_names())

        found = [t for t in tables if t.lower() in {e.lower() for e in existing}]
        missing = [t for t in tables if t.lower() not in {e.lower() for e in existing}]

        if missing:
            return {
                "name": name,
                "passed": False,
                "message": f"表不存在: {', '.join(missing)}",
                "data": {"found": found, "missing": missing},
            }

        return {
            "name": name,
            "passed": True,
            "message": f"所有引用表存在: {', '.join(found)}",
            "data": {"found": found, "missing": []},
        }
    except Exception as e:
        # Connection failure already caught — treat metadata failure as warning
        return {
            "name": name,
            "passed": True,  # Non-blocking
            "message": f"表检查跳过(连接异常): {e}",
            "data": {"found": [], "missing": []},
        }


def _check_permissions(sql: str, dialect: str) -> Dict[str, Any]:
    """Check if the operation type is compatible with available connections.

    Verifies that write operations have admin credentials configured.
    Read-only operations always pass.
    """
    name = "permission_check"
    sql_upper = sql.strip().upper()

    # Read-only operations
    read_ops = ("SELECT", "SHOW", "DESCRIBE", "DESC", "EXPLAIN", "SET", "USE")
    if any(sql_upper.startswith(op) for op in read_ops):
        return {
            "name": name,
            "passed": True,
            "message": "只读操作，权限足够",
            "data": {"operation": "readonly"},
        }

    # Write operations: check if admin credentials are configured
    import os
    admin_user = os.environ.get("DBA_PG_TEST_ADMIN_USER", "")
    if not admin_user:
        admin_user = os.environ.get("DBA_ADMIN_USER", "")

    if not admin_user:
        return {
            "name": name,
            "passed": False,
            "message": "写操作需要管理员连接，但未配置管理员凭证",
            "data": {"operation": "write"},
        }

    return {
        "name": name,
        "passed": True,
        "message": "管理员连接已配置",
        "data": {"operation": "write"},
    }


def _prefetch_metadata(
    instance_name: str,
    dialect: str,
    sql: str,
) -> Dict[str, Any]:
    """Pre-fetch metadata for tables referenced in SQL.

    Results are cached by metadata_reader (1h TTL) so downstream stages
    benefit from the pre-fetch without extra queries.
    """
    name = "metadata_prefetch"
    tables = _extract_tables(sql, dialect)

    if not tables:
        return {"name": name, "passed": True, "message": "无需预获取元数据",
                "data": {}}

    prefetched = {}
    try:
        try:
            from ..tools.metadata_reader import read_metadata
        except ImportError:
            from tools.metadata_reader import read_metadata

        for table in tables[:5]:  # Cap at 5 tables
            try:
                meta = read_metadata(
                    instance_name=instance_name,
                    dialect=dialect,
                    table=table,
                    info_type="columns",
                )
                prefetched[table] = meta
            except Exception:
                pass

        return {
            "name": name,
            "passed": True,
            "message": f"预获取了 {len(prefetched)} 张表的元数据",
            "data": {"table_metadata": prefetched},
        }
    except Exception as e:
        return {
            "name": name,
            "passed": True,  # Non-blocking
            "message": f"元数据预获取跳过: {e}",
            "data": {},
        }


# ============================================================
# SQL Table Extraction
# ============================================================

def _extract_tables(sql: str, dialect: str = "postgresql") -> List[str]:
    """Extract table names from SQL using sqlglot.

    Returns an empty list for CREATE TABLE (the table doesn't exist yet).
    """
    sql_upper = sql.strip().upper()

    # CREATE TABLE — table doesn't exist yet, skip check
    if sql_upper.startswith("CREATE"):
        return []

    try:
        import sqlglot
        import sqlglot.expressions as exp

        sg_dialect = {
            "mysql": "mysql", "postgresql": "postgres", "postgres": "postgres",
            "oracle": "oracle", "sqlserver": "tsql",
        }.get(dialect.lower(), dialect.lower())

        parsed = sqlglot.parse(sql, dialect=sg_dialect)
        if not parsed or not parsed[0]:
            return []

        tables = []
        for table in parsed[0].find_all(exp.Table):
            name = table.name
            if name and name.upper() not in ("DUAL", "SYSIBM.SYSDUMMY1"):
                tables.append(name)

        return list(dict.fromkeys(tables))  # dedupe, preserve order
    except Exception:
        # Fallback: regex extraction
        return _extract_tables_regex(sql)


def _extract_tables_regex(sql: str) -> List[str]:
    """Fallback regex-based table extraction."""
    patterns = [
        r'\bFROM\s+(\w+)',
        r'\bJOIN\s+(\w+)',
        r'\bINTO\s+(\w+)',
        r'\bUPDATE\s+(\w+)',
        r'\bTABLE\s+(\w+)',
    ]
    tables = []
    for pat in patterns:
        for m in re.finditer(pat, sql, re.IGNORECASE):
            name = m.group(1)
            if name.upper() not in ("SET", "INTO", "VALUES", "SELECT", "WHERE", "FROM"):
                tables.append(name)
    return list(dict.fromkeys(tables))
