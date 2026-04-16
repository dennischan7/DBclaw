"""Phase 4 测试套件 — 闭环执行引擎与多智能体流水线。

分为:
  A. Pipeline阶段定义与任务模型测试
  B. 预检模块测试 (连接/表存在/权限/元数据预取)
  C. 双校验器测试 (语法+性能并行)
  D. 闭环流水线测试 (完整流程/跳过逻辑/重写循环/审批阻断)
  E. 状态持久化测试 (保存/加载/恢复/过期清理)
  F. 端到端集成测试 (pipeline→state→resume 全链路)
"""

import json
import os
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

plugin_root = Path(__file__).parent.parent
sys.path.insert(0, str(plugin_root))

PG_AVAILABLE = bool(
    os.environ.get("DBA_PG_TEST_RO_USER")
    and os.environ.get("DBA_PG_TEST_RO_PASS")
)


# ========================================================================
# A. Pipeline阶段定义与任务模型测试
# ========================================================================

class TestPipelineModels:
    """Test DBATask and pipeline stage definitions."""

    def test_pipeline_stage_order(self):
        from engine.dba_loop import PipelineStage
        stages = PipelineStage.ordered()
        assert len(stages) == 9
        assert stages[0] == PipelineStage.INTENT_CLASSIFY
        assert stages[-1] == PipelineStage.AUDIT

    def test_create_task(self):
        from engine.dba_loop import create_task
        task = create_task("SELECT 1", "pg_test", "postgresql")
        assert task.sql == "SELECT 1"
        assert task.instance_name == "pg_test"
        assert task.dialect == "postgresql"
        assert task.task_id.startswith("dba_")
        assert task.risk_level == 0
        assert task.rewrite_count == 0
        assert task.stage_results == []

    def test_create_task_custom_id(self):
        from engine.dba_loop import create_task
        task = create_task("SELECT 1", "pg_test", task_id="my_task_001")
        assert task.task_id == "my_task_001"

    def test_task_to_dict(self):
        from engine.dba_loop import create_task
        task = create_task("SELECT 1", "pg_test")
        d = task.to_dict()
        assert "task_id" in d
        assert d["sql"] == "SELECT 1"
        assert d["current_stage"] == "intent_classify"
        assert d["stages"] == []

    def test_step_result_to_dict(self):
        from engine.dba_loop import StepResult, PipelineStage, StageStatus
        sr = StepResult(
            stage=PipelineStage.SQL_VALIDATE,
            status=StageStatus.PASSED,
            data={"valid": True},
            duration_ms=42,
        )
        d = sr.to_dict()
        assert d["stage"] == "sql_validate"
        assert d["status"] == "passed"
        assert d["duration_ms"] == 42

    def test_stage_status_values(self):
        from engine.dba_loop import StageStatus
        assert StageStatus.PENDING == "pending"
        assert StageStatus.BLOCKED == "blocked"
        assert StageStatus.PASSED == "passed"
        assert StageStatus.FAILED == "failed"


# ========================================================================
# B. 预检模块测试
# ========================================================================

