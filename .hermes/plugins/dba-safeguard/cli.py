"""DBA CLI subcommand — `hermes dba` 子命令。

用法:
  hermes dba status        — 查看DBA SafeGuard状态
  hermes dba audit         — 查询审计日志
  hermes dba instances     — 列出配置的数据库实例
  hermes dba test-connect  — 测试数据库连接
"""

from __future__ import annotations

import json
import sys


def setup_dba_parser(subparsers) -> None:
    """Set up the 'dba' CLI subcommand parser."""
    dba_parser = subparsers.add_parser("dba", help="DBA SafeGuard management commands")
    dba_sub = dba_parser.add_subparsers(dest="dba_command")

    # dba status
    dba_sub.add_parser("status", help="Show DBA SafeGuard status")

    # dba instances
    dba_sub.add_parser("instances", help="List configured database instances")

    # dba audit
    audit_parser = dba_sub.add_parser("audit", help="Query audit logs")
    audit_parser.add_argument("--limit", type=int, default=20, help="Number of records")
    audit_parser.add_argument("--risk-level", type=int, help="Filter by risk level (0-4)")
    audit_parser.add_argument("--instance", type=str, help="Filter by instance name")

    # dba test-connect
    test_parser = dba_sub.add_parser("test-connect", help="Test database connection")
    test_parser.add_argument("instance_name", help="Instance name to test")


def handle_dba_command(args) -> None:
    """Handle the 'dba' CLI subcommand."""
    cmd = getattr(args, "dba_command", None)

    if cmd == "status":
        _cmd_status()
    elif cmd == "instances":
        _cmd_instances()
    elif cmd == "audit":
        _cmd_audit(args)
    elif cmd == "test-connect":
        _cmd_test_connect(args)
    else:
        print("Usage: hermes dba {status|instances|audit|test-connect}")
        print("Run 'hermes dba <command> --help' for more information")


def _cmd_status():
    """Show DBA SafeGuard plugin status."""
    import os
    enabled = os.environ.get("DBA_SAFEGUARD_ENABLED", "false")
    project_plugins = os.environ.get("HERMES_ENABLE_PROJECT_PLUGINS", "false")

    print("=== DBA SafeGuard Status ===")
    print(f"  DBA_SAFEGUARD_ENABLED: {enabled}")
    print(f"  HERMES_ENABLE_PROJECT_PLUGINS: {project_plugins}")

    try:
        from .tools.db_connector import get_connection_manager
        mgr = get_connection_manager()
        mgr.load_config()
        instances = mgr.list_instances()
        print(f"  Configured instances: {len(instances)}")
    except Exception as e:
        print(f"  Config load error: {e}")

    try:
        from .tools.audit_logger import _get_audit_db
        db = _get_audit_db()
        count = db.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
        print(f"  Audit log entries: {count}")
    except Exception as e:
        print(f"  Audit DB error: {e}")


def _cmd_instances():
    """List configured database instances."""
    try:
        from .tools.db_connector import get_connection_manager
        mgr = get_connection_manager()
        mgr.load_config()
        instances = mgr.list_instances()
        if not instances:
            print("No database instances configured.")
            print("Configure instances in .hermes/plugins/dba-safeguard/config/dba_config.yaml")
            return
        print(f"{'Name':<20} {'Type':<12} {'Host':<30}")
        print("-" * 62)
        for inst in instances:
            print(f"{inst['name']:<20} {inst['type']:<12} {inst['host']:<30}")
    except Exception as e:
        print(f"Error: {e}")


def _cmd_audit(args):
    """Query audit logs."""
    try:
        from .tools.audit_logger import query_audit_logs
        logs = query_audit_logs(
            limit=args.limit,
            risk_level=args.risk_level,
            instance_name=args.instance or "",
        )
        if not logs:
            print("No audit logs found.")
            return
        for log in logs:
            ts = log.get("timestamp", 0)
            op = log.get("operation_type", "")
            risk = log.get("risk_level", 0)
            inst = log.get("instance_name", "")
            sql = (log.get("original_sql") or "")[:60]
            print(f"  [{ts:.0f}] L{risk} {op:<16} {inst:<16} {sql}")
    except Exception as e:
        print(f"Error: {e}")


def _cmd_test_connect(args):
    """Test database connection."""
    try:
        from .tools.db_connector import handle_db_connect
        result = handle_db_connect({"instance_name": args.instance_name})
        data = json.loads(result)
        if "error" in data:
            print(f"FAILED: {data['error']}")
        else:
            print(f"OK: {data.get('result', 'connected')}")
    except Exception as e:
        print(f"Error: {e}")
