"""风险拦截器 — pre_tool_call 钩子，拦截并分级所有SQL执行请求。

核心逻辑:
  1. pre_tool_call 触发时检查是否是 db_execute 调用
  2. 自动调用 sql_validate 做L0-L4分级
  3. 根据 hitl_matrix.yaml 决定是否需要人工审批
  4. L0: 自动放行
  5. L1: 通知+自动放行（或可配HITL）
  6. L2: 必须人工确认
  7. L3-L4: 强制阻断，需要高权限审批
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

logger = logging.getLogger("dba_safeguard.harnesses.risk_interceptor")


def load_hitl_matrix() -> Dict[str, Any]:
    """Load the HITL decision matrix from config."""
    matrix_path = Path(__file__).parent / "contracts" / "hitl_matrix.yaml"
    if not matrix_path.exists():
        logger.warning("HITL matrix not found at %s, using defaults", matrix_path)
        return _default_matrix()
    try:
        import yaml
        with open(matrix_path) as f:
            return yaml.safe_load(f) or _default_matrix()
    except Exception as e:
        logger.error("Failed to load HITL matrix: %s", e)
        return _default_matrix()


def _default_matrix() -> Dict[str, Any]:
    """Default HITL decision matrix."""
    return {
        "risk_levels": {
            0: {"action": "auto_approve", "label": "L0_READONLY", "require_approval": False},
            1: {"action": "notify_approve", "label": "L1_LOW_DML", "require_approval": False},
            2: {"action": "human_confirm", "label": "L2_MEDIUM_BATCH", "require_approval": True},
            3: {"action": "force_block", "label": "L3_HIGH_DESTRUCTIVE", "require_approval": True, "require_admin": True},
            4: {"action": "force_block", "label": "L4_CATASTROPHIC", "require_approval": True, "require_admin": True},
        },
    }


async def pre_tool_call_hook(
    tool_name: str,
    tool_args: Dict[str, Any],
    context: Optional[Any] = None,
    **kwargs,
) -> Optional[Dict[str, Any]]:
    """Hermes pre_tool_call hook for risk interception.

    Called before any tool execution. For db_execute:
      - Validate SQL
      - Determine risk level
      - Apply HITL matrix rules
      - Block, approve, or request human confirmation

    Returns:
        None to proceed normally, or a dict with {"block": True, "message": str}
        to prevent tool execution.
    """
    # Only intercept db_execute tool
    if tool_name != "db_execute":
        return None

    sql = tool_args.get("sql", "")
    dialect = tool_args.get("dialect", "mysql")
    provided_risk = tool_args.get("risk_level")

    if not sql.strip():
        return {"block": True, "message": "SQL语句为空，拒绝执行"}

    # Step 1: Validate SQL if not already validated
    try:
        from ..tools.sql_ast_validator import validate_sql
    except ImportError:
        from tools.sql_ast_validator import validate_sql

    validation = validate_sql(sql, dialect)

    if not validation["valid"]:
        errors = "; ".join(e["message"] for e in validation["errors"])
        return {
            "block": True,
            "message": f"SQL校验失败: {errors}\n建议: {'; '.join(validation.get('suggestions', []))}",
        }

    risk_level = validation["risk_level"]
    risk_label = validation["risk_label"]

    # Override with provided risk level if higher
    if provided_risk is not None and provided_risk > risk_level:
        risk_level = provided_risk

    # Step 2: Apply HITL matrix
    matrix = load_hitl_matrix()
    levels = matrix.get("risk_levels", {})
    level_config = levels.get(risk_level, levels.get(4))  # Default to L4 if unknown

    action = level_config.get("action", "force_block")
    require_approval = level_config.get("require_approval", True)

    # Step 3: Decision
    if action == "auto_approve":
        logger.info("[L%d] Auto-approving: %s", risk_level, sql[:80])
        # Set approved flag
        tool_args["risk_level"] = risk_level
        tool_args["approved"] = True
        return None  # Proceed

    if action == "notify_approve":
        logger.info("[L%d] Notify-approving: %s", risk_level, sql[:80])
        tool_args["risk_level"] = risk_level
        tool_args["approved"] = True
        return None  # Proceed (notification logged)

    if action == "human_confirm":
        # Check if already approved
        if tool_args.get("approved"):
            logger.info("[L%d] Already approved: %s", risk_level, sql[:80])
            tool_args["risk_level"] = risk_level
            return None

        return {
            "block": True,
            "message": (
                f"⚠️ [{risk_label}] 该操作需要人工确认\n"
                f"SQL: {sql[:200]}\n"
                f"影响表: {', '.join(validation.get('tables', []))}\n"
                f"风险: {'; '.join(validation.get('warnings', []))}\n"
                f"请确认后使用 approved=true 重新执行"
            ),
        }

    if action == "force_block":
        return {
            "block": True,
            "message": (
                f"🚫 [{risk_label}] 该操作已被强制阻断\n"
                f"SQL: {sql[:200]}\n"
                f"影响表: {', '.join(validation.get('tables', []))}\n"
                f"风险: {'; '.join(validation.get('warnings', []))}\n"
                f"L3/L4操作需要管理员权限审批。"
            ),
        }

    # Unknown action — block by default
    return {"block": True, "message": f"未知风险等级动作: {action}，默认阻断"}