class TestPreflight:
    """Test pre-execution checks."""

    def test_extract_tables_select(self):
        from engine.preflight import _extract_tables
        tables = _extract_tables("SELECT * FROM users WHERE id = 1", "postgresql")
        assert "users" in tables

    def test_extract_tables_join(self):
        from engine.preflight import _extract_tables
        tables = _extract_tables(
            "SELECT u.id, o.amount FROM users u JOIN orders o ON u.id = o.user_id",
            "postgresql"
        )
        assert "users" in tables or "u" in tables
        assert "orders" in tables or "o" in tables

    def test_extract_tables_update(self):
        from engine.preflight import _extract_tables
        tables = _extract_tables("UPDATE orders SET status = 1 WHERE id = 5", "postgresql")
        assert "orders" in tables

    def test_extract_tables_create_returns_empty(self):
        from engine.preflight import _extract_tables
        tables = _extract_tables("CREATE TABLE new_table (id INT)", "postgresql")
        assert tables == []

    def test_extract_tables_regex_fallback(self):
        from engine.preflight import _extract_tables_regex
        tables = _extract_tables_regex("SELECT * FROM users JOIN orders ON 1=1")
        assert "users" in tables
        assert "orders" in tables

    def test_permission_check_readonly(self):
        from engine.preflight import _check_permissions
        result = _check_permissions("SELECT * FROM users", "postgresql")
        assert result["passed"] is True
        assert result["data"]["operation"] == "readonly"

    def test_permission_check_write_with_admin(self):
        with patch.dict(os.environ, {"DBA_PG_TEST_ADMIN_USER": "admin_user"}):
            from engine.preflight import _check_permissions
            result = _check_permissions("INSERT INTO users VALUES (1)", "postgresql")
            assert result["passed"] is True
            assert result["data"]["operation"] == "write"

    def test_permission_check_write_no_admin(self):
        env = {k: v for k, v in os.environ.items()
               if k not in ("DBA_PG_TEST_ADMIN_USER", "DBA_ADMIN_USER")}
        with patch.dict(os.environ, env, clear=True):
            from engine.preflight import _check_permissions
            result = _check_permissions("DELETE FROM users WHERE id=1", "postgresql")
            assert result["passed"] is False

    def test_preflight_skip_connection(self):
        from engine.preflight import run_preflight
        result = run_preflight(
            "SELECT 1", "pg_test", "postgresql",
            skip_connection=True, skip_table_check=True,
        )
        assert result["passed"] is True
        # Should have permission check at least
        assert len(result["checks"]) >= 1

    @pytest.mark.skipif(not PG_AVAILABLE, reason="No PG test instance")
    def test_preflight_pg_connection(self):
        from engine.preflight import run_preflight
        from tools.db_connector import get_connection_manager
        mgr = get_connection_manager()
        mgr.load_config()
        result = run_preflight(
            "SELECT 1", "pg_test", "postgresql",
            skip_table_check=True,
        )
        assert result["passed"] is True
        conn_check = next(c for c in result["checks"] if c["name"] == "connection_check")
        assert conn_check["passed"] is True


# ========================================================================
# C. 双校验器测试
# ========================================================================

class TestDualValidator:
    """Test dual syntax + performance validation."""

    def test_syntax_valid_select(self):
        from engine.dual_validator import _validate_syntax
        result = _validate_syntax("SELECT * FROM users", "postgresql", "pg_test")
        assert result["passed"] is True

    def test_syntax_invalid_sql(self):
        from engine.dual_validator import _validate_syntax
        result = _validate_syntax("SELEC FORM users", "postgresql", "pg_test")
        assert result["passed"] is False
        assert len(result["errors"]) > 0

    def test_syntax_with_library_search(self):
        """Valid ALTER TABLE triggers library search."""
        from engine.dual_validator import _validate_syntax
        result = _validate_syntax(
            "ALTER TABLE users ADD COLUMN email VARCHAR(255)",
            "postgresql", "pg_test",
        )
        assert result["passed"] is True
        # library_refs may or may not be populated depending on library content

    def test_dual_validation_readonly(self):
        """L0 SELECT skips performance check."""
        from engine.dual_validator import run_dual_validation
        result = run_dual_validation(
            "SELECT 1", "pg_test", "postgresql",
            risk_level=0,
        )
        assert result["passed"] is True
        assert result["performance"].get("skipped") is True

    def test_dual_validation_syntax_failure(self):
        from engine.dual_validator import run_dual_validation
        result = run_dual_validation(
            "SELEC FORM users", "pg_test", "postgresql",
            risk_level=1,
        )
        assert result["passed"] is False
        assert len(result["errors"]) > 0

    def test_build_library_query_alter(self):
        from engine.dual_validator import _build_library_query
        q = _build_library_query("ALTER TABLE users ADD COLUMN email VARCHAR(255)", "postgresql")
        assert q is not None
        assert "ALTER TABLE" in q

    def test_build_library_query_simple_select(self):
        from engine.dual_validator import _build_library_query
        q = _build_library_query("SELECT * FROM users", "postgresql")
        assert q is None  # simple SELECT should not trigger search

    def test_build_library_query_join(self):
        from engine.dual_validator import _build_library_query
        q = _build_library_query("SELECT * FROM users JOIN orders ON 1=1", "postgresql")
        assert q is not None
        assert "JOIN" in q

    def test_dialect_to_db_type(self):
        from engine.dual_validator import _dialect_to_db_type
        assert _dialect_to_db_type("postgresql") == "postgres"
        assert _dialect_to_db_type("mysql") == "mysql"
        assert _dialect_to_db_type("oracle") == "oracle"

    @pytest.mark.skipif(not PG_AVAILABLE, reason="No PG test instance")
    def test_performance_validation_pg(self):
        from engine.dual_validator import _validate_performance
        result = _validate_performance(
            "SELECT * FROM users WHERE id = 1",
            "pg_test", "postgresql",
        )
        assert result["passed"] is True


