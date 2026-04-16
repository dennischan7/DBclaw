"""Phase 6 Tests — 自进化DBA技能体系。

TestSkillManager:  14 tests — 内置注册/权限/版本/启禁/统计/草案/补丁
TestSkillGenerator: 10 tests — 触发评估/草案生成/确认/拒绝
TestSkillOptimizer: 10 tests — 执行记录/评估/补丁生成/确认
"""

import os
import sys
import json
import time
import pytest
import sqlite3
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure plugin root and skill_engine are importable
_plugin_root = Path(__file__).parent.parent
if str(_plugin_root) not in sys.path:
    sys.path.insert(0, str(_plugin_root))


# ============================================================
# Fixtures
# ============================================================

@pytest.fixture(autouse=True)
def isolate_skill_db(tmp_path):
    """Isolate skill_manager DB per test."""
    from skill_engine.skill_manager import set_skill_db_path
    import skill_engine.skill_manager as sm
    # Reset globals
    sm._CONN = None
    sm._DB_PATH = None
    set_skill_db_path(tmp_path / "skill.db")
    yield tmp_path
    # Cleanup
    if sm._CONN is not None:
        sm._CONN.close()
        sm._CONN = None
    sm._DB_PATH = None


# ============================================================
# TestSkillManager
# ============================================================

