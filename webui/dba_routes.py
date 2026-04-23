"""DBA Routes — REST API + SSE endpoints.

All endpoints under /api/dba/. Route dispatch is done by path matching.

Endpoints:
  GET  /api/dba/health                  Health check
  GET  /api/dba/session                 Get/init session + CSRF token
  GET  /api/dba/events                  SSE event stream
  GET  /api/dba/mode                    Get current safety mode
  POST /api/dba/mode                    Switch safety mode
  POST /api/dba/mode/lock               Lock mode
  POST /api/dba/mode/unlock             Unlock mode
  GET  /api/dba/approvals               List approvals
  POST /api/dba/approvals/approve       Approve request
  POST /api/dba/approvals/reject        Reject request
  POST /api/dba/approvals/modify        Modify + approve
  GET  /api/dba/audit                   Query audit logs
  GET  /api/dba/audit/export            Export audit CSV
  GET  /api/dba/rules                   List risk rules
  POST /api/dba/rules                   Add custom rule
  DELETE /api/dba/rules                 Delete custom rule
  GET  /api/dba/instances               List DB instances
  POST /api/dba/instances/test          Test instance connection
  GET  /api/dba/skills                  List skills
  GET  /api/dba/dashboard/stats         Dashboard statistics
  GET  /api/dba/dashboard/ops-trend     Operations trend chart data
  GET  /api/dba/dashboard/risk-dist     Risk distribution chart data
"""

from __future__ import annotations

import json
import logging
import queue
import time
import threading
from copy import deepcopy
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs

from auth_middleware import require_auth, require_admin, check_csrf, set_auth_headers
import dba_bridge as bridge
import chat_store

logger = logging.getLogger("dba_webui.routes")


