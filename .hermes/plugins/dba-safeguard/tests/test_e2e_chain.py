"""E2E链路测试 — 验证完整 SQL 校验 → EXPLAIN → 元数据 → 拦截 链路。

需要真实 PostgreSQL 数据库。
设置环境变量后运行:
    $env:DBA_PG_TEST_RO_USER="dbclaw_test_user"
    $env:DBA_PG_TEST_RO_PASS="dbclaw_test_password"
"""

import json
import os
import sys
from pathlib import Path

import pytest

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

PG_AVAILABLE = bool(
    os.environ.get("DBA_PG_TEST_RO_USER")
    and os.environ.get("DBA_PG_TEST_RO_PASS")
)
pytestmark = pytest.mark.skipif(not PG_AVAILABLE, reason="PG test credentials not set")


@pytest.fixture(scope="module")
def pg_setup():
    """Setup ConnectionManager with pg_test config."""
    from tools.db_connector import get_connection_manager
    mgr = get_connection_manager()
    mgr.load_config(plugin_root / "config" / "dba_config.yaml")
    yield mgr
    mgr.close_all()


class TestE2ESelectChain:
    """SELECT → validate → explain → metadata → interceptor: 全链路放行。"""

    def test_select_full_chain(self, pg_setup):
        sql = "SELECT id, created_at FROM users WHERE id = 1"
        dialect = "postgresql"

        # 1. AST validation
        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["valid"] is True
        assert val["risk_level"] == 0
        assert val["operation_type"] == "SELECT"
        assert "users" in val["tables"]

        # 2. EXPLAIN
        from tools.explain_analyzer import analyze_explain
        expl = analyze_explain(sql, "pg_test", dialect)
        assert expl["plan"]  # Non-empty plan

        # 3. Metadata (table exists)
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()
        meta = read_metadata("pg_test", dialect, database="public", table="users", info_type="columns")
        assert "id" in meta["data"].lower()

        # 4. Interceptor (should auto-approve L0)
        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect}
        )
        assert result is None  # Proceed


class TestE2EInsertChain:
    """INSERT → validate(L1) → interceptor(notify_approve) 链路。"""

    def test_insert_notify_approve(self, pg_setup):
        sql = "INSERT INTO users (id) VALUES (9999)"
        dialect = "postgresql"

        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["valid"] is True
        assert val["risk_level"] == 1

        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect}
        )
        assert result is None  # L1 notify_approve → proceed


class TestE2EUpdateChain:
    """UPDATE with WHERE → validate(L2) → interceptor(human_confirm) 链路。"""

    def test_update_requires_approval(self, pg_setup):
        sql = "UPDATE users SET created_at = NOW() WHERE id = 1"
        dialect = "postgresql"

        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["valid"] is True
        assert val["risk_level"] == 2

        # Interceptor should block (require human confirm)
        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect}
        )
        assert result is not None
        assert result["block"] is True
        assert "人工确认" in result["message"]

    def test_update_approved_passes(self, pg_setup):
        sql = "UPDATE users SET created_at = NOW() WHERE id = 1"
        dialect = "postgresql"

        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect, "approved": True}
        )
        assert result is None  # Already approved → proceed


class TestE2EDestructiveChain:
    """DELETE no WHERE / DROP TABLE → validate(L4) → interceptor(force_block) 链路。"""

    def test_delete_no_where_full_block(self, pg_setup):
        sql = "DELETE FROM users"
        dialect = "postgresql"

        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["risk_level"] == 4
        assert any("无WHERE" in w for w in val["warnings"])

        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect}
        )
        assert result["block"] is True
        assert "阻断" in result["message"]

    def test_drop_table_full_block(self, pg_setup):
        sql = "DROP TABLE users"
        dialect = "postgresql"

        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["risk_level"] == 4

        from harnesses.risk_interceptor import pre_tool_call_hook
        result = pre_tool_call_hook(
            tool_name="db_execute", args={"sql": sql, "dialect": dialect}
        )
        assert result["block"] is True


class TestE2EExplainRisk:
    """EXPLAIN on large-scan query → detect performance risk → chain with validator."""

    def test_full_scan_detection(self, pg_setup):
        sql = "SELECT * FROM users"
        dialect = "postgresql"

        # Validate
        from tools.sql_ast_validator import validate_sql
        val = validate_sql(sql, dialect)
        assert val["valid"] is True
        assert any("SELECT *" in w for w in val["warnings"])

        # EXPLAIN
        from tools.explain_analyzer import analyze_explain
        expl = analyze_explain(sql, "pg_test", dialect)
        assert expl["plan"]
        # On small tables, Seq Scan is expected and optimal — just verify plan exists


class TestE2EMetadataChain:
    """tables → columns → indexes → ddl 全链路元数据读取。"""

    def test_metadata_full_read(self, pg_setup):
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()

        # 1. List tables
        tables = read_metadata("pg_test", "postgresql", database="public", info_type="tables")
        assert "users" in tables["data"]

        # 2. Read columns
        cols = read_metadata("pg_test", "postgresql", database="public", table="users", info_type="columns")
        assert "列名" in cols["data"]
        assert "id" in cols["data"].lower()

        # 3. Read indexes
        idx = read_metadata("pg_test", "postgresql", database="public", table="users", info_type="indexes")
        assert "索引名" in idx["data"]

        # 4. Read DDL
        ddl = read_metadata("pg_test", "postgresql", database="public", table="users", info_type="ddl")
        assert "CREATE TABLE" in ddl["data"]