class TestSkillManager:

    def test_builtin_registration(self):
        from skill_engine.skill_manager import list_skills, UserRole
        skills = list_skills(user_role=UserRole.ADMIN)
        names = [s["name"] for s in skills]
        assert "dba-sql-safe" in names
        assert "dba-ddl-change" in names
        assert "dba-health-check" in names
        assert "dba-index-optimize" in names
        assert "dba-troubleshoot" in names
        assert len(names) == 5

    def test_get_skill(self):
        from skill_engine.skill_manager import get_skill
        skill = get_skill("dba-sql-safe")
        assert skill is not None
        assert skill["category"] == "query"
        assert skill["risk_level"] == 0
        assert skill["source"] == "builtin"

    def test_get_skill_nonexistent(self):
        from skill_engine.skill_manager import get_skill
        assert get_skill("nonexistent") is None

    def test_permission_admin(self):
        from skill_engine.skill_manager import list_skills, UserRole
        skills = list_skills(user_role=UserRole.ADMIN)
        # Admin sees all 5 built-in skills
        assert len(skills) == 5

    def test_permission_developer(self):
        from skill_engine.skill_manager import list_skills, UserRole
        skills = list_skills(user_role=UserRole.DEVELOPER)
        names = [s["name"] for s in skills]
        # Developer sees all 5 (min_role=readonly or developer, ≤ DEVELOPER)
        assert "dba-sql-safe" in names       # readonly
        assert "dba-ddl-change" in names     # developer
        assert "dba-health-check" in names   # readonly
        assert "dba-index-optimize" in names # developer
        assert "dba-troubleshoot" in names   # readonly

    def test_permission_readonly(self):
        from skill_engine.skill_manager import list_skills, UserRole
        skills = list_skills(user_role=UserRole.READONLY)
        names = [s["name"] for s in skills]
        # Readonly only sees readonly skills
        assert "dba-sql-safe" in names
        assert "dba-health-check" in names
        assert "dba-troubleshoot" in names
        # Developer-only skills excluded
        assert "dba-ddl-change" not in names
        assert "dba-index-optimize" not in names

    def test_check_permission(self):
        from skill_engine.skill_manager import check_permission, UserRole
        assert check_permission(UserRole.ADMIN, "dba-ddl-change") is True
        assert check_permission(UserRole.DEVELOPER, "dba-ddl-change") is True
        assert check_permission(UserRole.READONLY, "dba-ddl-change") is False
        assert check_permission(UserRole.READONLY, "dba-sql-safe") is True

    def test_enable_disable(self):
        from skill_engine.skill_manager import (
            enable_skill, disable_skill, get_skill, check_permission, UserRole,
        )
        assert disable_skill("dba-sql-safe") is True
        skill = get_skill("dba-sql-safe")
        assert skill["enabled"] == 0
        # Disabled skill not accessible to anyone
        assert check_permission(UserRole.ADMIN, "dba-sql-safe") is False
        # Re-enable
        assert enable_skill("dba-sql-safe") is True
        assert check_permission(UserRole.ADMIN, "dba-sql-safe") is True

    def test_version_management(self):
        from skill_engine.skill_manager import (
            save_version, get_versions, get_latest_version, rollback_version,
        )
        assert save_version("dba-sql-safe", "v1 content", "1.0.0", "Initial") is True
        assert save_version("dba-sql-safe", "v1.1 content", "1.1.0", "Update") is True
        # Latest version is 1.1.0
        assert get_latest_version("dba-sql-safe") == "1.1.0"
        versions = get_versions("dba-sql-safe")
        assert len(versions) == 2
        assert versions[0]["version"] == "1.1.0"  # newest first
        # Rollback to 1.0.0
        assert rollback_version("dba-sql-safe", "1.0.0") is True
        assert get_latest_version("dba-sql-safe") == "1.0.0"

    def test_version_duplicate_rejected(self):
        from skill_engine.skill_manager import save_version
        assert save_version("dba-sql-safe", "content", "2.0.0") is True
        assert save_version("dba-sql-safe", "content", "2.0.0") is False

    def test_execution_stats(self):
        from skill_engine.skill_manager import record_execution, get_execution_stats
        record_execution("dba-sql-safe", "t1", success=True, duration_ms=100)
        record_execution("dba-sql-safe", "t2", success=True, duration_ms=200)
        record_execution("dba-sql-safe", "t3", success=False, duration_ms=50, error="timeout")
        stats = get_execution_stats("dba-sql-safe")
        assert stats["total"] == 3
        assert stats["successes"] == 2
        assert abs(stats["success_rate"] - 2/3) < 0.01
        assert stats["avg_duration_ms"] > 0

    def test_execution_stats_empty(self):
        from skill_engine.skill_manager import get_execution_stats
        stats = get_execution_stats("nonexistent")
        assert stats["total"] == 0
        assert stats["success_rate"] == 0.0

    def test_register_skill(self):
        from skill_engine.skill_manager import register_skill, get_skill
        assert register_skill(
            name="my-custom-skill",
            display_name="Custom Skill",
            description="Test skill",
            category="custom",
            risk_level=2,
            min_role="admin",
        ) is True
        skill = get_skill("my-custom-skill")
        assert skill is not None
        assert skill["risk_level"] == 2
        assert skill["min_role"] == "admin"
        # Duplicate rejected
        assert register_skill(name="my-custom-skill", display_name="Dup") is False

    def test_draft_lifecycle(self, tmp_path):
        from skill_engine.skill_manager import (
            save_draft, get_pending_drafts, get_draft,
            confirm_draft, reject_draft, get_skill,
        )
        # Save a draft
        save_draft("d1", "test-skill-1", "# Skill Content", "repeated_success", ["e1"])
        save_draft("d2", "test-skill-2", "# Skill 2", "self_repair")

        drafts = get_pending_drafts()
        assert len(drafts) == 2

        # Confirm d1 — installs as a skill
        assert confirm_draft("d1") is True
        skill = get_skill("test-skill-1")
        assert skill is not None
        assert skill["source"] == "generated"
        # File written
        gen_dir = tmp_path / "generated_skills"
        assert (gen_dir / "test-skill-1.md").exists()
        # Draft no longer pending
        assert get_draft("d1")["status"] == "confirmed"

        # Reject d2
        assert reject_draft("d2") is True
        assert get_draft("d2")["status"] == "rejected"

        # No more pending
        assert len(get_pending_drafts()) == 0

    def test_patch_lifecycle(self, tmp_path):
        from skill_engine.skill_manager import (
            save_patch, get_pending_patches, get_patch,
            confirm_patch, reject_patch, get_latest_version,
            register_skill,
        )
        # Register a generated skill first
        register_skill("gen-skill", "Generated", source="generated", file_name="gen-skill.md")
        # Create the file so confirm_patch can write to it
        gen_dir = tmp_path / "generated_skills"
        gen_dir.mkdir(exist_ok=True)
        (gen_dir / "gen-skill.md").write_text("old content", encoding="utf-8")

        # Save patches
        save_patch("p1", "gen-skill", "1.0.0", "# improved content", "fix errors", {"key": "val"})
        save_patch("p2", "gen-skill", "1.0.0", "# another patch", "add docs")

        assert len(get_pending_patches()) == 2

        # Confirm p1 — version increments 1.0.0 → 1.0.1
        assert confirm_patch("p1") is True
        assert get_latest_version("gen-skill") == "1.0.1"
        assert get_patch("p1")["status"] == "confirmed"

        # File updated
        assert "improved content" in (gen_dir / "gen-skill.md").read_text(encoding="utf-8")

        # Reject p2
        assert reject_patch("p2") is True
        assert get_patch("p2")["status"] == "rejected"


# ============================================================
# TestSkillGenerator
# ============================================================

