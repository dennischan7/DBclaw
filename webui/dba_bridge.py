"""DBA Bridge — Backend bridge to DBA SafeGuard plugin modules.

All plugin imports are centralized here. Route handlers call bridge functions
instead of importing plugin modules directly.

Thread safety: All functions are read-safe. Write operations (approve, switch mode)
use the plugin's own SQLite connections with WAL mode.
"""

from __future__ import annotations

import json
import logging
import re
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_webui.bridge")

# ---------------------------------------------------------------------------
# Ensure plugin directory is on sys.path
# ---------------------------------------------------------------------------

_PLUGIN_DIR = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard"
if _PLUGIN_DIR.exists() and str(_PLUGIN_DIR) not in sys.path:
    sys.path.insert(0, str(_PLUGIN_DIR))

# ---------------------------------------------------------------------------
# Plugin imports
# ---------------------------------------------------------------------------

try:
    from security.approval_manager import (
        create_approval_request,
        approve_request,
        reject_request,
        modify_and_approve,
        get_pending_requests,
        get_request,
        get_request_history,
        ApprovalStatus,
        ApprovalEventType,
        register_event_listener,
        clear_event_listeners,
    )
    _HAS_APPROVAL = True
except ImportError as e:
    logger.warning("approval_manager import failed: %s", e)
    _HAS_APPROVAL = False

try:
    from security.safety_mode import (
        SafetyMode,
        get_current_mode,
        switch_mode,
        is_mode_locked,
        get_mode_lock_info,
        lock_mode,
        unlock_mode,
        get_mode_history,
        MODE_AUTO_APPROVE_THRESHOLD,
    )
    _HAS_SAFETY_MODE = True
except ImportError as e:
    logger.warning("safety_mode import failed: %s", e)
    _HAS_SAFETY_MODE = False

try:
    from security.risk_rules import (
        RiskLevel,
        list_custom_rules,
        add_custom_rule,
        remove_custom_rule,
    )
    _HAS_RISK_RULES = True
except ImportError as e:
    logger.warning("risk_rules import failed: %s", e)
    _HAS_RISK_RULES = False

try:
    from tools.audit_logger import (
        query_audit_logs,
        export_audit_csv,
    )
    _HAS_AUDIT = True
except ImportError as e:
    logger.warning("audit_logger import failed: %s", e)
    _HAS_AUDIT = False

try:
    from engine.dba_loop import PipelineStage, StageStatus
    _HAS_ENGINE = True
except ImportError as e:
    logger.warning("dba_loop import failed: %s", e)
    _HAS_ENGINE = False

try:
    from tools.db_connector import ConnectionManager
    _HAS_CONNECTOR = True
except ImportError as e:
    logger.warning("db_connector import failed: %s", e)
    _HAS_CONNECTOR = False

try:
    from skill_engine.skill_manager import list_skills as _plugin_list_skills, UserRole
    _HAS_SKILLS = True
except ImportError as e:
    logger.warning("skill_manager import failed: %s", e)
    _HAS_SKILLS = False


# ---------------------------------------------------------------------------
# Safety Mode Bridge
# ---------------------------------------------------------------------------

def bridge_get_safety_mode() -> Dict[str, Any]:
    """Get current safety mode info."""
    if not _HAS_SAFETY_MODE:
        return {"error": "safety_mode module not available"}

    mode = get_current_mode()
    locked = is_mode_locked()
    lock_info = get_mode_lock_info()

    return {
        "mode": mode.value,
        "mode_name": mode.display_name,
        "description": mode.description,
        "locked": locked,
        "locked_by": lock_info.get("locked_by") if lock_info else None,
        "auto_approve_threshold": MODE_AUTO_APPROVE_THRESHOLD.get(mode, -1),
    }


def bridge_switch_mode(
    new_mode: int,
    changed_by: str = "webui_user",
    admin_password: Optional[str] = None,
    reason: str = "",
) -> Dict[str, Any]:
    """Switch safety mode."""
    if not _HAS_SAFETY_MODE:
        return {"success": False, "error": "safety_mode module not available"}

    try:
        target = SafetyMode(new_mode)
    except ValueError:
        return {"success": False, "error": f"无效的安全模式: {new_mode}"}

    return switch_mode(target, changed_by, admin_password, reason)


def bridge_lock_mode(locked_by: str = "admin") -> Dict[str, Any]:
    """Lock current safety mode."""
    if not _HAS_SAFETY_MODE:
        return {"success": False, "error": "safety_mode module not available"}
    return {"success": lock_mode(locked_by)}


def bridge_unlock_mode() -> Dict[str, Any]:
    """Unlock safety mode."""
    if not _HAS_SAFETY_MODE:
        return {"success": False, "error": "safety_mode module not available"}
    return {"success": unlock_mode()}


def bridge_get_mode_history(limit: int = 20) -> List[Dict]:
    """Get mode change history."""
    if not _HAS_SAFETY_MODE:
        return []
    try:
        return get_mode_history(limit=limit)
    except Exception:
        return []


# ---------------------------------------------------------------------------
# Approval Bridge
# ---------------------------------------------------------------------------

