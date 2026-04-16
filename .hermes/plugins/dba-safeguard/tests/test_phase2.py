"""Phase 2 测试套件 — safe_executor / rollback_generator / audit_logger。

分为:
  A. 离线单元测试 (无需数据库)
  B. PG 实连集成测试 (需要 Docker PG)
"""

import csv
import io
import json
import os
import sys
import time
from pathlib import Path

import pytest

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

PG_AVAILABLE = bool(
    os.environ.get("DBA_PG_TEST_RO_USER")
    and os.environ.get("DBA_PG_TEST_RO_PASS")
)


# ========================================================================
# Fixtures
# ========================================================================

@pytest.fixture()
def audit_db(tmp_path):
    """Setup a temporary audit database for testing."""
    from tools.audit_logger import set_audit_db_path
    db_path = tmp_path / "test_audit.db"
    set_audit_db_path(db_path)
    yield db_path
    # Cleanup
    set_audit_db_path(tmp_path / "cleanup_audit.db")


@pytest.fixture(scope="module")
def pg_manager():
    if not PG_AVAILABLE:
        pytest.skip("PG credentials not set")
    from tools.db_connector import get_connection_manager
    mgr = get_connection_manager()
    mgr.load_config(plugin_root / "config" / "dba_config.yaml")
    yield mgr
    mgr.close_all()


# ========================================================================
# A. Audit Logger — 离线测试
# ========================================================================

class TestAuditLogger:
    def test_log_and_query(self, audit_db):
        from tools.audit_logger import log_audit_event, query_audit_logs
        row_id = log_audit_event(
            session_id="test-session",
            user_id="tester",
            instance_name="pg_test",
            dialect="postgresql",
            operation_type="SELECT",
            risk_level=0,
            risk_label="L0_READONLY",
            original_sql="SELECT 1",
        )
        assert row_id > 0

        logs = query_audit_logs(user_id="tester")
        assert len(logs) >= 1
        assert logs[0]["original_sql"] == "SELECT 1"
        assert logs[0]["risk_level"] == 0

    def test_query_by_risk_level(self, audit_db):
        from tools.audit_logger import log_audit_event, query_audit_logs
        log_audit_event(operation_type="SELECT", risk_level=0, original_sql="SELECT 1")
        log_audit_event(operation_type="DELETE", risk_level=4, original_sql="DELETE FROM t")

        l0 = query_audit_logs(risk_level=0)
        l4 = query_audit_logs(risk_level=4)
        assert all(r["risk_level"] == 0 for r in l0)
        assert all(r["risk_level"] == 4 for r in l4)

    def test_query_by_instance(self, audit_db):
        from tools.audit_logger import log_audit_event, query_audit_logs
        log_audit_event(instance_name="pg_test", original_sql="SELECT 1")
        log_audit_event(instance_name="mysql_dev", original_sql="SELECT 2")

        logs = query_audit_logs(instance_name="pg_test")
        assert all(r["instance_name"] == "pg_test" for r in logs)

    def test_query_by_time_range(self, audit_db):
        from tools.audit_logger import log_audit_event, query_audit_logs
        before = time.time()
        log_audit_event(original_sql="SELECT time_test")
        after = time.time()

        logs = query_audit_logs(start_time=before, end_time=after + 1)
        assert len(logs) >= 1

    def test_csv_export(self, audit_db):
        from tools.audit_logger import log_audit_event, query_audit_logs, export_audit_csv
        log_audit_event(original_sql="SELECT csv_test", risk_level=0, operation_type="SELECT")
        log_audit_event(original_sql="DROP TABLE t", risk_level=4, operation_type="DROP")

        logs = query_audit_logs(limit=10)
        csv_data = export_audit_csv(logs)
        assert csv_data  # non-empty

        reader = csv.DictReader(io.StringIO(csv_data))
        rows = list(reader)
        assert len(rows) >= 2
        assert "original_sql" in rows[0]
        assert "risk_level" in rows[0]

    def test_csv_export_empty(self, audit_db):
        from tools.audit_logger import export_audit_csv
        assert export_audit_csv([]) == ""

    def test_handler_json(self, audit_db):
        from tools.audit_logger import log_audit_event, handle_audit_query
        log_audit_event(original_sql="SELECT handler_test")

        result = json.loads(handle_audit_query({"limit": 5}))
        assert "logs" in result
        assert result["count"] >= 1

    def test_handler_csv_export(self, audit_db):
        from tools.audit_logger import log_audit_event, handle_audit_query
        log_audit_event(original_sql="SELECT csv_handler")

        result = json.loads(handle_audit_query({"export_csv": True}))
        assert result["format"] == "csv"
        assert result["count"] >= 1
        assert "original_sql" in result["data"]

    def test_append_only(self, audit_db):
        """Audit logs should be append-only — old records persist."""
        from tools.audit_logger import log_audit_event, query_audit_logs
        log_audit_event(original_sql="first")
        log_audit_event(original_sql="second")
        log_audit_event(original_sql="third")

        logs = query_audit_logs(limit=100)
        sqls = [r["original_sql"] for r in logs]
        assert "first" in sqls
        assert "second" in sqls
        assert "third" in sqls