class TestSkillGenerator:

    def test_no_trigger_for_failed_task(self):
        from skill_engine.skill_generator import evaluate_trigger
        result = evaluate_trigger({"success": False, "category": "optimization"})
        assert result is None

    def test_trigger_self_repair(self):
        from skill_engine.skill_generator import evaluate_trigger, TriggerType
        result = evaluate_trigger({
            "success": True,
            "category": "pitfall",
            "rewrite_count": 2,
        })
        assert result == TriggerType.SELF_REPAIR

    def test_trigger_user_correction(self):
        from skill_engine.skill_generator import evaluate_trigger, TriggerType
        result = evaluate_trigger({
            "success": True,
            "category": "best_practice",
            "rewrite_count": 0,
            "user_corrected": True,
        })
        assert result == TriggerType.USER_CORRECTION

    def test_trigger_repeated_success(self):
        """Mock L3 experience to have ≥2 confirmed entries."""
        from skill_engine.skill_generator import evaluate_trigger, TriggerType

        mock_experiences = [
            {"status": "confirmed", "title": "exp1"},
            {"status": "confirmed", "title": "exp2"},
        ]
        with patch("skill_engine.skill_generator.list_by_category",
                    create=True) as mock_list:
            # Patch the import inside _check_repeated_success
            import skill_engine.skill_generator as sg
            original_check = sg._check_repeated_success

            def patched_check(category):
                if category == "optimization":
                    return len(mock_experiences) >= 2
                return False

            sg._check_repeated_success = patched_check
            try:
                result = evaluate_trigger({
                    "success": True,
                    "category": "optimization",
                    "rewrite_count": 0,
                })
                assert result == TriggerType.REPEATED_SUCCESS
            finally:
                sg._check_repeated_success = original_check

    def test_no_trigger_no_conditions(self):
        from skill_engine.skill_generator import evaluate_trigger
        result = evaluate_trigger({
            "success": True,
            "category": "general",  # not in _DBA_CATEGORIES
            "rewrite_count": 0,
            "user_corrected": False,
        })
        assert result is None

    def test_generate_draft_creates_pending(self):
        from skill_engine.skill_generator import generate_draft, TriggerType
        from skill_engine.skill_manager import get_pending_drafts, get_draft

        draft_id = generate_draft(
            trigger_type=TriggerType.SELF_REPAIR,
            task_data={
                "category": "ddl_workflow",
                "sql": "ALTER TABLE users ADD COLUMN age INT",
                "dialect": "postgresql",
            },
        )
        assert draft_id.startswith("draft_")
        drafts = get_pending_drafts()
        assert len(drafts) == 1
        assert drafts[0]["trigger_reason"] == "self_repair"

    def test_build_skill_content_has_frontmatter(self):
        from skill_engine.skill_generator import _build_skill_content, TriggerType
        content = _build_skill_content(
            {"category": "optimization", "sql": "SELECT 1", "dialect": "mysql"},
            TriggerType.REPEATED_SUCCESS,
        )
        assert content.startswith("---")
        assert "version: 1.0.0" in content
        assert "auto-generated" in content
        assert "SELECT 1" in content
        assert "mysql" in content

    def test_build_skill_content_safety_rules(self):
        from skill_engine.skill_generator import _build_skill_content, TriggerType
        content = _build_skill_content(
            {"category": "pitfall"}, TriggerType.SELF_REPAIR,
        )
        assert "sql_validate" in content
        assert "回滚脚本" in content
        assert "审计日志" in content

    def test_derive_skill_name(self):
        from skill_engine.skill_generator import _derive_skill_name
        name = _derive_skill_name({"category": "ddl_workflow", "intent": "ddl_workflow"})
        assert name.startswith("dba-auto-ddl_workflow-")

    def test_draft_confirm_installs_skill(self, tmp_path):
        from skill_engine.skill_generator import generate_draft, TriggerType
        from skill_engine.skill_manager import confirm_draft, get_pending_drafts, get_skill

        draft_id = generate_draft(
            TriggerType.USER_CORRECTION,
            {"category": "optimization", "sql": "CREATE INDEX idx ON t(c)"},
        )
        assert confirm_draft(draft_id) is True
        # No more pending
        assert len(get_pending_drafts()) == 0


# ============================================================
# TestSkillOptimizer
# ============================================================

