"""会话生命周期钩子 — on_session_start / on_session_end。

on_session_start:
  - 初始化 ConnectionManager
  - 加载 DBA 配置
  - 初始化审计数据库

on_session_end:
  - 关闭所有数据库连接
  - 写入会话级审计摘要
"""

from __future__ import annotations

import logging
from typing import Any, Optional

logger = logging.getLogger("dba_safeguard.harnesses.session_hooks")


async def on_session_start_hook(
    context: Optional[Any] = None,
    **kwargs,
) -> None:
    """Initialize DBA SafeGuard resources at session start."""
    logger.info("DBA SafeGuard session starting...")

    try:
        # Load DB config
        from ..tools.db_connector import get_connection_manager
        mgr = get_connection_manager()
        mgr.load_config()
        logger.info("DBA config loaded, %d instances configured", len(mgr.list_instances()))
    except Exception as e:
        logger.warning("DBA config load failed (non-fatal): %s", e)

    try:
        # Initialize audit DB
        from ..tools.audit_logger import _get_audit_db
        _get_audit_db()
        logger.info("Audit database initialized")
    except Exception as e:
        logger.warning("Audit DB init failed (non-fatal): %s", e)


async def on_session_end_hook(
    context: Optional[Any] = None,
    **kwargs,
) -> None:
    """Clean up DBA SafeGuard resources at session end."""
    logger.info("DBA SafeGuard session ending...")

    try:
        from ..tools.db_connector import get_connection_manager
        get_connection_manager().close_all()
        logger.info("All database connections closed")
    except Exception as e:
        logger.warning("Connection cleanup failed: %s", e)
