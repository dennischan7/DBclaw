"""Phase 7 Tests — 零信任安全管控与五档人机协同。

TestRiskRules       — L0-L4风险分级引擎 (18 tests)
TestSafetyMode      — 五档人机协同模式 (17 tests)
TestApprovalManager — 审批流程管理器 (18 tests)
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Import helpers — dual-import pattern for package / standalone
# ---------------------------------------------------------------------------
_plugin_root = Path(__file__).resolve().parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))

from security.risk_rules import (
    RiskLevel,
    HARDCODED_ESCALATIONS,
    BASE_RISK_CLASSIFICATION,
    assess_risk,
    add_custom_rule,
    remove_custom_rule,
    list_custom_rules,
    get_risk_level_config,
    set_risk_rules_db_path,
    RiskAssessment,
)
from security.safety_mode import (
    SafetyMode,
    MODE_AUTO_APPROVE_THRESHOLD,
    READONLY_MODES,
    get_current_mode,
    switch_mode,
    lock_mode,
    unlock_mode,
    is_mode_locked,
    set_admin_password,
    verify_admin_password,
    has_admin_password,
    should_auto_approve,
    should_block_write,
    requires_rollback_review,
    get_approval_decision,
    get_mode_history,
    list_modes,
    set_safety_mode_db_path,
)
from security.approval_manager import (
    ApprovalStatus,
    ApprovalEventType,
    create_approval_request,
    approve_request,
    reject_request,
    modify_and_approve,
    get_request,
    get_pending_requests,
    get_request_history,
    get_audit_trail,
    is_approved,
    get_effective_sql,
    get_approval_stats,
    register_event_listener,
    clear_event_listeners,
    set_approval_db_path,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def isolate_security_dbs(tmp_path):
    """Isolate all security DBs to temp directory per test."""
    risk_db = tmp_path / "risk_rules.db"
    mode_db = tmp_path / "safety_mode.db"
    approval_db = tmp_path / "approval.db"

    set_risk_rules_db_path(risk_db)
    set_safety_mode_db_path(mode_db)
    set_approval_db_path(approval_db)
    clear_event_listeners()

    yield

    set_risk_rules_db_path(None)
    set_safety_mode_db_path(None)
    set_approval_db_path(None)
    clear_event_listeners()


# ===================================================================
# TestRiskRules — L0-L4 风险分级引擎
# ===================================================================

class TestRiskRules:
    """18 tests for risk_rules.py."""

    # --- RiskLevel Enum ---

    def test_risk_level_values(self):
        assert RiskLevel.L0_READONLY == 0
        assert RiskLevel.L1_LOW_DML == 1
        assert RiskLevel.L2_MEDIUM_BATCH == 2
        assert RiskLevel.L3_HIGH_DESTRUCTIVE == 3
        assert RiskLevel.L4_CATASTROPHIC == 4

    def test_risk_level_label(self):
        assert RiskLevel.L0_READONLY.label == "L0_READONLY"
        assert RiskLevel.L4_CATASTROPHIC.label == "L4_CATASTROPHIC"

    def test_risk_level_description(self):
        assert "只读" in RiskLevel.L0_READONLY.description
        assert "灾难" in RiskLevel.L4_CATASTROPHIC.description

    # --- Base Classification ---

    def test_base_classification_readonly(self):
        for op in ("SELECT", "SHOW", "DESCRIBE", "EXPLAIN"):
            assert BASE_RISK_CLASSIFICATION[op] == 0

    def test_base_classification_dml(self):
        assert BASE_RISK_CLASSIFICATION["INSERT"] == 1
        assert BASE_RISK_CLASSIFICATION["UPDATE"] == 2
        assert BASE_RISK_CLASSIFICATION["DELETE"] == 2

    def test_base_classification_destructive(self):
        assert BASE_RISK_CLASSIFICATION["DROP TABLE"] == 4
        assert BASE_RISK_CLASSIFICATION["DROP DATABASE"] == 4
        assert BASE_RISK_CLASSIFICATION["TRUNCATE"] == 3

    # --- Risk Assessment ---

    def test_assess_risk_readonly(self):
        result = assess_risk("SELECT * FROM users", operation="SELECT", ast_risk_level=0)
        assert result.risk_level == 0
        assert result.risk_label == "L0_READONLY"
        assert result.hardcoded_hit is False

    def test_assess_risk_preserves_ast_level(self):
        result = assess_risk("INSERT INTO t VALUES (1)", operation="INSERT", ast_risk_level=1)
        assert result.risk_level == 1
        assert result.base_level == 1

    def test_assess_risk_delete_no_where_hardcoded(self):
        result = assess_risk("DELETE FROM users", operation="DELETE", ast_risk_level=2)
        assert result.risk_level == 4
        assert result.hardcoded_hit is True
        assert any("HC-001" in r for r in result.escalation_reasons)

    def test_assess_risk_update_no_where_hardcoded(self):
        result = assess_risk("UPDATE users SET status = 0", operation="UPDATE", ast_risk_level=2)
        assert result.risk_level == 4
        assert result.hardcoded_hit is True

    def test_assess_risk_drop_database_hardcoded(self):
        result = assess_risk("DROP DATABASE mydb", operation="DROP DATABASE", ast_risk_level=4)
        assert result.risk_level == 4
        # AST already at L4, so hardcoded rule doesn't need to escalate further
        # but level is still correctly L4

    def test_assess_risk_drop_database_from_lower_base(self):
        """When AST underestimates, hardcoded rule catches it."""
        result = assess_risk("DROP DATABASE mydb", operation="DROP DATABASE", ast_risk_level=2)
        assert result.risk_level == 4
        assert result.hardcoded_hit is True

    def test_assess_risk_with_where_not_escalated(self):
        result = assess_risk(
            "DELETE FROM users WHERE id = 5", operation="DELETE", ast_risk_level=2,
        )
        assert result.risk_level == 2
        assert result.hardcoded_hit is False

    def test_assess_risk_production_escalation(self):
        result = assess_risk(
            "INSERT INTO t VALUES (1)", operation="INSERT",
            ast_risk_level=1, environment="production",
        )
        assert result.risk_level == 2
        assert "生产环境" in result.final_reason

    def test_assess_risk_monotonic_increase(self):
        """Risk can only be raised, never lowered."""
        result = assess_risk(
            "SELECT 1", operation="SELECT", ast_risk_level=3,
        )
        # ast_risk_level=3 even for SELECT — should not go down
        assert result.risk_level >= 3

    # --- Custom Rules ---

    def test_add_custom_rule(self):
        ok = add_custom_rule(
            rule_id="CR-001", name="Test rule",
            pattern=r"(?i)DELETE.*sensitive_table",
            target_level=4, reason="Sensitive table",
        )
        assert ok is True
        rules = list_custom_rules()
        assert len(rules) == 1
        assert rules[0]["rule_id"] == "CR-001"

    def test_custom_rule_applied(self):
        add_custom_rule(
            rule_id="CR-002", name="Custom escalation",
            pattern=r"(?i)sensitive_data",
            target_level=3, reason="Sensitive data table",
        )
        result = assess_risk(
            "SELECT * FROM sensitive_data", operation="SELECT", ast_risk_level=0,
        )
        assert result.risk_level == 3
        assert "CR-002" in result.custom_rules_hit

    def test_remove_custom_rule(self):
        add_custom_rule("CR-003", "Temp", r"temp", 2, "test")
        ok = remove_custom_rule("CR-003")
        assert ok is True
        assert len(list_custom_rules()) == 0

    def test_to_dict(self):
        result = assess_risk("SELECT 1", operation="SELECT", ast_risk_level=0)
        d = result.to_dict()
        assert "risk_level" in d
        assert "risk_label" in d
        assert "hardcoded_hit" in d


# ===================================================================
# TestSafetyMode — 五档人机协同模式
# ===================================================================

class TestSafetyMode:
    """17 tests for safety_mode.py."""

    # --- Enum ---

    def test_safety_mode_values(self):
        assert SafetyMode.READONLY_AUDIT == 0
        assert SafetyMode.ULTRA_CONSERVATIVE == 1
        assert SafetyMode.MODERATE == 2
        assert SafetyMode.AGGRESSIVE == 3
        assert SafetyMode.MADMAN == 4

    def test_display_names(self):
        assert "只读" in SafetyMode.READONLY_AUDIT.display_name
        assert "保守" in SafetyMode.ULTRA_CONSERVATIVE.display_name
        assert "适度" in SafetyMode.MODERATE.display_name
        assert "激进" in SafetyMode.AGGRESSIVE.display_name
        assert "疯子" in SafetyMode.MADMAN.display_name

    def test_descriptions(self):
        for m in SafetyMode:
            assert len(m.description) > 5

    # --- Default State ---

    def test_default_mode_is_moderate(self):
        assert get_current_mode() == SafetyMode.MODERATE

    # --- Mode Switching ---

    def test_switch_to_conservative(self):
        result = switch_mode(SafetyMode.ULTRA_CONSERVATIVE, changed_by="admin")
        assert result["success"] is True
        assert get_current_mode() == SafetyMode.ULTRA_CONSERVATIVE

    def test_switch_to_aggressive(self):
        result = switch_mode(SafetyMode.AGGRESSIVE, changed_by="dev")
        assert result["success"] is True
        assert get_current_mode() == SafetyMode.AGGRESSIVE

    def test_switch_to_madman_requires_password(self):
        result = switch_mode(SafetyMode.MADMAN, changed_by="user")
        assert result["success"] is False
        assert "密码" in result["error"]

    def test_switch_to_madman_with_password(self):
        set_admin_password("admin123456")
        result = switch_mode(
            SafetyMode.MADMAN, changed_by="admin",
            admin_password="admin123456",
        )
        assert result["success"] is True
        assert get_current_mode() == SafetyMode.MADMAN

    def test_switch_to_madman_wrong_password(self):
        set_admin_password("correct_pwd")
        result = switch_mode(
            SafetyMode.MADMAN, changed_by="admin",
            admin_password="wrong_pwd",
        )
        assert result["success"] is False

    # --- Mode Lock ---

    def test_lock_mode(self):
        lock_mode("admin")
        assert is_mode_locked() is True
        # Non-admin cannot switch
        result = switch_mode(SafetyMode.AGGRESSIVE, changed_by="user")
        assert result["success"] is False
        assert "锁定" in result["error"]

    def test_admin_can_switch_when_locked(self):
        lock_mode("admin")
        result = switch_mode(SafetyMode.ULTRA_CONSERVATIVE, changed_by="admin")
        assert result["success"] is True

    def test_unlock_mode(self):
        lock_mode("admin")
        unlock_mode()
        assert is_mode_locked() is False

    # --- Admin Password ---

    def test_set_and_verify_password(self):
        assert has_admin_password() is False
        set_admin_password("secure_pass123")
        assert has_admin_password() is True
        assert verify_admin_password("secure_pass123") is True
        assert verify_admin_password("wrong") is False

    def test_password_too_short(self):
        ok = set_admin_password("123")
        assert ok is False

    # --- Decision Engine ---

    def test_moderate_mode_decisions(self):
        # Default mode (MODERATE): auto-approve L0/L1, human_confirm L2+
        assert should_auto_approve(0) is True
        assert should_auto_approve(1) is True
        assert should_auto_approve(2) is False
        assert should_auto_approve(3) is False

    def test_readonly_blocks_writes(self):
        switch_mode(SafetyMode.READONLY_AUDIT)
        assert should_block_write(0) is False
        assert should_block_write(1) is True
        assert should_block_write(2) is True

    def test_get_approval_decision_moderate(self):
        dec = get_approval_decision(2)
        assert dec["action"] == "human_confirm"
        assert dec["require_approval"] is True
        assert "适度" in dec["mode"]

    # --- History ---

    def test_mode_history(self):
        switch_mode(SafetyMode.AGGRESSIVE, changed_by="dev", reason="testing")
        switch_mode(SafetyMode.MODERATE, changed_by="admin", reason="back to default")
        history = get_mode_history()
        assert len(history) >= 2
        assert history[0]["changed_by"] == "admin"

    def test_list_modes(self):
        modes = list_modes()
        assert len(modes) == 5
        active = [m for m in modes if m["active"]]
        assert len(active) == 1


# ===================================================================
# TestApprovalManager — 审批流程管理器
# ===================================================================

class TestApprovalManager:
    """18 tests for approval_manager.py."""

    # --- Create Request ---

    def test_create_request(self):
        req = create_approval_request(
            task_id="task-001",
            sql="ALTER TABLE users ADD COLUMN email VARCHAR(255)",
            risk_level=2,
            risk_label="L2_MEDIUM_BATCH",
            operation_type="ALTER TABLE ADD",
            instance_name="pg_test",
            tables_affected=["users"],
            validation_summary="校验通过",
            created_by="system",
        )
        assert req.request_id.startswith("apr-")
        assert req.status == ApprovalStatus.PENDING
        assert req.sql == "ALTER TABLE users ADD COLUMN email VARCHAR(255)"

    def test_create_request_with_rollback(self):
        req = create_approval_request(
            task_id="task-002",
            sql="ALTER TABLE orders ADD COLUMN status INT",
            risk_level=2,
            rollback_sql="ALTER TABLE orders DROP COLUMN status",
        )
        assert req.rollback_sql == "ALTER TABLE orders DROP COLUMN status"

    # --- Approve ---

    def test_approve_request(self):
        req = create_approval_request(
            task_id="task-003", sql="DROP INDEX idx_old", risk_level=3,
        )
        result = approve_request(req.request_id, reviewer="admin", comment="确认安全")
        assert result["success"] is True
        assert result["request"]["status"] == "approved"
        assert is_approved(req.request_id) is True

    def test_approve_nonexistent(self):
        result = approve_request("nonexistent", reviewer="admin")
        assert result["success"] is False
        assert "不存在" in result["error"]

    def test_cannot_approve_twice(self):
        req = create_approval_request(task_id="task-004", sql="SELECT 1", risk_level=2)
        approve_request(req.request_id, "admin")
        result = approve_request(req.request_id, "admin")
        assert result["success"] is False

    # --- Reject ---

    def test_reject_request(self):
        req = create_approval_request(task_id="task-005", sql="TRUNCATE orders", risk_level=3)
        result = reject_request(req.request_id, reviewer="admin", comment="风险太高")
        assert result["success"] is True
        assert result["request"]["status"] == "rejected"
        assert is_approved(req.request_id) is False

    def test_reject_requires_comment(self):
        req = create_approval_request(task_id="task-006", sql="DROP TABLE t", risk_level=4)
        result = reject_request(req.request_id, reviewer="admin", comment="")
        assert result["success"] is False
        assert "原因" in result["error"]

    def test_cannot_reject_approved(self):
        req = create_approval_request(task_id="task-007", sql="SELECT 1", risk_level=2)
        approve_request(req.request_id, "admin")
        result = reject_request(req.request_id, "admin", "changed mind")
        assert result["success"] is False

    # --- Modify and Approve ---

    def test_modify_and_approve(self):
        req = create_approval_request(
            task_id="task-008",
            sql="DELETE FROM users",
            risk_level=4,
        )
        result = modify_and_approve(
            req.request_id, reviewer="admin",
            modified_sql="DELETE FROM users WHERE status = 'inactive'",
            comment="添加WHERE条件",
        )
        assert result["success"] is True
        assert result["request"]["status"] == "modified"

    def test_get_effective_sql_original(self):
        req = create_approval_request(task_id="task-009", sql="UPDATE t SET x=1 WHERE id=5", risk_level=2)
        approve_request(req.request_id, "admin")
        assert get_effective_sql(req.request_id) == "UPDATE t SET x=1 WHERE id=5"

    def test_get_effective_sql_modified(self):
        req = create_approval_request(task_id="task-010", sql="DELETE FROM t", risk_level=4)
        modify_and_approve(req.request_id, "admin", "DELETE FROM t WHERE id=1", "safe ver")
        assert get_effective_sql(req.request_id) == "DELETE FROM t WHERE id=1"

    def test_modify_empty_sql_fails(self):
        req = create_approval_request(task_id="task-011", sql="X", risk_level=2)
        result = modify_and_approve(req.request_id, "admin", "", "no sql")
        assert result["success"] is False

    # --- Pending Requests ---

    def test_get_pending_requests(self):
        create_approval_request(task_id="task-012", sql="S1", risk_level=2)
        create_approval_request(task_id="task-013", sql="S2", risk_level=3)
        pending = get_pending_requests()
        assert len(pending) == 2

    # --- Audit Trail ---

    def test_audit_trail_immutable(self):
        req = create_approval_request(task_id="task-014", sql="DROP INDEX idx", risk_level=3)
        approve_request(req.request_id, "admin", "ok")
        trail = get_audit_trail(req.request_id)
        assert len(trail) == 2  # created + approved
        assert trail[0]["action"] == "created"
        assert trail[1]["action"] == "approved"

    def test_audit_trail_reject(self):
        req = create_approval_request(task_id="task-015", sql="TRUNCATE t", risk_level=3)
        reject_request(req.request_id, "admin", "too risky")
        trail = get_audit_trail(req.request_id)
        assert len(trail) == 2
        assert trail[1]["action"] == "rejected"
        assert "too risky" in trail[1]["detail"]

    # --- SSE Events ---

    def test_sse_event_emitted_on_create(self):
        events = []
        register_event_listener(lambda e: events.append(e))
        create_approval_request(task_id="task-016", sql="ALTER TABLE t ADD x INT", risk_level=2)
        assert len(events) == 1
        assert events[0]["event"] == ApprovalEventType.APPROVAL_REQUESTED.value

    def test_sse_event_emitted_on_approve(self):
        events = []
        register_event_listener(lambda e: events.append(e))
        req = create_approval_request(task_id="task-017", sql="S", risk_level=2)
        approve_request(req.request_id, "admin")
        assert len(events) == 2  # created + approved
        assert events[1]["event"] == ApprovalEventType.APPROVAL_APPROVED.value

    # --- Stats ---

    def test_approval_stats(self):
        create_approval_request(task_id="t1", sql="S1", risk_level=2)
        req2 = create_approval_request(task_id="t2", sql="S2", risk_level=3)
        approve_request(req2.request_id, "admin")
        stats = get_approval_stats()
        assert stats["total"] == 2
        assert stats["pending"] == 1
        assert stats["approved"] == 1

    # --- To Dict / SSE ---

    def test_request_to_dict(self):
        req = create_approval_request(
            task_id="task-018", sql="SELECT 1", risk_level=0,
            tables_affected=["t1", "t2"],
        )
        d = req.to_dict()
        assert d["request_id"] == req.request_id
        assert d["tables_affected"] == ["t1", "t2"]

    def test_request_to_sse_event(self):
        req = create_approval_request(task_id="task-019", sql="SELECT 1", risk_level=0)
        sse = req.to_sse_event(ApprovalEventType.APPROVAL_REQUESTED)
        assert "event" in sse
        assert "data" in sse
        assert sse["data"]["request_id"] == req.request_id
