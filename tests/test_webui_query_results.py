from pathlib import Path
import importlib
import importlib.util
import types
import sys


project_root = Path(__file__).resolve().parent.parent
webui_root = project_root / "webui"
plugin_root = Path(__file__).resolve().parent.parent / ".hermes" / "plugins" / "dba-safeguard"
plugin_tools_root = plugin_root / "tools"
if str(webui_root) not in sys.path:
    sys.path.insert(0, str(webui_root))
if str(plugin_root) not in sys.path:
    sys.path.insert(0, str(plugin_root))


def _reset_modules(prefixes):
    for name in list(sys.modules):
        if name == "tools" or any(name.startswith(prefix) for prefix in prefixes):
            sys.modules.pop(name, None)


def setup_module(module):
    module._ORIGINAL_TOOL_MODULES = {
        name: loaded_module
        for name, loaded_module in sys.modules.items()
        if name == "tools" or name.startswith("tools.")
    }


def teardown_module(module):
    _reset_modules(("tools.",))
    sys.modules.update(getattr(module, "_ORIGINAL_TOOL_MODULES", {}))


def _import_plugin_module(module_name):
    sys.modules.pop("tools", None)
    sys.modules.pop(module_name, None)
    tools_spec = importlib.util.spec_from_file_location(
        "tools",
        plugin_tools_root / "__init__.py",
        submodule_search_locations=[str(plugin_tools_root)],
    )
    tools_module = importlib.util.module_from_spec(tools_spec)
    sys.modules["tools"] = tools_module
    assert tools_spec.loader is not None
    tools_spec.loader.exec_module(tools_module)
    return importlib.import_module(module_name)


class _FakeResult:
    def __init__(self, rows, columns):
        self._rows = list(rows)
        self._columns = list(columns)
        self.returns_rows = True
        self.closed = False

    def keys(self):
        return self._columns

    def fetchmany(self, size):
        if size <= 0:
            return []
        batch = self._rows[:size]
        self._rows = self._rows[size:]
        return batch

    def close(self):
        self.closed = True


class _FakeNoRowsResult:
    returns_rows = False
    rowcount = 0

    def close(self):
        return None


class _FakeConnection:
    def __init__(self, result):
        self._result = result
        self.closed = False
        self.executed_sql = []

    def execute(self, statement):
        sql = str(statement)
        self.executed_sql.append(sql)
        if sql.strip().upper().startswith("SET "):
            return _FakeNoRowsResult()
        return self._result

    def close(self):
        self.closed = True


class _FakeEngine:
    def __init__(self, connection):
        self._connection = connection

    def connect(self):
        return self._connection


class _FakeManager:
    def __init__(self, connection):
        self._connection = connection

    def get_readonly_engine(self, instance_name):
        return _FakeEngine(self._connection)

    def get_admin_engine(self, instance_name):
        return _FakeEngine(self._connection)


def _install_fake_sqlalchemy(monkeypatch):
    fake_sqlalchemy = types.SimpleNamespace(text=lambda sql: sql)
    monkeypatch.setitem(sys.modules, "sqlalchemy", fake_sqlalchemy)


def test_execute_sql_limits_initial_select_rows_and_streams_next_page(monkeypatch):
    safe_executor = _import_plugin_module("tools.safe_executor")
    _install_fake_sqlalchemy(monkeypatch)

    rows = [(index, f"row-{index}") for index in range(1, 206)]
    result_proxy = _FakeResult(rows, ["id", "name"])
    connection = _FakeConnection(result_proxy)
    manager = _FakeManager(connection)

    monkeypatch.setattr("tools.db_connector.get_connection_manager", lambda: manager)
    monkeypatch.setattr(safe_executor, "_audit_execution", lambda *args, **kwargs: None)

    with safe_executor._RESULT_CACHE_LOCK:
        safe_executor._RESULT_CACHE.clear()

    result = safe_executor.execute_sql(
        "SELECT id, name FROM demo_table",
        "pg_test",
        "postgresql",
        risk_level=0,
        task_id="task-select-preview",
        session_id="conv-1",
        user_id="tester",
    )

    preview = result["data"]
    assert result["success"] is True
    assert len(preview["rows"]) == 100
    assert preview["loaded_count"] == 100
    assert preview["has_more"] is True
    assert preview["result_set_id"] == "task-select-preview"
    assert connection.closed is False

    safe_executor.bind_result_cache_owner(
        "task-select-preview",
        conversation_id="conv-1",
        user_id="tester",
    )
    next_page = safe_executor.fetch_result_page(
        "task-select-preview",
        offset=100,
        limit=100,
        conversation_id="conv-1",
        user_id="tester",
    )
    final_page = safe_executor.fetch_result_page(
        "task-select-preview",
        offset=200,
        limit=100,
        conversation_id="conv-1",
        user_id="tester",
    )

    assert len(next_page["rows"]) == 100
    assert next_page["has_more"] is True
    assert len(final_page["rows"]) == 5
    assert final_page["has_more"] is False
    assert final_page["total_rows"] == 205
    assert connection.closed is True
    assert result_proxy.closed is True


