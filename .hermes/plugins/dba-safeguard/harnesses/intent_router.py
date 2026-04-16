"""意图分类与路由引擎 — 识别用户需求、目标数据库、风险预判，自动挂载规范。

核心能力:
  - 双路径分类: 关键词快速匹配 (SQL语句) + LLM fallback (自然语言)
  - 数据库类型+版本识别: 从上下文或配置推断目标数据库
  - 风险预分级: 根据意图类型预判风险等级
  - 规范自动挂载: 根据分类结果加载对应 harness 和 library 路径
  - 规则热重载: taxonomy YAML 修改后自动生效
"""

from __future__ import annotations

import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import yaml

logger = logging.getLogger("dba_safeguard.harnesses.intent_router")

_TAXONOMY_PATH = Path(__file__).parent / "taxonomy" / "intent_classification.yaml"

# Cached taxonomy config (with mtime check for hot-reload)
_taxonomy_cache: Optional[Dict[str, Any]] = None
_taxonomy_mtime: float = 0.0


# ============================================================
# Public API
# ============================================================

def classify_intent(
    user_message: str,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Classify a user message into DBA intent category.

    Args:
        user_message: The user's input text
        context: Optional context (active_instance, dialect, session history)

    Returns:
        {
          "intent": str,           # intent key (e.g. "query", "dml_update")
          "label": str,            # human label (e.g. "数据更新")
          "confidence": float,     # 0.0 - 1.0
          "method": str,           # "keyword" or "llm"
          "risk_preset": int,      # pre-judged risk level
          "db_type": str | None,   # detected database type
          "db_version": str | None,
          "required_tools": list,
          "workflow": str | None,
          "harness_files": list,   # auto-mounted harness file paths
        }
    """
    taxonomy = _load_taxonomy()
    context = context or {}

    # Step 1: Try keyword-based fast classification
    result = _classify_by_keywords(user_message, taxonomy)

    # Step 2: If low confidence, try LLM classification (stub for now)
    if result["confidence"] < 0.6:
        result = _classify_fallback(user_message, taxonomy, result)

    # Step 3: Detect database type and version
    db_type, db_version = _detect_db_type(user_message, taxonomy, context)
    result["db_type"] = db_type or context.get("dialect")
    result["db_version"] = db_version or context.get("db_version")

    # Step 4: Enrich with category metadata
    categories = taxonomy.get("intent_categories", {})
    cat = categories.get(result["intent"], {})
    result["label"] = cat.get("label", result["intent"])
    result["risk_preset"] = cat.get("risk_preset", 0)
    result["required_tools"] = cat.get("required_tools", [])
    result["workflow"] = cat.get("workflow")

    # Step 5: Apply escalation rules from category
    escalation_rules = cat.get("escalation_rules", [])
    for rule in escalation_rules:
        if _check_escalation(user_message, rule):
            result["risk_preset"] = max(result["risk_preset"], rule.get("target_level", result["risk_preset"]))

    # Step 6: Mount harness files
    result["harness_files"] = _resolve_harness_files(result["workflow"], result["intent"])

    return result


def get_routing_context(
    intent_result: Dict[str, Any],
) -> Dict[str, Any]:
    """Build routing context for downstream tool orchestration.

    Translates classification result into actionable instructions
    for the agent loop (which tools to call, in what order).
    """
    tools = intent_result.get("required_tools", [])
    risk = intent_result.get("risk_preset", 0)
    workflow = intent_result.get("workflow")

    routing = {
        "tool_sequence": tools,
        "risk_level": risk,
        "requires_approval": risk >= 2,
        "requires_rollback": risk >= 2,
        "requires_explain": risk >= 1 or intent_result["intent"] in ("query", "optimize"),
        "requires_library_search": "library_search" in tools,
        "workflow_file": None,
        "db_type": intent_result.get("db_type"),
        "db_version": intent_result.get("db_version"),
    }

    # Resolve workflow stage file
    if workflow:
        stage_file = _get_stage_file(workflow)
        if stage_file:
            routing["workflow_file"] = str(stage_file)

    return routing


def list_intents() -> List[Dict[str, str]]:
    """List all available intent categories (for help/debug)."""
    taxonomy = _load_taxonomy()
    categories = taxonomy.get("intent_categories", {})
    return [
        {"key": k, "label": v.get("label", k), "description": v.get("description", "")}
        for k, v in categories.items()
    ]


# ============================================================
# Taxonomy Loading (hot-reload aware)
# ============================================================

def _load_taxonomy() -> Dict[str, Any]:
    """Load taxonomy YAML with mtime-based hot-reload."""
    global _taxonomy_cache, _taxonomy_mtime

    if not _TAXONOMY_PATH.exists():
        logger.warning("Taxonomy file not found: %s", _TAXONOMY_PATH)
        return {}

    current_mtime = _TAXONOMY_PATH.stat().st_mtime
    if _taxonomy_cache is not None and current_mtime == _taxonomy_mtime:
        return _taxonomy_cache

    try:
        with open(_TAXONOMY_PATH, encoding="utf-8") as f:
            _taxonomy_cache = yaml.safe_load(f) or {}
        _taxonomy_mtime = current_mtime
        logger.debug("Taxonomy loaded/reloaded from %s", _TAXONOMY_PATH)
    except Exception as e:
        logger.error("Failed to load taxonomy: %s", e)
        if _taxonomy_cache is None:
            _taxonomy_cache = {}

    return _taxonomy_cache


def reload_taxonomy() -> bool:
    """Force taxonomy reload (for hot-reload mechanism)."""
    global _taxonomy_cache, _taxonomy_mtime
    _taxonomy_cache = None
    _taxonomy_mtime = 0.0
    try:
        _load_taxonomy()
        return True
    except Exception:
        return False


# ============================================================
# Keyword Classification (fast path)
# ============================================================

def _classify_by_keywords(
    text: str,
    taxonomy: Dict[str, Any],
) -> Dict[str, Any]:
    """Fast classification using regex keyword rules."""
    result = {
        "intent": "general",
        "label": "通用咨询",
        "confidence": 0.3,
        "method": "keyword",
        "risk_preset": 0,
        "db_type": None,
        "db_version": None,
        "required_tools": [],
        "workflow": None,
        "harness_files": [],
    }

    rules = taxonomy.get("keyword_rules", [])
    best_confidence = 0.0

    for rule in rules:
        patterns = rule.get("patterns", [])
        for pattern in patterns:
            try:
                if re.search(pattern, text, re.IGNORECASE):
                    confidence = rule.get("confidence", 0.5)
                    if confidence > best_confidence:
                        best_confidence = confidence
                        result["intent"] = rule["intent"]
                        result["confidence"] = confidence
                    break  # matched this rule, move to next
            except re.error:
                logger.debug("Invalid regex pattern: %s", pattern)

    return result


# ============================================================
# LLM Fallback Classification (stub — will integrate with Hermes)
# ============================================================

def _classify_fallback(
    text: str,
    taxonomy: Dict[str, Any],
    current: Dict[str, Any],
) -> Dict[str, Any]:
    """Fallback classification for ambiguous inputs.

    Currently uses enhanced keyword matching.
    Future: integrate with Hermes auxiliary_client for LLM classification.
    """
    text_lower = text.lower()
    categories = taxonomy.get("intent_categories", {})

    # Score each category by keyword overlap with description
    best_intent = current["intent"]
    best_score = current["confidence"]

    for key, cat in categories.items():
        desc = cat.get("description", "").lower()
        label = cat.get("label", "").lower()
        # Simple overlap scoring
        score = 0.0
        desc_words = re.split(r'[\s,，、—/]+', desc + " " + label)
        for word in desc_words:
            if len(word) > 1 and word in text_lower:
                score += 0.15
        if score > best_score:
            best_score = min(score, 0.8)  # cap at 0.8 for non-keyword
            best_intent = key

    current["intent"] = best_intent
    current["confidence"] = best_score
    current["method"] = "fallback"
    return current


# ============================================================
# DB Type Detection
# ============================================================

def _detect_db_type(
    text: str,
    taxonomy: Dict[str, Any],
    context: Dict[str, Any],
) -> Tuple[Optional[str], Optional[str]]:
    """Detect database type and version from the user message."""
    text_lower = text.lower()
    rules = taxonomy.get("db_type_rules", {})

    detected_type: Optional[str] = None
    detected_version: Optional[str] = None

    for db_type, rule in rules.items():
        patterns = rule.get("patterns", [])
        if any(p.lower() in text_lower for p in patterns):
            detected_type = db_type

            # Try to detect version
            version_patterns = rule.get("version_patterns", {})
            for version, v_patterns in version_patterns.items():
                for vp in v_patterns:
                    if re.search(vp, text_lower, re.IGNORECASE):
                        detected_version = version
                        break
                if detected_version:
                    break
            break

    return detected_type, detected_version


# ============================================================
# Escalation Rules
# ============================================================

def _check_escalation(text: str, rule: Dict[str, Any]) -> bool:
    """Check if an escalation condition matches the input text."""
    condition = rule.get("condition", "")
    text_upper = text.upper().strip()

    if condition == "no_where_clause":
        # Check if text looks like DELETE/UPDATE without WHERE
        if re.match(r'^\s*(DELETE|UPDATE)\b', text_upper):
            return "WHERE" not in text_upper
    elif condition == "drop_column":
        return "DROP COLUMN" in text_upper or "DROP\n" in text_upper
    elif condition == "modify_column_type":
        return "MODIFY" in text_upper or "ALTER COLUMN" in text_upper

    return False


# ============================================================
# Harness File Resolution
# ============================================================

_STAGES_DIR = Path(__file__).parent / "stages"


def _resolve_harness_files(workflow: Optional[str], intent: str) -> List[str]:
    """Resolve which harness files to mount based on workflow and intent."""
    files = []

    # Always include HITL matrix
    hitl = Path(__file__).parent / "contracts" / "hitl_matrix.yaml"
    if hitl.exists():
        files.append(str(hitl))

    # Include workflow stage file if available
    if workflow:
        stage_file = _get_stage_file(workflow)
        if stage_file:
            files.append(str(stage_file))

    return files


def _get_stage_file(workflow: str) -> Optional[Path]:
    """Get the stage workflow file for a given workflow name."""
    for ext in (".md", ".yaml"):
        path = _STAGES_DIR / f"{workflow}{ext}"
        if path.exists():
            return path
    return None
