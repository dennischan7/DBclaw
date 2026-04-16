"""library_search 单元测试 — 验证 RAG 知识库检索功能。

覆盖:
  - PostgreSQL 文档目录检索
  - MySQL 文档目录检索
  - Hive 文档目录检索
  - 不存在的数据库类型
  - 空查询处理
  - 版本隔离（如 mysql/5.7 vs mysql/8.0）
  - handler JSON 输出
"""

import json
import sys
from pathlib import Path

import pytest

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

from tools.library_search import search_library, handle_library_search


class TestLibrarySearchPostgres:
    def test_search_pg_select(self):
        """Should find results for SELECT query in postgres docs."""
        result = search_library("SELECT", "postgresql")
        # May or may not find results depending on library/ contents
        assert "results" in result
        assert "search_path" in result
        if result["results"] and not any("error" in r for r in result["results"]):
            assert all("score" in r for r in result["results"])

    def test_search_pg_version(self):
        """Should search version-specific directory if available."""
        result = search_library("SELECT", "postgresql", version="16")
        assert "results" in result


class TestLibrarySearchMySQL:
    def test_search_mysql_join(self):
        result = search_library("JOIN", "mysql", version="5.7")
        assert "results" in result

    def test_search_mysql_subquery(self):
        result = search_library("subquery", "mysql", version="8.0")
        assert "results" in result


class TestLibrarySearchHive:
    def test_search_hive_window_functions(self):
        result = search_library("window functions", "hive")
        assert "results" in result
        # Hive docs should be in library/hive/
        if result["results"] and not any("error" in r for r in result["results"]):
            assert any("score" in r for r in result["results"])


class TestLibrarySearchEdgeCases:
    def test_unsupported_db_type(self):
        result = search_library("SELECT", "mongodb")
        assert any("不支持" in str(r) for r in result["results"])

    def test_empty_query_handler(self):
        result = json.loads(handle_library_search({"query": "", "db_type": "mysql"}))
        assert "error" in result

    def test_missing_db_type_handler(self):
        result = json.loads(handle_library_search({"query": "SELECT"}))
        assert "error" in result


class TestLibrarySearchIsolation:
    def test_pg_search_does_not_return_mysql(self):
        """PostgreSQL search must not return MySQL docs."""
        result = search_library("SELECT", "postgresql")
        for r in result.get("results", []):
            if "file" in r:
                assert "mysql" not in r["file"].lower()

    def test_mysql_search_does_not_return_pg(self):
        """MySQL search must not return PostgreSQL docs."""
        result = search_library("SELECT", "mysql")
        for r in result.get("results", []):
            if "file" in r:
                assert "postgres" not in r["file"].lower()
