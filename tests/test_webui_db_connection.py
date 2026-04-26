import builtins
import sys
import types


class _FakeConnection:
    def __init__(self):
        self.executed = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, statement):
        self.executed.append(str(statement))


class _FakeEngine:
    def __init__(self):
        self.connection = _FakeConnection()
        self.disposed = False

    def connect(self):
        return self.connection

    def dispose(self):
        self.disposed = True


class _FakeConnectionManager:
    def load_config(self):
        return None

    def _get_instance_config(self, instance_name):
        return None

    def close_all(self):
        return None


def test_bridge_test_connection_reports_missing_sqlalchemy(monkeypatch):
    from webui import dba_bridge

    original_import = builtins.__import__

    def _raising_import(name, globals=None, locals=None, fromlist=(), level=0):
        if name == "sqlalchemy":
            raise ModuleNotFoundError("No module named 'sqlalchemy'", name="sqlalchemy")
        return original_import(name, globals, locals, fromlist, level)

    monkeypatch.setattr(dba_bridge, "_HAS_CONNECTOR", True)
    monkeypatch.setattr(dba_bridge, "ConnectionManager", _FakeConnectionManager, raising=False)
    monkeypatch.setattr(builtins, "__import__", _raising_import)

    result = dba_bridge.bridge_test_connection(
        "pg_test",
        direct_creds={
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "demo",
            "readonly_user": "demo",
            "readonly_pass": "secret",
        },
    )

    assert result["success"] is False
    assert "sqlalchemy" in result["error"]
    assert "pip install -e ." in result["error"]


def test_bridge_test_connection_reports_optional_sqlserver_driver(monkeypatch):
    from webui import dba_bridge

    fake_sqlalchemy = types.SimpleNamespace(
        create_engine=lambda url: (_ for _ in ()).throw(ModuleNotFoundError("No module named 'pyodbc'", name="pyodbc")),
        text=lambda sql: sql,
    )

    monkeypatch.setattr(dba_bridge, "_HAS_CONNECTOR", True)
    monkeypatch.setattr(dba_bridge, "ConnectionManager", _FakeConnectionManager, raising=False)
    monkeypatch.setitem(sys.modules, "sqlalchemy", fake_sqlalchemy)

    result = dba_bridge.bridge_test_connection(
        "sqlserver_test",
        direct_creds={
            "type": "sqlserver",
            "host": "localhost",
            "port": 1433,
            "database": "demo",
            "readonly_user": "sa",
            "readonly_pass": "secret",
        },
    )

    assert result["success"] is False
    assert ".[dba-sqlserver]" in result["error"]
    assert "ODBC" in result["error"]


def test_bridge_test_connection_succeeds_with_core_dependencies(monkeypatch):
    from webui import dba_bridge

    engine = _FakeEngine()
    fake_sqlalchemy = types.SimpleNamespace(create_engine=lambda url: engine, text=lambda sql: sql)

    monkeypatch.setattr(dba_bridge, "_HAS_CONNECTOR", True)
    monkeypatch.setattr(dba_bridge, "ConnectionManager", _FakeConnectionManager, raising=False)
    monkeypatch.setitem(sys.modules, "sqlalchemy", fake_sqlalchemy)

    result = dba_bridge.bridge_test_connection(
        "pg_test",
        direct_creds={
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "database": "demo",
            "readonly_user": "demo",
            "readonly_pass": "secret",
        },
    )

    assert result == {"success": True, "instance": "pg_test"}
    assert engine.connection.executed == ["SELECT 1"]
    assert engine.disposed is True