def _build_task_snapshot(task: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not task or not isinstance(task, dict):
        return task

    snapshot = deepcopy(task)
    execution_result = snapshot.get("execution_result")
    if isinstance(execution_result, dict):
        data = execution_result.get("data")
        if isinstance(data, dict):
            data.pop("result_set_id", None)
    return snapshot


# ---------------------------------------------------------------------------
# Time-range helper
# ---------------------------------------------------------------------------

def _parse_time_range(query_params: Dict) -> tuple:
    """Parse time range from query params."""
    range_str = query_params.get("range", ["24h"])[0]
    now = time.time()

    ranges = {
        "1h": 3600,
        "24h": 86400,
        "7d": 7 * 86400,
        "30d": 30 * 86400,
        "all": 0,
    }

    seconds = ranges.get(range_str, 86400)
    start_time = now - seconds if seconds > 0 else 0
    return start_time, now


# ---------------------------------------------------------------------------
# Route dispatcher
# ---------------------------------------------------------------------------

def handle_dba_request(handler, method: str, path: str, body: dict, query: dict):
    """Main route dispatcher for /api/dba/* endpoints."""

    # Health check (no auth needed)
    if path == "/api/dba/health":
        handler.send_json({"status": "ok", "timestamp": time.time()})
        return

    # Session init (special: creates session if needed)
    if path == "/api/dba/session" and method == "GET":
        return _handle_session(handler)

    # SSE events (long-lived connection)
    if path == "/api/dba/events" and method == "GET":
        return _handle_sse_events(handler)

    # --- All other endpoints require auth ---
    session = require_auth(handler)
    if not session:
        return

    # Mode endpoints
    if path == "/api/dba/mode":
        if method == "GET":
            return _handle_get_mode(handler, session)
        if method == "POST":
            if not check_csrf(handler, session):
                return
            return _handle_switch_mode(handler, session, body)

    if path == "/api/dba/mode/lock" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_lock_mode(handler, session)

    if path == "/api/dba/mode/unlock" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_unlock_mode(handler, session)

    # Approval endpoints
    if path == "/api/dba/approvals" and method == "GET":
        return _handle_list_approvals(handler, session, query)

    if path == "/api/dba/approvals/approve" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_approve(handler, session, body)

    if path == "/api/dba/approvals/reject" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_reject(handler, session, body)

    if path == "/api/dba/approvals/modify" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_modify_approve(handler, session, body)

    # Audit endpoints
    if path == "/api/dba/audit" and method == "GET":
        return _handle_query_audit(handler, session, query)

    if path == "/api/dba/audit/export" and method == "GET":
        return _handle_export_audit(handler, session, query)

    # Risk rules
    if path == "/api/dba/rules":
        if method == "GET":
            return _handle_list_rules(handler, session)
        if method == "POST":
            if not check_csrf(handler, session):
                return
            return _handle_add_rule(handler, session, body)
        if method == "DELETE":
            if not check_csrf(handler, session):
                return
            return _handle_delete_rule(handler, session, body)

    # Instances
    if path == "/api/dba/instances" and method == "GET":
        return _handle_list_instances(handler, session)

    if path == "/api/dba/instances/test" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_test_instance(handler, session, body)

    # Skills
    if path == "/api/dba/skills" and method == "GET":
        return _handle_list_skills(handler, session)

    # Dashboard
    if path == "/api/dba/dashboard/stats" and method == "GET":
        return _handle_dashboard_stats(handler, session)

    if path == "/api/dba/dashboard/ops-trend" and method == "GET":
        return _handle_ops_trend(handler, session, query)

    if path == "/api/dba/dashboard/risk-dist" and method == "GET":
        return _handle_risk_dist(handler, session)

    # Chat — send message through DBA pipeline
    if path == "/api/dba/chat" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_chat(handler, session, body)

    if path.startswith("/api/dba/chat/results/") and method == "GET":
        result_set_id = path.rsplit("/", 1)[-1]
        return _handle_chat_result_page(handler, session, result_set_id, query)

    # Memory status (diagnostics)
    if path == "/api/dba/memory-status" and method == "GET":
        return _handle_memory_status(handler, session)

    # Instance add / remove
    if path == "/api/dba/instances" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_add_instance(handler, session, body)

    if path == "/api/dba/instances" and method == "DELETE":
        if not check_csrf(handler, session):
            return
        return _handle_remove_instance(handler, session, body)

    if path == "/api/dba/instances" and method == "PUT":
        if not check_csrf(handler, session):
            return
        return _handle_update_instance(handler, session, body)

    # LLM config
    if path == "/api/dba/llm-config" and method == "GET":
        return _handle_get_llm_config(handler, session)

    if path == "/api/dba/llm-config" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_save_llm_config(handler, session, body)

    if path == "/api/dba/llm-config/test" and method == "POST":
        if not check_csrf(handler, session):
            return
        return _handle_test_llm(handler, session, body)

    # Conversations
    if path == "/api/dba/conversations":
        if method == "GET":
            return _handle_list_conversations(handler, session, query)
        if method == "POST":
            if not check_csrf(handler, session):
                return
            return _handle_create_conversation(handler, session, body)

    if path == "/api/dba/conversations/search" and method == "GET":
        return _handle_search_conversations(handler, session, query)

    # Conversation by ID: /api/dba/conversations/<id>  or  /api/dba/conversations/<id>/messages
    if path.startswith("/api/dba/conversations/"):
        parts = path.split("/")
        # /api/dba/conversations/<id>  → 5 parts
        # /api/dba/conversations/<id>/messages → 6 parts
        if len(parts) == 5 and parts[4] != "search":
            conv_id = parts[4]
            if method == "GET":
                return _handle_get_conversation_messages(handler, session, conv_id, query)
            if method == "DELETE":
                if not check_csrf(handler, session):
                    return
                return _handle_delete_conversation(handler, session, conv_id)
        elif len(parts) == 6 and parts[5] == "messages":
            conv_id = parts[4]
            return _handle_get_conversation_messages(handler, session, conv_id, query)

    # 404
    handler.send_json({"error": "Not found"}, status=404)


# ---------------------------------------------------------------------------
# Session
# ---------------------------------------------------------------------------

def _handle_session(handler):
    """Initialize session and return CSRF token."""
    session = require_auth(handler)
    if not session:
        return

    data = {
        "user_id": session.get("user_id"),
        "role": session.get("role"),
        "csrf_token": session.get("csrf_token", ""),
    }

    # Need to set cookie before sending JSON
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    handler.send_response(200)
    set_auth_headers(handler, session)
    from auth_middleware import flush_pending_headers
    flush_pending_headers(handler)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


# ---------------------------------------------------------------------------
# SSE Events
# ---------------------------------------------------------------------------

def _handle_sse_events(handler):
    """Server-Sent Events stream for real-time updates."""
    handler.send_sse_headers()

    # Create a queue for this client
    event_queue = queue.Queue(maxsize=100)
    bridge.register_sse_queue(event_queue)

    try:
        # Send initial state
        mode_info = bridge.bridge_get_safety_mode()
        pending_count = bridge.bridge_get_pending_count()

        handler.send_sse_event("init", {
            "mode": mode_info,
            "pending_count": pending_count,
        })

        # Heartbeat + event loop
        while True:
            try:
                event = event_queue.get(timeout=30)
                if event:
                    event_type = event.get("event", "message")
                    handler.send_sse_event(event_type, event.get("data", event))
            except queue.Empty:
                try:
                    # Send heartbeat
                    handler.send_sse_event("heartbeat", {"ts": time.time()})
                except (BrokenPipeError, ConnectionResetError,
                        ConnectionAbortedError, OSError):
                    break
            except (BrokenPipeError, ConnectionResetError,
                    ConnectionAbortedError, OSError):
                break
    finally:
        bridge.unregister_sse_queue(event_queue)


# ---------------------------------------------------------------------------
# Safety Mode
# ---------------------------------------------------------------------------

def _handle_get_mode(handler, session):
    result = bridge.bridge_get_safety_mode()
    handler.send_json(result)


def _handle_switch_mode(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    new_mode = body.get("mode")
    if new_mode is None:
        handler.send_json({"error": "缺少mode参数"}, status=400)
        return

    result = bridge.bridge_switch_mode(
        new_mode=int(new_mode),
        changed_by=session.get("user_id", "unknown"),
        admin_password=body.get("admin_password"),
        reason=body.get("reason", "WebUI切换"),
    )
    handler.send_json(result)


def _handle_lock_mode(handler, session):
    admin_session = require_admin(handler)
    if not admin_session:
        return
    result = bridge.bridge_lock_mode(session.get("user_id", "admin"))
    handler.send_json(result)


def _handle_unlock_mode(handler, session):
    admin_session = require_admin(handler)
    if not admin_session:
        return
    result = bridge.bridge_unlock_mode()
    handler.send_json(result)


# ---------------------------------------------------------------------------
# Approvals
# ---------------------------------------------------------------------------

def _handle_list_approvals(handler, session, query):
    status = query.get("status", [""])[0]
    risk_str = query.get("risk_level", [""])[0]
    risk_level = int(risk_str) if risk_str.isdigit() else None
    limit = int(query.get("limit", ["50"])[0])
    offset = int(query.get("offset", ["0"])[0])

    # Cap limits to prevent abuse
    limit = min(limit, 200)

    result = bridge.bridge_list_approvals(
        status=status, risk_level=risk_level, limit=limit, offset=offset,
    )
    handler.send_json(result)


def _handle_approve(handler, session, body):
    request_id = body.get("request_id")
    if not request_id:
        handler.send_json({"error": "缺少request_id"}, status=400)
        return

    result = bridge.bridge_approve(
        request_id=request_id,
        reviewer=session.get("user_id", "unknown"),
        comment=body.get("comment", ""),
    )
    handler.send_json(result)


def _handle_reject(handler, session, body):
    request_id = body.get("request_id")
    comment = body.get("comment", "")

    if not request_id:
        handler.send_json({"error": "缺少request_id"}, status=400)
        return
    if not comment.strip():
        handler.send_json({"error": "驳回必须填写原因"}, status=400)
        return

    result = bridge.bridge_reject(
        request_id=request_id,
        reviewer=session.get("user_id", "unknown"),
        comment=comment,
    )
    handler.send_json(result)


def _handle_modify_approve(handler, session, body):
    request_id = body.get("request_id")
    modified_sql = body.get("modified_sql", "")

    if not request_id:
        handler.send_json({"error": "缺少request_id"}, status=400)
        return
    if not modified_sql.strip():
        handler.send_json({"error": "修改后SQL不能为空"}, status=400)
        return

    result = bridge.bridge_modify_approve(
        request_id=request_id,
        reviewer=session.get("user_id", "unknown"),
        modified_sql=modified_sql,
        comment=body.get("comment", ""),
    )
    handler.send_json(result)


# ---------------------------------------------------------------------------
# Audit
# ---------------------------------------------------------------------------

def _handle_query_audit(handler, session, query):
    start_time, end_time = _parse_time_range(query)
    user_id = query.get("user_id", [""])[0]
    instance_name = query.get("instance_name", [""])[0]
    risk_str = query.get("risk_level", [""])[0]
    risk_level = int(risk_str) if risk_str.isdigit() else None
    operation_type = query.get("operation_type", [""])[0]
    limit = min(int(query.get("limit", ["50"])[0]), 500)

    result = bridge.bridge_query_audit(
        start_time=start_time,
        end_time=end_time,
        user_id=user_id,
        instance_name=instance_name,
        risk_level=risk_level,
        operation_type=operation_type,
        limit=limit,
    )
    handler.send_json(result)


def _handle_export_audit(handler, session, query):
    start_time, end_time = _parse_time_range(query)
    user_id = query.get("user_id", [""])[0]
    risk_str = query.get("risk_level", [""])[0]
    risk_level = int(risk_str) if risk_str.isdigit() else None

    audit_result = bridge.bridge_query_audit(
        start_time=start_time,
        end_time=end_time,
        user_id=user_id,
        risk_level=risk_level,
        limit=5000,
    )

    logs = audit_result.get("logs", [])
    csv_data = bridge.bridge_export_audit_csv(logs)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    if csv_data:
        handler.send_csv(csv_data, f"audit_export_{timestamp}.csv")
    else:
        # Return empty CSV with headers when no data
        empty_csv = "timestamp,user_id,instance,operation_type,risk_level,sql,status,duration_ms\n"
        handler.send_csv(empty_csv, f"audit_export_{timestamp}.csv")


# ---------------------------------------------------------------------------
# Risk Rules
# ---------------------------------------------------------------------------

def _handle_list_rules(handler, session):
    rules = bridge.bridge_list_risk_rules()
    handler.send_json({"rules": rules})


def _handle_add_rule(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    rule_id = body.get("rule_id", "")
    pattern = body.get("pattern", "")
    risk_level = body.get("risk_level")

    if not rule_id or not pattern or risk_level is None:
        handler.send_json({"error": "缺少必要参数: rule_id, pattern, risk_level"}, status=400)
        return

    result = bridge.bridge_add_custom_rule(
        rule_id=rule_id,
        pattern=pattern,
        risk_level=int(risk_level),
        description=body.get("description", ""),
    )
    handler.send_json(result)


def _handle_delete_rule(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    rule_id = body.get("rule_id", "")
    if not rule_id:
        handler.send_json({"error": "缺少rule_id"}, status=400)
        return

    result = bridge.bridge_delete_custom_rule(rule_id)
    handler.send_json(result)


# ---------------------------------------------------------------------------
# Instances
# ---------------------------------------------------------------------------

def _handle_list_instances(handler, session):
    # Include credentials for admin edit form
    include_creds = handler.headers.get("X-Include-Credentials", "") == "true"
    instances = bridge.bridge_list_instances(include_credentials=include_creds)
    handler.send_json({"instances": instances})


def _handle_test_instance(handler, session, body):
    instance_name = body.get("instance_name", "")
    if not instance_name:
        handler.send_json({"error": "缺少instance_name"}, status=400)
        return
    # Extract optional direct credentials from the form (non-empty values only)
    direct_creds = {}
    for key in ("type", "host", "port", "database", "readonly_user", "readonly_pass"):
        val = body.get(key, "")
        if val != "":
            direct_creds[key] = val
    result = bridge.bridge_test_connection(instance_name, direct_creds if direct_creds else None)
    handler.send_json(result)


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def _handle_list_skills(handler, session):
    skills = bridge.bridge_list_skills()
    handler.send_json({"skills": skills})


# ---------------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------------

def _handle_dashboard_stats(handler, session):
    stats = bridge.bridge_get_dashboard_stats()
    handler.send_json(stats)


def _handle_ops_trend(handler, session, query):
    # Support both ?hours=24 and ?range=24h/7d/30d
    range_val = query.get("range", [""])[0]
    range_map = {"24h": 24, "7d": 168, "30d": 720}
    hours = range_map.get(range_val, int(query.get("hours", ["24"])[0]))
    hours = min(hours, 720)  # Cap at 30 days
    trend = bridge.bridge_get_ops_trend(hours=hours)
    handler.send_json({"trend": trend})


def _handle_risk_dist(handler, session):
    dist = bridge.bridge_get_risk_distribution()
    handler.send_json({"distribution": dist})


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------

def _handle_memory_status(handler, session):
    """Return current multi-layer memory state for diagnostics."""
    try:
        import sys
        from pathlib import Path
        _plugin_dir = str(Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard")
        if _plugin_dir not in sys.path:
            sys.path.insert(0, _plugin_dir)
        from memory.dba_memory_provider import get_provider
        from memory.l2_session_store import get_session_records
        from memory.l3_experience import list_experiences

        mem = get_provider()

        # L1 workspace snapshot
        l1_data = {
            "item_count": 0,
            "total_tokens": 0,
            "items": [],
        }
        if mem._initialized:
            snap = mem._l1.snapshot()
            l1_data = {
                "item_count": snap.get("item_count", 0),
                "total_tokens": snap.get("total_tokens", 0),
                "items": [
                    {"key": it.get("key", ""), "value": str(it.get("value", ""))[:200],
                     "priority": it.get("priority", ""), "category": it.get("category", "")}
                    for it in snap.get("items", [])[:20]
                ],
            }

        # L2 recent records for current session
        l2_records = []
        try:
            session_id = getattr(mem, "_session_id", None)
            if session_id:
                rows = get_session_records(session_id, limit=10)
                l2_records = [
                    {"operation": r.get("operation_type", ""), "content": r.get("content", "")[:150],
                     "db_type": r.get("db_type", ""), "risk_level": r.get("risk_level", 0)}
                    for r in rows
                ]
        except Exception:
            pass

        # L3 experiences (most recent)
        l3_experiences = []
        try:
            exps = list_experiences(limit=10)
            l3_experiences = [
                {"id": e.get("id", ""), "title": e.get("title", ""), "status": e.get("status", ""),
                 "category": e.get("category", ""), "created_at": e.get("created_at", "")}
                for e in exps
            ]
        except Exception:
            pass

        handler.send_json({
            "initialized": mem._initialized,
            "session_id": getattr(mem, "_session_id", None),
            "l1_workspace": l1_data,
            "l2_recent_records": l2_records,
            "l3_experiences": l3_experiences,
        })
    except Exception as e:
        handler.send_json({"error": str(e), "initialized": False})


def _handle_chat(handler, session, body):
    try:
        message = body.get("message", "").strip()
        execute_sql = body.get("execute_sql", "").strip()
        source_message = body.get("source_message", "").strip()
        display_message = message or source_message or execute_sql

        if not display_message:
            handler.send_json({"error": "消息不能为空"}, status=400)
            return

        instance_name = body.get("instance_name", "pg_test")
        dialect = body.get("dialect", "postgresql")
        is_rollback = body.get("is_rollback", False)
        safety_mode = body.get("safety_mode", 2)
        conversation_id = body.get("conversation_id", "")

        # Auto-create conversation if not provided
        if not conversation_id:
            title = display_message[:30] + ("…" if len(display_message) > 30 else "")
            conv = chat_store.create_conversation(title=title, instance_name=instance_name)
            conversation_id = conv["id"]

        # Save user message
        chat_store.save_message(conversation_id, "user", display_message)

        # Load conversation history from DB for LLM context
        history = chat_store.get_history_for_llm(conversation_id, max_messages=20)

        result = bridge.bridge_chat(
            message=message,
            instance_name=instance_name,
            dialect=dialect,
            user_id=session.get("user_id", "webui_user"),
            session_id=conversation_id,
            is_rollback=is_rollback,
            safety_mode=safety_mode,
            history=history,
            execute_sql=execute_sql,
            source_message=source_message,
        )

        if result.get("task") and isinstance(result["task"], dict):
            execution_result = result["task"].get("execution_result")
            data = execution_result.get("data") if isinstance(execution_result, dict) else None
            result_set_id = data.get("result_set_id") if isinstance(data, dict) else None
            if result_set_id:
                try:
                    from tools.safe_executor import bind_result_cache_owner
                    bind_result_cache_owner(
                        result_set_id,
                        conversation_id=conversation_id,
                        user_id=session.get("user_id", "webui_user"),
                    )
                except Exception:
                    logger.debug("failed to bind result cache owner", exc_info=True)

        # Save assistant response
        response_text = result.get("response") or result.get("error", "")
        intent_label = ""
        risk_level = None
        task_snapshot = None
        if result.get("intent"):
            intent_label = result["intent"].get("label", result["intent"].get("intent", ""))
        if result.get("task"):
            risk_level = result["task"].get("risk_level")
            task_snapshot = _build_task_snapshot(result.get("task"))
        elif result.get("generated_sql"):
            task_snapshot = {
                "generated_sql": result.get("generated_sql"),
                "response_type": result.get("response_type", "generation"),
                "source_message": result.get("source_message") or source_message or message,
            }
        chat_store.save_message(
            conversation_id, "assistant", response_text,
            intent=intent_label, risk_level=risk_level, task_snapshot=task_snapshot,
        )

        # Memory A: record every turn to L1 (workspace) + L2 (session store)
        # Memory B: every 10 user-turns trigger L3 distillation
        try:
            import sys
            from pathlib import Path
            _plugin_dir = str(Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard")
            if _plugin_dir not in sys.path:
                sys.path.insert(0, _plugin_dir)
            from memory.dba_memory_provider import get_provider
            mem = get_provider()
            if not mem._initialized or getattr(mem, "_session_id", None) != conversation_id:
                mem.initialize(
                    session_id=conversation_id,
                    user_id=session.get("user_id", "webui_user"),
                )
            mem.record_operation(
                intent_label or "chat",
                f"Q:{display_message[:80]}|A:{response_text[:160]}",
                risk_level=risk_level or 0,
                sql_text=(result.get("task") or {}).get("sql", "") if result.get("task") else "",
                db_type=dialect,
                instance_name=instance_name,
                intent_label=intent_label,
            )
            # Memory B: every 10 turns (=20 messages user+assistant) distil L3 experiences
            conv_info = chat_store.get_conversation(conversation_id)
            if conv_info and conv_info.get("message_count", 0) % 20 == 0:
                task_results = [result["task"]] if result.get("task") else []
                mem.on_session_end(task_results=task_results)
        except Exception:
            pass

        # Include conversation_id in response
        result["conversation_id"] = conversation_id
        handler.send_json(result)
    except Exception as e:
        logger.error("chat route failed: %s", e, exc_info=True)
        handler.send_json(
            {
                "error": f"聊天请求处理失败: {str(e)}",
                "conversation_id": body.get("conversation_id", ""),
            },
            status=500,
        )


def _handle_chat_result_page(handler, session, result_set_id, query):
    conversation_id = query.get("conversation_id", [""])[0].strip()
    if not conversation_id:
        handler.send_json({"error": "缺少conversation_id参数"}, status=400)
        return

    offset = max(int(query.get("offset", ["0"])[0]), 0)
    limit = min(max(int(query.get("limit", ["100"])[0]), 1), 100)

    try:
        from tools.safe_executor import fetch_result_page

        payload = fetch_result_page(
            result_set_id,
            offset=offset,
            limit=limit,
            conversation_id=conversation_id,
            user_id=session.get("user_id", "webui_user"),
        )
        status = 200 if not payload.get("error") else 404
        handler.send_json(payload, status=status)
    except Exception as e:
        logger.error("chat result page failed: %s", e, exc_info=True)
        handler.send_json({"error": f"结果分页读取失败: {e}"}, status=500)


# ---------------------------------------------------------------------------
# Conversations
# ---------------------------------------------------------------------------

def _handle_list_conversations(handler, session, query):
    limit = min(int(query.get("limit", ["50"])[0]), 200)
    offset = int(query.get("offset", ["0"])[0])
    convs = chat_store.list_conversations(limit=limit, offset=offset)
    handler.send_json({"conversations": convs})


def _handle_create_conversation(handler, session, body):
    title = body.get("title", "")
    instance_name = body.get("instance_name", "pg_test")
    conv = chat_store.create_conversation(title=title, instance_name=instance_name)
    handler.send_json(conv)


def _handle_get_conversation_messages(handler, session, conv_id, query):
    conv = chat_store.get_conversation(conv_id)
    if not conv:
        handler.send_json({"error": "会话不存在"}, status=404)
        return
    limit = min(int(query.get("limit", ["200"])[0]), 1000)
    messages = chat_store.get_messages(conv_id, limit=limit)
    handler.send_json({"conversation": conv, "messages": messages})


def _handle_delete_conversation(handler, session, conv_id):
    ok = chat_store.delete_conversation(conv_id)
    if ok:
        handler.send_json({"success": True})
    else:
        handler.send_json({"error": "会话不存在"}, status=404)


def _handle_search_conversations(handler, session, query):
    q = query.get("q", [""])[0].strip()
    if not q:
        handler.send_json({"conversations": []})
        return
    results = chat_store.search_conversations(q, limit=20)
    handler.send_json({"conversations": results})


# ---------------------------------------------------------------------------
# Instance Add / Remove
# ---------------------------------------------------------------------------

def _handle_add_instance(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    result = bridge.bridge_add_instance(body)
    handler.send_json(result)


def _handle_remove_instance(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    instance_name = body.get("name", "")
    if not instance_name:
        handler.send_json({"error": "缺少实例名称"}, status=400)
        return

    result = bridge.bridge_remove_instance(instance_name)
    handler.send_json(result)


def _handle_update_instance(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    instance_name = body.get("original_name", "") or body.get("name", "")
    if not instance_name:
        handler.send_json({"error": "缺少实例名称"}, status=400)
        return

    result = bridge.bridge_update_instance(instance_name, body)
    handler.send_json(result)


# ---------------------------------------------------------------------------
# LLM Config
# ---------------------------------------------------------------------------

def _handle_get_llm_config(handler, session):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    from llm_client import get_model_config, is_llm_configured
    config = get_model_config()
    # Don't leak actual API key — only show env var name
    handler.send_json({
        "config": config,
        "configured": is_llm_configured(),
    })


def _handle_save_llm_config(handler, session, body):
    admin_session = require_admin(handler)
    if not admin_session:
        return

    from llm_client import save_model_config
    result = save_model_config(body)
    handler.send_json(result)


def _handle_test_llm(handler, session, body):
    """Test LLM connectivity with a simple prompt."""
    from llm_client import chat_completion, is_llm_configured

    if not is_llm_configured():
        handler.send_json({"success": False, "error": "LLM 未配置"})
        return

    result = chat_completion(
        [{"role": "user", "content": "你好，请用一句话介绍自己。"}],
        max_tokens=100,
    )
    handler.send_json(result)
