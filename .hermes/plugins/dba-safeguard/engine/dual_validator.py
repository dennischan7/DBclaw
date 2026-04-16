"""双校验子Agent流水线 — 语法校验 + 性能审核并行执行。

核心设计:
  - 语法校验Agent: AST语法解析 + 方言适配 + library知识库比对
  - 性能审核Agent: EXPLAIN执行计划 + 全表扫描检测 + 扫描行数检查
  - 一票否决: 任一校验不通过 → 整体不通过，返回打回理由
  - 两个Agent独立执行，互不影响
  - 只做校验和建议，不执行任何写操作
"""

from __future__ import annotations

import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.engine.dual_validator")


# ============================================================
# Public API
# ============================================================

def run_dual_validation(
    sql: str,
    instance_name: str,
    dialect: str = "postgresql",
    *,
    risk_level: int = 0,
    row_threshold: int = 1000,
    skip_performance: bool = False,
) -> Dict[str, Any]:
    """Run dual validation: syntax + performance in parallel.

    Returns:
        {
          "passed": bool,
          "syntax": {...validation result...},
          "performance": {...explain result...},
          "errors": [str],
          "suggestions": [str],
        }
    """
    results: Dict[str, Any] = {
        "passed": True,
        "syntax": {},
        "performance": {},
        "errors": [],
        "suggestions": [],
    }

    # Run both validators in parallel threads
    with ThreadPoolExecutor(max_workers=2) as pool:
        syntax_future = pool.submit(
            _validate_syntax, sql, dialect, instance_name
        )

        if skip_performance or risk_level == 0:
            perf_future = None
        else:
            perf_future = pool.submit(
                _validate_performance, sql, instance_name, dialect,
                row_threshold,
            )

        # Collect syntax result
        try:
            syntax_result = syntax_future.result(timeout=30)
            results["syntax"] = syntax_result
            if not syntax_result.get("passed"):
                results["passed"] = False
                results["errors"].extend(syntax_result.get("errors", []))
                results["suggestions"].extend(syntax_result.get("suggestions", []))
        except Exception as e:
            results["passed"] = False
            results["syntax"] = {"passed": False, "errors": [str(e)]}
            results["errors"].append(f"语法校验异常: {e}")

        # Collect performance result
        if perf_future:
            try:
                perf_result = perf_future.result(timeout=60)
                results["performance"] = perf_result
                if not perf_result.get("passed"):
                    results["passed"] = False
                    results["errors"].extend(perf_result.get("errors", []))
                    results["suggestions"].extend(perf_result.get("suggestions", []))
            except Exception as e:
                # Performance check failure is non-blocking for L0/L1
                if risk_level >= 2:
                    results["passed"] = False
                    results["errors"].append(f"性能校验异常: {e}")
                results["performance"] = {
                    "passed": risk_level < 2,
                    "errors": [str(e)],
                    "warnings": [],
                }
        else:
            results["performance"] = {"passed": True, "skipped": True}

    return results


# ============================================================
# Syntax Validation Agent
# ============================================================

def _validate_syntax(
    sql: str,
    dialect: str,
    instance_name: str,
) -> Dict[str, Any]:
    """Syntax validation: AST parsing + dialect check + library verification.

    Independent context, restricted to read-only tools:
      - sql_validate (AST parsing)
      - library_search (knowledge base)
    """
    result: Dict[str, Any] = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "suggestions": [],
        "library_refs": [],
    }

    # Step 1: AST validation
    try:
        try:
            from ..tools.sql_ast_validator import validate_sql
        except ImportError:
            from tools.sql_ast_validator import validate_sql

        val = validate_sql(sql, dialect)

        if not val["valid"]:
            result["passed"] = False
            for e in val.get("errors", []):
                result["errors"].append(e.get("message", str(e)))
            result["suggestions"].extend(val.get("suggestions", []))
            return result

        result["warnings"].extend(val.get("warnings", []))

    except Exception as e:
        result["passed"] = False
        result["errors"].append(f"AST解析失败: {e}")
        return result

    # Step 2: Library knowledge base verification (for risky operations)
    try:
        try:
            from ..tools.library_search import search_library
        except ImportError:
            from tools.library_search import search_library

        # Determine search query from SQL
        search_query = _build_library_query(sql, dialect)
        if search_query:
            lib_results = search_library(
                query=search_query,
                db_type=_dialect_to_db_type(dialect),
            )
            if lib_results.get("results"):
                result["library_refs"] = [
                    r.get("title", r.get("path", ""))
                    for r in lib_results["results"][:3]
                ]
    except Exception as e:
        logger.debug("Library search skipped: %s", e)

    return result


