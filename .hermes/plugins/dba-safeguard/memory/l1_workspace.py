"""L1 工作区记忆 — 当前会话的临时上下文管理。

核心规则:
  - 严格控制长度: 总长度≤4000 token (MAX_WORKSPACE_TOKENS)
  - 存储当前工单需求、目标库表结构、历史重试草稿、当前任务状态/风险等级
  - 会话结束后自动归档到L2 (由session_hooks调用)
  - 自动压缩无效内容，保留高价值上下文

Token估算: 1 token ≈ 4 字符 (英文) / 2 字符 (中文), 取保守估计 ~3 chars/token
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.memory.l1_workspace")

MAX_WORKSPACE_TOKENS = 4000
CHARS_PER_TOKEN = 3  # conservative estimate


class ContextPriority(str, Enum):
    """Priority levels for workspace context items."""
    CRITICAL = "critical"    # current task state, risk level — never evict
    HIGH = "high"            # target schema metadata, validation results
    NORMAL = "normal"        # user requirements, retry drafts
    LOW = "low"              # informational messages, hints


@dataclass
class WorkspaceItem:
    """A single context item in workspace memory."""
    key: str
    content: str
    priority: ContextPriority = ContextPriority.NORMAL
    timestamp: float = 0.0
    token_estimate: int = 0
    category: str = ""       # "task", "metadata", "validation", "retry", "info"

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = time.time()
        if not self.token_estimate:
            self.token_estimate = _estimate_tokens(self.content)


def _estimate_tokens(text: str) -> int:
    """Estimate token count for a string."""
    if not text:
        return 0
    return max(1, len(text) // CHARS_PER_TOKEN)


class L1WorkspaceMemory:
    """Token-bounded workspace memory for the current session.

    Manages a prioritized set of context items within a strict token budget.
    Lower-priority items are evicted first when the budget is exceeded.
    """

    def __init__(self, max_tokens: int = MAX_WORKSPACE_TOKENS):
        self._max_tokens = max_tokens
        self._items: Dict[str, WorkspaceItem] = {}

    @property
    def total_tokens(self) -> int:
        return sum(item.token_estimate for item in self._items.values())

    @property
    def remaining_tokens(self) -> int:
        return max(0, self._max_tokens - self.total_tokens)

    @property
    def item_count(self) -> int:
        return len(self._items)

    # ------------------------------------------------------------------
    # Core Operations
    # ------------------------------------------------------------------

    def set(
        self,
        key: str,
        content: str,
        priority: ContextPriority = ContextPriority.NORMAL,
        category: str = "",
    ) -> bool:
        """Set a context item. Replaces if key exists. Returns True if successful.

        If the new item exceeds budget, low-priority items are evicted.
        If still insufficient, the content is truncated.
        """
        new_item = WorkspaceItem(
            key=key, content=content, priority=priority, category=category,
        )

        # Remove old version if exists (to reclaim tokens)
        old = self._items.pop(key, None)

        # Check if fits
        if self.total_tokens + new_item.token_estimate <= self._max_tokens:
            self._items[key] = new_item
            return True

        # Evict lower-priority items to make room
        needed = self.total_tokens + new_item.token_estimate - self._max_tokens
        evicted = self._evict(needed, min_priority=new_item.priority)

        if self.total_tokens + new_item.token_estimate <= self._max_tokens:
            self._items[key] = new_item
            return True

        # Still not enough — truncate the content
        available = self._max_tokens - self.total_tokens
        if available > 10:  # at least 10 tokens worth
            truncated = content[:available * CHARS_PER_TOKEN]
            new_item = WorkspaceItem(
                key=key, content=truncated, priority=priority, category=category,
            )
            self._items[key] = new_item
            logger.debug("Truncated workspace item '%s' to %d tokens", key, new_item.token_estimate)
            return True

        # Restore old item if eviction failed completely
        if old:
            self._items[key] = old
        return False

    def get(self, key: str) -> Optional[str]:
        """Get a context item's content by key."""
        item = self._items.get(key)
        return item.content if item else None

    def remove(self, key: str) -> bool:
        """Remove a context item."""
        return self._items.pop(key, None) is not None

    def clear(self) -> None:
        """Clear all workspace items."""
        self._items.clear()

    def get_all(self) -> List[WorkspaceItem]:
        """Get all items sorted by priority (critical first) then timestamp."""
        priority_order = {
            ContextPriority.CRITICAL: 0,
            ContextPriority.HIGH: 1,
            ContextPriority.NORMAL: 2,
            ContextPriority.LOW: 3,
        }
        return sorted(
            self._items.values(),
            key=lambda x: (priority_order.get(x.priority, 9), x.timestamp),
        )

    # ------------------------------------------------------------------
    # Context Rendering
    # ------------------------------------------------------------------

    def render_context(self, max_tokens: Optional[int] = None) -> str:
        """Render workspace memory as a formatted context string for LLM injection.

        Args:
            max_tokens: Optional further limit on output tokens.
        """
        items = self.get_all()
        if not items:
            return ""

        sections: Dict[str, List[str]] = {}
        total = 0
        limit = max_tokens or self._max_tokens

        for item in items:
            if total + item.token_estimate > limit:
                break
            cat = item.category or "其他"
            if cat not in sections:
                sections[cat] = []
            sections[cat].append(f"- **{item.key}**: {item.content}")
            total += item.token_estimate

        lines = ["## 当前工作区上下文"]
        category_labels = {
            "task": "📋 任务状态",
            "metadata": "📊 库表元数据",
            "validation": "✅ 校验记录",
            "retry": "🔄 重试草稿",
            "info": "ℹ️ 信息",
        }
        for cat, entries in sections.items():
            label = category_labels.get(cat, f"📎 {cat}")
            lines.append(f"\n### {label}")
            lines.extend(entries)

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Convenience Methods
    # ------------------------------------------------------------------

    def set_task_state(self, task_id: str, sql: str, risk_level: int,
                       current_stage: str = "") -> None:
        """Update current task state (CRITICAL priority)."""
        parts = [f"任务ID: {task_id}", f"风险等级: L{risk_level}"]
        if current_stage:
            parts.append(f"当前阶段: {current_stage}")
        if sql:
            # Truncate SQL to avoid blowing budget
            sql_preview = sql[:500] + ("..." if len(sql) > 500 else "")
            parts.append(f"SQL: {sql_preview}")
        self.set("current_task", "\n".join(parts),
                 priority=ContextPriority.CRITICAL, category="task")

    def set_metadata(self, key: str, content: str) -> None:
        """Add metadata context (HIGH priority)."""
        self.set(f"meta:{key}", content,
                 priority=ContextPriority.HIGH, category="metadata")

    def add_validation_result(self, stage: str, passed: bool, detail: str = "") -> None:
        """Record a validation result (HIGH priority)."""
        status = "✅ 通过" if passed else "❌ 失败"
        content = f"{status}" + (f" — {detail}" if detail else "")
        self.set(f"val:{stage}", content,
                 priority=ContextPriority.HIGH, category="validation")

    def add_retry_draft(self, round_num: int, sql: str) -> None:
        """Record a retry SQL draft (NORMAL priority)."""
        sql_preview = sql[:300] + ("..." if len(sql) > 300 else "")
        self.set(f"retry:{round_num}", sql_preview,
                 priority=ContextPriority.NORMAL, category="retry")

    def snapshot(self) -> Dict[str, Any]:
        """Create a serializable snapshot for archival to L2."""
        return {
            "timestamp": time.time(),
            "total_tokens": self.total_tokens,
            "items": [
                {
                    "key": item.key,
                    "content": item.content,
                    "priority": item.priority.value,
                    "category": item.category,
                    "timestamp": item.timestamp,
                }
                for item in self.get_all()
            ],
        }

    # ------------------------------------------------------------------
    # Eviction
    # ------------------------------------------------------------------

    def _evict(self, tokens_needed: int, min_priority: ContextPriority) -> int:
        """Evict lowest-priority items to free at least `tokens_needed` tokens.

        Only evicts items with priority lower than `min_priority`.
        Returns the number of tokens freed.
        """
        priority_rank = {
            ContextPriority.CRITICAL: 0,
            ContextPriority.HIGH: 1,
            ContextPriority.NORMAL: 2,
            ContextPriority.LOW: 3,
        }
        min_rank = priority_rank.get(min_priority, 9)

        # Sort candidates: lowest priority first, oldest first
        candidates = [
            (k, v) for k, v in self._items.items()
            if priority_rank.get(v.priority, 9) > min_rank
        ]
        candidates.sort(key=lambda x: (-priority_rank.get(x[1].priority, 9), x[1].timestamp))

        freed = 0
        for key, item in candidates:
            if freed >= tokens_needed:
                break
            freed += item.token_estimate
            del self._items[key]
            logger.debug("Evicted workspace item '%s' (priority=%s, tokens=%d)",
                         key, item.priority.value, item.token_estimate)

        return freed