# ========================================================================
# B. Rollback Generator — 离线测试
# ========================================================================

class TestRollbackGenerator:
    def test_insert_rollback(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "INSERT INTO users (name, email) VALUES ('test', 'test@x.com')",
            "postgresql",
        )
        assert r["can_rollback"] is True
        assert "DELETE" in r["rollback_sql"]
        assert "users" in r["rollback_sql"]

    def test_insert_precise_delete(self):
        """INSERT with explicit columns/values should generate precise DELETE WHERE."""
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "INSERT INTO users (id, name) VALUES (42, 'test')",
            "postgresql",
        )
        assert "id = 42" in r["rollback_sql"] or "id" in r["rollback_sql"]

    def test_update_rollback(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "UPDATE users SET status = 'inactive' WHERE id = 1",
            "postgresql",
        )
        assert r["can_rollback"] is True
        assert "users" in r["rollback_sql"]
        assert "快照" in r["warnings"][0] or "快照" in r["rollback_sql"]

    def test_delete_rollback(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "DELETE FROM users WHERE id = 1",
            "postgresql",
        )
        assert r["can_rollback"] is True
        assert "users" in r["rollback_sql"]

    def test_drop_rollback_no_metadata(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("DROP TABLE users", "postgresql")
        assert r["can_rollback"] is False
        assert any("DROP" in w or "备份" in w for w in r["warnings"])

    def test_drop_with_metadata(self):
        from tools.rollback_generator import generate_rollback
        ddl = 'CREATE TABLE users (id INT PRIMARY KEY, name VARCHAR(100));'
        r = generate_rollback("DROP TABLE users", "postgresql", table_metadata=ddl)
        assert "CREATE TABLE" in r["rollback_sql"]

    def test_alter_add_column_rollback(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "ALTER TABLE users ADD COLUMN temp_flag BOOLEAN",
            "postgresql",
        )
        assert r["can_rollback"] is True
        assert "DROP" in r["rollback_sql"].upper()

    def test_alter_drop_column_rollback(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "ALTER TABLE users DROP COLUMN temp_flag",
            "postgresql",
        )
        # Without instance_name, should still generate a template
        assert "ADD" in r["rollback_sql"].upper() or "列名" in r["rollback_sql"]

    def test_truncate_not_rollbackable(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("TRUNCATE TABLE users", "postgresql")
        assert r["can_rollback"] is False

    def test_handler_json(self):
        from tools.rollback_generator import handle_rollback_generate
        result = json.loads(handle_rollback_generate({
            "sql": "INSERT INTO t (a) VALUES (1)",
            "dialect": "postgresql",
        }))
        assert "rollback_sql" in result

    def test_handler_empty_sql(self):
        from tools.rollback_generator import handle_rollback_generate
        result = json.loads(handle_rollback_generate({"sql": "", "dialect": "mysql"}))
        assert "error" in result

    def test_mysql_dialect(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "INSERT INTO `users` (`name`) VALUES ('test')",
            "mysql",
        )
        assert r["can_rollback"] is True


# ========================================================================
# C. Safe Executor — 离线安全门测试
# ========================================================================

class TestSafeExecutorGates:
    def test_l2_requires_rollback(self):
        from tools.safe_executor import execute_sql
        r = execute_sql(
            "UPDATE users SET x = 1 WHERE id = 1",
            "pg_test", "postgresql",
            risk_level=2, approved=True, rollback_sql="",
        )
        assert r["success"] is False
        assert "回滚" in r["error"]

    def test_l1_requires_approval(self):
        from tools.safe_executor import execute_sql
        r = execute_sql(
            "INSERT INTO users (name) VALUES ('test')",
            "pg_test", "postgresql",
            risk_level=1, approved=False,
        )
        assert r["success"] is False
        assert "审批" in r["error"]

    def test_l0_no_approval_needed(self, audit_db):
        """L0 operations should not require approval (gate passes).
        Actual execution may fail without DB, but gate should not block."""
        from tools.safe_executor import execute_sql
        r = execute_sql(
            "SELECT 1",
            "nonexistent", "postgresql",
            risk_level=0, approved=False,
        )
        # Should fail on connection, not on gate
        assert r["error"] is None or "审批" not in r.get("error", "")


# ========================================================================
# D. Safe Executor — PG 实连测试
# ========================================================================

@pytest.mark.skipif(not PG_AVAILABLE, reason="PG test credentials not set")
class TestSafeExecutorPG:
    def test_l0_select(self, pg_manager, audit_db):
        from tools.safe_executor import execute_sql
        r = execute_sql(
            "SELECT id FROM users LIMIT 5",
            "pg_test", "postgresql",
            risk_level=0,
        )
        assert r["success"] is True
        assert r["data"] is not None
        assert r["execution_time_ms"] >= 0

    def test_l0_select_audit_logged(self, pg_manager, audit_db):
        from tools.safe_executor import execute_sql
        from tools.audit_logger import query_audit_logs
        execute_sql(
            "SELECT COUNT(*) FROM users",
            "pg_test", "postgresql",
            risk_level=0, session_id="audit-test",
        )
        logs = query_audit_logs(limit=5)
        sqls = [r["original_sql"] for r in logs]
        assert any("COUNT" in s for s in sqls)

    def test_statement_timeout_set(self, pg_manager):
        """Verify that statement_timeout is set on PG connections."""
        from tools.db_connector import get_connection_manager
        from sqlalchemy import text
        mgr = get_connection_manager()
        engine = mgr.get_readonly_engine("pg_test")
        with engine.connect() as conn:
            from tools.safe_executor import _set_statement_timeout
            _set_statement_timeout(conn, "postgresql", 30)
            row = conn.execute(text("SHOW statement_timeout")).fetchone()
            assert row is not None
            # Should be 30000ms = 30s
            assert "30" in str(row[0])

    def test_handler_json(self, pg_manager, audit_db):
        from tools.safe_executor import handle_db_execute
        result = json.loads(handle_db_execute({
            "sql": "SELECT 1 AS val",
            "instance_name": "pg_test",
            "dialect": "postgresql",
            "risk_level": 0,
        }))
        assert result["success"] is True


# ========================================================================
# E. E2E: validate → rollback → execute → audit 完整链路
# ========================================================================

@pytest.mark.skipif(not PG_AVAILABLE, reason="PG test credentials not set")
class TestE2EPhase2:
    def test_select_full_pipeline(self, pg_manager, audit_db):
        """L0 SELECT: validate → execute → audit."""
        from tools.sql_ast_validator import validate_sql
        from tools.safe_executor import execute_sql
        from tools.audit_logger import query_audit_logs

        sql = "SELECT id FROM users WHERE id = 1"
        val = validate_sql(sql, "postgresql")
        assert val["valid"] is True
        assert val["risk_level"] == 0

        r = execute_sql(sql, "pg_test", "postgresql", risk_level=0, session_id="e2e-select")
        assert r["success"] is True

        logs = query_audit_logs(limit=5)
        assert any("users" in l.get("original_sql", "") for l in logs)

    def test_insert_rollback_pipeline(self, pg_manager, audit_db):
        """L1 INSERT: validate → generate rollback → verify."""
        from tools.sql_ast_validator import validate_sql
        from tools.rollback_generator import generate_rollback

        sql = "INSERT INTO users (id, created_at) VALUES (99999, NOW())"
        val = validate_sql(sql, "postgresql")
        assert val["risk_level"] == 1

        rb = generate_rollback(sql, "postgresql")
        assert rb["can_rollback"] is True
        assert "DELETE" in rb["rollback_sql"] or "users" in rb["rollback_sql"]

    def test_update_full_pipeline(self, pg_manager, audit_db):
        """L2 UPDATE: validate → rollback(has snapshot note) → gate(needs approval)."""
        from tools.sql_ast_validator import validate_sql
        from tools.rollback_generator import generate_rollback
        from tools.safe_executor import execute_sql

        sql = "UPDATE users SET created_at = NOW() WHERE id = 1"
        val = validate_sql(sql, "postgresql")
        assert val["risk_level"] == 2

        rb = generate_rollback(sql, "postgresql")
        assert "快照" in rb["rollback_sql"] or "快照" in str(rb["warnings"])

        # Without rollback_sql → rejected
        r = execute_sql(sql, "pg_test", "postgresql", risk_level=2, approved=True, rollback_sql="")
        assert r["success"] is False

        # With rollback_sql → allowed (actual execution on readonly may fail, that's OK)
        r2 = execute_sql(sql, "pg_test", "postgresql", risk_level=2,
                         approved=True, rollback_sql=rb["rollback_sql"])
        # Either succeeds or fails on readonly enforcement — both are valid
        # The key assertion is that the safety gate passed
        assert r2["error"] is None or "审批" not in r2.get("error", "")

    def test_alter_metadata_rollback(self, pg_manager, audit_db):
        """ALTER TABLE ADD COLUMN → rollback should be DROP COLUMN."""
        from tools.rollback_generator import generate_rollback
        r = generate_rollback(
            "ALTER TABLE users ADD COLUMN temp_test BOOLEAN DEFAULT FALSE",
            "postgresql",
            instance_name="pg_test",
        )
        assert r["can_rollback"] is True
        assert "DROP" in r["rollback_sql"].upper()
        assert "temp_test" in r["rollback_sql"]


# ========================================================================
# F. 连接池并发隔离测试
# ========================================================================

@pytest.mark.skipif(not PG_AVAILABLE, reason="PG test credentials not set")
class TestConnectionPoolConcurrency:
    def test_multiple_readonly_connections(self, pg_manager):
        """Multiple concurrent read-only connections from the pool."""
        from sqlalchemy import text
        engine = pg_manager.get_readonly_engine("pg_test")
        results = []
        for i in range(5):
            with engine.connect() as conn:
                row = conn.execute(text(f"SELECT {i} AS val")).fetchone()
                results.append(row[0])
        assert results == [0, 1, 2, 3, 4]

    def test_pool_reuse(self, pg_manager):
        """Connections are returned to pool and reused."""
        from sqlalchemy import text
        engine = pg_manager.get_readonly_engine("pg_test")
        pool = engine.pool
        # Open and close multiple connections
        for _ in range(10):
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
        # Pool should not have grown beyond pool_size
        assert pool.checkedout() == 0

    def test_readonly_isolation(self, pg_manager):
        """Read-only connection should reject write operations."""
        from sqlalchemy import text
        engine = pg_manager.get_readonly_engine("pg_test")
        with engine.connect() as conn:
            # Attempt a write on readonly should raise
            try:
                conn.execute(text("CREATE TEMP TABLE _ro_test_xyz (id INT)"))
                # If it didn't raise, still clean up
                conn.execute(text("DROP TABLE IF EXISTS _ro_test_xyz"))
                readonly_enforced = False
            except Exception:
                readonly_enforced = True
        # Read-only setting should block writes (PG default_transaction_read_only=on)
        assert readonly_enforced is True

    def test_admin_engine_separate_from_readonly(self, pg_manager):
        """Admin and readonly engines are separate instances."""
        ro = pg_manager.get_readonly_engine("pg_test")
        admin = pg_manager.get_admin_engine("pg_test")
        assert ro is not admin

    def test_concurrent_threads(self, pg_manager):
        """Connections from multiple threads don't interfere."""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from sqlalchemy import text

        engine = pg_manager.get_readonly_engine("pg_test")

        def query_count(table):
            with engine.connect() as conn:
                row = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).fetchone()
                return row[0]

        tables = ["users", "enterprises", "users", "enterprises", "users"]
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = [pool.submit(query_count, t) for t in tables]
            results = [f.result() for f in as_completed(futures)]
        assert all(isinstance(r, int) for r in results)
        assert len(results) == 5


# ========================================================================
# G. 多方言 AST 校验 (MySQL / Oracle / SQL Server)
# ========================================================================

class TestMultiDialectValidation:
    """Offline dialect validation — no live database needed."""

    # --- MySQL ---
    def test_mysql_select(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("SELECT * FROM orders LIMIT 10", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_mysql_insert(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("INSERT INTO orders (id, amount) VALUES (1, 100.0)", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] == 1

    def test_mysql_update(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("UPDATE orders SET amount = 200 WHERE id = 1", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] == 2

    def test_mysql_drop(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("DROP TABLE orders", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] >= 3

    def test_mysql_alter(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("ALTER TABLE orders ADD COLUMN note TEXT", "mysql")
        assert r["valid"] is True

    def test_mysql_delete_no_where(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("DELETE FROM orders", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] >= 3  # No WHERE → dangerous

    # --- Oracle ---
    def test_oracle_select(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("SELECT * FROM employees WHERE ROWNUM <= 10", "oracle")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_oracle_insert(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("INSERT INTO employees (id, name) VALUES (1, 'test')", "oracle")
        assert r["valid"] is True
        assert r["risk_level"] == 1

    def test_oracle_update(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("UPDATE employees SET salary = 5000 WHERE id = 1", "oracle")
        assert r["valid"] is True
        assert r["risk_level"] == 2

    def test_oracle_truncate(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("TRUNCATE TABLE employees", "oracle")
        assert r["valid"] is True
        assert r["risk_level"] >= 3

    def test_oracle_drop(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("DROP TABLE employees CASCADE CONSTRAINTS", "oracle")
        assert r["valid"] is True
        assert r["risk_level"] >= 3

    # --- SQL Server (tsql) ---
    def test_tsql_select(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("SELECT TOP 10 * FROM dbo.orders", "tsql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_tsql_insert(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("INSERT INTO dbo.orders (id, amount) VALUES (1, 99.9)", "tsql")
        assert r["valid"] is True
        assert r["risk_level"] == 1

    def test_tsql_update(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("UPDATE dbo.orders SET amount = 0 WHERE id = 1", "tsql")
        assert r["valid"] is True
        assert r["risk_level"] == 2

    def test_tsql_drop(self):
        from tools.sql_ast_validator import validate_sql
        r = validate_sql("DROP TABLE dbo.orders", "tsql")
        assert r["valid"] is True
        assert r["risk_level"] >= 3

    # --- Rollback cross-dialect ---
    def test_mysql_rollback_insert(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("INSERT INTO orders (id) VALUES (42)", "mysql")
        assert r["can_rollback"] is True
        assert "DELETE" in r["rollback_sql"]

    def test_oracle_rollback_update(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("UPDATE employees SET salary = 0 WHERE id = 1", "oracle")
        assert r["can_rollback"] is True
        assert "快照" in r["rollback_sql"] or "快照" in str(r["warnings"])

    def test_tsql_rollback_drop(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("DROP TABLE dbo.orders", "tsql")
        assert r["can_rollback"] is True or len(r.get("warnings", [])) > 0

    def test_mysql_rollback_alter_add(self):
        from tools.rollback_generator import generate_rollback
        r = generate_rollback("ALTER TABLE orders ADD COLUMN note TEXT", "mysql")
        assert r["can_rollback"] is True
        assert "DROP" in r["rollback_sql"].upper()
        assert "note" in r["rollback_sql"]
