"""DBA技能自优化器 — 技能使用后自动评估并生成优化建议。

核心流程:
  技能执行完成 → record_execution() → 累积足够数据 →
  evaluate_effectiveness() → 发现改进点 → generate_patch() →
  用户确认 → apply (confirm_patch) → 版本递增

约束:
  - 优化必须经过用户确认，禁止自动修改已启用技能
  - 采用patch方式，保留所有历史版本
  - 禁止降级安全规则
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.skill_engine.skill_optimizer")

# Minimum executions before evaluating effectiveness
MIN_EXECUTIONS_FOR_EVAL = 3

# Success rate threshold below which optimization is suggested
SUCCESS_RATE_THRESHOLD = 0.8

# Recent failures threshold
RECENT_FAILURE_THRESHOLD = 2


# ============================================================
# Execution Recording (delegates to skill_manager)
# ============================================================

def record_execution(
    skill_name: str,
    task_id: str = "",
    success: bool = True,
    duration_ms: int = 0,
    error: str = "",
) -> None:
    """Record a skill execution result for tracking."""
    try:
        from .skill_manager import record_execution as _rec
    except ImportError:
        from skill_engine.skill_manager import record_execution as _rec
    _rec(skill_name, task_id, success, duration_ms, error)


# ============================================================
# Effectiveness Evaluation
# ============================================================

def evaluate_effectiveness(skill_name: str) -> Dict[str, Any]:
    """Evaluate a skill's effectiveness based on execution history.

    Returns:
        {
            "skill_name": str,
            "total_executions": int,
            "success_rate": float,
            "avg_duration_ms": int,
            "needs_optimization": bool,
            "reasons": [str],
            "recent_errors": [str],  # only if failures exist
        }
    """
    try:
        from .skill_manager import get_execution_stats
    except ImportError:
        from skill_engine.skill_manager import get_execution_stats

    stats = get_execution_stats(skill_name)

    result: Dict[str, Any] = {
        "skill_name": skill_name,
        "total_executions": stats["total"],
        "success_rate": stats["success_rate"],
        "avg_duration_ms": stats["avg_duration_ms"],
        "needs_optimization": False,
        "reasons": [],
    }

    if stats["total"] < MIN_EXECUTIONS_FOR_EVAL:
        result["reasons"].append(
            f"数据不足 ({stats['total']}/{MIN_EXECUTIONS_FOR_EVAL})"
        )
        return result

    # Check: success rate below threshold
    if stats["success_rate"] < SUCCESS_RATE_THRESHOLD:
        result["needs_optimization"] = True
        result["reasons"].append(
            f"成功率偏低: {stats['success_rate']:.1%} (阈值{SUCCESS_RATE_THRESHOLD:.0%})"
        )

    # Check: recent failures
    recent_failures = _get_recent_failures(skill_name, limit=5)
    if len(recent_failures) >= RECENT_FAILURE_THRESHOLD:
        result["needs_optimization"] = True
        result["reasons"].append(f"近期失败 {len(recent_failures)} 次")
        result["recent_errors"] = [
            f["error_message"] for f in recent_failures if f.get("error_message")
        ]

    return result


def _get_recent_failures(
    skill_name: str, limit: int = 5
) -> List[Dict[str, Any]]:
    """Get recent failed executions."""
    try:
        from .skill_manager import _get_db
    except ImportError:
        from skill_engine.skill_manager import _get_db

    db = _get_db()
    rows = db.execute("""
        SELECT * FROM skill_executions
        WHERE skill_name = ? AND success = 0
        ORDER BY created_at DESC LIMIT ?
    """, (skill_name, limit)).fetchall()
    return [dict(r) for r in rows]


# ============================================================
# Patch Generation
# ============================================================

def generate_patch(
    skill_name: str,
    improvements: Optional[Dict[str, Any]] = None,
) -> Optional[str]:
    """Generate an optimization patch for a skill.

    Returns patch_id if generated, None if no optimization needed.
    """
    evaluation = evaluate_effectiveness(skill_name)
    if not evaluation["needs_optimization"] and not improvements:
        return None

    try:
        from .skill_manager import (
            get_skill, get_skill_content, get_latest_version, save_patch,
        )
    except ImportError:
        from skill_engine.skill_manager import (
            get_skill, get_skill_content, get_latest_version, save_patch,
        )

    skill = get_skill(skill_name)
    if not skill:
        return None

    current_content = get_skill_content(skill_name) or ""
    current_version = get_latest_version(skill_name) or "1.0.0"

    # Build improved content
    new_content = _apply_improvements(current_content, evaluation, improvements)
    if new_content == current_content:
        return None

    # Build change summary
    reasons = list(evaluation.get("reasons", []))
    if improvements and improvements.get("reasons"):
        reasons.extend(improvements["reasons"])
    change_summary = "; ".join(reasons) or "自动优化"

    patch_id = f"patch_{int(time.time() * 1000)}"
    save_patch(
        patch_id=patch_id,
        skill_name=skill_name,
        old_version=current_version,
        new_content=new_content,
        change_summary=change_summary,
        improvements=improvements or {"evaluation": evaluation},
    )
    return patch_id


def _apply_improvements(
    content: str,
    evaluation: Dict[str, Any],
    improvements: Optional[Dict[str, Any]] = None,
) -> str:
    """Apply improvements to skill content via append (patch-style).

    Never removes existing content — only adds new sections.
    Safety rules are never downgraded.
    """
    additions: List[str] = []

    # Add error handling notes if success rate is low
    if evaluation.get("success_rate", 1.0) < SUCCESS_RATE_THRESHOLD:
        recent_errors = evaluation.get("recent_errors", [])
        if recent_errors:
            additions.extend([
                "",
                "## 已知问题与处理",
                "以下错误模式需要注意:",
            ])
            for err in recent_errors[:3]:
                if err:
                    additions.append(f"- {err}")

    # Add explicit improvements if provided
    if improvements and improvements.get("additions"):
        additions.extend([
            "",
            "## 优化补充",
        ])
        for item in improvements["additions"]:
            additions.append(f"- {item}")

    if not additions:
        return content

    return content + "\n" + "\n".join(additions)


# ============================================================
# Convenience: get pending patches / confirm / reject
# (delegates to skill_manager)
# ============================================================

def get_pending_patches() -> List[Dict[str, Any]]:
    """Get all pending optimization patches."""
    try:
        from .skill_manager import get_pending_patches as _get
    except ImportError:
        from skill_engine.skill_manager import get_pending_patches as _get
    return _get()


def confirm_optimization(patch_id: str) -> bool:
    """Confirm an optimization patch — updates version + file."""
    try:
        from .skill_manager import confirm_patch
    except ImportError:
        from skill_engine.skill_manager import confirm_patch
    return confirm_patch(patch_id)


def reject_optimization(patch_id: str) -> bool:
    """Reject an optimization patch."""
    try:
        from .skill_manager import reject_patch
    except ImportError:
        from skill_engine.skill_manager import reject_patch
    return reject_patch(patch_id)
