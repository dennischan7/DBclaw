"""DBA SafeGuard WebUI — LLM Client.

Reads model configuration from dba_config.yaml and provides
OpenAI-compatible chat completion calls.

Config format in dba_config.yaml:
    model:
      provider: "openai-compatible"
      model_name: "qwen3.6-flash"
      base_url: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      api_key_env: "DASHSCOPE_API_KEY"
"""

from __future__ import annotations

import json
import logging
import os
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger("dba_webui.llm")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

_PLUGIN_DIR = Path(__file__).parent.parent / ".hermes" / "plugins" / "dba-safeguard"
_CONFIG_PATH = _PLUGIN_DIR / "config" / "dba_config.yaml"

_cached_config: Optional[Dict] = None


def _load_model_config() -> Dict[str, Any]:
    """Load model config from dba_config.yaml. Cached after first load."""
    global _cached_config
    if _cached_config is not None:
        return _cached_config

    try:
        import yaml
    except ImportError:
        logger.warning("PyYAML not installed — LLM config unavailable")
        _cached_config = {}
        return _cached_config

    if not _CONFIG_PATH.exists():
        logger.warning("Config not found: %s", _CONFIG_PATH)
        _cached_config = {}
        return _cached_config

    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        _cached_config = cfg.get("model", {})
        return _cached_config
    except Exception as e:
        logger.error("Failed to load config: %s", e)
        _cached_config = {}
        return _cached_config


def reload_model_config() -> Dict[str, Any]:
    """Force reload model config."""
    global _cached_config
    _cached_config = None
    return _load_model_config()


def get_model_config() -> Dict[str, Any]:
    """Get current model config dict."""
    return _load_model_config().copy()


def save_model_config(new_config: Dict[str, Any]) -> Dict[str, Any]:
    """Save model config to dba_config.yaml."""
    try:
        import yaml
    except ImportError:
        return {"success": False, "error": "PyYAML not installed"}

    if not _CONFIG_PATH.exists():
        return {"success": False, "error": "Config file not found"}

    try:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}

        cfg["model"] = {
            "provider": new_config.get("provider", "openai-compatible"),
            "model_name": new_config.get("model_name", ""),
            "base_url": new_config.get("base_url", ""),
            "api_key_env": new_config.get("api_key_env", ""),
        }

        with open(_CONFIG_PATH, "w", encoding="utf-8") as f:
            yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        reload_model_config()
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ---------------------------------------------------------------------------
# LLM Client
# ---------------------------------------------------------------------------

# DBA system prompt for WebUI chat
DBA_SYSTEM_PROMPT = """\
你是 DBA SafeGuard 数据库助手，帮助用户管理和操作数据库。

你的能力：
- 回答数据库相关问题（PostgreSQL, MySQL, Oracle, Hive 等）
- 解释 SQL 语句的作用和风险
- 帮助用户编写安全的 SQL
- 提供数据库性能优化建议
- 说明当前连接的数据库实例信息

当前环境信息：
- 实例: {instance_name}
- 数据库类型: {dialect}
- 安全模式: {safety_mode} (0=只读, 1=保守, 2=适中, 3=激进, 4=无限制)

重要规则：
- 对于危险操作（DROP, TRUNCATE, DELETE without WHERE），提醒用户注意风险
- 生成 SQL 时始终包含安全建议
- 回答简洁准确
- 使用中文回答
"""


def _get_api_key() -> Optional[str]:
    """Resolve API key from environment variable."""
    config = _load_model_config()
    env_var = config.get("api_key_env", "")
    if env_var:
        return os.environ.get(env_var, "")
    return None


def is_llm_configured() -> bool:
    """Check if LLM is properly configured."""
    config = _load_model_config()
    if not config.get("base_url") or not config.get("model_name"):
        return False
    key = _get_api_key()
    return bool(key)


def chat_completion(
    messages: List[Dict[str, str]],
    *,
    instance_name: str = "pg_test",
    dialect: str = "postgresql",
    safety_mode: int = 2,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Dict[str, Any]:
    """Call OpenAI-compatible chat completion API.

    Returns:
        {"success": True, "content": "response text", "usage": {...}}
        or {"success": False, "error": "error message"}
    """
    config = _load_model_config()
    base_url = config.get("base_url", "").rstrip("/")
    model_name = config.get("model_name", "")
    api_key = _get_api_key()

    if not base_url or not model_name:
        return {"success": False, "error": "LLM 未配置。请在管理面板 → LLM配置 中设置模型信息。"}

    if not api_key:
        env_var = config.get("api_key_env", "DASHSCOPE_API_KEY")
        return {"success": False, "error": f"API密钥未设置。请设置环境变量 {env_var}。"}

    # Build system prompt with context
    system_prompt = DBA_SYSTEM_PROMPT.format(
        instance_name=instance_name,
        dialect=dialect,
        safety_mode=safety_mode,
    )

    # Prepend system message
    full_messages = [{"role": "system", "content": system_prompt}] + messages

    # Build request
    url = f"{base_url}/chat/completions"
    payload = {
        "model": model_name,
        "messages": full_messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    try:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        choices = result.get("choices", [])
        if not choices:
            return {"success": False, "error": "LLM 返回空结果"}

        content = choices[0].get("message", {}).get("content", "")
        usage = result.get("usage", {})

        return {
            "success": True,
            "content": content,
            "usage": usage,
            "model": result.get("model", model_name),
        }

    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")[:500]
        except Exception:
            pass
        logger.error("LLM API error %d: %s", e.code, body)
        return {"success": False, "error": f"LLM API 错误 ({e.code}): {body}"}

    except urllib.error.URLError as e:
        logger.error("LLM connection error: %s", e.reason)
        return {"success": False, "error": f"无法连接 LLM 服务: {e.reason}"}

    except Exception as e:
        logger.error("LLM call failed: %s", e, exc_info=True)
        return {"success": False, "error": f"LLM 调用失败: {str(e)}"}
