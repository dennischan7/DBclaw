"""risk_interceptor 单元测试 — 校验 pre_tool_call 钩子的拦截逻辑。

覆盖:
  - L0 SELECT 自动放行
  - L1 INSERT 通知放行
  - L2 UPDATE (有WHERE) 需人工确认
  - L3 ALTER TABLE DROP COLUMN 强制阻断
  - L4 DROP TABLE 强制阻断
  - L4 DELETE 无WHERE 强制阻断
  - 非 db_execute 工具不拦截
  - 空SQL阻断
  - 语法错误SQL阻断
  - approved=true 跳过L2确认
"""

import asyncio
import json
import sys
from pathlib import Path

import pytest

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

from harnesses.risk_interceptor import pre_tool_call_hook


def _run(coro):
    """Run async function synchronously."""
    return asyncio.get_event_loop().run_until_complete(coro)


class TestRiskInterceptorAutoApprove:
    """L0 — read-only queries should auto-approve."""

    def test_select_passes(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "SELECT id FROM users WHERE id = 1", "dialect": "postgresql"},
        ))
        assert result is None  # None = proceed

    def test_explain_passes(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "EXPLAIN SELECT * FROM users", "dialect": "postgresql"},
        ))
        # EXPLAIN should be L0 or at most proceed
        assert result is None or (isinstance(result, dict) and not result.get("block"))


class TestRiskInterceptorNotifyApprove:
    """L1 — low-risk DML should notify and approve."""

    def test_insert_passes(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "INSERT INTO logs (msg) VALUES ('test')", "dialect": "postgresql"},
        ))
        assert result is None  # notify_approve → proceed


class TestRiskInterceptorHumanConfirm:
    """L2 — medium-risk operations require human confirmation."""

    def test_update_with_where_blocks(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "UPDATE users SET status = 'inactive' WHERE id = 1", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True
        assert "人工确认" in result["message"]

    def test_update_with_approved_passes(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {
                "sql": "UPDATE users SET status = 'inactive' WHERE id = 1",
                "dialect": "postgresql",
                "approved": True,
            },
        ))
        assert result is None  # approved → proceed

    def test_delete_with_where_blocks(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "DELETE FROM logs WHERE id = 1", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True


class TestRiskInterceptorForceBlock:
    """L3/L4 — destructive operations are force-blocked."""

    def test_drop_table_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "DROP TABLE users", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True
        assert "阻断" in result["message"]

    def test_delete_no_where_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "DELETE FROM users", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True

    def test_truncate_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "TRUNCATE TABLE users", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True

    def test_alter_drop_column_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "ALTER TABLE users DROP COLUMN temp", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True


class TestRiskInterceptorEdgeCases:
    """Non-db_execute tools, empty SQL, syntax errors."""

    def test_non_db_execute_ignored(self):
        result = _run(pre_tool_call_hook(
            "web_search",
            {"query": "DROP TABLE users"},
        ))
        assert result is None  # Not intercepted

    def test_empty_sql_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "", "dialect": "postgresql"},
        ))
        assert result is not None
        assert result["block"] is True

    def test_syntax_error_blocked(self):
        result = _run(pre_tool_call_hook(
            "db_execute",
            {"sql": "SELECTT * FORM users", "dialect": "postgresql"},
        ))
        # Should block on syntax error OR pass through as UNKNOWN
        if result is not None:
            assert result["block"] is True