# ========================================================================
# D. 闭环流水线测试
# ========================================================================

class TestDBAPipeline:
    """Test the full closed-loop pipeline."""

    def test_pipeline_readonly_select(self):
        """L0 SELECT: intent→preflight→validate→dual→risk→[skip rollback/approve]→execute→audit."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage

        task = create_task(
            "SELECT 1", "pg_test", "postgresql",
            task_id="test_ro_001",
        )

        # Mock preflight to skip real DB connection
        with patch("engine.preflight.run_preflight") as mock_pf:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}

            # Mock execute to skip real DB
            with patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
                mock_exec.return_value = MagicMock(
                    stage=PipelineStage.EXECUTE,
                    status=StageStatus.PASSED,
                    data={"success": True},
                    duration_ms=10,
                )

                pipeline = DBAPipeline()
                result = pipeline.run(task)

        assert result.risk_level == 0
        # Should have skipped rollback_gen and approval
        stage_names = [s.stage for s in result.stage_results]
        skipped_stages = [s for s in result.stage_results if s.status == StageStatus.SKIPPED]
        skipped_names = [s.stage for s in skipped_stages]
        assert PipelineStage.ROLLBACK_GEN in skipped_names
        assert PipelineStage.APPROVAL in skipped_names

    def test_pipeline_validation_failure_triggers_rewrite(self):
        """Validation failure should set rewrite_count and return early."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage, StepResult

        task = create_task(
            "SELEC FORM users", "pg_test", "postgresql",
            task_id="test_rewrite_001",
        )
        # Pre-set intent as SQL query so it doesn't skip SQL stages
        task.intent = {"intent": "query", "label": "数据查询", "confidence": 0.95}
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY, status=StageStatus.PASSED,
            data={"intent": "query"},
        ))

        with patch("engine.preflight.run_preflight") as mock_pf:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            pipeline = DBAPipeline()
            result = pipeline.run(task)

        # Should fail at sql_validate and increment rewrite_count
        assert result.rewrite_count == 1
        failed = [s for s in result.stage_results if s.status == StageStatus.FAILED]
        assert len(failed) >= 1

    def test_pipeline_max_rewrite_exhausted(self):
        """After MAX_REWRITE_ROUNDS, pipeline stops."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, MAX_REWRITE_ROUNDS

        task = create_task("SELEC FORM users", "pg_test", "postgresql")
        task.rewrite_count = MAX_REWRITE_ROUNDS  # Already exhausted

        with patch("engine.preflight.run_preflight") as mock_pf:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            pipeline = DBAPipeline()
            result = pipeline.run(task)

        # Should stay failed without incrementing — rewrite_count remains at max
        assert result.rewrite_count == MAX_REWRITE_ROUNDS

    def test_pipeline_preflight_failure_stops(self):
        """Preflight failure terminates the pipeline immediately."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage

        task = create_task("SELECT * FROM nonexistent_table", "pg_test")

        with patch("engine.preflight.run_preflight") as mock_pf:
            mock_pf.return_value = {
                "passed": False,
                "checks": [{"name": "connection_check", "passed": False, "message": "连接失败"}],
                "failures": [{"name": "connection_check", "message": "连接失败"}],
                "metadata": {},
            }
            pipeline = DBAPipeline()
            result = pipeline.run(task)

        assert result.stage_results[-1].status == StageStatus.FAILED
        assert result.stage_results[-1].stage == PipelineStage.PREFLIGHT

    def test_pipeline_approval_blocked(self):
        """L2 operation without approval callback → BLOCKED status."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage, StepResult

        task = create_task(
            "UPDATE users SET name='x' WHERE id=1", "pg_test", "postgresql",
            task_id="test_block_001",
        )

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dual_validator.run_dual_validation") as mock_dv, \
             patch("engine.dba_loop.DBAPipeline._stage_rollback_gen") as mock_rb:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_dv.return_value = {"passed": True, "syntax": {"passed": True}, "performance": {"passed": True}, "errors": [], "suggestions": []}
            mock_rb.return_value = StepResult(
                stage=PipelineStage.ROLLBACK_GEN, status=StageStatus.PASSED,
                data={"rollback_sql": "-- rollback"},
            )

            pipeline = DBAPipeline()  # No on_approval_needed callback
            result = pipeline.run(task)

        # Should be blocked at approval stage
        assert any(s.status == StageStatus.BLOCKED for s in result.stage_results)

    def test_pipeline_approval_callback_approved(self):
        """L2 with approval callback returning True → proceeds to execute."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage, StepResult

        task = create_task(
            "UPDATE users SET name='x' WHERE id=1", "pg_test", "postgresql",
            task_id="test_approve_001",
        )

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dual_validator.run_dual_validation") as mock_dv, \
             patch("engine.dba_loop.DBAPipeline._stage_rollback_gen") as mock_rb, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_dv.return_value = {"passed": True, "syntax": {"passed": True}, "performance": {"passed": True}, "errors": [], "suggestions": []}
            mock_rb.return_value = StepResult(
                stage=PipelineStage.ROLLBACK_GEN, status=StageStatus.PASSED,
                data={"rollback_sql": "-- rollback"},
            )
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=10,
            )

            pipeline = DBAPipeline(on_approval_needed=lambda t: True)
            result = pipeline.run(task)

        assert result.approved is True
        assert any(s.stage == PipelineStage.EXECUTE and s.status == StageStatus.PASSED
                   for s in result.stage_results)

    def test_pipeline_approval_callback_rejected(self):
        """L2 with approval callback returning False → pipeline fails."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage, StepResult

        task = create_task(
            "UPDATE users SET name='x' WHERE id=1", "pg_test", "postgresql",
        )

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dual_validator.run_dual_validation") as mock_dv, \
             patch("engine.dba_loop.DBAPipeline._stage_rollback_gen") as mock_rb:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_dv.return_value = {"passed": True, "syntax": {"passed": True}, "performance": {"passed": True}, "errors": [], "suggestions": []}
            mock_rb.return_value = StepResult(
                stage=PipelineStage.ROLLBACK_GEN, status=StageStatus.PASSED,
                data={"rollback_sql": "-- rollback"},
            )

            pipeline = DBAPipeline(on_approval_needed=lambda t: False)
            result = pipeline.run(task)

        assert result.approved is False
        assert any(s.stage == PipelineStage.APPROVAL and s.status == StageStatus.FAILED
                   for s in result.stage_results)

    def test_pipeline_skip_non_sql_intents(self):
        """health_check intent should skip SQL-specific stages."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage

        task = create_task("检查数据库健康状态", "pg_test", "postgresql")
        task.intent = {"intent": "health_check", "label": "健康检查", "confidence": 0.95}

        # Pre-fill intent classify stage as done
        from engine.dba_loop import StepResult
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY,
            status=StageStatus.PASSED,
            data={"intent": "health_check"},
        ))

        with patch("engine.preflight.run_preflight") as mock_pf:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}

            pipeline = DBAPipeline()
            result = pipeline.run(task)

        skipped = [s.stage for s in result.stage_results if s.status == StageStatus.SKIPPED]
        assert PipelineStage.SQL_VALIDATE in skipped
        assert PipelineStage.DUAL_VALIDATE in skipped
        assert PipelineStage.EXECUTE in skipped

    def test_pipeline_status_callback(self):
        """on_status callback fires after each stage."""
        from engine.dba_loop import DBAPipeline, create_task

        callback_log = []

        def on_status(task, result):
            callback_log.append((result.stage.value, result.status.value))

        task = create_task("SELECT 1", "pg_test", "postgresql")

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            from engine.dba_loop import StepResult, PipelineStage, StageStatus
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=5,
            )

            pipeline = DBAPipeline(on_status=on_status)
            pipeline.run(task)

        assert len(callback_log) >= 3
        stage_names = [c[0] for c in callback_log]
        assert "intent_classify" in stage_names

    def test_pipeline_resume_skips_completed(self):
        """Pipeline resume: pre-completed stages are skipped."""
        from engine.dba_loop import (
            DBAPipeline, create_task, StepResult, PipelineStage, StageStatus,
        )

        task = create_task("SELECT 1", "pg_test", "postgresql")
        # Simulate intent already classified
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY, status=StageStatus.PASSED,
            data={"intent": "query"},
        ))

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=5,
            )

            pipeline = DBAPipeline()
            result = pipeline.run(task)

        # Should NOT have a second intent_classify result
        intent_stages = [s for s in result.stage_results
                         if s.stage == PipelineStage.INTENT_CLASSIFY]
        assert len(intent_stages) == 1


