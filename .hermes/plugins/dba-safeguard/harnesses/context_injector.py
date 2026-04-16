"""上下文注入器 — pre_llm_call 钩子，注入DBA系统提示和知识库上下文。

核心逻辑:
  - 在每次LLM调用前注入DBA角色系统提示
  - 注入当前连接的数据库实例信息
  - 如果检测到SQL生成意图，自动从library/注入相关文档片段
  - 注入当前会话的风险操作历史摘要
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.harnesses.context_injector")

DBA_SYSTEM_CONTEXT = """## DBA SafeGuard 安全规范

你是一个数据库安全管家，必须遵守以下规则：

### 操作约束
1. **禁止直接执行未经校验的SQL** — 任何SQL必须先调用 `sql_validate` 校验
2. **禁止跳过风险分级** — 所有写操作必须标注L0-L4风险等级
3. **L2+操作必须生成回滚脚本** — 调用 `rollback_generate` 生成
4. **L3/L4操作必须管理员审批** — 不可自动执行
5. **DELETE/UPDATE 必须有 WHERE** — 无WHERE条件的全表操作为L4级
6. **全链路审计** — 所有操作自动记录审计日志

### 操作流程
查询: sql_validate → explain_analyze → db_execute(L0)
修改: sql_validate → explain_analyze → rollback_generate → [人工审批] → db_execute
DDL:  sql_validate → rollback_generate → [管理员审批] → db_execute

### 知识库使用
生成SQL前必须调用 `library_search` 查阅对应数据库版本的官方文档，确保语法正确。
"""


async def pre_llm_call_hook(
    messages: List[Dict[str, Any]],
    context: Optional[Any] = None,
    **kwargs,
) -> Optional[List[Dict[str, Any]]]:
    """Hermes pre_llm_call hook for context injection.

    Injects DBA system context, active connection info, and relevant
    library snippets into the messages before LLM processing.

    Returns:
        Modified messages list, or None to keep original.
    """
    injections = []

    # 1. DBA system context
    injections.append(DBA_SYSTEM_CONTEXT)

    # 2. Active connection info
    try:
        from ..tools.db_connector import get_connection_manager
        mgr = get_connection_manager()
        instances = mgr.list_instances()
        if instances:
            conn_info = "\n## 当前可用数据库实例\n"
            for inst in instances:
                conn_info += f"- **{inst['name']}** ({inst['type']}) @ {inst['host']}\n"
            injections.append(conn_info)
    except Exception:
        pass

    # 3. Classify intent and mount relevant harness specs
    user_msg = _get_last_user_message(messages)
    if user_msg:
        try:
            from .intent_router import classify_intent, get_routing_context
            from .config_watcher import get_config_watcher

            watcher = get_config_watcher()
            watcher.check_and_reload()  # hot-reload any changed configs

            intent = classify_intent(user_msg, context={"dialect": None})
            routing = get_routing_context(intent)

            # Inject intent classification summary
            intent_info = (
                f"\n## 意图分析\n"
                f"- **分类**: {intent['label']} ({intent['intent']})\n"
                f"- **置信度**: {intent['confidence']:.0%}\n"
                f"- **风险预判**: L{intent['risk_preset']}\n"
            )
            if intent.get("db_type"):
                intent_info += f"- **目标数据库**: {intent['db_type']}"
                if intent.get("db_version"):
                    intent_info += f" {intent['db_version']}"
                intent_info += "\n"
            if routing.get("tool_sequence"):
                intent_info += f"- **建议工具链**: {' → '.join(routing['tool_sequence'])}\n"
            injections.append(intent_info)

            # Mount stage workflow if available
            if routing.get("workflow_file"):
                workflow_content = watcher.get_stage_workflow(
                    intent.get("workflow", "")
                )
                if workflow_content:
                    injections.append(
                        f"\n## 当前工作流规范\n\n{workflow_content[:2000]}"
                    )

        except Exception as e:
            logger.debug("Intent classification skipped: %s", e)

        # Fallback: if no intent classification, use simple SQL detection
        if not any("意图分析" in inj for inj in injections):
            if _detect_sql_intent(user_msg):
                injections.append(
                    "\n## 提示\n"
                    "检测到SQL相关操作意图。请先使用 `library_search` 查阅官方文档，"
                    "确认目标数据库方言的正确语法后再生成SQL。"
                )

    if not injections:
        return None

    # Inject as a system-level context block
    injection_text = "\n".join(injections)

    # Prepend to messages as a system instruction
    modified = list(messages)
    # Find the first system message and append to it, or insert new one
    for i, msg in enumerate(modified):
        if msg.get("role") == "system":
            modified[i] = {
                **msg,
                "content": msg.get("content", "") + "\n\n" + injection_text,
            }
            return modified

    # No system message found — insert one at the beginning
    modified.insert(0, {"role": "system", "content": injection_text})
    return modified


def _get_last_user_message(messages: List[Dict]) -> str:
    """Extract the last user message text."""
    for msg in reversed(messages):
        if msg.get("role") == "user":
            content = msg.get("content", "")
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                parts = [p.get("text", "") for p in content if isinstance(p, dict)]
                return " ".join(parts)
    return ""


def _detect_sql_intent(text: str) -> bool:
    """Detect if the user message implies SQL generation or database operations."""
    sql_keywords = [
        "sql", "query", "查询", "select", "insert", "update", "delete",
        "create table", "alter table", "drop", "index", "join",
        "执行", "数据库", "表结构", "建表", "加字段", "删表",
        "存储过程", "触发器", "视图", "分区", "索引",
    ]
    text_lower = text.lower()
    return any(kw in text_lower for kw in sql_keywords)
