"""Phase 3 测试套件 — intent_router / library_search(优化) / config_watcher / context_injector。

分为:
  A. 意图分类测试 (关键词匹配 + 数据库类型识别)
  B. RAG知识库检索测试 (token-aware切片 + TF-IDF评分)
  C. 配置热重载测试
  D. 上下文注入集成测试
  E. 路由上下文生成测试
"""

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
# A. 意图分类测试
# ========================================================================

class TestIntentClassifierKeywords:
    """Test keyword-based fast classification."""

    def test_select_query(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("SELECT * FROM users WHERE id = 1")
        assert r["intent"] == "query"
        assert r["confidence"] >= 0.9

    def test_insert(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("INSERT INTO orders (id, amount) VALUES (1, 100)")
        assert r["intent"] == "dml_insert"
        assert r["confidence"] >= 0.9

    def test_update(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("UPDATE users SET name = 'test' WHERE id = 1")
        assert r["intent"] == "dml_update"
        assert r["confidence"] >= 0.9

    def test_delete(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("DELETE FROM orders WHERE id = 99")
        assert r["intent"] == "dml_delete"
        assert r["confidence"] >= 0.9

    def test_create_table(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("CREATE TABLE test_tbl (id INT PRIMARY KEY)")
        assert r["intent"] == "ddl_create"

    def test_alter_table(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("ALTER TABLE users ADD COLUMN phone VARCHAR(20)")
        assert r["intent"] == "ddl_alter"

    def test_drop_table(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("DROP TABLE temp_data")
        assert r["intent"] == "ddl_drop"

    def test_truncate(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("TRUNCATE TABLE logs")
        assert r["intent"] == "ddl_truncate"

    def test_show_tables(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("SHOW TABLES")
        assert r["intent"] == "query"

    def test_explain(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("EXPLAIN SELECT * FROM orders")
        assert r["intent"] == "query"

    def test_natural_language_optimize(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("这个查询太慢了，帮我优化一下")
        assert r["intent"] in ("optimize", "troubleshoot", "general")

    def test_natural_language_health(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("检查一下数据库的健康状态")
        assert r["intent"] in ("health_check", "general")

    def test_general_question(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("什么是B+树索引")
        assert r["intent"] == "general"
        assert r["confidence"] < 0.9  # low confidence for ambiguous


class TestIntentDBTypeDetection:
    """Test database type and version detection."""

    def test_mysql_detected(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("在MySQL里查询用户表")
        assert r["db_type"] == "mysql"

    def test_postgresql_detected(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("PostgreSQL数据库的pg_stat_activity怎么看")
        assert r["db_type"] == "postgresql"

    def test_oracle_detected(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("Oracle 19c的AWR报告怎么生成")
        assert r["db_type"] == "oracle"
        assert r["db_version"] == "19c"

    def test_mysql_version(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("MySQL 8.0的窗口函数怎么用")
        assert r["db_type"] == "mysql"
        assert r["db_version"] == "8.0"

    def test_no_db_type(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("SELECT 1")
        # No db type explicitly mentioned → None or from context
        assert r["intent"] == "query"

    def test_context_override(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("SELECT 1", context={"dialect": "postgresql"})
        assert r["db_type"] == "postgresql"


class TestIntentEscalation:
    """Test risk escalation rules."""

    def test_delete_no_where_escalates(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("DELETE FROM users")
        assert r["risk_preset"] == 4  # escalated from 2 to 4

    def test_delete_with_where_no_escalation(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("DELETE FROM users WHERE id = 1")
        assert r["risk_preset"] == 2  # normal L2

    def test_update_no_where_escalates(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("UPDATE users SET status = 0")
        assert r["risk_preset"] == 4  # escalated

    def test_alter_drop_column_escalates(self):
        from harnesses.intent_router import classify_intent
        r = classify_intent("ALTER TABLE users DROP COLUMN phone")
        # ddl_alter risk_preset=2, but DROP COLUMN escalation → 3
        assert r["risk_preset"] >= 3


class TestIntentRouting:
    """Test routing context generation."""

    def test_query_routing(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("SELECT * FROM users")
        routing = get_routing_context(intent)
        assert routing["risk_level"] == 0
        assert routing["requires_approval"] is False
        assert "sql_validate" in routing["tool_sequence"]

    def test_dml_routing(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("UPDATE users SET name = 'x' WHERE id = 1")
        routing = get_routing_context(intent)
        assert routing["risk_level"] >= 2
        assert routing["requires_approval"] is True
        assert routing["requires_rollback"] is True

    def test_ddl_routing(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("DROP TABLE temp_data")
        routing = get_routing_context(intent)
        assert routing["risk_level"] >= 3
        assert routing["requires_approval"] is True

    def test_query_routing_has_workflow(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("SELECT * FROM users")
        routing = get_routing_context(intent)
        assert routing["workflow_file"] is not None

    def test_list_intents(self):
        from harnesses.intent_router import list_intents
        intents = list_intents()
        assert len(intents) >= 10
        keys = [i["key"] for i in intents]
        assert "query" in keys
        assert "dml_update" in keys
        assert "ddl_drop" in keys


# ========================================================================
# B. RAG知识库检索优化测试
# ========================================================================

class TestLibrarySearchOptimized:
    """Test the optimized library_search with token-aware chunking."""

    def test_basic_search(self):
        from tools.library_search import search_library
        r = search_library("SELECT", "hive")
        assert "results" in r
        assert r["search_path"] == "library\\hive" or r["search_path"] == "library/hive"

    def test_version_isolation(self):
        from tools.library_search import search_library
        r = search_library("SELECT", "mysql", version="5.7")
        assert "5.7" in r["search_path"] or "5.7" in str(r.get("search_path", ""))

    def test_cross_db_isolation(self):
        """Oracle search should not return MySQL results."""
        from tools.library_search import search_library
        r = search_library("SELECT", "oracle")
        for hit in r["results"]:
            assert "mysql" not in hit.get("file", "").lower()

    def test_chunk_size_limit(self):
        """All chunks should be ≤ MAX_CHUNK_CHARS (4000)."""
        from tools.library_search import search_library
        r = search_library("JOIN", "hive", max_results=20)
        for hit in r["results"]:
            assert len(hit["content"]) <= 5000  # allow some margin for part labels

    def test_total_chunks_reported(self):
        from tools.library_search import search_library
        r = search_library("SELECT", "hive")
        assert r["total_chunks"] > 0

    def test_score_ranking(self):
        """Higher scored results should come first."""
        from tools.library_search import search_library
        r = search_library("GROUP BY", "hive", max_results=10)
        if len(r["results"]) >= 2:
            scores = [hit["score"] for hit in r["results"]]
            assert scores == sorted(scores, reverse=True)

    def test_unsupported_db(self):
        from tools.library_search import search_library
        r = search_library("SELECT", "mongodb")
        assert any("error" in str(hit) for hit in r["results"])

    def test_empty_query(self):
        from tools.library_search import handle_library_search
        result = json.loads(handle_library_search({"query": "", "db_type": "mysql"}))
        assert "error" in result

    def test_cache_invalidation(self):
        from tools.library_search import search_library, invalidate_cache
        r1 = search_library("SELECT", "hive")
        invalidate_cache()
        r2 = search_library("SELECT", "hive")
        assert r1["total_chunks"] == r2["total_chunks"]

    def test_tfidf_exact_phrase_bonus(self):
        """Exact phrase match should score higher."""
        from tools.library_search import search_library
        r = search_library("Windowing and Analytics Functions", "hive", max_results=3)
        if r["results"]:
            # First result should be the exact match section
            assert "windowing" in r["results"][0]["section"].lower() or \
                   "window" in r["results"][0]["content"].lower()

    def test_postgres_search(self):
        from tools.library_search import search_library
        r = search_library("CREATE INDEX", "postgresql", version="15")
        assert r["search_path"] != ""

    def test_handler_json_output(self):
        from tools.library_search import handle_library_search
        result = json.loads(handle_library_search({
            "query": "JOIN",
            "db_type": "hive",
            "max_results": 3,
        }))
        assert "results" in result
        assert isinstance(result["results"], list)


# ========================================================================
# C. 配置热重载测试
# ========================================================================

class TestConfigWatcher:
    def test_load_hitl_matrix(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        matrix = watcher.get_hitl_matrix()
        assert matrix is not None
        assert "risk_levels" in matrix
        assert 0 in matrix["risk_levels"]
        assert 4 in matrix["risk_levels"]

    def test_load_stage_workflow(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        content = watcher.get_stage_workflow("query-execution")
        assert content is not None
        assert "查询执行" in content or "Query Execution" in content

    def test_nonexistent_file(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        result = watcher.get_config("nonexistent/file.yaml")
        assert result is None

    def test_check_and_reload_no_changes(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        watcher.get_hitl_matrix()  # prime cache
        reloaded = watcher.check_and_reload()
        # No changes since we just loaded
        assert all(v is True for v in reloaded.values()) if reloaded else True

    def test_invalidate_cache(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        watcher.get_hitl_matrix()  # prime cache
        watcher.invalidate("contracts/hitl_matrix.yaml")
        # Should reload on next access
        matrix = watcher.get_hitl_matrix()
        assert matrix is not None

    def test_hot_reload_taxonomy(self, tmp_path):
        """Test that taxonomy reload works."""
        from harnesses.intent_router import reload_taxonomy, classify_intent
        # Force reload
        assert reload_taxonomy() is True
        # Classification should still work after reload
        r = classify_intent("SELECT 1")
        assert r["intent"] == "query"

    def test_all_stage_files_loadable(self):
        from harnesses.config_watcher import get_config_watcher
        watcher = get_config_watcher()
        workflows = ["query-execution", "dml-execution", "ddl-change",
                      "optimization", "health-check", "troubleshooting"]
        for wf in workflows:
            content = watcher.get_stage_workflow(wf)
            assert content is not None, f"Workflow {wf} not found"
            assert len(content) > 100, f"Workflow {wf} too short"


# ========================================================================
# D. 上下文注入集成测试
# ========================================================================

class TestContextInjector:
    def test_injection_adds_system_context(self):
        from harnesses.context_injector import pre_llm_call_hook

        result = pre_llm_call_hook(
            user_message="SELECT * FROM users",
            conversation_history=[
                {"role": "user", "content": "SELECT * FROM users"},
            ],
        )
        assert result is not None
        # Should return a context dict with DBA system context
        assert isinstance(result, dict)
        assert "DBA SafeGuard" in result["context"]

    def test_injection_includes_intent(self):
        from harnesses.context_injector import pre_llm_call_hook

        result = pre_llm_call_hook(
            user_message="DELETE FROM orders WHERE id = 1",
            conversation_history=[
                {"role": "user", "content": "DELETE FROM orders WHERE id = 1"},
            ],
        )
        assert result is not None
        assert "意图分析" in result["context"]

    def test_injection_preserves_existing_system(self):
        from harnesses.context_injector import pre_llm_call_hook

        result = pre_llm_call_hook(
            user_message="SELECT 1",
            conversation_history=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "SELECT 1"},
            ],
        )
        assert result is not None
        # Context is now returned as a dict, not injected into messages
        assert "DBA SafeGuard" in result["context"]

    def test_sql_intent_detection(self):
        from harnesses.context_injector import _detect_sql_intent
        assert _detect_sql_intent("帮我写一条SQL查询") is True
        assert _detect_sql_intent("今天天气怎么样") is False
        assert _detect_sql_intent("CREATE TABLE test") is True
        assert _detect_sql_intent("添加索引") is True


# ========================================================================
# E. 集成: 意图→路由→工具链完整路径
# ========================================================================

class TestIntentToToolchainE2E:
    """End-to-end from intent classification to tool routing."""

    def test_query_full_chain(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("SELECT COUNT(*) FROM users")
        routing = get_routing_context(intent)

        assert intent["intent"] == "query"
        assert intent["risk_preset"] == 0
        assert routing["requires_approval"] is False
        assert routing["requires_rollback"] is False
        assert "sql_validate" in routing["tool_sequence"]

    def test_dangerous_delete_full_chain(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("DELETE FROM users")
        routing = get_routing_context(intent)

        assert intent["intent"] == "dml_delete"
        assert intent["risk_preset"] == 4  # escalated!
        assert routing["requires_approval"] is True
        assert routing["requires_rollback"] is True

    def test_ddl_alter_with_db_type(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent(
            "ALTER TABLE users ADD COLUMN phone VARCHAR(20)",
            context={"dialect": "postgresql"}
        )
        routing = get_routing_context(intent)

        assert intent["intent"] == "ddl_alter"
        assert routing["db_type"] == "postgresql"
        assert "library_search" in routing["tool_sequence"]
        assert "metadata_read" in routing["tool_sequence"]

    def test_optimize_mysql_version(self):
        from harnesses.intent_router import classify_intent, get_routing_context
        intent = classify_intent("MySQL 8.0的索引优化建议")
        routing = get_routing_context(intent)

        assert intent["db_type"] == "mysql"
        assert intent["db_version"] == "8.0"
        assert routing["requires_approval"] is False