# ========================================================================
# E. 状态持久化测试
# ========================================================================

class TestTaskState:
    """Test task state persistence."""

    @pytest.fixture(autouse=True)
    def setup_tmp_db(self, tmp_path):
        from engine.task_state import set_state_db_path
        set_state_db_path(tmp_path / "test_state.db")
        yield
        set_state_db_path(None)

    def test_save_and_load_task(self):
        from engine.dba_loop import create_task, StepResult, PipelineStage, StageStatus
        from engine.task_state import save_task, load_task

        task = create_task("SELECT 1", "pg_test", "postgresql", task_id="state_001")
        task.risk_level = 0
        task.risk_label = "L0_READONLY"
        task.intent = {"intent": "query", "label": "数据查询"}
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY,
            status=StageStatus.PASSED,
            data={"intent": "query"},
            duration_ms=5,
        ))

        save_task(task)

        loaded = load_task("state_001")
        assert loaded is not None
        assert loaded.task_id == "state_001"
        assert loaded.sql == "SELECT 1"
        assert loaded.risk_level == 0
        assert loaded.intent["intent"] == "query"
        assert len(loaded.stage_results) == 1
        assert loaded.stage_results[0].stage == PipelineStage.INTENT_CLASSIFY

    def test_save_updates_existing(self):
        from engine.dba_loop import create_task, StepResult, PipelineStage, StageStatus
        from engine.task_state import save_task, load_task

        task = create_task("UPDATE t SET x=1", "pg_test", task_id="state_002")
        task.risk_level = 2
        save_task(task)

        # Update task
        task.approved = True
        task.stage_results.append(StepResult(
            stage=PipelineStage.APPROVAL,
            status=StageStatus.PASSED,
            data={"auto_approved": False},
        ))
        save_task(task)

        loaded = load_task("state_002")
        assert loaded.approved is True
        # Note: stages accumulate on each save — load checks latest state
        assert len(loaded.stage_results) >= 1

    def test_load_nonexistent_returns_none(self):
        from engine.task_state import load_task
        assert load_task("nonexistent_999") is None

    def test_list_tasks(self):
        from engine.dba_loop import create_task
        from engine.task_state import save_task, list_tasks

        for i in range(3):
            t = create_task(f"SELECT {i}", "pg_test", task_id=f"list_{i}")
            save_task(t)

        tasks = list_tasks()
        assert len(tasks) >= 3

    def test_list_tasks_filter_status(self):
        from engine.dba_loop import create_task, StepResult, PipelineStage, StageStatus
        from engine.task_state import save_task, list_tasks

        t1 = create_task("SELECT 1", "pg_test", task_id="filter_running")
        save_task(t1)

        t2 = create_task("SELECT 2", "pg_test", task_id="filter_done")
        t2.stage_results.append(StepResult(
            stage=PipelineStage.AUDIT, status=StageStatus.PASSED, data={},
        ))
        save_task(t2)

        running = list_tasks(status="running")
        assert any(t["task_id"] == "filter_running" for t in running)

    def test_get_task_status(self):
        from engine.dba_loop import create_task, StepResult, PipelineStage, StageStatus
        from engine.task_state import save_task, get_task_status

        task = create_task("SELECT 1", "pg_test", task_id="status_001")
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY,
            status=StageStatus.PASSED,
            data={}, duration_ms=5,
        ))
        save_task(task)

        status = get_task_status("status_001")
        assert status is not None
        assert status["task_id"] == "status_001"
        assert len(status["stages"]) >= 1

    def test_approve_blocked_task(self):
        from engine.dba_loop import create_task, StepResult, PipelineStage, StageStatus
        from engine.task_state import save_task, approve_task, load_task

        task = create_task("UPDATE t SET x=1", "pg_test", task_id="approve_001")
        task.stage_results.append(StepResult(
            stage=PipelineStage.APPROVAL, status=StageStatus.BLOCKED,
            data={}, error="等待审批",
        ))
        save_task(task)

        assert approve_task("approve_001") is True

        loaded = load_task("approve_001")
        assert loaded.approved is True

    def test_approve_non_blocked_returns_false(self):
        from engine.dba_loop import create_task
        from engine.task_state import save_task, approve_task

        task = create_task("SELECT 1", "pg_test", task_id="approve_002")
        save_task(task)
        assert approve_task("approve_002") is False

    def test_cleanup_expired(self):
        from engine.dba_loop import create_task
        from engine.task_state import save_task, cleanup_expired, list_tasks, _get_conn

        task = create_task("SELECT 1", "pg_test", task_id="old_001")
        save_task(task)

        # Manually set updated_at to 30 days ago
        conn = _get_conn()
        old_time = time.time() - 30 * 86400
        conn.execute("UPDATE tasks SET updated_at = ?, created_at = ? WHERE task_id = ?",
                      (old_time, old_time, "old_001"))
        conn.commit()
        conn.close()

        removed = cleanup_expired(days=7)
        assert removed >= 1

        tasks = list_tasks()
        assert not any(t["task_id"] == "old_001" for t in tasks)