def bridge_list_approvals(
    status: str = "",
    risk_level: Optional[int] = None,
    limit: int = 50,
    offset: int = 0,
) -> Dict[str, Any]:
    """List approval requests with filters."""
    if not _HAS_APPROVAL:
        return {"requests": [], "total": 0, "error": "approval module not available"}

    try:
        requests = get_request_history(
            status=status,
            limit=limit,
        )
        return {
            "requests": [r.to_dict() for r in requests] if requests else [],
            "total": len(requests),
        }
    except Exception as e:
        logger.error("bridge_list_approvals error: %s", e)
        return {"requests": [], "total": 0, "error": str(e)}


def bridge_get_pending_count() -> int:
    """Get count of pending approvals."""
    if not _HAS_APPROVAL:
        return 0
    try:
        pending = get_pending_requests()
        return len(pending) if pending else 0
    except Exception:
        return 0


def bridge_approve(request_id: str, reviewer: str, comment: str = "") -> Dict[str, Any]:
    """Approve a request."""
    if not _HAS_APPROVAL:
        return {"success": False, "error": "approval module not available"}
    return approve_request(request_id, reviewer, comment)


def bridge_reject(request_id: str, reviewer: str, comment: str) -> Dict[str, Any]:
    """Reject a request."""
    if not _HAS_APPROVAL:
        return {"success": False, "error": "approval module not available"}
    return reject_request(request_id, reviewer, comment)


def bridge_modify_approve(
    request_id: str, reviewer: str, modified_sql: str, comment: str = ""
) -> Dict[str, Any]:
    """Modify and approve a request."""
    if not _HAS_APPROVAL:
        return {"success": False, "error": "approval module not available"}
    return modify_and_approve(request_id, reviewer, modified_sql, comment)


# ---------------------------------------------------------------------------
# Audit Bridge
# ---------------------------------------------------------------------------

def bridge_query_audit(
    start_time: float = 0,
    end_time: float = 0,
    user_id: str = "",
    instance_name: str = "",
    risk_level: Optional[int] = None,
    operation_type: str = "",
    limit: int = 50,
) -> Dict[str, Any]:
    """Query audit logs."""
    if not _HAS_AUDIT:
        return {"logs": [], "count": 0, "error": "audit module not available"}

    try:
        logs = query_audit_logs(
            start_time=start_time,
            end_time=end_time,
            user_id=user_id,
            instance_name=instance_name,
            risk_level=risk_level,
            operation_type=operation_type,
            limit=limit,
        )
        return {"logs": logs, "count": len(logs)}
    except Exception as e:
        logger.error("bridge_query_audit error: %s", e)
        return {"logs": [], "count": 0, "error": str(e)}


def bridge_export_audit_csv(logs: List[Dict]) -> str:
    """Export audit logs as CSV string."""
    if not _HAS_AUDIT:
        return ""
    return export_audit_csv(logs)


# ---------------------------------------------------------------------------
# Risk Rules Bridge
# ---------------------------------------------------------------------------

def bridge_list_risk_rules() -> List[Dict]:
    """List all custom risk rules."""
    if not _HAS_RISK_RULES:
        return []
    try:
        rules = list_custom_rules()
        return rules if isinstance(rules, list) else []
    except Exception as e:
        logger.error("bridge_list_risk_rules error: %s", e)
        return []


def bridge_add_custom_rule(
    rule_id: str,
    pattern: str,
    risk_level: int,
    description: str = "",
) -> Dict[str, Any]:
    """Add a custom risk rule."""
    if not _HAS_RISK_RULES:
        return {"success": False, "error": "risk_rules module not available"}
    try:
        return add_custom_rule(rule_id, pattern, risk_level, description)
    except Exception as e:
        return {"success": False, "error": str(e)}


def bridge_delete_custom_rule(rule_id: str) -> Dict[str, Any]:
    """Delete a custom risk rule."""
    if not _HAS_RISK_RULES:
        return {"success": False, "error": "risk_rules module not available"}
    try:
        success = remove_custom_rule(rule_id)
        return {"success": success}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# Instances Bridge
# ---------------------------------------------------------------------------

def _mask_password(value: str) -> str:
    """Mask a password for display: show first char + asterisks."""
    if not value:
        return ""
    if len(value) <= 2:
        return "*" * len(value)
    return value[0] + "*" * (len(value) - 1)


def bridge_list_instances(include_credentials: bool = False) -> List[Dict]:
    """List configured database instances from config.

    Args:
        include_credentials: If True, include masked passwords + raw usernames
                             for the admin edit form.
    """
    try:
        import yaml
        config_path = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "config" / "dba_config.yaml"
        if not config_path.exists():
            return []
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        instances = cfg.get("databases", {}).get("instances", [])
        result = []
        for inst in instances:
            entry = {
                "name": inst.get("name", ""),
                "type": inst.get("type", ""),
                "host": inst.get("host", ""),
                "port": inst.get("port", 0),
                "database": inst.get("database", ""),
                "timeout": inst.get("timeout", 30),
                "version": inst.get("version", ""),
            }
            if include_credentials:
                entry["readonly_user"] = inst.get("readonly_user", "")
                entry["readonly_pass"] = _mask_password(inst.get("readonly_pass", ""))
                entry["admin_user"] = inst.get("admin_user", "")
                entry["admin_pass"] = _mask_password(inst.get("admin_pass", ""))
                entry["has_readonly_pass"] = bool(inst.get("readonly_pass"))
                entry["has_admin_pass"] = bool(inst.get("admin_pass"))
            result.append(entry)
        return result
    except Exception as e:
        logger.error("bridge_list_instances error: %s", e)
        return []


