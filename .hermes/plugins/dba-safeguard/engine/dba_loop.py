"""DBA闭环执行引擎 — 主Agent Loop。

核心流程:
  需求接收 → 意图分类 → 规范挂载 → 元数据预检 → 方案生成 →
  双Agent并行校验 → 风险定级 → 人工审批(按需) → 安全执行 →
  结果反馈 → 经验沉淀

设计原则:
  - 不修改Hermes核心源码，通过组合现有工具+钩子实现闭环
  - 闭环引擎是插件层的编排器，协调现有工具的调用顺序
  - 校验不通过自动打回重写，最多MAX_REWRITE_ROUNDS=2轮
  - 全流程状态追踪，支持断点续跑
"""

from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.engine.dba_loop")


# ============================================================
# Pipeline Stage Definition
# ============================================================

class StageStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    BLOCKED = "blocked"       # blocked by HITL, waiting for approval


class PipelineStage(str, Enum):
    """Ordered stages of the DBA execution pipeline."""
    INTENT_CLASSIFY = "intent_classify"
    PREFLIGHT = "preflight"
    SQL_VALIDATE = "sql_validate"
    DUAL_VALIDATE = "dual_validate"
    RISK_ASSESS = "risk_assess"
    ROLLBACK_GEN = "rollback_gen"
    APPROVAL = "approval"
    EXECUTE = "execute"
    AUDIT = "audit"

    @classmethod
    def ordered(cls) -> list:
        return list(cls)


# ============================================================
# Step Result
# ============================================================

@dataclass
class StepResult:
    """Result of a single pipeline stage."""
    stage: PipelineStage
    status: StageStatus
    data: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stage": self.stage.value,
            "status": self.status.value,
            "data": self.data,
            "error": self.error,
            "duration_ms": self.duration_ms,
        }


# ============================================================
# DBA Task
# ============================================================

@dataclass
class DBATask:
    """Represents a DBA operation task flowing through the pipeline."""
    task_id: str
    sql: str
    instance_name: str
    dialect: str = "postgresql"
    user_message: str = ""
    user_id: str = "default"
    session_id: str = ""

    # Pipeline state (populated as it flows)
    intent: Dict[str, Any] = field(default_factory=dict)
    risk_level: int = 0
    risk_label: str = ""
    validation: Dict[str, Any] = field(default_factory=dict)
    explain_result: Dict[str, Any] = field(default_factory=dict)
    rollback_sql: str = ""
    approved: bool = False
    execution_result: Dict[str, Any] = field(default_factory=dict)

    # Flow control
    current_stage: PipelineStage = PipelineStage.INTENT_CLASSIFY
    stage_results: List[StepResult] = field(default_factory=list)
    rewrite_count: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "sql": self.sql,
            "instance_name": self.instance_name,
            "dialect": self.dialect,
            "risk_level": self.risk_level,
            "risk_label": self.risk_label,
            "current_stage": self.current_stage.value,
            "rewrite_count": self.rewrite_count,
            "approved": self.approved,
            "stages": [s.to_dict() for s in self.stage_results],
        }


# ============================================================
# DBA Pipeline Engine
# ============================================================

MAX_REWRITE_ROUNDS = 2