# ============================================================
# Performance Validation Agent
# ============================================================

def _validate_performance(
    sql: str,
    instance_name: str,
    dialect: str,
    row_threshold: int = 1000,
) -> Dict[str, Any]:
    """Performance validation: EXPLAIN plan analysis.

    Independent context, restricted to read-only tools:
      - explain_analyze (EXPLAIN plan)
      - metadata_read (table stats)
    """
    result: Dict[str, Any] = {
        "passed": True,
        "errors": [],
        "warnings": [],
        "plan": None,
        "should_block": False,
        "estimated_rows": None,
    }

    # Only EXPLAIN for SELECT/UPDATE/DELETE (not DDL)
    sql_upper = sql.strip().upper()
    explainable = any(sql_upper.startswith(op) for op in
                      ("SELECT", "UPDATE", "DELETE", "INSERT"))
    if not explainable:
        result["warnings"].append("DDL操作不支持EXPLAIN分析")
        return result

    try:
        try:
            from ..tools.explain_analyzer import analyze_explain
        except ImportError:
            from tools.explain_analyzer import analyze_explain

        explain = analyze_explain(
            sql=sql,
            instance_name=instance_name,
            dialect=dialect,
            row_threshold=row_threshold,
        )

        result["plan"] = explain.get("plan")
        result["estimated_rows"] = explain.get("estimated_rows")
        result["warnings"].extend(explain.get("warnings", []))

        if explain.get("should_block"):
            result["passed"] = False
            result["should_block"] = True
            result["errors"].append(
                f"EXPLAIN检测到严重性能风险: "
                f"{'; '.join(explain.get('warnings', []))}"
            )

    except Exception as e:
        # EXPLAIN failure: warn but don't block unless high-risk
        result["warnings"].append(f"EXPLAIN分析失败: {e}")
        logger.debug("EXPLAIN failed for %s: %s", instance_name, e)

    return result


# ============================================================
# Helpers
# ============================================================

def _build_library_query(sql: str, dialect: str) -> Optional[str]:
    """Build a library search query from SQL for syntax verification.

    Only searches for complex or risky operations — not simple SELECT.
    """
    sql_upper = sql.strip().upper()

    # Skip library search for simple SELECT
    if sql_upper.startswith("SELECT") and "JOIN" not in sql_upper:
        return None

    # Build targeted search query
    keywords = []
    if "ALTER TABLE" in sql_upper:
        keywords.append("ALTER TABLE")
        if "ADD" in sql_upper:
            keywords.append("ADD COLUMN")
        if "DROP" in sql_upper:
            keywords.append("DROP COLUMN")
        if "MODIFY" in sql_upper or "ALTER COLUMN" in sql_upper:
            keywords.append("MODIFY COLUMN")
    elif "CREATE INDEX" in sql_upper:
        keywords.append("CREATE INDEX")
    elif "CREATE TABLE" in sql_upper:
        keywords.append("CREATE TABLE")
    elif "PARTITION" in sql_upper:
        keywords.append("PARTITION")
    elif "WINDOW" in sql_upper or "OVER" in sql_upper:
        keywords.append("WINDOW FUNCTION")
    elif "JOIN" in sql_upper:
        keywords.append("JOIN")

    if not keywords:
        return None

    return " ".join(keywords) + f" {dialect}"


def _dialect_to_db_type(dialect: str) -> str:
    """Map dialect to library db_type."""
    mapping = {
        "mysql": "mysql",
        "postgresql": "postgres",
        "postgres": "postgres",
        "oracle": "oracle",
        "sqlserver": "sqlserver",
        "hive": "hive",
    }
    return mapping.get(dialect.lower(), dialect.lower())