def bridge_test_connection(instance_name: str, direct_creds: Dict = None) -> Dict[str, Any]:
    """Test database connectivity for an instance.

    Args:
        instance_name: Name of the instance to test.
        direct_creds: Optional dict with form-provided values (type, host, port,
                      database, readonly_user, readonly_pass) that override the
                      saved YAML config.  Allows testing *before* saving.
    """
    if not _HAS_CONNECTOR:
        return {"success": False, "error": "db_connector module not available"}
    try:
        import os as _os
        from sqlalchemy import create_engine, text as sa_text
        from urllib.parse import quote_plus

        # --- 1. Start from saved config (if the instance already exists) ---
        host, port, database, db_type = "localhost", 5432, "", "postgresql"
        user, password = "", ""
        try:
            cm = ConnectionManager()
            cm.load_config()
            saved = cm._get_instance_config(instance_name)
            if saved:
                host = saved.get("host", "localhost")
                port = int(saved.get("port", 5432))
                database = saved.get("database", "")
                db_type = saved.get("type", "postgresql").lower()
                # Resolve credentials: env var first, then direct config value
                user_env = saved.get("readonly_user_env", "")
                pass_env = saved.get("readonly_pass_env", "")
                user = (_os.environ.get(user_env) or saved.get("readonly_user", "")) if user_env else saved.get("readonly_user", "")
                password = (_os.environ.get(pass_env) or saved.get("readonly_pass", "")) if pass_env else saved.get("readonly_pass", "")
            cm.close_all()
        except Exception:
            pass  # Instance may not exist yet — form values will fill in below

        # --- 2. Override with form-provided values (non-empty wins) ---
        if direct_creds:
            if direct_creds.get("type"):          db_type = direct_creds["type"].lower()
            if direct_creds.get("host"):          host = direct_creds["host"]
            if direct_creds.get("port"):          port = int(direct_creds["port"])
            if direct_creds.get("database"):      database = direct_creds["database"]
            if direct_creds.get("readonly_user"): user = direct_creds["readonly_user"]
            if direct_creds.get("readonly_pass"): password = direct_creds["readonly_pass"]

        # --- 3. Build a temporary engine and test ---
        safe_password = quote_plus(password) if password else ""
        dialect_map = {
            "postgresql": f"postgresql+psycopg2://{user}:{safe_password}@{host}:{port}/{database}",
            "mysql":      f"mysql+pymysql://{user}:{safe_password}@{host}:{port}/{database}",
            "oracle":     f"oracle+cx_oracle://{user}:{safe_password}@{host}:{port}/{database}",
            "sqlserver":  f"mssql+pyodbc://{user}:{safe_password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server",
            "hive":       f"hive://{user}:{safe_password}@{host}:{port}/{database}",
        }
        url = dialect_map.get(db_type, dialect_map["postgresql"])
        engine = create_engine(url)
        with engine.connect() as conn:
            conn.execute(sa_text("SELECT 1"))
        engine.dispose()
        return {"success": True, "instance": instance_name}
    except Exception as e:
        return {"success": False, "instance": instance_name, "error": str(e)}


# ---------------------------------------------------------------------------
# Skills Bridge
# ---------------------------------------------------------------------------

def bridge_list_skills() -> List[Dict]:
    """List available skills."""
    if not _HAS_SKILLS:
        return []
    try:
        skills = _plugin_list_skills(user_role=UserRole.ADMIN, include_disabled=True)
        return skills if isinstance(skills, list) else []
    except Exception as e:
        logger.error("bridge_list_skills error: %s", e)
        return []


# ---------------------------------------------------------------------------
# Dashboard Bridge
# ---------------------------------------------------------------------------

def bridge_get_dashboard_stats() -> Dict[str, Any]:
    """Get dashboard summary statistics."""
    now = time.time()
    today_start = now - (now % 86400)  # Start of today UTC

    stats = {
        "ops_today": 0,
        "pending_approvals": 0,
        "block_rate": 0.0,
        "risk_index": 0.0,
    }

    # Audit stats
    if _HAS_AUDIT:
        try:
            logs = query_audit_logs(start_time=today_start, limit=10000)
            stats["ops_today"] = len(logs)
            if logs:
                blocked = sum(1 for l in logs if l.get("approval_status") == "rejected")
                stats["block_rate"] = round(blocked / len(logs) * 100, 1) if logs else 0
                risk_sum = sum(l.get("risk_level", 0) for l in logs)
                stats["risk_index"] = round(risk_sum / len(logs), 2) if logs else 0
        except Exception as e:
            logger.error("dashboard audit stats error: %s", e)

    # Pending approvals
    stats["pending_approvals"] = bridge_get_pending_count()

    return stats


