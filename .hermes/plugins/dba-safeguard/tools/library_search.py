"""RAG知识库检索工具 — 从library/目录检索数据库官方文档。

核心能力:
  - 物理目录隔离: 按数据库类型+版本锁定检索路径
  - 强制检索: SQL生成/校验环节必须触发
  - 切片匹配: 基于heading切分，单片≤1000 token

安全约束:
  - 禁止跨库检索（Oracle操作不能搜MySQL文档）
  - 禁止修改library/下的文档
"""

from __future__ import annotations

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_safeguard.tools.library_search")

# Project root (where library/ lives)
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent


def search_library(
    query: str,
    db_type: str,
    version: str = "",
    max_results: int = 5,
) -> Dict[str, Any]:
    """Search the library knowledge base for relevant documentation.

    Args:
        query: Search query (keywords, SQL syntax, function names, etc.)
        db_type: Database type (mysql, postgresql, oracle, hive, etc.)
        version: Specific version (e.g., "5.7", "8.0", "19c")
        max_results: Maximum number of results to return

    Returns:
        {"results": [{"file": str, "section": str, "content": str, "score": float}]}
    """
    result: Dict[str, Any] = {"results": [], "search_path": ""}

    # Build search path with isolation
    lib_path = _PROJECT_ROOT / "library"
    if not lib_path.exists():
        result["results"].append({"error": f"知识库目录不存在: {lib_path}"})
        return result

    # Map db_type to library directory name
    type_map = {
        "mysql": "mysql",
        "postgresql": "postgres",
        "postgres": "postgres",
        "oracle": "oracle",
        "hive": "hive",
        "sqlserver": "sqlserver",
    }
    dir_name = type_map.get(db_type.lower())
    if not dir_name:
        result["results"].append({"error": f"不支持的数据库类型: {db_type}"})
        return result

    search_dir = lib_path / dir_name
    if version:
        version_dir = search_dir / version
        if version_dir.exists():
            search_dir = version_dir

    if not search_dir.exists():
        result["results"].append({"error": f"知识库路径不存在: {search_dir}"})
        return result

    result["search_path"] = str(search_dir.relative_to(_PROJECT_ROOT))

    # Search MD files
    matches = _search_md_files(search_dir, query, max_results)
    result["results"] = matches

    return result


def _search_md_files(
    directory: Path,
    query: str,
    max_results: int,
) -> List[Dict[str, Any]]:
    """Search Markdown files for relevant sections."""
    query_lower = query.lower()
    query_terms = [t.strip() for t in re.split(r'\s+', query_lower) if len(t.strip()) > 1]

    candidates: List[Dict[str, Any]] = []

    for md_file in directory.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            sections = _split_by_headings(text)

            for section_title, section_content in sections:
                if not section_content.strip():
                    continue

                score = _score_section(section_title, section_content, query_terms)
                if score > 0:
                    # Truncate to ~1000 tokens (~4000 chars)
                    content_preview = section_content[:4000]
                    if len(section_content) > 4000:
                        content_preview += "\n... (truncated)"

                    candidates.append({
                        "file": str(md_file.relative_to(directory)),
                        "section": section_title,
                        "content": content_preview,
                        "score": score,
                    })
        except Exception as e:
            logger.debug("Error reading %s: %s", md_file, e)

    # Sort by score descending and return top results
    candidates.sort(key=lambda x: x["score"], reverse=True)
    return candidates[:max_results]


def _split_by_headings(text: str) -> List[tuple]:
    """Split markdown text by headings."""
    sections = []
    current_title = "(top)"
    current_content = []

    for line in text.split("\n"):
        if line.startswith("#"):
            if current_content:
                sections.append((current_title, "\n".join(current_content)))
            current_title = line.lstrip("#").strip()
            current_content = [line]
        else:
            current_content.append(line)

    if current_content:
        sections.append((current_title, "\n".join(current_content)))

    return sections


def _score_section(title: str, content: str, query_terms: List[str]) -> float:
    """Score a section's relevance to the query."""
    title_lower = title.lower()
    content_lower = content.lower()
    score = 0.0

    for term in query_terms:
        # Title match is weighted higher
        if term in title_lower:
            score += 3.0
        # Content match
        count = content_lower.count(term)
        if count > 0:
            score += min(count, 5) * 0.5

    return score


# ---------------------------------------------------------------------------
# Tool Handler & Registration
# ---------------------------------------------------------------------------

def handle_library_search(args: dict, task_id: str = "", **kwargs) -> str:
    query = args.get("query", "")
    db_type = args.get("db_type", "")
    version = args.get("version", "")
    max_results = args.get("max_results", 5)

    if not query.strip():
        return json.dumps({"error": "query参数不能为空"})
    if not db_type:
        return json.dumps({"error": "db_type参数不能为空"})

    result = search_library(query, db_type, version, max_results)
    return json.dumps(result, ensure_ascii=False, indent=2)


LIBRARY_SEARCH_SCHEMA = {
    "name": "library_search",
    "description": (
        "从绝对真理RAG知识库检索数据库官方文档。"
        "按数据库类型+版本隔离检索路径，确保Oracle操作不会搜到MySQL文档。"
        "在生成SQL和校验语法时应主动调用此工具确认官方规范。"
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "检索关键词（SQL语法、函数名、功能描述等）",
            },
            "db_type": {
                "type": "string",
                "enum": ["mysql", "postgresql", "oracle", "hive", "sqlserver"],
                "description": "目标数据库类型",
            },
            "version": {
                "type": "string",
                "description": "数据库具体版本（如5.7、8.0、19c等）",
            },
            "max_results": {
                "type": "integer",
                "description": "最大返回结果数(默认5)",
                "default": 5,
            },
        },
        "required": ["query", "db_type"],
    },
}


def register_tools(ctx) -> None:
    ctx.register_tool(
        name="library_search",
        toolset="dba-safeguard",
        schema=LIBRARY_SEARCH_SCHEMA["parameters"],
        handler=handle_library_search,
        description=LIBRARY_SEARCH_SCHEMA["description"],
        emoji="📚",
    )
