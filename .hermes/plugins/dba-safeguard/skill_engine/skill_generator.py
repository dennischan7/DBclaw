"""DBA技能自动生成器 — 从成功任务中自动提炼可复用技能。

触发条件 (满足任一):
  1. repeated_success: 同类复杂任务成功执行 ≥ 2次
  2. self_repair: 执行中报错但完成自我修复 (rewrite_count > 0)
  3. user_correction: 被用户纠正并改进了方案
  4. efficient_solution: 发现了高效的运维解决方案

生成流程:
  任务完成 → evaluate_trigger() → 满足条件 →
  generate_draft() → 用户确认 → install → 版本管理

约束:
  - 技能生成必须经过用户确认，禁止自动入库启用
  - 禁止生成超出DBA领域的技能
  - 更新采用patch方式，不全量重写历史版本
"""

from __future__ import annotations

import json
import logging
import time
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.skill_engine.skill_generator")


# ============================================================
# Trigger Types
# ============================================================

class TriggerType(str, Enum):
    REPEATED_SUCCESS = "repeated_success"
    SELF_REPAIR = "self_repair"
    USER_CORRECTION = "user_correction"
    EFFICIENT_SOLUTION = "efficient_solution"


# Minimum confirmed experiences of same category to trigger REPEATED_SUCCESS
MIN_REPEAT_COUNT = 2

# DBA experience categories eligible for skill generation
_DBA_CATEGORIES = {
    "ddl_workflow", "pitfall", "optimization", "sql_pattern", "best_practice",
}


# ============================================================
# Trigger Evaluation
# ============================================================

def evaluate_trigger(task_data: Dict[str, Any]) -> Optional[TriggerType]:
    """Evaluate if a completed task should trigger skill generation.

    Args:
        task_data: {
            "task_id": str,
            "success": bool,
            "category": str,       # L3 experience category
            "sql": str,
            "rewrite_count": int,  # how many rewrites were needed
            "user_corrected": bool,
            "duration_ms": int,
        }

    Returns:
        TriggerType if generation should be triggered, None otherwise.
    """
    # Only successful tasks can generate skills
    if not task_data.get("success"):
        return None

    category = task_data.get("category", "")

    # Check: repeated success (same category ≥ MIN_REPEAT_COUNT)
    if _check_repeated_success(category):
        return TriggerType.REPEATED_SUCCESS

    # Check: self-repair (had to rewrite but ultimately succeeded)
    if task_data.get("rewrite_count", 0) > 0:
        return TriggerType.SELF_REPAIR

    # Check: user correction
    if task_data.get("user_corrected"):
        return TriggerType.USER_CORRECTION

    return None


def _check_repeated_success(category: str) -> bool:
    """Check L3 experience store for ≥ MIN_REPEAT_COUNT confirmed
    experiences of the same category."""
    if not category or category not in _DBA_CATEGORIES:
        return False
    try:
        try:
            from ..memory.l3_experience import list_by_category
        except ImportError:
            from memory.l3_experience import list_by_category

        experiences = list_by_category(category)
        confirmed = [e for e in experiences if e.get("status") == "confirmed"]
        return len(confirmed) >= MIN_REPEAT_COUNT
    except Exception:
        return False


# ============================================================
# Skill Draft Generation
# ============================================================

def generate_draft(
    trigger_type: TriggerType,
    task_data: Dict[str, Any],
    experience_ids: Optional[List[str]] = None,
) -> str:
    """Generate a skill draft from task data. Returns draft_id.

    The draft is saved as 'pending' — must be confirmed by user before
    it becomes an active skill.
    """
    try:
        from .skill_manager import save_draft
    except ImportError:
        from skill_engine.skill_manager import save_draft

    draft_id = f"draft_{int(time.time() * 1000)}"
    skill_name = _derive_skill_name(task_data)
    content = _build_skill_content(task_data, trigger_type, experience_ids)

    save_draft(
        draft_id=draft_id,
        skill_name=skill_name,
        content=content,
        trigger_reason=trigger_type.value,
        experience_ids=experience_ids,
    )
    return draft_id


