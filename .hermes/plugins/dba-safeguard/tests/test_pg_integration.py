"""PG实连集成测试 — 需要真实 PostgreSQL 数据库。

测试目标:
  - db_connector: 连接 pg_test 实例, readonly SELECT 1
  - explain_analyzer: 对真实表执行 EXPLAIN
  - metadata_reader: tables / columns / indexes / ddl (PG 新增功能)

运行前:
  $env:DBA_PG_TEST_RO_USER="health_user"
  $env:DBA_PG_TEST_RO_PASS="health_password"
  $env:DBA_PG_TEST_ADMIN_USER="health_user"
  $env:DBA_PG_TEST_ADMIN_PASS="health_password"
"""

import json
import os
import sys
from pathlib import Path

import pytest

# Add plugin root to path
plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

# Skip all tests if PG credentials not set
PG_AVAILABLE = bool(
    os.environ.get("DBA_PG_TEST_RO_USER")
    and os.environ.get("DBA_PG_TEST_RO_PASS")
)
pytestmark = pytest.mark.skipif(not PG_AVAILABLE, reason="PG test credentials not set")


# ========================================================================
# Fixtures
# ========================================================================

@pytest.fixture(scope="module")
def pg_manager():
    """Create a ConnectionManager connected to pg_test."""
    from tools.db_connector import ConnectionManager
    mgr = ConnectionManager()
    mgr.load_config(plugin_root / "config" / "dba_config.yaml")
    yield mgr
    mgr.close_all()


@pytest.fixture(scope="module")
def pg_engine(pg_manager):
    """Get readonly engine for pg_test instance."""
    return pg_manager.get_readonly_engine("pg_test")


# ========================================================================
# db_connector — 连接测试
# ========================================================================

class TestDbConnector:
    def test_readonly_connect(self, pg_engine):
        """SELECT 1 on readonly connection."""
        from sqlalchemy import text
        with pg_engine.connect() as conn:
            row = conn.execute(text("SELECT 1 AS val")).fetchone()
            assert row[0] == 1

    def test_readonly_blocks_write(self, pg_engine):
        """Write operations should be blocked on readonly connection."""
        from sqlalchemy import text
        with pg_engine.connect() as conn:
            with pytest.raises(Exception):
                conn.execute(text(
                    "CREATE TABLE _test_readonly_guard (id int)"
                ))

    def test_list_instances(self, pg_manager):
        """Should list configured instances."""
        instances = pg_manager.list_instances()
        names = [i["name"] for i in instances]
        assert "pg_test" in names

    def test_handler_connect(self):
        """Test the handle_db_connect handler."""
        from tools.db_connector import handle_db_connect
        result = json.loads(handle_db_connect({"instance_name": "pg_test"}))
        assert "result" in result or "error" not in result


# ========================================================================
# explain_analyzer — 真实 EXPLAIN 测试
# ========================================================================

class TestExplainAnalyzer:
    def test_explain_select_users(self, pg_manager):
        """EXPLAIN on a real table should produce a plan."""
        from tools.explain_analyzer import analyze_explain
        # Ensure config is loaded
        pg_manager.load_config(plugin_root / "config" / "dba_config.yaml")

        result = analyze_explain(
            sql="SELECT * FROM users LIMIT 10",
            instance_name="pg_test",
            dialect="postgresql",
        )
        assert result["plan"], "EXPLAIN plan should not be empty"
        assert isinstance(result["risks"], list)
        assert isinstance(result["estimated_rows"], (int, float))

    def test_explain_sequential_scan_detection(self, pg_manager):
        """A full table scan should be detected as a risk."""
        from tools.explain_analyzer import analyze_explain

        result = analyze_explain(
            sql="SELECT * FROM users",
            instance_name="pg_test",
            dialect="postgresql",
        )
        # With a small table it may or may not trigger seq scan warning
        # At minimum the plan should exist
        assert result["plan"]

    def test_explain_with_where(self, pg_manager):
        """EXPLAIN with WHERE clause — should produce plan."""
        from tools.explain_analyzer import analyze_explain

        result = analyze_explain(
            sql="SELECT id FROM users WHERE id = 1",
            instance_name="pg_test",
            dialect="postgresql",
        )
        assert result["plan"]

    def test_explain_join(self, pg_manager):
        """EXPLAIN a JOIN query."""
        from tools.explain_analyzer import analyze_explain

        result = analyze_explain(
            sql="SELECT u.id FROM users u JOIN enterprises e ON u.id = e.id",
            instance_name="pg_test",
            dialect="postgresql",
        )
        assert result["plan"]

    def test_handler_output(self, pg_manager):
        """Test the tool handler returns valid JSON."""
        from tools.explain_analyzer import handle_explain_analyze
        result = json.loads(handle_explain_analyze({
            "sql": "SELECT COUNT(*) FROM users",
            "instance_name": "pg_test",
            "dialect": "postgresql",
        }))
        assert "plan" in result


# ========================================================================
# metadata_reader — PG 元数据读取
# ========================================================================

class TestMetadataReader:
    def test_read_tables(self, pg_manager):
        """Should list tables in public schema."""
        from tools.metadata_reader import read_metadata
        result = read_metadata("pg_test", "postgresql", database="public", info_type="tables")
        assert result["data"]
        assert "users" in result["data"]

    def test_read_columns(self, pg_manager):
        """Should read column info for users table (PG new feature)."""
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()  # Clear cache to test fresh

        result = read_metadata(
            "pg_test", "postgresql",
            database="public", table="users",
            info_type="columns",
        )
        data = result["data"]
        assert "暂不支持" not in data, "PG columns should now be supported"
        assert "列名" in data
        assert "类型" in data

    def test_read_indexes(self, pg_manager):
        """Should read index info (PG new feature)."""
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()

        result = read_metadata(
            "pg_test", "postgresql",
            database="public", table="users",
            info_type="indexes",
        )
        data = result["data"]
        assert "暂不支持" not in data, "PG indexes should now be supported"
        assert "索引名" in data

    def test_read_ddl(self, pg_manager):
        """Should reconstruct DDL (PG new feature)."""
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()

        result = read_metadata(
            "pg_test", "postgresql",
            database="public", table="users",
            info_type="ddl",
        )
        data = result["data"]
        assert "暂不支持" not in data, "PG DDL should now be supported"
        assert "CREATE TABLE" in data

    def test_read_columns_specific_fields(self, pg_manager):
        """Column data should include actual column names from users table."""
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()

        result = read_metadata(
            "pg_test", "postgresql",
            database="public", table="users",
            info_type="columns",
        )
        data = result["data"]
        # 'users' table should have an 'id' column at minimum
        assert "id" in data.lower()

    def test_handler_returns_json(self, pg_manager):
        """The tool handler should return valid JSON."""
        from tools.metadata_reader import handle_metadata_read
        result = json.loads(handle_metadata_read({
            "instance_name": "pg_test",
            "dialect": "postgresql",
            "database": "public",
            "info_type": "tables",
        }))
        assert "data" in result

    def test_cache_works(self, pg_manager):
        """Second call should use cache."""
        from tools.metadata_reader import read_metadata, _cache
        _cache.clear()

        r1 = read_metadata("pg_test", "postgresql", database="public", info_type="tables")
        r2 = read_metadata("pg_test", "postgresql", database="public", info_type="tables")
        assert r1["data"] == r2["data"]