def test_fetch_result_page_rejects_wrong_conversation(monkeypatch):
    safe_executor = _import_plugin_module("tools.safe_executor")
    _install_fake_sqlalchemy(monkeypatch)

    rows = [(index,) for index in range(1, 105)]
    result_proxy = _FakeResult(rows, ["id"])
    connection = _FakeConnection(result_proxy)
    manager = _FakeManager(connection)

    monkeypatch.setattr("tools.db_connector.get_connection_manager", lambda: manager)
    monkeypatch.setattr(safe_executor, "_audit_execution", lambda *args, **kwargs: None)

    with safe_executor._RESULT_CACHE_LOCK:
        safe_executor._RESULT_CACHE.clear()

    result = safe_executor.execute_sql(
        "SELECT id FROM demo_table",
        "pg_test",
        "postgresql",
        risk_level=0,
        task_id="task-owner-check",
        session_id="conv-allowed",
        user_id="tester",
    )
    assert result["data"]["result_set_id"] == "task-owner-check"

    safe_executor.bind_result_cache_owner(
        "task-owner-check",
        conversation_id="conv-allowed",
        user_id="tester",
    )
    denied = safe_executor.fetch_result_page(
        "task-owner-check",
        offset=100,
        limit=100,
        conversation_id="conv-denied",
        user_id="tester",
    )

    assert denied["error"] == "无权访问该结果集"


def test_build_task_snapshot_strips_live_result_set_id():
    from webui.dba_routes import _build_task_snapshot

    task = {
        "task_id": "task-1",
        "execution_result": {
            "success": True,
            "data": {
                "columns": ["id"],
                "rows": [[1]],
                "result_set_id": "task-1",
                "has_more": True,
            },
        },
    }

    snapshot = _build_task_snapshot(task)

    assert snapshot["execution_result"]["data"].get("result_set_id") is None
    assert task["execution_result"]["data"]["result_set_id"] == "task-1"


def test_pipeline_chat_summary_uses_loaded_rows_for_select(monkeypatch):
    from engine import dba_loop
    from webui import dba_bridge

    class _FakeTask:
        def __init__(self):
            self.rollback_sql = ""
            self.execution_result = {
                "success": True,
                "rows_affected": 0,
                "data": {
                    "columns": ["id"],
                    "rows": [[1]],
                    "loaded_count": 100,
                    "has_more": True,
                },
            }
            self.intent = {"intent": "query", "label": "查询"}
            self.risk_level = 0
            self.stage_results = []

        def to_dict(self):
            return {
                "task_id": "task-summary",
                "risk_level": 0,
                "stages": [],
                "sql": "SELECT * FROM demo_table",
            }

    monkeypatch.setattr(dba_loop, "run_pipeline", lambda **kwargs: _FakeTask())

    result = dba_bridge._run_pipeline_chat(
        sql_text="SELECT * FROM demo_table",
        source_message="查一下 demo_table",
        instance_name="pg_test",
        dialect="postgresql",
        user_id="tester",
        session_id="conv-1",
        intent_info={"intent": "query", "label": "查询"},
    )

    assert "已加载 100 行" in result["response"]
    assert "影响 0 行" not in result["response"]