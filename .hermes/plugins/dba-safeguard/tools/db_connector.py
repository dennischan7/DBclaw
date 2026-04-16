"""数据库安全连接适配器。

基于SQLAlchemy 2.x封装，实现读写分离的数据库连接池管理。
支持Oracle、MySQL、PostgreSQL、SQL Server四种数据库。

安全约束:
  - 默认仅实例化只读连接
  - 管理员连接需审批通过后按需创建
  - 密码通过环境变量/.env管理，禁止硬编码
  - 连接超时默认30s
  - 日志中禁止输出敏感信息
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("dba_safeguard.tools.db_connector")

# ---------------------------------------------------------------------------
# Connection Manager (singleton per plugin lifecycle)
# ---------------------------------------------------------------------------

class ConnectionManager:
    """Manage database connections with read/write separation."""

    def __init__(self):
        self._readonly_engines: Dict[str, Any] = {}
        self._admin_engines: Dict[str, Any] = {}
        self._config: Dict[str, Any] = {}

    def load_config(self, config_path: Optional[Path] = None) -> None:
        """Load database instance configurations from dba_config.yaml."""
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config" / "dba_config.yaml"
        if not config_path.exists():
            logger.warning("DBA config not found at %s", config_path)
            return
        try:
            import yaml
            with open(config_path) as f:
                self._config = yaml.safe_load(f) or {}
        except Exception as e:
            logger.error("Failed to load DBA config: %s", e)

    def get_readonly_engine(self, instance_name: str):
        """Get or create a read-only connection engine for the named instance."""
        if instance_name in self._readonly_engines:
            return self._readonly_engines[instance_name]

        instance_cfg = self._get_instance_config(instance_name)
        if not instance_cfg:
            raise ValueError(f"Unknown database instance: {instance_name}")

        from sqlalchemy import create_engine
        url = self._build_connection_url(instance_cfg, readonly=True)
        engine = create_engine(
            url,
            pool_size=5,
            pool_recycle=3600,
            connect_args=self._get_connect_args(instance_cfg, readonly=True),
            echo=False,
        )
        self._readonly_engines[instance_name] = engine
        logger.info("Created readonly engine for instance: %s", instance_name)
        return engine

    def get_admin_engine(self, instance_name: str):
        """Get or create an admin (read-write) connection engine.

        This should ONLY be called after approval for write operations.
        """
        if instance_name in self._admin_engines:
            return self._admin_engines[instance_name]

        instance_cfg = self._get_instance_config(instance_name)
        if not instance_cfg:
            raise ValueError(f"Unknown database instance: {instance_name}")

        from sqlalchemy import create_engine
        url = self._build_connection_url(instance_cfg, readonly=False)
        engine = create_engine(
            url,
            pool_size=2,
            pool_recycle=3600,
            connect_args=self._get_connect_args(instance_cfg, readonly=False),
            echo=False,
        )
        self._admin_engines[instance_name] = engine
        logger.info("Created admin engine for instance: %s", instance_name)
        return engine

    def close_all(self) -> None:
        """Dispose all connection engines."""
        for name, engine in {**self._readonly_engines, **self._admin_engines}.items():
            try:
                engine.dispose()
                logger.debug("Disposed engine: %s", name)
            except Exception as e:
                logger.warning("Error disposing engine %s: %s", name, e)
        self._readonly_engines.clear()
        self._admin_engines.clear()

    def list_instances(self) -> list:
        """Return list of configured database instances."""
        instances = self._config.get("databases", {}).get("instances", [])
        return [
            {"name": inst.get("name"), "type": inst.get("type"), "host": inst.get("host")}
            for inst in instances
        ]

    def _get_instance_config(self, name: str) -> Optional[Dict]:
        instances = self._config.get("databases", {}).get("instances", [])
        for inst in instances:
            if inst.get("name") == name:
                return inst
        return None

    def _build_connection_url(self, cfg: Dict, readonly: bool) -> str:
        """Build SQLAlchemy connection URL from instance config."""
        db_type = cfg.get("type", "").lower()
        host = cfg.get("host", "localhost")
        port = cfg.get("port")
        database = cfg.get("database", "")

        # Use readonly or admin credentials from env vars
        user_env = cfg.get("readonly_user_env" if readonly else "admin_user_env", "")
        pass_env = cfg.get("readonly_pass_env" if readonly else "admin_pass_env", "")
        user = os.environ.get(user_env, cfg.get("readonly_user", ""))
        password = os.environ.get(pass_env, "")

        dialect_map = {
            "mysql": f"mysql+pymysql://{user}:{password}@{host}:{port or 3306}/{database}",
            "postgresql": f"postgresql+psycopg2://{user}:{password}@{host}:{port or 5432}/{database}",
            "oracle": f"oracle+cx_oracle://{user}:{password}@{host}:{port or 1521}/{database}",
            "sqlserver": f"mssql+pyodbc://{user}:{password}@{host}:{port or 1433}/{database}?driver=ODBC+Driver+17+for+SQL+Server",
        }
        url = dialect_map.get(db_type)
        if not url:
            raise ValueError(f"Unsupported database type: {db_type}")
        return url

    def _get_connect_args(self, cfg: Dict, readonly: bool) -> dict:
        """Get database-specific connection arguments."""
        timeout = cfg.get("timeout", 30)
        db_type = cfg.get("type", "").lower()
        args: dict = {}
        if db_type == "mysql":
            args["connect_timeout"] = timeout
            if readonly:
                args["init_command"] = "SET SESSION TRANSACTION READ ONLY"
        elif db_type == "postgresql":
            args["connect_timeout"] = timeout
            if readonly:
                args["options"] = "-c default_transaction_read_only=on"
        return args


# Singleton
_connection_manager = ConnectionManager()


def get_connection_manager() -> ConnectionManager:
    return _connection_manager


# ---------------------------------------------------------------------------
# Tool Handlers
# ---------------------------------------------------------------------------

def handle_db_connect(args: dict, task_id: str = "", **kwargs) -> str:
    """Connect to a database instance."""
    instance = args.get("instance_name", "")
    if not instance:
        return json.dumps({"error": "instance_name is required"})
    try:
        mgr = get_connection_manager()
        mgr.load_config()
        engine = mgr.get_readonly_engine(instance)
        # Test connection
        with engine.connect() as conn:
            conn.execute(__import__("sqlalchemy").text("SELECT 1"))
        return json.dumps({"result": f"Successfully connected to '{instance}' (readonly)"})
    except Exception as e:
        return json.dumps({"error": f"Connection failed: {e}"})


def handle_db_disconnect(args: dict, task_id: str = "", **kwargs) -> str:
    """Disconnect from all database instances."""
    try:
        get_connection_manager().close_all()
        return json.dumps({"result": "All connections closed"})
    except Exception as e:
        return json.dumps({"error": str(e)})


# ---------------------------------------------------------------------------
# Tool Registration
# ---------------------------------------------------------------------------

DB_CONNECT_SCHEMA = {
    "name": "db_connect",
    "description": (
        "连接到指定的数据库实例（只读模式）。连接成功后即可使用其他DBA工具操作该实例。"
        "数据库实例需在dba_config.yaml中预先配置。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "instance_name": {
                "type": "string",
                "description": "要连接的数据库实例名称（在dba_config.yaml中定义）",
            },
        },
        "required": ["instance_name"],
    },
}

DB_DISCONNECT_SCHEMA = {
    "name": "db_disconnect",
    "description": "断开所有数据库连接，释放连接池资源。",
    "parameters": {
        "type": "object",
        "properties": {},
        "required": [],
    },
}


def register_tools(ctx) -> None:
    """Register database connection tools with Hermes."""
    ctx.register_tool(
        name="db_connect",
        toolset="dba-safeguard",
        schema=DB_CONNECT_SCHEMA["parameters"],
        handler=handle_db_connect,
        description=DB_CONNECT_SCHEMA["description"],
        emoji="🔌",
    )
    ctx.register_tool(
        name="db_disconnect",
        toolset="dba-safeguard",
        schema=DB_DISCONNECT_SCHEMA["parameters"],
        handler=handle_db_disconnect,
        description=DB_DISCONNECT_SCHEMA["description"],
        emoji="🔌",
    )