# ========================================================================
# F. 端到端集成测试
# ========================================================================

class TestE2EPipeline:
    """End-to-end pipeline with state persistence."""

    @pytest.fixture(autouse=True)
    def setup_tmp_db(self, tmp_path):
        from engine.task_state import set_state_db_path
        set_state_db_path(tmp_path / "e2e_state.db")
        yield
        set_state_db_path(None)

    def test_pipeline_saves_state(self):
        """After pipeline run, task state is persisted."""
        from engine.dba_loop import DBAPipeline, create_task, StageStatus, PipelineStage, StepResult
        from engine.task_state import save_task, load_task

        task = create_task("SELECT 1", "pg_test", "postgresql", task_id="e2e_001")

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=5,
            )

            pipeline = DBAPipeline()
            result = pipeline.run(task)

        save_task(result)

        loaded = load_task("e2e_001")
        assert loaded is not None
        assert len(loaded.stage_results) >= 3

    def test_pipeline_resume_after_interruption(self):
        """Simulate interruption and resume from checkpoint."""
        from engine.dba_loop import (
            DBAPipeline, create_task, StepResult, PipelineStage, StageStatus,
        )
        from engine.task_state import save_task, load_task

        # Step 1: Run pipeline that gets "interrupted" at preflight
        task = create_task("SELECT * FROM users", "pg_test", task_id="resume_001")
        task.stage_results.append(StepResult(
            stage=PipelineStage.INTENT_CLASSIFY,
            status=StageStatus.PASSED,
            data={"intent": "query"},
        ))
        save_task(task)

        # Step 2: "Resume" by loading and continuing
        loaded = load_task("resume_001")
        assert loaded is not None
        assert len(loaded.stage_results) == 1  # Only intent done

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=5,
            )

            pipeline = DBAPipeline()
            result = pipeline.run(loaded)

        # Should have completed from preflight onwards (intent skipped)
        stages = [s.stage for s in result.stage_results]
        assert PipelineStage.INTENT_CLASSIFY in stages
        assert PipelineStage.PREFLIGHT in stages

    def test_pipeline_blocked_then_approved_then_resumed(self):
        """Full cycle: run→blocked→approve→resume→execute."""
        from engine.dba_loop import (
            DBAPipeline, create_task, StepResult, PipelineStage, StageStatus,
        )
        from engine.task_state import save_task, load_task, approve_task

        task = create_task(
            "UPDATE users SET name='x' WHERE id=1", "pg_test", "postgresql",
            task_id="block_resume_001",
        )

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dual_validator.run_dual_validation") as mock_dv, \
             patch("engine.dba_loop.DBAPipeline._stage_rollback_gen") as mock_rb:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            mock_dv.return_value = {"passed": True, "syntax": {"passed": True}, "performance": {"passed": True}, "errors": [], "suggestions": []}
            mock_rb.return_value = StepResult(
                stage=PipelineStage.ROLLBACK_GEN, status=StageStatus.PASSED,
                data={"rollback_sql": "-- rollback"},
            )

            pipeline = DBAPipeline()  # No approval callback → blocks
            result = pipeline.run(task)

        assert any(s.status == StageStatus.BLOCKED for s in result.stage_results)
        save_task(result)

        # Approve externally
        assert approve_task("block_resume_001") is True

        # Resume with approval callback
        loaded = load_task("block_resume_001")
        assert loaded.approved is True

        # Remove the BLOCKED stage result so pipeline retries approval
        loaded.stage_results = [
            s for s in loaded.stage_results
            if not (s.stage == PipelineStage.APPROVAL and s.status == StageStatus.BLOCKED)
        ]

        with patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=10,
            )

            pipeline2 = DBAPipeline(on_approval_needed=lambda t: t.approved)
            result2 = pipeline2.run(loaded)

        assert any(
            s.stage == PipelineStage.EXECUTE and s.status == StageStatus.PASSED
            for s in result2.stage_results
        )

    def test_run_pipeline_convenience(self):
        """Test the run_pipeline one-shot convenience function."""
        from engine.dba_loop import run_pipeline, StageStatus

        with patch("engine.preflight.run_preflight") as mock_pf, \
             patch("engine.dba_loop.DBAPipeline._stage_execute") as mock_exec:
            mock_pf.return_value = {"passed": True, "checks": [], "failures": [], "metadata": {}}
            from engine.dba_loop import StepResult, PipelineStage
            mock_exec.return_value = StepResult(
                stage=PipelineStage.EXECUTE, status=StageStatus.PASSED,
                data={"success": True}, duration_ms=5,
            )

            result = run_pipeline("SELECT 1", "pg_test", "postgresql")

        assert result.task_id.startswith("dba_")
        passed = [s for s in result.stage_results if s.status == StageStatus.PASSED]
        assert len(passed) >= 3