class TestSkillOptimizer:

    def test_record_execution(self):
        from skill_engine.skill_optimizer import record_execution
        from skill_engine.skill_manager import get_execution_stats
        record_execution("dba-sql-safe", "t1", success=True, duration_ms=100)
        stats = get_execution_stats("dba-sql-safe")
        assert stats["total"] == 1

    def test_evaluate_insufficient_data(self):
        from skill_engine.skill_optimizer import evaluate_effectiveness, record_execution
        record_execution("dba-sql-safe", success=True, duration_ms=100)
        result = evaluate_effectiveness("dba-sql-safe")
        assert result["needs_optimization"] is False
        assert "数据不足" in result["reasons"][0]

    def test_evaluate_good_skill(self):
        from skill_engine.skill_optimizer import evaluate_effectiveness, record_execution
        for i in range(5):
            record_execution("dba-sql-safe", f"t{i}", success=True, duration_ms=100)
        result = evaluate_effectiveness("dba-sql-safe")
        assert result["needs_optimization"] is False
        assert result["success_rate"] == 1.0

    def test_evaluate_needs_optimization(self):
        from skill_engine.skill_optimizer import evaluate_effectiveness, record_execution
        # 2 successes, 3 failures → 40% success rate
        record_execution("dba-sql-safe", "t1", success=True, duration_ms=100)
        record_execution("dba-sql-safe", "t2", success=True, duration_ms=100)
        record_execution("dba-sql-safe", "t3", success=False, duration_ms=50, error="err1")
        record_execution("dba-sql-safe", "t4", success=False, duration_ms=50, error="err2")
        record_execution("dba-sql-safe", "t5", success=False, duration_ms=50, error="err3")
        result = evaluate_effectiveness("dba-sql-safe")
        assert result["needs_optimization"] is True
        assert result["success_rate"] < 0.8
        assert "成功率偏低" in result["reasons"][0]
        assert "近期失败" in result["reasons"][1]

    def test_generate_patch_no_need(self):
        from skill_engine.skill_optimizer import generate_patch, record_execution
        # All successes → no patch needed
        for i in range(5):
            record_execution("dba-sql-safe", f"t{i}", success=True, duration_ms=100)
        result = generate_patch("dba-sql-safe")
        assert result is None

    def test_generate_patch_with_improvements(self, tmp_path):
        from skill_engine.skill_optimizer import generate_patch
        from skill_engine.skill_manager import get_pending_patches

        # Create a skill file for content reading
        skills_dir = Path(__file__).parent.parent / "skills"
        # The builtin skill exists, so get_skill_content will read it

        patch_id = generate_patch("dba-sql-safe", improvements={
            "reasons": ["New best practice discovered"],
            "additions": ["Use LIMIT for pagination queries"],
        })
        assert patch_id is not None
        assert patch_id.startswith("patch_")
        patches = get_pending_patches()
        assert len(patches) == 1
        assert "New best practice" in patches[0]["change_summary"]

    def test_apply_improvements(self):
        from skill_engine.skill_optimizer import _apply_improvements
        original = "# Skill Content\nSome instructions."
        evaluation = {"success_rate": 0.5, "recent_errors": ["timeout error", "conn refused"]}
        result = _apply_improvements(original, evaluation)
        assert "已知问题与处理" in result
        assert "timeout error" in result
        assert "conn refused" in result

    def test_apply_improvements_with_explicit(self):
        from skill_engine.skill_optimizer import _apply_improvements
        result = _apply_improvements(
            "# Content", {},
            improvements={"additions": ["Always use EXPLAIN before large queries"]},
        )
        assert "优化补充" in result
        assert "EXPLAIN" in result

    def test_apply_improvements_no_change(self):
        from skill_engine.skill_optimizer import _apply_improvements
        result = _apply_improvements("# Content", {"success_rate": 1.0})
        assert result == "# Content"

    def test_confirm_optimization(self, tmp_path):
        from skill_engine.skill_optimizer import (
            record_execution, generate_patch, confirm_optimization,
            get_pending_patches,
        )
        from skill_engine.skill_manager import (
            register_skill, get_latest_version,
        )
        # Register a generated skill
        register_skill("opt-test", "Opt Test", source="generated", file_name="opt-test.md")
        gen_dir = tmp_path / "generated_skills"
        gen_dir.mkdir(exist_ok=True)
        (gen_dir / "opt-test.md").write_text("# Original", encoding="utf-8")

        # Generate patch with explicit improvements
        patch_id = generate_patch("opt-test", improvements={
            "reasons": ["Better error handling"],
            "additions": ["Add retry logic for transient errors"],
        })
        assert patch_id is not None
        assert confirm_optimization(patch_id) is True
        assert get_latest_version("opt-test") == "1.0.1"
        assert len(get_pending_patches()) == 0