def _derive_skill_name(task_data: Dict[str, Any]) -> str:
    """Derive a unique skill name from task data."""
    category = task_data.get("category", "general")
    intent = task_data.get("intent", category)
    ts = int(time.time())
    # Sanitize: keep only alphanums, hyphens, underscores
    safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in intent)
    return f"dba-auto-{safe}-{ts}"


def _build_skill_content(
    task_data: Dict[str, Any],
    trigger_type: TriggerType,
    experience_ids: Optional[List[str]] = None,
) -> str:
    """Build SKILL.md content from task data and related experiences."""
    category = task_data.get("category", "general")
    sql = task_data.get("sql", "")
    skill_name = _derive_skill_name(task_data)

    # --- YAML Frontmatter ---
    lines = [
        "---",
        f"name: {skill_name}",
        f"description: 从成功任务自动生成的DBA技能 ({trigger_type.value})",
        "version: 1.0.0",
        "metadata:",
        "  hermes:",
        f"    tags: [dba, auto-generated, {category}]",
        "    config: {}",
        "---",
        "",
        f"# DBA技能: {category}",
        "",
        "## 背景",
        f"本技能从 **{_trigger_label(trigger_type)}** 模式中自动提炼。",
        "",
        "## 适用场景",
        f"- 数据库操作类型: {category}",
    ]

    if task_data.get("dialect"):
        lines.append(f"- 数据库方言: {task_data['dialect']}")

    # --- SQL Template ---
    if sql:
        lines.extend([
            "",
            "## SQL模板",
            "```sql",
            sql,
            "```",
        ])

    # --- Experience Context ---
    exp_ctx = _gather_experience_context(experience_ids)
    if exp_ctx:
        lines.extend([
            "",
            "## 经验参考",
            exp_ctx,
        ])

    # --- Workflow ---
    lines.extend([
        "",
        "## 工作流程",
        "1. 使用 `library_search` 确认目标数据库版本的语法兼容性",
        "2. 使用 `sql_validate` 校验SQL语法和风险等级",
        "3. 使用 `explain_analyze` 评估性能影响（如适用）",
        "4. 根据风险等级走审批流程",
        "5. 使用 `db_execute` 安全执行",
        "6. 执行后验证并记录审计日志",
    ])

    # --- Safety Rules ---
    lines.extend([
        "",
        "## 安全规则",
        "- 所有SQL必须经过 `sql_validate` 校验",
        "- 写操作必须按风险等级走审批流程",
        "- L2+必须生成回滚脚本",
        "- 执行结果自动记录审计日志",
        "- 生产环境操作必须包含事务控制",
    ])

    return "\n".join(lines)


def _trigger_label(trigger_type: TriggerType) -> str:
    """Human-readable trigger label."""
    labels = {
        TriggerType.REPEATED_SUCCESS: "同类任务反复成功",
        TriggerType.SELF_REPAIR: "错误自修复",
        TriggerType.USER_CORRECTION: "用户纠正优化",
        TriggerType.EFFICIENT_SOLUTION: "高效解决方案",
    }
    return labels.get(trigger_type, trigger_type.value)


def _gather_experience_context(experience_ids: Optional[List[str]]) -> str:
    """Gather context from related L3 experiences."""
    if not experience_ids:
        return ""

    lines = []
    try:
        try:
            from ..memory.l3_experience import _get_db
        except ImportError:
            from memory.l3_experience import _get_db

        db = _get_db()
        for eid in experience_ids[:5]:
            row = db.execute(
                "SELECT title, summary FROM experiences WHERE id = ?", (eid,)
            ).fetchone()
            if row:
                lines.append(f"- **{row[0]}**: {row[1]}")
    except Exception:
        pass

    return "\n".join(lines)
