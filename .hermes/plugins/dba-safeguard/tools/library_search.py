"""RAG知识库检索工具 — 从library/目录检索数据库官方文档。

核心能力:
  - 物理目录隔离: 按数据库类型+版本锁定检索路径
  - 强制检索: SQL生成/校验环节必须触发
  - Token感知切片: 基于heading切分，单片≤1000 token (~4000 chars)
  - 多级评分: 标题权重×3 + 精确匹配×2 + 关键词频率

安全约束:
  - 禁止跨库检索（Oracle操作不能搜MySQL文档）
  - 禁止修改library/下的文档
"""

from __future__ import annotations

import json
import logging
import math
import os
import re
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("dba_safeguard.tools.library_search")

# Project root (where library/ lives)
_PROJECT_ROOT = Path(__file__).parent.parent.parent.parent.parent

# Token estimation: ~4 chars per token for English, ~2 chars for CJK
MAX_CHUNK_TOKENS = 1000
MAX_CHUNK_CHARS = MAX_CHUNK_TOKENS * 4  # conservative English estimate

# Cache for indexed chunks (invalidated on search_path change)
_chunk_cache: Dict[str, List[Dict[str, Any]]] = {}


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
        {"results": [{"file": str, "section": str, "content": str, "score": float}],
         "search_path": str, "total_chunks": int}
    """
    result: Dict[str, Any] = {"results": [], "search_path": "", "total_chunks": 0}

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

    # Get or build chunk index
    chunks = _get_chunks(search_dir)
    result["total_chunks"] = len(chunks)

    # Score and rank
    matches = _rank_chunks(chunks, query, max_results)
    result["results"] = matches

    return result


def _get_chunks(search_dir: Path) -> List[Dict[str, Any]]:
    """Get token-aware chunks for a search directory (with caching)."""
    cache_key = str(search_dir)
    if cache_key in _chunk_cache:
        return _chunk_cache[cache_key]

    chunks: List[Dict[str, Any]] = []
    for md_file in search_dir.rglob("*.md"):
        try:
            text = md_file.read_text(encoding="utf-8", errors="ignore")
            rel_path = str(md_file.relative_to(search_dir))
            file_chunks = _chunk_document(text, rel_path)
            chunks.extend(file_chunks)
        except Exception as e:
            logger.debug("Error reading %s: %s", md_file, e)

    _chunk_cache[cache_key] = chunks
    return chunks


def invalidate_cache(search_dir: Optional[str] = None) -> None:
    """Invalidate chunk cache. If search_dir given, only that path."""
    if search_dir:
        _chunk_cache.pop(search_dir, None)
    else:
        _chunk_cache.clear()


def _chunk_document(text: str, file_path: str) -> List[Dict[str, Any]]:
    """Split a document into token-aware chunks (≤1000 tokens each).

    Strategy:
      1. Split by headings first
      2. If a section exceeds MAX_CHUNK_CHARS, split by paragraphs
      3. Each chunk keeps its heading context for relevance
    """
    sections = _split_by_headings(text)
    chunks: List[Dict[str, Any]] = []

    for title, content in sections:
        if not content.strip():
            continue

        if len(content) <= MAX_CHUNK_CHARS:
            chunks.append({
                "file": file_path,
                "section": title,
                "content": content,
            })
        else:
            # Split oversized section by paragraphs
            sub_chunks = _split_by_paragraphs(content, title, MAX_CHUNK_CHARS)
            for i, sub in enumerate(sub_chunks):
                chunks.append({
                    "file": file_path,
                    "section": f"{title} (part {i + 1})" if len(sub_chunks) > 1 else title,
                    "content": sub,
                })

    return chunks


def _split_by_headings(text: str) -> List[Tuple[str, str]]:
    """Split markdown text by headings."""
    sections: List[Tuple[str, str]] = []
    current_title = "(top)"
    current_content: List[str] = []

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


def _split_by_paragraphs(text: str, title: str, max_chars: int) -> List[str]:
    """Split text into chunks at paragraph boundaries, keeping under max_chars."""
    paragraphs = re.split(r'\n\s*\n', text)
    chunks: List[str] = []
    current: List[str] = []
    current_len = 0

    for para in paragraphs:
        para_len = len(para)
        if current_len + para_len > max_chars and current:
            chunks.append("\n\n".join(current))
            current = [para]
            current_len = para_len
        else:
            current.append(para)
            current_len += para_len

    if current:
        chunks.append("\n\n".join(current))

    return chunks


def _rank_chunks(
    chunks: List[Dict[str, Any]],
    query: str,
    max_results: int,
) -> List[Dict[str, Any]]:
    """Rank chunks by relevance using multi-signal scoring."""
    query_lower = query.lower()
    query_terms = [t.strip() for t in re.split(r'\s+', query_lower) if len(t.strip()) > 1]
    if not query_terms:
        return []

    # Build document frequency for IDF
    num_chunks = len(chunks)
    if num_chunks == 0:
        return []

    doc_freq: Counter = Counter()
    for chunk in chunks:
        combined = (chunk["section"] + " " + chunk["content"]).lower()
        seen = set()
        for term in query_terms:
            if term in combined and term not in seen:
                doc_freq[term] += 1
                seen.add(term)

    scored: List[Dict[str, Any]] = []
    for chunk in chunks:
        score = _score_chunk(chunk, query_terms, query_lower, doc_freq, num_chunks)
        if score > 0:
            scored.append({
                "file": chunk["file"],
                "section": chunk["section"],
                "content": chunk["content"],
                "score": round(score, 3),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:max_results]


def _score_chunk(
    chunk: Dict[str, Any],
    query_terms: List[str],
    query_lower: str,
    doc_freq: Counter,
    num_chunks: int,
) -> float:
    """Multi-signal scoring for a chunk."""
    title_lower = chunk["section"].lower()
    content_lower = chunk["content"].lower()
    score = 0.0

    for term in query_terms:
        idf = math.log(1 + num_chunks / (1 + doc_freq.get(term, 0)))

        # Title match (high weight)
        if term in title_lower:
            score += 3.0 * idf

        # Content TF-IDF
        tf = content_lower.count(term)
        if tf > 0:
            norm_tf = 1 + math.log(tf)  # log-normalized TF
            score += norm_tf * idf * 0.5

    # Bonus: exact phrase match in content
    if len(query_terms) > 1 and query_lower in content_lower:
        score += 5.0

    # Bonus: exact phrase match in title
    if len(query_terms) > 1 and query_lower in title_lower:
        score += 8.0

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
