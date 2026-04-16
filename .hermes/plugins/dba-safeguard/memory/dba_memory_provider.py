"""DBA Memory Provider — 4层记忆体系（L1-L4）统一编排器。

四层架构:
  L1 — 工作区记忆 (token-bounded, ≤4000 token, 会话内临时上下文)
  L2 — 情景会话记忆 (SQLite FTS5, DBA标签, 跨会话检索)
  L3 — 运维经验记忆 (经验沉淀+人工确认, FTS5检索)
  L4 — 业务图谱与用户建模 (血缘关系/字典/规则/画像)

注册方式: 通过 PluginContext.register_context_engine() 注入，
而非替换Hermes内置memory，二者并行工作。

Hooks integration:
  - pre_llm_call → get_injection_context() — 注入L1/L2/L3/L4上下文
  - post_tool_call → record_operation() — 记录操作到L1+L2
  - on_session_start → initialize() — 初始化所有层
  - on_session_end → on_session_end() — 归档L1→L2, 沉淀L3经验
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, List, Optional

try:
    from .l1_workspace import L1WorkspaceMemory, ContextPriority
    from .l2_session_store import (
        save_session_record,
        search_sessions,
        search_similar_operations,
        get_session_summary,
        archive_old_sessions,
    )
    from .l3_experience import (
        distill_experience,
        search_experiences,
        recall_for_task,
        get_pending_experiences,
        confirm_experience,
    )
    from .l4_business_graph import (
        get_graph_context,
        get_user_profile,
        update_user_profile,
        record_user_operation,
    )
except ImportError:
    from l1_workspace import L1WorkspaceMemory, ContextPriority
    from l2_session_store import (
        save_session_record,
        search_sessions,
        search_similar_operations,
        get_session_summary,
        archive_old_sessions,
    )
    from l3_experience import (
        distill_experience,
        search_experiences,
        recall_for_task,
        get_pending_experiences,
        confirm_experience,
    )
    from l4_business_graph import (
        get_graph_context,
        get_user_profile,
        update_user_profile,
        record_user_operation,
    )

logger = logging.getLogger("dba_safeguard.memory.dba_memory_provider")


class DBAMemoryProvider:
    """Unified DBA memory provider orchestrating all 4 layers.

    NOT a subclass of MemoryProvider — registered as context engine
    via ctx.register_context_engine().

    Called from hooks:
      - pre_llm_call → inject L1/L2/L3/L4 context
      - post_tool_call → persist to L1 + L2
      - on_session_start → initialize
      - on_session_end → archive L1→L2, distill L3
    """

    def __init__(self):
        self._session_id: str = ""
        self._user_id: str = "default"
        self._initialized: bool = False

        # L1: Token-bounded workspace memory
        self._l1 = L1WorkspaceMemory()

        # Legacy L2 in-memory list (kept for backward compat)
        self._working_memory: List[Dict[str, Any]] = []
        self._max_working_items = 50

    def initialize(self, session_id: str = "", user_id: str = "default",
                   hermes_home: str = "", **kwargs) -> None:
        """Initialize all memory layers."""
        self._session_id = session_id
        self._user_id = user_id
        self._initialized = True

        # L1 starts empty each session
        self._l1.clear()

        # Archive old L2 sessions
        try:
            archive_old_sessions()
        except Exception as e:
            logger.debug("L2 archival skipped: %s", e)

        logger.info("DBA memory provider initialized (session=%s)", session_id)

    # -----------------------------------------------------------------------
    # L1: Workspace Memory (token-bounded)
    # -----------------------------------------------------------------------

    @property
    def workspace(self) -> L1WorkspaceMemory:
        """Direct access to L1 workspace memory."""
        return self._l1

    # -----------------------------------------------------------------------
    # Operation Recording (L1 + L2)
    # -----------------------------------------------------------------------

    def record_operation(
        self,
        operation: str,
        detail: str,
        *,
        risk_level: int = 0,
        sql_text: str = "",
        db_type: str = "",
        instance_name: str = "",
        intent_label: str = "",
        extra: Dict[str, Any] = None,
    ) -> None:
        """Record a DBA operation to L1 workspace + L2 session store.

        Called from post_tool_call hook or pipeline stages.
        """
        # L1: Update workspace with latest operation
        self._l1.set(
            f"op:{operation}",
            f"{detail}" + (f" (L{risk_level})" if risk_level else ""),
            priority=ContextPriority.HIGH if risk_level >= 2 else ContextPriority.NORMAL,
            category="validation" if "validat" in operation.lower() else "task",
        )

        # L2: Persist to session store
        try:
            save_session_record(
                session_id=self._session_id,
                role="tool",
                content=f"[{operation}] {detail}",
                db_type=db_type,
                instance_name=instance_name,
                operation_type=operation,
                risk_level=risk_level,
                intent_label=intent_label,
                sql_text=sql_text,
                extra_data=json.dumps(extra, ensure_ascii=False) if extra else "",
            )
        except Exception as e:
            logger.debug("L2 record failed: %s", e)

        # Legacy in-memory working memory (backward compat)
        item = {
            "operation": operation,
            "detail": detail,
            "risk_level": risk_level,
            "timestamp": time.time(),
        }
        self._working_memory.append(item)
        if len(self._working_memory) > self._max_working_items:
            self._working_memory = self._working_memory[-self._max_working_items:]

        # L4: Record for user profiling
        try:
            record_user_operation(self._user_id, operation, db_type)
        except Exception as e:
            logger.debug("L4 user profiling failed: %s", e)

    # -----------------------------------------------------------------------
    # Legacy L2: Working Memory (backward compat)
    # -----------------------------------------------------------------------

    def add_working_memory(self, item: Dict[str, Any]) -> None:
        """Add an item to the current session's working memory (legacy)."""
        item["timestamp"] = time.time()
        self._working_memory.append(item)
        if len(self._working_memory) > self._max_working_items:
            self._working_memory = self._working_memory[-self._max_working_items:]

    def get_working_memory_summary(self, max_items: int = 10) -> str:
        """Get a text summary of recent working memory."""
        if not self._working_memory:
            return ""
        recent = self._working_memory[-max_items:]
        lines = ["## 当前会话操作历史"]
        for item in recent:
            op = item.get("operation", "unknown")
            detail = item.get("detail", "")
            risk = item.get("risk_level", "")
            lines.append(f"- [{op}] {detail}" + (f" (L{risk})" if risk else ""))
        return "\n".join(lines)

    def clear_working_memory(self) -> None:
        self._working_memory.clear()

    # -----------------------------------------------------------------------
    # Context Injection (called from pre_llm_call hook)
    # -----------------------------------------------------------------------

    def get_injection_context(
        self,
        user_query: str = "",
        tables: List[str] = None,
    ) -> str:
        """Build multi-layer context to inject into LLM prompt.

        Aggregates context from all 4 layers:
          L1: Current workspace state
          L2: Similar past operations
          L3: Relevant confirmed experiences
          L4: Business graph + user profile
        """
        parts = []

        # L1: Workspace context (token-bounded snapshot)
        l1_ctx = self._l1.render_context(max_tokens=2000)
        if l1_ctx:
            parts.append(l1_ctx)

        # L2: Working memory summary (in-memory, fast)
        l2_summary = self.get_working_memory_summary()
        if l2_summary:
            parts.append(l2_summary)

        # L3: Relevant confirmed experiences
        if user_query:
            try:
                experiences = search_experiences(user_query, limit=3)
                if experiences:
                    exp_lines = ["## 相关运维经验"]
                    for exp in experiences:
                        exp_lines.append(f"### {exp['title']} ({exp['category']})")
                        exp_lines.append(exp["content"][:800])
                    parts.append("\n".join(exp_lines))
            except Exception as e:
                logger.debug("L3 experience search failed: %s", e)

        # L4: Business graph context
        if tables:
            try:
                graph_ctx = get_graph_context(
                    tables=tables,
                    user_id=self._user_id,
                    instance_name="",
                )
                if graph_ctx:
                    parts.append(graph_ctx)
            except Exception as e:
                logger.debug("L4 graph context failed: %s", e)

        return "\n\n".join(parts)

    # -----------------------------------------------------------------------
    # Session Lifecycle
    # -----------------------------------------------------------------------

    def on_session_end(self, task_results: List[Dict] = None) -> None:
        """End-of-session processing.

        1. Archive L1 workspace snapshot to L2
        2. Distill successful tasks to L3 (pending confirmation)
        3. Flush working memory
        """
        # Archive L1 → L2
        if self._l1.item_count > 0:
            snapshot = self._l1.snapshot()
            try:
                save_session_record(
                    session_id=self._session_id,
                    role="system",
                    content=f"会话结束 — 工作区快照 ({self._l1.total_tokens} tokens, "
                            f"{self._l1.item_count} items)",
                    workspace_snapshot=json.dumps(snapshot, ensure_ascii=False),
                )
            except Exception as e:
                logger.debug("L1→L2 archive failed: %s", e)

        # Distill L3 experiences from successful tasks
        pending_count = 0
        for result in (task_results or []):
            try:
                exp_id = distill_experience(result, require_confirmation=True)
                if exp_id:
                    pending_count += 1
            except Exception as e:
                logger.debug("L3 distillation failed for task: %s", e)

        if pending_count:
            logger.info("Created %d pending experiences for user confirmation", pending_count)

        # Legacy: flush high-risk ops summary
        high_risk_ops = [
            m for m in self._working_memory
            if m.get("risk_level", 0) >= 2
        ]
        if high_risk_ops:
            try:
                save_session_record(
                    session_id=self._session_id,
                    role="system",
                    content=f"高风险操作汇总: {len(high_risk_ops)} ops",
                    risk_level=max(m.get("risk_level", 0) for m in high_risk_ops),
                    tags="high_risk,summary",
                )
            except Exception as e:
                logger.debug("High-risk summary save failed: %s", e)

        self._l1.clear()
        self.clear_working_memory()

    def shutdown(self) -> None:
        """Cleanup resources."""
        self._l1.clear()
        self._working_memory.clear()
        self._initialized = False


