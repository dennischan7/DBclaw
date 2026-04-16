"""DB-SafeGuard Enterprise — DBA垂直领域安全运维插件。

基于Hermes Agent Plugin系统实现，不修改Hermes核心源码。
通过register(ctx)注册工具、钩子、CLI命令，实现DBA专属能力。

Architecture:
  - tools/       → DBA工具（连接、校验、执行、审计等）
  - memory/      → DBAMemoryProvider（四层记忆体系）
  - harnesses/   → 规范引擎（风险矩阵、意图分类、工作流）
  - skills/      → DBA内置技能MD文件
  - config/      → DBA专属配置
"""

from __future__ import annotations

import logging
import os
from pathlib import Path

logger = logging.getLogger("dba_safeguard")

# Plugin root directory
PLUGIN_DIR = Path(__file__).parent


def register(ctx) -> None:
    """Register all DBA SafeGuard capabilities with Hermes.

    Called by Hermes plugin discovery system exactly once at startup.
    """
    if not _is_enabled():
        logger.info("DBA SafeGuard plugin is disabled (DBA_SAFEGUARD_ENABLED != true)")
        return

    logger.info("Registering DBA SafeGuard plugin v0.1.0")

    # --- Register Tools ---------------------------------------------------
    _register_tools(ctx)

    # --- Register Hooks ---------------------------------------------------
    _register_hooks(ctx)

    # --- Register CLI Commands --------------------------------------------
    _register_cli_commands(ctx)

    logger.info("DBA SafeGuard plugin registered successfully")


def _is_enabled() -> bool:
    """Check if plugin should activate."""
    val = os.environ.get("DBA_SAFEGUARD_ENABLED", "true").lower()
    return val in ("1", "true", "yes", "on")


# ---------------------------------------------------------------------------
# Tool Registration
# ---------------------------------------------------------------------------

def _register_tools(ctx) -> None:
    """Register all DBA tools."""
    from .tools.db_connector import register_tools as reg_connector
    from .tools.sql_ast_validator import register_tools as reg_validator
    from .tools.explain_analyzer import register_tools as reg_explain
    from .tools.metadata_reader import register_tools as reg_metadata
    from .tools.rollback_generator import register_tools as reg_rollback
    from .tools.safe_executor import register_tools as reg_executor
    from .tools.audit_logger import register_tools as reg_audit
    from .tools.library_search import register_tools as reg_library

    for reg_fn in (
        reg_connector,
        reg_validator,
        reg_explain,
        reg_metadata,
        reg_rollback,
        reg_executor,
        reg_audit,
        reg_library,
    ):
        reg_fn(ctx)


# ---------------------------------------------------------------------------
# Hook Registration
# ---------------------------------------------------------------------------

def _register_hooks(ctx) -> None:
    """Register lifecycle hooks for DBA risk interception and context injection."""
    from .harnesses.risk_interceptor import pre_tool_call_hook
    from .harnesses.context_injector import pre_llm_call_hook
    from .harnesses.audit_hook import post_tool_call_hook
    from .harnesses.session_hooks import on_session_start_hook, on_session_end_hook

    ctx.register_hook("pre_tool_call", pre_tool_call_hook)
    ctx.register_hook("post_tool_call", post_tool_call_hook)
    ctx.register_hook("pre_llm_call", pre_llm_call_hook)
    ctx.register_hook("on_session_start", on_session_start_hook)
    ctx.register_hook("on_session_end", on_session_end_hook)


# ---------------------------------------------------------------------------
# CLI Command Registration
# ---------------------------------------------------------------------------

def _register_cli_commands(ctx) -> None:
    """Register DBA-specific CLI subcommands."""
    from .cli import setup_dba_parser, handle_dba_command

    ctx.register_cli_command(
        name="dba",
        help="DB-SafeGuard DBA运维管理命令",
        setup_fn=setup_dba_parser,
        handler_fn=handle_dba_command,
        description="管理数据库连接、查看审计日志、切换安全模式等",
    )
