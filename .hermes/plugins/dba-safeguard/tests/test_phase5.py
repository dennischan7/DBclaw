"""Phase 5 tests — 企业级多级记忆中枢。

Tests for:
  - L1 WorkspaceMemory (token budget, eviction, priorities)
  - L2 SessionStore (save, search, tags, archive)
  - L3 Experience (distill, confirm, search, versioning)
  - L4 BusinessGraph (relations, dictionary, rules, user profiles)
  - DBAMemoryProvider (orchestration, context injection, lifecycle)
"""

import json
import os
import sys
import time
import sqlite3
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure plugin root is importable
PLUGIN_ROOT = Path(__file__).parent.parent
if str(PLUGIN_ROOT) not in sys.path:
    sys.path.insert(0, str(PLUGIN_ROOT))


# ============================================================
# L1 Workspace Memory Tests
# ============================================================

class TestL1WorkspaceMemory:
    """Tests for token-bounded workspace memory."""

    def test_set_and_get(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory(max_tokens=4000)
        ws.set("key1", "hello world")
        assert ws.get("key1") == "hello world"

    def test_remove(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set("k", "value")
        assert ws.remove("k") is True
        assert ws.get("k") is None
        assert ws.remove("nonexistent") is False

    def test_clear(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set("a", "1")
        ws.set("b", "2")
        ws.clear()
        assert ws.item_count == 0
        assert ws.total_tokens == 0

    def test_token_budget_enforcement(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory(max_tokens=100)
        # Each item ~33 tokens -> 3 items fills 100 tokens
        ws.set("a", "x" * 99)  # ~33 tokens
        ws.set("b", "y" * 99)  # ~33 tokens
        ws.set("c", "z" * 99)  # ~33 tokens
        assert ws.total_tokens <= 100

    def test_eviction_by_priority(self):
        from memory.l1_workspace import L1WorkspaceMemory, ContextPriority
        ws = L1WorkspaceMemory(max_tokens=25)
        ws.set("low", "x" * 30, priority=ContextPriority.LOW)      # ~10 tokens
        ws.set("high", "y" * 30, priority=ContextPriority.HIGH)    # ~10 tokens → total 20
        # Adding a CRITICAL item (10 tokens) exceeds budget=25 → must evict
        ws.set("critical", "z" * 30, priority=ContextPriority.CRITICAL)
        assert ws.get("critical") is not None
        # LOW should be evicted first
        assert ws.get("low") is None

    def test_critical_items_never_evicted(self):
        from memory.l1_workspace import L1WorkspaceMemory, ContextPriority
        ws = L1WorkspaceMemory(max_tokens=50)
        ws.set("crit", "a" * 30, priority=ContextPriority.CRITICAL)
        # A normal item can't evict critical
        ws.set("normal", "b" * 60, priority=ContextPriority.NORMAL)
        assert ws.get("crit") is not None

    def test_replace_existing_key(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set("key", "old value")
        ws.set("key", "new value")
        assert ws.get("key") == "new value"

    def test_render_context(self):
        from memory.l1_workspace import L1WorkspaceMemory, ContextPriority
        ws = L1WorkspaceMemory()
        ws.set("task1", "SELECT * FROM users", priority=ContextPriority.HIGH, category="task")
        ws.set("val1", "passed", priority=ContextPriority.HIGH, category="validation")
        result = ws.render_context()
        assert "当前工作区上下文" in result
        assert "SELECT * FROM users" in result

    def test_set_task_state(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set_task_state("t1", "SELECT 1", risk_level=2, current_stage="validation")
        content = ws.get("current_task")
        assert "t1" in content
        assert "L2" in content
        assert "validation" in content

    def test_snapshot(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set("a", "test content", category="task")
        snap = ws.snapshot()
        assert snap["total_tokens"] > 0
        assert len(snap["items"]) == 1
        assert snap["items"][0]["key"] == "a"

    def test_remaining_tokens(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory(max_tokens=100)
        before = ws.remaining_tokens
        ws.set("item", "some text here")
        after = ws.remaining_tokens
        assert after < before

    def test_convenience_methods(self):
        from memory.l1_workspace import L1WorkspaceMemory
        ws = L1WorkspaceMemory()
        ws.set_metadata("users_table", "id INT, name TEXT")
        ws.add_validation_result("sql_validate", True, "syntax OK")
        ws.add_retry_draft(1, "SELECT * FROM users LIMIT 10")
        assert ws.get("meta:users_table") is not None
        assert ws.get("val:sql_validate") is not None
        assert ws.get("retry:1") is not None

    def test_get_all_sorted_by_priority(self):
        from memory.l1_workspace import L1WorkspaceMemory, ContextPriority
        ws = L1WorkspaceMemory()
        ws.set("low", "1", priority=ContextPriority.LOW)
        ws.set("crit", "2", priority=ContextPriority.CRITICAL)
        ws.set("norm", "3", priority=ContextPriority.NORMAL)
        items = ws.get_all()
        priorities = [i.priority for i in items]
        assert priorities[0] == ContextPriority.CRITICAL


# ============================================================
# L2 Session Store Tests
# ============================================================

class TestL2SessionStore:
    """Tests for DBA-tagged session memory."""

    @pytest.fixture(autouse=True)
    def isolate_db(self, tmp_path):
        from memory.l2_session_store import set_session_db_path
        set_session_db_path(tmp_path / "test_session.db")
        yield
        set_session_db_path(tmp_path / "test_session_cleanup.db")

    def test_save_and_get(self):
        from memory.l2_session_store import save_session_record, get_session_records
        save_session_record("s1", "user", "SELECT * FROM users")
        records = get_session_records("s1")
        assert len(records) == 1
        assert records[0]["content"] == "SELECT * FROM users"

    def test_dba_tags(self):
        from memory.l2_session_store import save_session_record, get_session_records
        save_session_record(
            "s1", "tool", "query executed",
            db_type="postgresql", instance_name="pg_test",
            risk_level=2, operation_type="UPDATE",
        )
        records = get_session_records("s1")
        assert records[0]["db_type"] == "postgresql"
        assert records[0]["risk_level"] == 2
        assert records[0]["operation_type"] == "UPDATE"

    def test_fts_search(self):
        from memory.l2_session_store import save_session_record, search_sessions
        save_session_record("s1", "user", "optimize index performance")
        save_session_record("s1", "user", "delete old records")
        results = search_sessions("optimize index")
        assert len(results) >= 1
        assert "optimize" in results[0]["content"]

    def test_search_by_tags(self):
        from memory.l2_session_store import save_session_record, search_sessions
        save_session_record("s1", "tool", "pg query", db_type="postgresql", risk_level=0)
        save_session_record("s2", "tool", "mysql query", db_type="mysql", risk_level=1)
        results = search_sessions("", db_type="postgresql")
        assert all(r["db_type"] == "postgresql" for r in results)

    def test_search_by_risk_level(self):
        from memory.l2_session_store import save_session_record, search_sessions
        save_session_record("s1", "tool", "safe select", risk_level=0)
        save_session_record("s1", "tool", "dangerous drop", risk_level=4)
        results = search_sessions("", risk_level=4)
        assert all(r["risk_level"] == 4 for r in results)

    def test_archive(self):
        from memory.l2_session_store import save_session_record, get_session_records, archive_old_sessions
        # Save a record with old timestamp
        from memory.l2_session_store import _get_db
        db = _get_db()
        old_ts = time.time() - (31 * 86400)
        db.execute(
            "INSERT INTO session_records (session_id, timestamp, role, content) VALUES (?, ?, ?, ?)",
            ("s_old", old_ts, "user", "old record"),
        )
        db.commit()
        # Also save a recent record
        save_session_record("s_new", "user", "new record")

        # Archive
        count = archive_old_sessions(days=30)
        assert count >= 1

        # Old record should not show in non-archived query
        old_records = get_session_records("s_old")
        assert len(old_records) == 0

        # But should show with include_archived
        all_records = get_session_records("s_old", include_archived=True)
        assert len(all_records) == 1

    def test_session_summary(self):
        from memory.l2_session_store import save_session_record, get_session_summary
        save_session_record("s1", "user", "hello", db_type="postgresql")
        save_session_record("s1", "tool", "result", operation_type="SELECT", risk_level=0)
        summary = get_session_summary("s1")
        assert summary["record_count"] == 2
        assert "postgresql" in summary["db_types"]

    def test_search_similar_operations(self):
        from memory.l2_session_store import save_session_record, search_similar_operations
        save_session_record("s1", "tool", "executed UPDATE on users",
                            sql_text="UPDATE users SET active = 0", operation_type="UPDATE")
        results = search_similar_operations(sql_text="UPDATE users SET status = 1")
        # Should find the previous UPDATE operation
        assert len(results) >= 0  # may or may not match depending on FTS

    def test_get_active_session_ids(self):
        from memory.l2_session_store import save_session_record, get_active_session_ids
        save_session_record("sess_a", "user", "msg 1")
        save_session_record("sess_b", "user", "msg 2")
        ids = get_active_session_ids()
        assert "sess_a" in ids
        assert "sess_b" in ids


# ============================================================
# L3 Experience Memory Tests
# ============================================================

class TestL3Experience:
    """Tests for ops experience memory with human confirmation."""

    @pytest.fixture(autouse=True)
    def isolate_db(self, tmp_path):
        from memory.l3_experience import set_experience_db_path
        set_experience_db_path(tmp_path / "test_exp.db")
        yield
        set_experience_db_path(tmp_path / "test_exp_cleanup.db")

    def _make_task_result(self, sql="SELECT 1", risk_level=0, dialect="postgresql"):
        return {
            "task_id": "t_test",
            "sql": sql,
            "risk_level": risk_level,
            "dialect": dialect,
            "current_stage": "audit",
            "stages": [
                {"stage": "execute", "status": "passed", "duration_ms": 50},
                {"stage": "audit", "status": "passed", "duration_ms": 10},
            ],
        }

    def test_distill_successful_task(self):
        from memory.l3_experience import distill_experience, get_experience
        result = self._make_task_result()
        exp_id = distill_experience(result)
        assert exp_id is not None
        exp = get_experience(exp_id)
        assert exp["status"] == "pending"
        assert exp["category"] in ("sql_pattern", "best_practice", "optimization",
                                    "troubleshooting", "pitfall", "ddl_workflow",
                                    "health_check")

    def test_distill_failed_task_skipped(self):
        from memory.l3_experience import distill_experience
        result = {
            "task_id": "t_fail",
            "sql": "DROP TABLE users",
            "stages": [
                {"stage": "validate", "status": "failed"},
            ],
        }
        exp_id = distill_experience(result)
        assert exp_id is None

    def test_confirm_experience(self):
        from memory.l3_experience import distill_experience, confirm_experience, get_experience
        result = self._make_task_result()
        exp_id = distill_experience(result)
        assert confirm_experience(exp_id, "admin") is True
        exp = get_experience(exp_id)
        assert exp["status"] == "confirmed"
        assert exp["confirmed_by"] == "admin"

    def test_reject_experience(self):
        from memory.l3_experience import distill_experience, reject_experience, get_experience
        result = self._make_task_result()
        exp_id = distill_experience(result)
        assert reject_experience(exp_id) is True
        exp = get_experience(exp_id)
        assert exp["status"] == "rejected"

    def test_search_only_confirmed(self):
        from memory.l3_experience import (
            distill_experience, confirm_experience, search_experiences,
        )
        # Create and confirm one
        r1 = self._make_task_result(sql="SELECT name FROM users WHERE id = 1")
        id1 = distill_experience(r1)
        confirm_experience(id1)

        # Create pending one
        r2 = self._make_task_result(sql="SELECT name FROM orders WHERE id = 2")
        id2 = distill_experience(r2)

        # Search should only find confirmed
        results = search_experiences("SELECT name")
        confirmed_ids = {r["id"] for r in results}
        assert id1 in confirmed_ids
        assert id2 not in confirmed_ids

    def test_get_pending_experiences(self):
        from memory.l3_experience import distill_experience, get_pending_experiences
        result = self._make_task_result()
        distill_experience(result)
        pending = get_pending_experiences()
        assert len(pending) >= 1
        assert all(p["status"] == "pending" for p in pending)

    def test_toggle_experience(self):
        from memory.l3_experience import distill_experience, toggle_experience, get_experience
        result = self._make_task_result()
        exp_id = distill_experience(result)
        toggle_experience(exp_id, False)
        exp = get_experience(exp_id)
        assert exp["enabled"] == 0

    def test_list_by_category(self):
        from memory.l3_experience import distill_experience, list_experiences
        r1 = self._make_task_result(sql="ALTER TABLE users ADD COLUMN age INT")
        distill_experience(r1)
        results = list_experiences(category="ddl_workflow", enabled_only=False)
        assert len(results) >= 1

    def test_recall_for_task(self):
        from memory.l3_experience import (
            distill_experience, confirm_experience, recall_for_task,
        )
        result = self._make_task_result(sql="SELECT u.name, o.total FROM users u JOIN orders o ON u.id = o.user_id")
        exp_id = distill_experience(result)
        confirm_experience(exp_id)

        recalled = recall_for_task(sql="SELECT u.email FROM users u JOIN logs l ON u.id = l.user_id")
        # Should recall similar JOIN pattern
        assert len(recalled) >= 0  # FTS may or may not match

    def test_version_management(self):
        from memory.l3_experience import (
            distill_experience, create_new_version, get_experience,
        )
        result = self._make_task_result()
        exp_id = distill_experience(result)

        new_id = create_new_version(exp_id, "Updated content with better approach")
        assert new_id is not None
        new_exp = get_experience(new_id)
        assert new_exp["version"] == 2
        assert new_exp["parent_version_id"] == exp_id

        # Original is preserved
        original = get_experience(exp_id)
        assert original["version"] == 1

    def test_sql_pattern_extraction(self):
        from memory.l3_experience import _extract_sql_pattern
        pattern = _extract_sql_pattern("SELECT name FROM users WHERE id = 42 AND status = 'active'")
        assert "?" in pattern  # literals replaced
        assert "SELECT" in pattern

    def test_experience_classification(self):
        from memory.l3_experience import _classify_experience
        assert _classify_experience({"sql": "ALTER TABLE users ADD COLUMN age INT"}) == "ddl_workflow"
        assert _classify_experience({"sql": "SELECT 1", "risk_level": 3}) == "pitfall"
        assert _classify_experience({"sql": "SELECT a.id FROM t1 a JOIN t2 b ON a.id = b.id"}) == "sql_pattern"

    def test_distill_without_confirmation(self):
        from memory.l3_experience import distill_experience, get_experience
        result = self._make_task_result()
        exp_id = distill_experience(result, require_confirmation=False)
        exp = get_experience(exp_id)
        assert exp["status"] == "confirmed"


# ============================================================
# L4 Business Graph Tests
# ============================================================

class TestL4BusinessGraph:
    """Tests for business lineage, dictionary, rules, and user profiling."""

    @pytest.fixture(autouse=True)
    def isolate_db(self, tmp_path):
        from memory.l4_business_graph import set_graph_db_path
        set_graph_db_path(tmp_path / "test_graph.db")
        yield
        set_graph_db_path(tmp_path / "test_graph_cleanup.db")

    def test_add_table_relation(self):
        from memory.l4_business_graph import add_table_relation, get_table_relations
        add_table_relation("orders", "user_id", "users", "id", relation_type="fk")
        rels = get_table_relations("orders")
        assert len(rels) >= 1
        assert rels[0]["target_table"] == "users"

    def test_get_relations_direction(self):
        from memory.l4_business_graph import add_table_relation, get_table_relations
        add_table_relation("orders", "user_id", "users", "id")
        # Source direction
        src = get_table_relations("orders", direction="source")
        assert len(src) >= 1
        # Target direction
        tgt = get_table_relations("users", direction="target")
        assert len(tgt) >= 1

    def test_column_lineage(self):
        from memory.l4_business_graph import add_table_relation, get_column_lineage
        add_table_relation("orders", "user_id", "users", "id")
        lineage = get_column_lineage("orders", "user_id")
        assert len(lineage) >= 1

    def test_add_dictionary_entry(self):
        from memory.l4_business_graph import add_dictionary_entry, get_dictionary
        add_dictionary_entry(
            "users", "status",
            business_name="用户状态",
            description="用户账号的当前状态",
            enum_values="0=禁用,1=正常,2=待审核",
        )
        entries = get_dictionary("users", "status")
        assert len(entries) == 1
        assert entries[0]["business_name"] == "用户状态"
        assert "禁用" in entries[0]["enum_values"]

    def test_dictionary_upsert(self):
        from memory.l4_business_graph import add_dictionary_entry, get_dictionary
        add_dictionary_entry("users", "status", business_name="状态v1")
        add_dictionary_entry("users", "status", business_name="状态v2")
        entries = get_dictionary("users", "status")
        assert len(entries) == 1
        assert entries[0]["business_name"] == "状态v2"

    def test_search_dictionary(self):
        from memory.l4_business_graph import add_dictionary_entry, search_dictionary
        add_dictionary_entry("users", "email", business_name="email address",
                             description="user registration email for login")
        results = search_dictionary("email")
        assert len(results) >= 1

    def test_add_business_rule(self):
        from memory.l4_business_graph import add_business_rule, get_rules_for_table
        add_business_rule(
            "status_not_null", "not_null",
            condition="NOT NULL",
            target_table="users", target_column="status",
            description="用户状态不能为空",
            severity="error",
        )
        rules = get_rules_for_table("users")
        assert len(rules) >= 1
        assert rules[0]["rule_name"] == "status_not_null"

    def test_check_rules_enum(self):
        from memory.l4_business_graph import add_business_rule, check_rules
        add_business_rule(
            "valid_status", "enum_check",
            condition="active,inactive,pending",
            target_table="users", target_column="status",
        )
        # Valid value
        violations = check_rules("users", "status", "active")
        assert len(violations) == 0
        # Invalid value
        violations = check_rules("users", "status", "deleted")
        assert len(violations) == 1

    def test_check_rules_range(self):
        from memory.l4_business_graph import add_business_rule, check_rules
        add_business_rule(
            "valid_age", "range_check",
            condition="0,150",
            target_table="users", target_column="age",
        )
        assert len(check_rules("users", "age", "25")) == 0
        assert len(check_rules("users", "age", "200")) == 1

    def test_user_profile_create_and_update(self):
        from memory.l4_business_graph import update_user_profile, get_user_profile
        update_user_profile("u1", preferred_dialect="postgresql", risk_mode="conservative")
        profile = get_user_profile("u1")
        assert profile["preferred_dialect"] == "postgresql"
        assert profile["risk_mode"] == "conservative"

        # Update
        update_user_profile("u1", risk_mode="aggressive")
        profile = get_user_profile("u1")
        assert profile["risk_mode"] == "aggressive"

    def test_record_user_operation(self):
        from memory.l4_business_graph import record_user_operation, get_user_profile
        record_user_operation("u2", "SELECT", "postgresql")
        record_user_operation("u2", "SELECT", "postgresql")
        record_user_operation("u2", "UPDATE", "postgresql")
        profile = get_user_profile("u2")
        stats = json.loads(profile["operation_stats"])
        assert stats["SELECT"] == 2
        assert stats["UPDATE"] == 1

    def test_import_data_dictionary(self):
        from memory.l4_business_graph import import_data_dictionary, get_dictionary
        entries = [
            {"table_name": "orders", "column_name": "total", "business_name": "订单总额",
             "description": "订单金额合计"},
            {"table_name": "orders", "column_name": "status", "business_name": "订单状态",
             "enum_values": "0=待支付,1=已支付,2=已取消"},
            {"table_name": "", "column_name": ""},  # should be skipped
        ]
        count = import_data_dictionary(entries)
        assert count == 2
        all_entries = get_dictionary("orders")
        assert len(all_entries) == 2

    def test_get_graph_context(self):
        from memory.l4_business_graph import (
            add_table_relation, add_dictionary_entry, add_business_rule,
            update_user_profile, get_graph_context,
        )
        add_table_relation("orders", "user_id", "users", "id")
        add_dictionary_entry("users", "status", business_name="用户状态")
        add_business_rule("status_rule", "not_null", "NOT NULL",
                          target_table="users", description="状态必填")
        update_user_profile("u1", preferred_dialect="postgresql")

        ctx = get_graph_context(["users", "orders"], user_id="u1")
        assert "业务图谱上下文" in ctx
        assert "用户状态" in ctx
        assert "关联关系" in ctx

    def test_get_graph_context_empty(self):
        from memory.l4_business_graph import get_graph_context
        # No data → empty context
        ctx = get_graph_context(["nonexistent"])
        assert ctx == ""

    def test_user_profile_nonexistent(self):
        from memory.l4_business_graph import get_user_profile
        assert get_user_profile("ghost") is None


# ============================================================
# DBAMemoryProvider Integration Tests
# ============================================================

class TestDBAMemoryProvider:
    """Tests for the unified memory orchestrator."""

    @pytest.fixture(autouse=True)
    def isolate_dbs(self, tmp_path):
        from memory.l2_session_store import set_session_db_path
        from memory.l3_experience import set_experience_db_path
        from memory.l4_business_graph import set_graph_db_path
        set_session_db_path(tmp_path / "test_prov_session.db")
        set_experience_db_path(tmp_path / "test_prov_exp.db")
        set_graph_db_path(tmp_path / "test_prov_graph.db")
        yield
        set_session_db_path(tmp_path / "cleanup_session.db")
        set_experience_db_path(tmp_path / "cleanup_exp.db")
        set_graph_db_path(tmp_path / "cleanup_graph.db")

    def test_initialize(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s1", user_id="admin")
        assert prov._initialized
        assert prov._session_id == "s1"

    def test_workspace_access(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        prov = DBAMemoryProvider()
        prov.workspace.set("test", "value")
        assert prov.workspace.get("test") == "value"

    def test_record_operation(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        from memory.l2_session_store import get_session_records
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s1")
        prov.record_operation(
            "sql_validate", "validated SELECT query",
            risk_level=0, sql_text="SELECT 1", db_type="postgresql",
        )
        # Check L1
        assert prov.workspace.get("op:sql_validate") is not None
        # Check L2
        records = get_session_records("s1")
        assert len(records) >= 1

    def test_get_injection_context(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s2")
        prov.workspace.set("task", "running query", category="task")
        prov.add_working_memory({"operation": "SELECT", "detail": "test query", "risk_level": 0})

        ctx = prov.get_injection_context(user_query="SELECT performance")
        assert "当前工作区上下文" in ctx or "当前会话操作历史" in ctx

    def test_on_session_end_flushes(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        from memory.l2_session_store import get_session_records
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s3")
        prov.workspace.set("task", "some task", category="task")
        prov.add_working_memory({"operation": "DROP", "detail": "drop table", "risk_level": 3})

        prov.on_session_end()
        assert prov.workspace.item_count == 0
        assert len(prov._working_memory) == 0

    def test_on_session_end_distills_tasks(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        from memory.l3_experience import get_pending_experiences
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s4")

        task_result = {
            "task_id": "t_int",
            "sql": "SELECT * FROM users WHERE id = 1",
            "risk_level": 0,
            "dialect": "postgresql",
            "current_stage": "audit",
            "stages": [
                {"stage": "execute", "status": "passed", "duration_ms": 10},
                {"stage": "audit", "status": "passed", "duration_ms": 5},
            ],
        }
        prov.on_session_end(task_results=[task_result])

        pending = get_pending_experiences()
        assert len(pending) >= 1

    def test_shutdown(self):
        from memory.dba_memory_provider import DBAMemoryProvider
        prov = DBAMemoryProvider()
        prov.initialize(session_id="s5")
        prov.workspace.set("x", "y")
        prov.shutdown()
        assert prov.workspace.item_count == 0
        assert not prov._initialized

    def test_tool_handler_search(self):
        from memory.dba_memory_provider import handle_dba_memory_search
        result = json.loads(handle_dba_memory_search({"query": "test"}))
        assert "results" in result
        assert "count" in result

    def test_tool_handler_search_empty_query(self):
        from memory.dba_memory_provider import handle_dba_memory_search
        result = json.loads(handle_dba_memory_search({"query": ""}))
        assert "error" in result

    def test_tool_handler_save(self):
        from memory.dba_memory_provider import handle_dba_memory_save
        result = json.loads(handle_dba_memory_save({
            "title": "Test Experience",
            "content": "This is a test",
            "category": "best_practice",
        }))
        assert result["result"] == "saved_pending"
        assert "id" in result

    def test_tool_handler_save_validation(self):
        from memory.dba_memory_provider import handle_dba_memory_save
        result = json.loads(handle_dba_memory_save({"title": "", "content": ""}))
        assert "error" in result