# ---------------------------------------------------------------------------
# Module-level singleton
# ---------------------------------------------------------------------------

_provider = DBAMemoryProvider()


def get_provider() -> DBAMemoryProvider:
    return _provider


# ---------------------------------------------------------------------------
# Tool Handlers (exposed as Hermes tools)
# ---------------------------------------------------------------------------

def handle_dba_memory_search(args: dict, task_id: str = "", **kwargs) -> str:
    query = args.get("query", "")
    limit = args.get("limit", 5)
    if not query:
        return json.dumps({"error": "query参数不能为空"})
    # Search both L3 experiences and L2 sessions
    results = []
    try:
        experiences = search_experiences(query, limit=limit)
        for exp in experiences:
            results.append({
                "source": "L3_experience",
                "id": exp.get("id"),
                "title": exp.get("title", ""),
                "category": exp.get("category", ""),
                "content": exp.get("content", "")[:500],
                "db_type": exp.get("db_type", ""),
            })
    except Exception:
        pass

    try:
        sessions = search_sessions(query, limit=limit)
        for sess in sessions:
            results.append({
                "source": "L2_session",
                "id": sess.get("id"),
                "content": sess.get("content", "")[:500],
                "db_type": sess.get("db_type", ""),
                "risk_level": sess.get("risk_level", -1),
            })
    except Exception:
        pass

    return json.dumps({"results": results, "count": len(results)}, ensure_ascii=False, default=str)


