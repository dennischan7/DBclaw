"""DBA Memory Provider — 4层记忆体系（L1-L4）的Hermes MemoryProvider实现。

继承 agent.memory_provider.MemoryProvider ABC:
  L1 — 对话上下文缓存 (Hermes内置，无需重复实现)
  L2 — 会话级工作记忆 (当前会话的SQL操作历史/元数据快照)
  L3 — 知识库RAG (library/目录，由library_search工具提供)
  L4 — 长期经验记忆 (跨会话的DBA操作经验/最佳实践)

注册方式: 通过 PluginContext.register_context_engine() 注入，
而非替换Hermes内置memory，二者并行工作。
"""

from __future__ import annotations

import json
import logging
import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.memory.dba_memory_provider")


class DBAMemoryProvider:
    """DBA-specific memory provider.

    NOT a subclass of MemoryProvider — we register as a context engine
    via ctx.register_context_engine() so it works alongside the built-in
    memory (only one external MemoryProvider allowed, we don't compete).

    Instead, this is called from our hooks:
      - pre_llm_call → inject L2/L4 context
      - post_tool_call → persist L2 working memory
      - on_session_end → flush to L4
    """

    def __init__(self):
        self._session_id: str = ""
        self._db_path: Optional[Path] = None
        self._conn: Optional[sqlite3.Connection] = None
        # L2: in-memory working state for current session
        self._working_memory: List[Dict[str, Any]] = []
        self._max_working_items = 50

    def initialize(self, session_id: str = "", hermes_home: str = "", **kwargs) -> None:
        """Initialize the DBA memory store."""
        self._session_id = session_id

        # Store L4 in persistent SQLite
        data_dir = Path(__file__).parent.parent / "data"
        data_dir.mkdir(parents=True, exist_ok=True)
        self._db_path = data_dir / "dba_memory.db"

        self._conn = sqlite3.connect(str(self._db_path), check_same_thread=False)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript("""
            CREATE TABLE IF NOT EXISTS l4_experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                category TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                db_type TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                relevance_score REAL DEFAULT 0.0
            );
            CREATE INDEX IF NOT EXISTS idx_l4_category ON l4_experience(category);
            CREATE INDEX IF NOT EXISTS idx_l4_tags ON l4_experience(tags);

            CREATE VIRTUAL TABLE IF NOT EXISTS l4_fts USING fts5(
                title, content, category, tags, content='l4_experience', content_rowid='id'
            );

            -- Triggers for FTS sync
            CREATE TRIGGER IF NOT EXISTS l4_ai AFTER INSERT ON l4_experience BEGIN
                INSERT INTO l4_fts(rowid, title, content, category, tags)
                VALUES (new.id, new.title, new.content, new.category, new.tags);
            END;
            CREATE TRIGGER IF NOT EXISTS l4_ad AFTER DELETE ON l4_experience BEGIN
                INSERT INTO l4_fts(l4_fts, rowid, title, content, category, tags)
                VALUES ('delete', old.id, old.title, old.content, old.category, old.tags);
            END;
        """)
        logger.info("DBA memory initialized, L4 store at %s", self._db_path)

    # -----------------------------------------------------------------------
    # L2: Working Memory (session-scoped)
    # -----------------------------------------------------------------------

    def add_working_memory(self, item: Dict[str, Any]) -> None:
        """Add an item to the current session's working memory."""
        item["timestamp"] = time.time()
        self._working_memory.append(item)
        # Evict oldest if over limit
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
    # L4: Long-term Experience
    # -----------------------------------------------------------------------

    def save_experience(
        self,
        category: str,
        title: str,
        content: str,
        db_type: str = "",
        tags: str = "",
    ) -> int:
        """Save a DBA experience to L4 persistent store."""
        if not self._conn:
            self.initialize()
        cursor = self._conn.execute(
            "INSERT INTO l4_experience (timestamp, category, title, content, db_type, tags) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (time.time(), category, title, content, db_type, tags),
        )
        self._conn.commit()
        return cursor.lastrowid

    def search_experience(self, query: str, limit: int = 5) -> List[Dict]:
        """Full-text search in L4 experience store."""
        if not self._conn:
            self.initialize()
        try:
            rows = self._conn.execute(
                """SELECT l4_experience.* FROM l4_experience
                   JOIN l4_fts ON l4_experience.id = l4_fts.rowid
                   WHERE l4_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query, limit),
            ).fetchall()
            columns = ["id", "timestamp", "category", "title", "content", "db_type", "tags", "relevance_score"]
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            logger.warning("L4 FTS search failed: %s", e)
            return []

    # -----------------------------------------------------------------------
    # Context Injection (called from pre_llm_call hook)
    # -----------------------------------------------------------------------

    def get_injection_context(self, user_query: str = "") -> str:
        """Build context to inject into LLM prompt."""
        parts = []

        # L2: Working memory summary
        l2 = self.get_working_memory_summary()
        if l2:
            parts.append(l2)

        # L4: Relevant experience
        if user_query:
            experiences = self.search_experience(user_query, limit=3)
            if experiences:
                parts.append("## 相关DBA经验")
                for exp in experiences:
                    parts.append(f"### {exp['title']} ({exp['category']})")
                    parts.append(exp["content"][:1000])

        return "\n\n".join(parts)

    # -----------------------------------------------------------------------
    # Session Lifecycle
    # -----------------------------------------------------------------------

    def on_session_end(self) -> None:
        """Flush working memory insights to L4 on session end."""
        if not self._working_memory:
            return

        # Extract session summary as L4 experience
        high_risk_ops = [
            m for m in self._working_memory
            if m.get("risk_level", 0) >= 2
        ]
        if high_risk_ops:
            summary_lines = []
            for op in high_risk_ops:
                summary_lines.append(f"- {op.get('operation')}: {op.get('detail', '')[:200]}")
            self.save_experience(
                category="session_summary",
                title=f"会话高风险操作记录 ({len(high_risk_ops)} ops)",
                content="\n".join(summary_lines),
                tags="session,high_risk",
            )
            logger.info("Flushed %d high-risk ops to L4", len(high_risk_ops))

        self.clear_working_memory()

    def shutdown(self) -> None:
        """Close L4 database connection."""
        if self._conn:
            self._conn.close()
            self._conn = None


# ---------------------------------------------------------------------------
# Tool Handlers (exposed as Hermes tools)
# ---------------------------------------------------------------------------

_provider = DBAMemoryProvider()


def get_provider() -> DBAMemoryProvider:
    return _provider


def handle_dba_memory_search(args: dict, task_id: str = "", **kwargs) -> str:
    query = args.get("query", "")
    limit = args.get("limit", 5)
    if not query:
        return json.dumps({"error": "query参数不能为空"})
    results = _provider.search_experience(query, limit)
    return json.dumps({"results": results, "count": len(results)}, ensure_ascii=False, default=str)


def handle_dba_memory_save(args: dict, task_id: str = "", **kwargs) -> str:
    category = args.get("category", "general")
    title = args.get("title", "")
    content = args.get("content", "")
    db_type = args.get("db_type", "")
    tags = args.get("tags", "")
    if not title or not content:
        return json.dumps({"error": "title和content参数不能为空"})
    row_id = _provider.save_experience(category, title, content, db_type, tags)
    return json.dumps({"result": "saved", "id": row_id})


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
        description="搜索DBA长期经验库，查找历史操作经验和最佳实践。",
        emoji="🧠",
    )
    ctx.register_tool(
        name="dba_memory_save",
        toolset="dba-safeguard",
        schema=DBA_MEMORY_SAVE_SCHEMA["parameters"],
        handler=handle_dba_memory_save,
        description="保存DBA操作经验到长期记忆库，供未来会话参考。",
        emoji="🧠",
    )