def bridge_get_ops_trend(hours: int = 24) -> List[Dict]:
    """Get hourly operation count for trend chart."""
    if not _HAS_AUDIT:
        return []

    now = time.time()
    start = now - (hours * 3600)

    try:
        logs = query_audit_logs(start_time=start, limit=10000)
        # Group by hour
        buckets = {}
        for log in logs:
            ts = log.get("timestamp", 0)
            hour_key = int(ts // 3600) * 3600
            buckets[hour_key] = buckets.get(hour_key, 0) + 1

        result = []
        for h in range(int(start // 3600) * 3600, int(now // 3600) * 3600 + 3600, 3600):
            result.append({"timestamp": h, "count": buckets.get(h, 0)})
        return result
    except Exception:
        return []


def bridge_get_risk_distribution() -> Dict[str, int]:
    """Get risk level distribution for donut chart."""
    if not _HAS_AUDIT:
        return {}

    now = time.time()
    start = now - 86400  # Last 24h

    try:
        logs = query_audit_logs(start_time=start, limit=10000)
        dist = {"L0": 0, "L1": 0, "L2": 0, "L3": 0, "L4": 0}
        for log in logs:
            level = log.get("risk_level", 0)
            key = f"L{level}" if 0 <= level <= 4 else "L0"
            dist[key] = dist.get(key, 0) + 1
        return dist
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Chat / Pipeline Bridge
# ---------------------------------------------------------------------------

def bridge_chat(
    message: str,
    instance_name: str = "pg_test",
    dialect: str = "postgresql",
    user_id: str = "webui_user",
    session_id: str = "",
    is_rollback: bool = False,
    safety_mode: int = 2,
    history: list = None,
    execute_sql: str = "",
    source_message: str = "",
) -> Dict[str, Any]:
    """Smart chat: classify intent → route to pipeline or LLM.

    - SQL intents (query, dml_*, ddl_*) → run DBA pipeline
    - General/troubleshoot/health_check → call LLM with DBA context
    - Pipeline results are summarized for the user

    ``history`` is loaded from SQLite by the route handler — a list of
    {"role": "user"|"assistant", "content": "..."} dicts in chronological order.
    """
    from llm_client import chat_completion, is_llm_configured

    # Step 1: Classify intent
    intent_info = _classify_message(message)
    intent_key = intent_info.get("intent", "general")

    # Step 2: Search library BEFORE routing — both pipeline and LLM paths benefit
    library_context = _search_library_context(message, dialect, instance_name)

    # SQL-specific intents → run pipeline
    sql_intents = {
        "query", "dml_insert", "dml_update", "dml_delete",
        "ddl_create", "ddl_alter", "ddl_drop", "ddl_truncate",
        "backup_restore",
    }

    if intent_key in sql_intents and _HAS_ENGINE:
        source_text = source_message.strip() or message

        if execute_sql.strip() or _looks_like_sql(message):
            sql_text = execute_sql.strip() or message
            pipeline_result = _run_pipeline_chat(
                sql_text=sql_text,
                source_message=source_text,
                instance_name=instance_name,
                dialect=dialect,
                user_id=user_id,
                session_id=session_id,
                intent_info=intent_info,
                library_context=library_context,
            )
            pipeline_result["response_type"] = "pipeline"
            if execute_sql.strip():
                pipeline_result["generated_sql"] = {
                    "sql": sql_text,
                    "summary": "用户已确认执行生成的 SQL",
                    "confidence": 1.0,
                    "requires_confirmation": False,
                    "library_context_used": bool(library_context),
                }
            return pipeline_result

        if not is_llm_configured():
            return {
                "error": "检测到数据库操作意图，但当前 LLM 未配置，无法先生成 SQL。",
                "intent": intent_info,
                "response_type": "generation_failed",
                "source_message": message,
            }

        generation = _generate_sql_from_nl(
            user_message=message,
            instance_name=instance_name,
            dialect=dialect,
            intent_info=intent_info,
            library_context=library_context,
            history=history or [],
            safety_mode=safety_mode,
        )
        if not generation.get("success"):
            return {
                "response": generation.get("response") or generation.get("error", "SQL 生成失败"),
                "error": generation.get("error", "SQL 生成失败"),
                "intent": intent_info,
                "response_type": "generation_failed",
                "generated_sql": generation,
                "source_message": message,
            }

        if intent_key == "query" and not generation.get("requires_confirmation", False):
            pipeline_result = _run_pipeline_chat(
                sql_text=generation.get("sql", ""),
                source_message=message,
                instance_name=instance_name,
                dialect=dialect,
                user_id=user_id,
                session_id=session_id,
                intent_info=intent_info,
                library_context=library_context,
                generation_meta=generation,
            )
            pipeline_result["response_type"] = "pipeline"
            pipeline_result["generated_sql"] = generation
            pipeline_result["source_message"] = message
            return pipeline_result

        return {
            "response": generation.get("response", "已生成候选 SQL，请确认后执行。"),
            "intent": intent_info,
            "response_type": "generation",
            "generated_sql": generation,
            "source_message": message,
        }

    # General / troubleshoot / health_check / optimize → LLM chat
    if not is_llm_configured():
        # Fallback: return intent classification + instance info
        return _fallback_response(message, instance_name, dialect, intent_info)

    # Build LLM messages with conversation history
    messages = []
    if history:
        for msg in history[-20:]:
            messages.append(msg)
    else:
        messages.append({"role": "user", "content": message})

    # Add context about current DB for relevant queries
    extra_context = _gather_db_context(instance_name, dialect, intent_key)
    if extra_context:
        # Inject as system-level context in the user message
        enriched = f"{message}\n\n[当前数据库上下文]\n{extra_context}"
        messages[-1]["content"] = enriched

    # Inject library documentation context (RAG) — already computed above
    if library_context:
        messages[-1]["content"] = messages[-1]["content"] + f"\n\n[数据库官方文档参考]\n{library_context}"

    result = chat_completion(
        messages,
        instance_name=instance_name,
        dialect=dialect,
        safety_mode=safety_mode,
    )

    if result.get("success"):
        return {
            "response": result["content"],
            "intent": intent_info,
            "usage": result.get("usage"),
            "model": result.get("model"),
        }
    else:
        return {"error": result.get("error", "LLM 调用失败")}


def _classify_message(message: str) -> Dict[str, Any]:
    """Classify user message intent."""
    try:
        from harnesses.intent_router import classify_intent
        return classify_intent(message)
    except Exception as e:
        logger.warning("Intent classification failed: %s", e)
        return {"intent": "general", "label": "通用咨询", "confidence": 0.5}


def _looks_like_sql(text: str) -> bool:
    text = (text or "").strip().lower()
    return bool(re.match(
        r"^(select|insert|update|delete|create|alter|drop|truncate|with|explain|show|desc|describe)\b",
        text,
    ))


def _extract_table_candidates(message: str) -> List[str]:
    patterns = [
        r"`([A-Za-z_][\w]*)`",
        r'"([A-Za-z_][\w]*)"',
        r"表\s*([A-Za-z_][\w]*)",
        r"table\s+([A-Za-z_][\w]*)",
    ]
    matches: List[str] = []
    for pattern in patterns:
        matches.extend(re.findall(pattern, message or "", flags=re.IGNORECASE))
    seen = set()
    result = []
    for item in matches:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result[:3]


def _collect_metadata_context(message: str, instance_name: str, dialect: str) -> str:
    try:
        from tools.metadata_reader import read_metadata
    except ImportError:
        try:
            from ..tools.metadata_reader import read_metadata  # type: ignore[import-not-found]
        except Exception:
            return ""

    parts = []
    for table in _extract_table_candidates(message):
        meta = read_metadata(
            instance_name=instance_name,
            dialect=dialect,
            table=table,
            info_type="columns",
        )
        data = (meta or {}).get("data", "")
        if data and not str(data).startswith("元数据读取失败"):
            parts.append(f"[表 {table} 的字段]\n{data}")
    return "\n\n".join(parts)


def _extract_json_payload(text: str) -> Dict[str, Any]:
    raw = (text or "").strip()
    if raw.startswith("```"):
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))


def _generate_sql_from_nl(
    user_message: str,
    instance_name: str,
    dialect: str,
    intent_info: Dict[str, Any],
    library_context: str,
    history: List[Dict[str, Any]],
    safety_mode: int,
) -> Dict[str, Any]:
    from llm_client import chat_completion

    db_context = _gather_db_context(instance_name, dialect, intent_info.get("intent", ""))
    metadata_context = _collect_metadata_context(user_message, instance_name, dialect)
    recent_history = []
    for msg in (history or [])[-6:]:
        role = msg.get("role")
        content = (msg.get("content") or "").strip()
        if role in {"user", "assistant"} and content:
            recent_history.append(f"{role}: {content[:300]}")

    prompt = (
        "请把用户的数据库操作需求转换为可执行 SQL。"
        "必须严格输出 JSON 对象，不要输出 Markdown，不要输出解释性前缀。\n\n"
        "返回 schema:\n"
        "{\n"
        '  "sql": "候选SQL，无法确定时留空",\n'
        '  "summary": "一句话说明",\n'
        '  "assumptions": ["假设1", "假设2"],\n'
        '  "confidence": 0.0,\n'
        '  "requires_confirmation": true,\n'
        '  "error": "如果无法生成则说明原因"\n'
        "}\n\n"
        "规则:\n"
        f"1. 数据库方言必须是 {dialect}.\n"
        "2. 只生成一条最合适的 SQL。\n"
        "3. 若请求是写操作或 DDL，requires_confirmation 必须为 true。\n"
        "4. 若信息不足，请把 sql 置空并在 error 中说明缺少什么。\n"
        "5. 仅依据提供的文档和上下文，不要臆造不存在的列名。\n\n"
        f"[用户原始需求]\n{user_message}\n\n"
        f"[意图分类]\n{json.dumps(intent_info, ensure_ascii=False)}\n\n"
        f"[数据库上下文]\n{db_context or '无'}\n\n"
        f"[官方文档片段]\n{library_context or '无'}\n\n"
        f"[表结构元数据]\n{metadata_context or '无'}\n\n"
        f"[最近对话]\n{'\n'.join(recent_history) or '无'}"
    )

    result = chat_completion(
        [{"role": "user", "content": prompt}],
        instance_name=instance_name,
        dialect=dialect,
        safety_mode=safety_mode,
        temperature=0.1,
        max_tokens=1200,
    )
    if not result.get("success"):
        return {
            "success": False,
            "error": result.get("error", "LLM SQL 生成失败"),
            "response": result.get("error", "LLM SQL 生成失败"),
            "sql": "",
            "library_context_used": bool(library_context),
        }

    try:
        payload = _extract_json_payload(result.get("content", ""))
    except Exception as exc:
        logger.error("Failed to parse SQL generation payload: %s", exc)
        return {
            "success": False,
            "error": "SQL 生成响应无法解析为结构化 JSON",
            "response": "SQL 生成失败：模型返回了无法解析的结果。",
            "sql": "",
            "raw": result.get("content", ""),
            "library_context_used": bool(library_context),
        }

    sql_text = str(payload.get("sql", "") or "").strip()
    error_text = str(payload.get("error", "") or "").strip()
    requires_confirmation = bool(payload.get("requires_confirmation", True))
    if intent_info.get("intent") == "query" and sql_text:
        requires_confirmation = False

    response = payload.get("summary") or "已生成候选 SQL。"
    if sql_text:
        response = f"已根据你的需求生成候选 SQL。{response}"
    elif error_text:
        response = f"暂时无法安全生成 SQL：{error_text}"

    return {
        "success": bool(sql_text),
        "sql": sql_text,
        "summary": str(payload.get("summary", "") or ""),
        "assumptions": payload.get("assumptions", []),
        "confidence": payload.get("confidence", 0),
        "requires_confirmation": requires_confirmation,
        "error": error_text,
        "response": response,
        "library_context_used": bool(library_context),
        "raw": result.get("content", ""),
    }


def _search_library_context(message: str, dialect: str, instance_name: str) -> str:
    """Search library knowledge base for relevant documentation context.

    Returns formatted context string or empty string if no results found.
    """
    try:
        import sys
        # Find the library_search module
        lib_search = sys.modules.get("tools.library_search")
        if lib_search is None:
            # Try to import from the plugin tools directory
            tools_dir = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "tools"
            if tools_dir.exists():
                sys.path.insert(0, str(tools_dir.parent))
                try:
                    from tools.library_search import search_library
                except ImportError:
                    # Try direct import
                    import importlib.util
                    spec = importlib.util.spec_from_file_location(
                        "library_search", tools_dir / "library_search.py"
                    )
                    if spec and spec.loader:
                        lib_search = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(lib_search)
                        search_library = lib_search.search_library
                    else:
                        return ""
            else:
                return ""
        else:
            search_library = lib_search.search_library

        # Resolve version from instance config
        version = ""
        try:
            import yaml
            config_path = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "config" / "dba_config.yaml"
            if config_path.exists():
                with open(config_path, "r", encoding="utf-8") as f:
                    cfg = yaml.safe_load(f) or {}
                for inst in cfg.get("databases", {}).get("instances", []):
                    if inst.get("name") == instance_name:
                        version = inst.get("version", "")
                        break
        except Exception:
            pass

        # Map dialect to db_type for library search
        db_type = dialect.lower()

        result = search_library(query=message, db_type=db_type, version=version, max_results=3)
        if not result or not result.get("results"):
            return ""

        # Filter out error results
        docs = [r for r in result["results"] if not r.get("error")]
        if not docs:
            return ""

        parts = []
        for doc in docs[:3]:
            section = doc.get("section", "")
            content = doc.get("content", "")
            score = doc.get("score", 0)
            if content and score > 0.1:
                header = f"[{section}]" if section else ""
                parts.append(f"{header}\n{content.strip()}")

        return "\n\n---\n\n".join(parts) if parts else ""

    except Exception as e:
        logger.debug("Library search failed: %s", e)
        return ""


def _gather_db_context(instance_name: str, dialect: str, intent_key: str) -> str:
    """Gather relevant DB context for LLM."""
    parts = []

    # Instance info
    instances = bridge_list_instances()
    for inst in instances:
        if inst.get("name") == instance_name:
            parts.append(f"实例: {inst['name']} ({inst.get('type', dialect)})")
            parts.append(f"主机: {inst.get('host', 'localhost')}:{inst.get('port', 5432)}")
            parts.append(f"数据库: {inst.get('database', '-')}")
            break

    # Safety mode info
    mode_info = bridge_get_safety_mode()
    if isinstance(mode_info, dict):
        mode = mode_info.get("mode", 2)
        mode_names = ["只读", "保守", "适中", "激进", "疯狂"]
        parts.append(f"安全模式: L{mode} ({mode_names[mode] if 0 <= mode <= 4 else '?'})")

    return "\n".join(parts)


def _run_pipeline_chat(
    sql_text: str,
    source_message: str,
    instance_name: str,
    dialect: str,
    user_id: str,
    session_id: str,
    intent_info: dict,
    library_context: str = "",
    generation_meta: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Run the DBA safety pipeline for SQL operations."""
    try:
        from engine.dba_loop import run_pipeline

        # Keep sql= actual SQL for AST validation/execution; preserve source text separately.
        enriched_user_message = source_message
        if library_context:
            enriched_user_message = source_message + "\n\n[数据库官方文档参考]\n" + library_context

        task = run_pipeline(
            sql=sql_text,
            instance_name=instance_name,
            dialect=dialect,
            user_message=enriched_user_message,
            user_id=user_id,
            session_id=session_id,
        )

        task_dict = task.to_dict()
        task_dict["source_message"] = source_message
        task_dict["rollback_sql"] = task.rollback_sql
        task_dict["execution_result"] = task.execution_result
        task_dict["stage_results"] = task_dict.pop("stages", [])
        task_dict["intent"] = task.intent
        if generation_meta:
            task_dict["generated_sql_meta"] = generation_meta

        needs_approval = False
        for sr in task.stage_results:
            if sr.status.value == "blocked" and sr.stage.value == "approval":
                needs_approval = True
                break

        response_parts = []
        if task.intent:
            response_parts.append(f"意图: {task.intent.get('label', task.intent.get('intent', ''))}")
        if task.risk_level is not None:
            risk_labels = ["只读", "低风险", "中风险", "高风险", "灾难级"]
            label = risk_labels[task.risk_level] if 0 <= task.risk_level <= 4 else f"L{task.risk_level}"
            response_parts.append(f"风险: L{task.risk_level} ({label})")

        exec_result = task.execution_result
        if exec_result and isinstance(exec_result, dict):
            if exec_result.get("success"):
                data = exec_result.get("data") if isinstance(exec_result.get("data"), dict) else None
                if data and data.get("columns") is not None:
                    total_rows = data.get("total_rows")
                    loaded_count = data.get("loaded_count")
                    if total_rows is not None:
                        response_parts.append(f"查询成功，返回 {total_rows} 行")
                    elif loaded_count is not None:
                        summary = f"查询成功，已加载 {loaded_count} 行"
                        if data.get("has_more"):
                            summary += "，向下滚动可继续加载"
                        response_parts.append(summary)
                    else:
                        response_parts.append("查询成功")
                else:
                    rows = exec_result.get("rows_affected")
                    response_parts.append(f"执行成功" + (f"，影响 {rows} 行" if rows is not None else ""))
            elif exec_result.get("error"):
                response_parts.append(f"执行失败: {exec_result['error']}")
        elif needs_approval:
            response_parts.append("⏳ 操作需要审批，已提交审批队列")

        for sr in task.stage_results:
            if sr.status.value == "failed":
                response_parts.append(f"❌ 阶段 {sr.stage.value} 失败: {sr.error or '未知错误'}")

        response = " | ".join(response_parts) if response_parts else "处理完成"

        return {
            "response": response,
            "task": task_dict,
            "needs_approval": needs_approval,
        }

    except Exception as e:
        logger.error("Pipeline error: %s", e, exc_info=True)
        return {"error": str(e)}


def _fallback_response(
    message: str,
    instance_name: str,
    dialect: str,
    intent_info: dict,
) -> Dict[str, Any]:
    """Fallback response when LLM is not configured."""
    from llm_client import get_model_config

    config = get_model_config()
    missing = []
    if not config.get("base_url"):
        missing.append("base_url")
    if not config.get("model_name"):
        missing.append("model_name")
    if not config.get("api_key_env"):
        missing.append("api_key_env 环境变量名")

    parts = [
        f"📋 意图识别: {intent_info.get('label', '通用咨询')} (置信度: {intent_info.get('confidence', 0):.0%})",
    ]

    # Add instance info even without LLM
    instances = bridge_list_instances()
    for inst in instances:
        if inst.get("name") == instance_name:
            parts.append(f"📍 当前实例: {inst['name']} ({inst.get('type', dialect)})")
            parts.append(f"   主机: {inst.get('host', 'localhost')}:{inst.get('port', 5432)}")
            parts.append(f"   数据库: {inst.get('database', '-')}")
            break

    if missing:
        parts.append(f"\n⚠️ LLM 未完全配置（缺少: {', '.join(missing)}）")
        parts.append("请在 管理面板 → LLM模型配置 中设置，或设置对应的环境变量。")
        if config.get("api_key_env"):
            parts.append(f"需要设置环境变量: {config['api_key_env']}")
    else:
        parts.append("\n⚠️ API 密钥未设置。请设置环境变量后重启服务。")

    return {
        "response": "\n".join(parts),
        "intent": intent_info,
    }


# ---------------------------------------------------------------------------
# Instance Add/Update Bridge
# ---------------------------------------------------------------------------

def bridge_add_instance(instance_data: Dict[str, Any]) -> Dict[str, Any]:
    """Add a new database instance to config."""
    try:
        import yaml
        config_path = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "config" / "dba_config.yaml"
        if not config_path.exists():
            return {"success": False, "error": "Config file not found"}

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        if "databases" not in cfg:
            cfg["databases"] = {}
        if "instances" not in cfg["databases"]:
            cfg["databases"]["instances"] = []

        instances = cfg["databases"]["instances"]

        # Validate required fields
        name = instance_data.get("name", "").strip()
        if not name:
            return {"success": False, "error": "实例名称不能为空"}

        # Check for duplicate name
        for inst in instances:
            if inst.get("name") == name:
                return {"success": False, "error": f"实例 '{name}' 已存在"}

        # Build instance entry with direct credentials support
        entry = {
            "name": name,
            "type": instance_data.get("type", "postgresql"),
            "host": instance_data.get("host", "localhost"),
            "port": int(instance_data.get("port", 5432)),
            "database": instance_data.get("database", ""),
            "timeout": int(instance_data.get("timeout", 30)),
        }

        # Store credentials directly (user can still use env vars if preferred)
        for key in ("readonly_user", "readonly_pass", "admin_user", "admin_pass"):
            val = instance_data.get(key, "").strip()
            if val:
                entry[key] = val

        # Keep env var names for backward compatibility (auto-generated)
        entry["readonly_user_env"] = instance_data.get("readonly_user_env", f"DBA_{name.upper()}_RO_USER")
        entry["readonly_pass_env"] = instance_data.get("readonly_pass_env", f"DBA_{name.upper()}_RO_PASS")
        entry["admin_user_env"] = instance_data.get("admin_user_env", f"DBA_{name.upper()}_ADMIN_USER")
        entry["admin_pass_env"] = instance_data.get("admin_pass_env", f"DBA_{name.upper()}_ADMIN_PASS")

        # Optional version for library search matching
        version = instance_data.get("version", "").strip()
        if version:
            entry["version"] = version

        instances.append(entry)

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Invalidate cached engines so next connection uses new config
        _invalidate_connection_cache()

        return {"success": True, "instance": entry}

    except Exception as e:
        logger.error("bridge_add_instance error: %s", e)
        return {"success": False, "error": str(e)}


def bridge_update_instance(instance_name: str, updates: Dict[str, Any]) -> Dict[str, Any]:
    """Update an existing database instance in config."""
    try:
        import yaml
        config_path = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "config" / "dba_config.yaml"
        if not config_path.exists():
            return {"success": False, "error": "Config file not found"}

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        instances = cfg.get("databases", {}).get("instances", [])
        target = None
        for inst in instances:
            if inst.get("name") == instance_name:
                target = inst
                break

        if target is None:
            return {"success": False, "error": f"实例 '{instance_name}' 不存在"}

        # If renaming, check for conflicts
        new_name = updates.get("name", "").strip()
        if new_name and new_name != instance_name:
            for inst in instances:
                if inst.get("name") == new_name:
                    return {"success": False, "error": f"实例 '{new_name}' 已存在"}

        # Update allowed fields
        allowed_fields = {"name", "type", "host", "port", "database", "timeout", "version",
                          "readonly_user", "readonly_pass", "admin_user", "admin_pass"}
        for key in allowed_fields:
            val = updates.get(key)
            if val is not None:
                val_str = str(val).strip()
                if val_str:
                    if key in ("port", "timeout"):
                        target[key] = int(val_str)
                    else:
                        target[key] = val_str
                elif key in ("readonly_pass", "admin_pass"):
                    # Empty password string means "clear it"
                    # but don't clear if not explicitly sent
                    pass

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        # Invalidate cached engines
        _invalidate_connection_cache()

        return {"success": True, "instance": target}

    except Exception as e:
        logger.error("bridge_update_instance error: %s", e)
        return {"success": False, "error": str(e)}


def _invalidate_connection_cache():
    """Clear cached connection engines so they pick up new config."""
    try:
        import sys
        # Get the db_connector module if loaded
        mod = sys.modules.get("tools.db_connector")
        if mod is None:
            # Try alternate import path used by webui
            for key, m in sys.modules.items():
                if key.endswith("db_connector") and hasattr(m, "_connection_manager"):
                    mod = m
                    break
        if mod and hasattr(mod, "_connection_manager"):
            mgr = mod._connection_manager
            mgr.close_all()
            mgr._config = {}  # force reload on next access
    except Exception as e:
        logger.debug("_invalidate_connection_cache: %s", e)


def bridge_remove_instance(instance_name: str) -> Dict[str, Any]:
    """Remove a database instance from config."""
    try:
        import yaml
        config_path = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard" / "config" / "dba_config.yaml"
        if not config_path.exists():
            return {"success": False, "error": "Config file not found"}

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        instances = cfg.get("databases", {}).get("instances", [])
        original_len = len(instances)
        instances = [i for i in instances if i.get("name") != instance_name]

        if len(instances) == original_len:
            return {"success": False, "error": f"实例 '{instance_name}' 不存在"}

        cfg["databases"]["instances"] = instances

        with open(config_path, "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        _invalidate_connection_cache()

        return {"success": True}

    except Exception as e:
        logger.error("bridge_remove_instance error: %s", e)
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# SSE Event Listener Registration
# ---------------------------------------------------------------------------

_sse_queues: List = []


def register_sse_queue(queue) -> None:
    """Register a queue to receive SSE events from the approval manager."""
    _sse_queues.append(queue)

    if _HAS_APPROVAL:
        def _forward(event):
            for q in _sse_queues:
                try:
                    q.put_nowait(event)
                except Exception:
                    pass
        register_event_listener(_forward)


def unregister_sse_queue(queue) -> None:
    """Remove an SSE queue."""
    try:
        _sse_queues.remove(queue)
    except ValueError:
        pass
