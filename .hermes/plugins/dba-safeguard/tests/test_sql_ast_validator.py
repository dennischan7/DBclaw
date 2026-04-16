"""sql_ast_validator 单元测试 — 纯离线，无数据库依赖。

覆盖:
  - SELECT/INSERT/UPDATE/DELETE 操作识别
  - DDL 操作识别 (CREATE/ALTER/DROP/TRUNCATE)
  - L0-L4 风险分级
  - WHERE 缺失告警 → L4升级
  - 多方言校验 (mysql/postgresql/oracle/hive)
  - 表名提取
  - 语法错误检测
  - SELECT * 告警
"""

import json
import sys
from pathlib import Path

import pytest

# Add plugin root to path
plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

from tools.sql_ast_validator import validate_sql, handle_sql_validate


# ========================================================================
# L0 — Read-only operations
# ========================================================================

class TestL0Readonly:
    def test_simple_select(self):
        r = validate_sql("SELECT id, name FROM users WHERE id = 1", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 0
        assert r["risk_label"] == "L0_READONLY"
        assert r["operation_type"] == "SELECT"
        assert "users" in r["tables"]

    def test_select_with_join(self):
        r = validate_sql(
            "SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 0
        assert "users" in r["tables"] or any("users" in t for t in r["tables"])

    def test_select_star_warning(self):
        r = validate_sql("SELECT * FROM users", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 0
        assert any("SELECT *" in w for w in r["warnings"])

    def test_select_count(self):
        r = validate_sql("SELECT COUNT(*) FROM users", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_select_subquery(self):
        r = validate_sql(
            "SELECT * FROM users WHERE id IN (SELECT user_id FROM orders WHERE total > 100)",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_select_cte(self):
        r = validate_sql(
            "WITH active AS (SELECT id FROM users WHERE status = 'active') "
            "SELECT * FROM active",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 0


# ========================================================================
# L1 — Low-risk DML
# ========================================================================

class TestL1LowDML:
    def test_insert_single_row(self):
        r = validate_sql(
            "INSERT INTO users (name, email) VALUES ('test', 'test@example.com')",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 1
        assert r["operation_type"] == "INSERT"
        assert "users" in r["tables"]

    def test_insert_multiple_values(self):
        r = validate_sql(
            "INSERT INTO users (name) VALUES ('a'), ('b'), ('c')",
            "mysql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 1


# ========================================================================
# L2 — Medium-risk batch DML / structure extension
# ========================================================================

class TestL2MediumBatch:
    def test_update_with_where(self):
        r = validate_sql(
            "UPDATE users SET status = 'inactive' WHERE last_login < '2025-01-01'",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 2
        assert r["operation_type"] == "UPDATE"

    def test_delete_with_where(self):
        r = validate_sql(
            "DELETE FROM temp_logs WHERE created_at < '2024-01-01'",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 2
        assert r["operation_type"] == "DELETE"

    def test_create_index(self):
        r = validate_sql(
            "CREATE INDEX idx_users_email ON users(email)",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] <= 2  # CREATE INDEX is L2


# ========================================================================
# L3 — High-risk structure destruction
# ========================================================================

class TestL3HighRisk:
    def test_alter_drop_column(self):
        r = validate_sql(
            "ALTER TABLE users DROP COLUMN temp_field",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] >= 3

    def test_truncate_table(self):
        r = validate_sql("TRUNCATE TABLE temp_logs", "postgresql")
        # sqlglot may or may not parse TRUNCATE fully, but risk should be >= 3
        assert r["risk_level"] >= 3


# ========================================================================
# L4 — Catastrophic operations
# ========================================================================

class TestL4Catastrophic:
    def test_drop_table(self):
        r = validate_sql("DROP TABLE users", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 4
        assert r["operation_type"].startswith("DROP")

    def test_drop_database(self):
        r = validate_sql("DROP DATABASE test_db", "postgresql")
        # Some dialects may parse this differently
        assert r["risk_level"] >= 4

    def test_delete_without_where(self):
        """DELETE without WHERE should be escalated to L4."""
        r = validate_sql("DELETE FROM users", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 4
        assert r["risk_label"] == "L4_CATASTROPHIC"
        assert any("无WHERE" in w for w in r["warnings"])

    def test_update_without_where(self):
        """UPDATE without WHERE should be escalated to L4."""
        r = validate_sql("UPDATE users SET status = 'deleted'", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 4
        assert any("无WHERE" in w for w in r["warnings"])


# ========================================================================
# Syntax error detection
# ========================================================================

class TestSyntaxErrors:
    def test_invalid_sql(self):
        r = validate_sql("SELECTT * FORM users", "mysql")
        # Should fail to parse or produce an error
        assert r["valid"] is False or len(r["errors"]) > 0 or r["operation_type"] == "UNKNOWN"

    def test_empty_sql(self):
        result = handle_sql_validate({"sql": "", "dialect": "mysql"})
        data = json.loads(result)
        assert "error" in data


# ========================================================================
# Multi-dialect support
# ========================================================================

class TestDialects:
    def test_mysql_backticks(self):
        r = validate_sql("SELECT `name` FROM `users` WHERE `id` = 1", "mysql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_postgresql_double_quotes(self):
        r = validate_sql('SELECT "name" FROM "users" WHERE "id" = 1', "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_postgresql_ilike(self):
        r = validate_sql("SELECT * FROM users WHERE name ILIKE '%test%'", "postgresql")
        assert r["valid"] is True
        assert r["risk_level"] == 0

    def test_postgresql_returning(self):
        r = validate_sql(
            "INSERT INTO users (name) VALUES ('test') RETURNING id",
            "postgresql",
        )
        assert r["valid"] is True
        assert r["risk_level"] == 1

    def test_postgresql_on_conflict(self):
        r = validate_sql(
            "INSERT INTO users (id, name) VALUES (1, 'test') "
            "ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name",
            "postgresql",
        )
        assert r["valid"] is True

    def test_hive_select(self):
        r = validate_sql("SELECT * FROM my_table LIMIT 10", "hive")
        assert r["valid"] is True

    def test_oracle_rownum(self):
        r = validate_sql("SELECT * FROM users WHERE ROWNUM <= 10", "oracle")
        assert r["valid"] is True


# ========================================================================
# Table extraction
# ========================================================================

class TestTableExtraction:
    def test_single_table(self):
        r = validate_sql("SELECT id FROM orders", "postgresql")
        assert "orders" in r["tables"]

    def test_multiple_tables_join(self):
        r = validate_sql(
            "SELECT u.name FROM users u JOIN orders o ON u.id = o.user_id",
            "postgresql",
        )
        assert len(r["tables"]) >= 2

    def test_schema_qualified(self):
        r = validate_sql("SELECT id FROM public.users", "postgresql")
        assert any("users" in t for t in r["tables"])


# ========================================================================
# Handler JSON output
# ========================================================================

class TestHandlerOutput:
    def test_handler_returns_json(self):
        result = handle_sql_validate({"sql": "SELECT 1", "dialect": "postgresql"})
        data = json.loads(result)
        assert data["valid"] is True
        assert "risk_level" in data

    def test_handler_missing_sql(self):
        result = handle_sql_validate({"dialect": "postgresql"})
        data = json.loads(result)
        assert "error" in data