class DBAPipeline:
    """Closed-loop DBA execution pipeline.

    Orchestrates:  classify → preflight → validate → dual_validate →
                   risk → rollback → approve → execute → audit

    Non-SQL tasks (health_check, troubleshoot, general) get a simplified
    pipeline that skips SQL-specific stages.
    """

    def __init__(
        self,
        *,
        on_status: Optional[Callable[[DBATask, StepResult], None]] = None,
        on_approval_needed: Optional[Callable[[DBATask], bool]] = None,
    ):
        """
        Args:
            on_status: Callback fired after each stage completes.
            on_approval_needed: Callback for L2+ approval. Returns True=approved.
                If None, L2+ tasks are blocked with BLOCKED status.
        """
        self._on_status = on_status
        self._on_approval_needed = on_approval_needed

    # ----------------------------------------------------------
    # Main Entry
    # ----------------------------------------------------------

    def run(self, task: DBATask) -> DBATask:
        """Run the full pipeline. Returns the task with all results populated.

        For resumption after interruption, pass a task with some stages
        already completed — the pipeline skips completed stages.
        """
        completed = {s.stage for s in task.stage_results if s.status == StageStatus.PASSED}

        for stage in PipelineStage.ordered():
            if stage in completed:
                continue

            # Skip SQL-specific stages for non-SQL intents
            if self._should_skip(task, stage):
                task.stage_results.append(StepResult(
                    stage=stage, status=StageStatus.SKIPPED,
                ))
                continue

            task.current_stage = stage
            result = self._run_stage(task, stage)
            task.stage_results.append(result)
            self._notify(task, result)

            if result.status == StageStatus.FAILED:
                # Rewrite loop: validation failures → retry up to MAX_REWRITE_ROUNDS
                if stage in (PipelineStage.SQL_VALIDATE, PipelineStage.DUAL_VALIDATE):
                    if task.rewrite_count < MAX_REWRITE_ROUNDS:
                        task.rewrite_count += 1
                        # Caller rewrites SQL, then calls run() again with updated task
                        return task
                # Non-retryable failure → stop pipeline
                return task

            if result.status == StageStatus.BLOCKED:
                return task  # Waiting for external approval

        return task

    # ----------------------------------------------------------
    # Stage Router
    # ----------------------------------------------------------

    def _run_stage(self, task: DBATask, stage: PipelineStage) -> StepResult:
        """Dispatch to the appropriate stage handler."""
        handlers = {
            PipelineStage.INTENT_CLASSIFY: self._stage_intent,
            PipelineStage.PREFLIGHT: self._stage_preflight,
            PipelineStage.SQL_VALIDATE: self._stage_sql_validate,
            PipelineStage.DUAL_VALIDATE: self._stage_dual_validate,
            PipelineStage.RISK_ASSESS: self._stage_risk_assess,
            PipelineStage.ROLLBACK_GEN: self._stage_rollback_gen,
            PipelineStage.APPROVAL: self._stage_approval,
            PipelineStage.EXECUTE: self._stage_execute,
            PipelineStage.AUDIT: self._stage_audit,
        }
        handler = handlers.get(stage)
        if not handler:
            return StepResult(stage=stage, status=StageStatus.FAILED,
                              error=f"Unknown stage: {stage}")
        start = time.time()
        try:
            result = handler(task)
            result.duration_ms = int((time.time() - start) * 1000)
            return result
        except Exception as e:
            logger.error("Stage %s failed: %s", stage.value, e, exc_info=True)
            return StepResult(
                stage=stage, status=StageStatus.FAILED,
                error=str(e),
                duration_ms=int((time.time() - start) * 1000),
            )

    # ----------------------------------------------------------
    # Skip Logic
    # ----------------------------------------------------------

    def _should_skip(self, task: DBATask, stage: PipelineStage) -> bool:
        """Decide if a stage should be skipped for this task."""
        intent_key = task.intent.get("intent", "")

        # Non-SQL intents skip SQL-specific stages
        non_sql_intents = {"health_check", "troubleshoot", "general", "backup_restore"}
        if intent_key in non_sql_intents:
            sql_stages = {
                PipelineStage.SQL_VALIDATE,
                PipelineStage.DUAL_VALIDATE,
                PipelineStage.RISK_ASSESS,
                PipelineStage.ROLLBACK_GEN,
                PipelineStage.APPROVAL,
                PipelineStage.EXECUTE,
            }
            if stage in sql_stages:
                return True

        # L0 read-only skips rollback and approval
        if task.risk_level == 0 and stage in (
            PipelineStage.ROLLBACK_GEN,
            PipelineStage.APPROVAL,
        ):
            return True

        # L1 doesn't require rollback
        if task.risk_level == 1 and stage == PipelineStage.ROLLBACK_GEN:
            return True

        return False

    # ----------------------------------------------------------
    # Stage Implementations
    # ----------------------------------------------------------

    def _stage_intent(self, task: DBATask) -> StepResult:
        """Stage 1: Intent classification."""
        try:
            from ..harnesses.intent_router import classify_intent
        except ImportError:
            from harnesses.intent_router import classify_intent

        text = task.user_message or task.sql
        intent = classify_intent(text)
        task.intent = intent

        return StepResult(
            stage=PipelineStage.INTENT_CLASSIFY,
            status=StageStatus.PASSED,
            data={"intent": intent["intent"], "label": intent["label"],
                  "confidence": intent["confidence"]},
        )

    def _stage_preflight(self, task: DBATask) -> StepResult:
        """Stage 2: Pre-execution checks."""
        try:
            from .preflight import run_preflight
        except ImportError:
            from engine.preflight import run_preflight

        check = run_preflight(
            sql=task.sql,
            instance_name=task.instance_name,
            dialect=task.dialect,
        )

        if not check["passed"]:
            return StepResult(
                stage=PipelineStage.PREFLIGHT,
                status=StageStatus.FAILED,
                data=check,
                error="; ".join(f["message"] for f in check["failures"]),
            )

        return StepResult(
            stage=PipelineStage.PREFLIGHT,
            status=StageStatus.PASSED,
            data=check,
        )

    def _stage_sql_validate(self, task: DBATask) -> StepResult:
        """Stage 3: AST-level SQL validation."""
        try:
            from ..tools.sql_ast_validator import validate_sql
        except ImportError:
            from tools.sql_ast_validator import validate_sql

        val = validate_sql(task.sql, task.dialect)
        task.validation = val
        task.risk_level = val["risk_level"]
        task.risk_label = val.get("risk_label", f"L{val['risk_level']}")

        if not val["valid"]:
            errors = "; ".join(e["message"] for e in val.get("errors", []))
            return StepResult(
                stage=PipelineStage.SQL_VALIDATE,
                status=StageStatus.FAILED,
                data=val, error=errors,
            )

        return StepResult(
            stage=PipelineStage.SQL_VALIDATE,
            status=StageStatus.PASSED,
            data=val,
        )

    def _stage_dual_validate(self, task: DBATask) -> StepResult:
        """Stage 4: Dual sub-agent validation (syntax + performance)."""
        try:
            from .dual_validator import run_dual_validation
        except ImportError:
            from engine.dual_validator import run_dual_validation

        result = run_dual_validation(
            sql=task.sql,
            instance_name=task.instance_name,
            dialect=task.dialect,
            risk_level=task.risk_level,
        )

        task.explain_result = result.get("performance", {})

        if not result["passed"]:
            reasons = []
            if result.get("syntax", {}).get("errors"):
                reasons.extend(result["syntax"]["errors"])
            if result.get("performance", {}).get("errors"):
                reasons.extend(result["performance"]["errors"])
            return StepResult(
                stage=PipelineStage.DUAL_VALIDATE,
                status=StageStatus.FAILED,
                data=result,
                error="; ".join(reasons),
            )

        return StepResult(
            stage=PipelineStage.DUAL_VALIDATE,
            status=StageStatus.PASSED,
            data=result,
        )

    def _stage_risk_assess(self, task: DBATask) -> StepResult:
        """Stage 5: Final risk assessment (combines AST + EXPLAIN + escalation)."""
        try:
            from ..harnesses.risk_interceptor import load_hitl_matrix
        except ImportError:
            from harnesses.risk_interceptor import load_hitl_matrix

        # Escalation from intent router (e.g., no-WHERE → L4)
        intent_risk = task.intent.get("risk_preset", 0)
        task.risk_level = max(task.risk_level, intent_risk)

        # Escalation from EXPLAIN (full table scan → +1)
        explain = task.explain_result
        if explain.get("should_block"):
            task.risk_level = max(task.risk_level, 3)
        elif explain.get("warnings"):
            task.risk_level = max(task.risk_level, task.risk_level + 1)

        # Cap at L4
        task.risk_level = min(task.risk_level, 4)

        matrix = load_hitl_matrix()
        levels = matrix.get("risk_levels", {})
        level_cfg = levels.get(task.risk_level, {})
        task.risk_label = level_cfg.get("label", f"L{task.risk_level}")

        return StepResult(
            stage=PipelineStage.RISK_ASSESS,
            status=StageStatus.PASSED,
            data={
                "risk_level": task.risk_level,
                "risk_label": task.risk_label,
                "action": level_cfg.get("action", "force_block"),
                "require_approval": level_cfg.get("require_approval", True),
            },
        )

    def _stage_rollback_gen(self, task: DBATask) -> StepResult:
        """Stage 6: Generate rollback script."""
        try:
            from ..tools.rollback_generator import generate_rollback
        except ImportError:
            from tools.rollback_generator import generate_rollback

        result = generate_rollback(
            sql=task.sql,
            dialect=task.dialect,
            instance_name=task.instance_name,
        )
        task.rollback_sql = result.get("rollback_sql", "")

        if not task.rollback_sql:
            return StepResult(
                stage=PipelineStage.ROLLBACK_GEN,
                status=StageStatus.FAILED,
                data=result,
                error="无法生成回滚脚本",
            )

        return StepResult(
            stage=PipelineStage.ROLLBACK_GEN,
            status=StageStatus.PASSED,
            data={"rollback_sql": task.rollback_sql},
        )

    def _stage_approval(self, task: DBATask) -> StepResult:
        """Stage 7: Human approval gate."""
        try:
            from ..harnesses.risk_interceptor import load_hitl_matrix
        except ImportError:
            from harnesses.risk_interceptor import load_hitl_matrix

        matrix = load_hitl_matrix()
        levels = matrix.get("risk_levels", {})
        level_cfg = levels.get(task.risk_level, {})

        if not level_cfg.get("require_approval", True):
            task.approved = True
            return StepResult(
                stage=PipelineStage.APPROVAL,
                status=StageStatus.PASSED,
                data={"auto_approved": True, "reason": level_cfg.get("action")},
            )

        # Try approval callback
        if self._on_approval_needed:
            approved = self._on_approval_needed(task)
            task.approved = approved
            if approved:
                return StepResult(
                    stage=PipelineStage.APPROVAL,
                    status=StageStatus.PASSED,
                    data={"human_approved": True},
                )
            return StepResult(
                stage=PipelineStage.APPROVAL,
                status=StageStatus.FAILED,
                data={"human_approved": False},
                error="人工审批被拒绝",
            )

        # No callback — block and wait
        return StepResult(
            stage=PipelineStage.APPROVAL,
            status=StageStatus.BLOCKED,
            data={
                "risk_level": task.risk_level,
                "risk_label": task.risk_label,
                "sql": task.sql[:500],
                "rollback_sql": task.rollback_sql[:500],
            },
            error="等待人工审批",
        )

    def _stage_execute(self, task: DBATask) -> StepResult:
        """Stage 8: Safe SQL execution."""
        try:
            from ..tools.safe_executor import execute_sql
        except ImportError:
            from tools.safe_executor import execute_sql

        result = execute_sql(
            sql=task.sql,
            instance_name=task.instance_name,
            dialect=task.dialect,
            risk_level=task.risk_level,
            approved=task.approved,
            rollback_sql=task.rollback_sql,
            task_id=task.task_id,
            session_id=task.session_id,
            user_id=task.user_id,
        )
        task.execution_result = result

        if not result.get("success"):
            return StepResult(
                stage=PipelineStage.EXECUTE,
                status=StageStatus.FAILED,
                data=result,
                error=result.get("error", "执行失败"),
            )

        return StepResult(
            stage=PipelineStage.EXECUTE,
            status=StageStatus.PASSED,
            data=result,
        )

    def _stage_audit(self, task: DBATask) -> StepResult:
        """Stage 9: Record pipeline audit summary."""
        summary = {
            "task_id": task.task_id,
            "sql": task.sql[:500],
            "instance": task.instance_name,
            "risk_level": task.risk_level,
            "risk_label": task.risk_label,
            "rewrite_count": task.rewrite_count,
            "stages_passed": sum(
                1 for s in task.stage_results if s.status == StageStatus.PASSED
            ),
            "stages_total": len(task.stage_results),
            "execution_success": task.execution_result.get("success", False),
            "total_duration_ms": sum(s.duration_ms for s in task.stage_results),
        }
        logger.info("Pipeline audit: %s", json.dumps(summary, ensure_ascii=False))

        return StepResult(
            stage=PipelineStage.AUDIT,
            status=StageStatus.PASSED,
            data=summary,
        )

    # ----------------------------------------------------------
    # Helpers
    # ----------------------------------------------------------

    def _notify(self, task: DBATask, result: StepResult) -> None:
        if self._on_status:
            try:
                self._on_status(task, result)
            except Exception as e:
                logger.debug("Status callback error: %s", e)


# ============================================================
# Convenience Functions
# ============================================================

def create_task(
    sql: str,
    instance_name: str,
    dialect: str = "postgresql",
    *,
    task_id: str = "",
    user_message: str = "",
    user_id: str = "default",
    session_id: str = "",
) -> DBATask:
    """Create a DBA task for the pipeline."""
    if not task_id:
        task_id = f"dba_{int(time.time() * 1000)}"
    return DBATask(
        task_id=task_id,
        sql=sql,
        instance_name=instance_name,
        dialect=dialect,
        user_message=user_message or sql,
        user_id=user_id,
        session_id=session_id,
    )


def run_pipeline(
    sql: str,
    instance_name: str,
    dialect: str = "postgresql",
    *,
    task_id: str = "",
    user_message: str = "",
    on_approval_needed: Optional[Callable] = None,
) -> DBATask:
    """One-shot pipeline execution."""
    task = create_task(sql, instance_name, dialect,
                       task_id=task_id, user_message=user_message)
    pipeline = DBAPipeline(on_approval_needed=on_approval_needed)
    return pipeline.run(task)