def handle_dba_memory_save(args: dict, task_id: str = "", **kwargs) -> str:
    category = args.get("category", "general")
    title = args.get("title", "")
    content = args.get("content", "")
    db_type = args.get("db_type", "")
    tags = args.get("tags", "")
    if not title or not content:
        return json.dumps({"error": "title和content参数不能为空"})

    # Save to L3 experience store (pending confirmation)
    try:
        from .l3_experience import _save_experience
    except ImportError:
        from l3_experience import _save_experience

    exp_id = _save_experience(
        category=category,
        title=title,
        content=content,
        db_type=db_type,
        tags=tags,
        status="pending",
    )
    return json.dumps({"result": "saved_pending", "id": exp_id,
                       "message": "经验已保存，需用户确认后生效"})


DBA_MEMORY_SEARCH_SCHEMA = {
    "parameters": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "搜索关键词"},
            "limit": {"type": "integer", "description": "最大返回数量", "default": 5},
        },
        "required": ["query"],
    },
}

DBA_MEMORY_SAVE_SCHEMA = {
    "parameters": {
        "type": "object",
        "properties": {
            "category": {"type": "string", "description": "经验类别(如troubleshooting, optimization, best_practice)"},
            "title": {"type": "string", "description": "经验标题"},
            "content": {"type": "string", "description": "经验内容"},
            "db_type": {"type": "string", "description": "相关数据库类型"},
            "tags": {"type": "string", "description": "标签(逗号分隔)"},
        },
        "required": ["title", "content"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="dba_memory_search",
        toolset="dba-safeguard",
        schema=DBA_MEMORY_SEARCH_SCHEMA["parameters"],
        handler=handle_dba_memory_search,
        description="搜索DBA记忆库（L2会话记忆+L3运维经验），查找历史操作经验和最佳实践。",
        emoji="🧠",
    )
    ctx.register_tool(
        name="dba_memory_save",
        toolset="dba-safeguard",
        schema=DBA_MEMORY_SAVE_SCHEMA["parameters"],
        handler=handle_dba_memory_save,
        description="保存DBA操作经验到L3长期记忆库（需用户确认后生效）。",
        emoji="🧠",
    )
