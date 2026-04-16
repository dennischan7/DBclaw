"""规范热重载引擎 — 监控harness配置文件变更，自动重载。

核心能力:
  - 监控 harnesses/ 下的 YAML/MD 文件变更
  - mtime-based 检测 (无需inotify/watchdog依赖)
  - 提供 check_and_reload() 供每次请求前调用
  - 缓存已加载的规范内容
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, Optional

import yaml

logger = logging.getLogger("dba_safeguard.harnesses.config_watcher")

_HARNESSES_DIR = Path(__file__).parent


class HarnessConfigWatcher:
    """Watch and auto-reload harness configuration files."""

    def __init__(self):
        self._file_mtimes: Dict[str, float] = {}
        self._file_cache: Dict[str, Any] = {}

    def get_config(self, rel_path: str) -> Optional[Any]:
        """Get a cached config file, reloading if modified.

        Args:
            rel_path: Relative path from harnesses/ dir (e.g. "contracts/hitl_matrix.yaml")

        Returns:
            Parsed YAML dict, or raw text for .md files, or None if not found.
        """
        full_path = _HARNESSES_DIR / rel_path
        if not full_path.exists():
            return None

        path_key = str(full_path)
        current_mtime = full_path.stat().st_mtime

        if path_key in self._file_mtimes and self._file_mtimes[path_key] == current_mtime:
            return self._file_cache.get(path_key)

        # File changed or first load
        content = self._load_file(full_path)
        self._file_mtimes[path_key] = current_mtime
        self._file_cache[path_key] = content
        logger.debug("Loaded/reloaded harness config: %s", rel_path)
        return content

    def check_and_reload(self) -> Dict[str, bool]:
        """Check all tracked files for changes.

        Returns:
            Dict of path → was_reloaded for any changed files.
        """
        reloaded = {}
        for path_key, old_mtime in list(self._file_mtimes.items()):
            full_path = Path(path_key)
            if not full_path.exists():
                self._file_mtimes.pop(path_key, None)
                self._file_cache.pop(path_key, None)
                reloaded[path_key] = True
                continue

            current_mtime = full_path.stat().st_mtime
            if current_mtime != old_mtime:
                content = self._load_file(full_path)
                self._file_mtimes[path_key] = current_mtime
                self._file_cache[path_key] = content
                reloaded[path_key] = True
                logger.info("Hot-reloaded harness config: %s", path_key)

        # Also trigger taxonomy reload
        if reloaded:
            try:
                from .intent_router import reload_taxonomy
                reload_taxonomy()
            except Exception:
                pass

        return reloaded

    def get_hitl_matrix(self) -> Optional[Dict]:
        """Shortcut to get the HITL risk matrix."""
        return self.get_config("contracts/hitl_matrix.yaml")

    def get_stage_workflow(self, workflow_name: str) -> Optional[str]:
        """Shortcut to get a stage workflow Markdown content."""
        return self.get_config(f"stages/{workflow_name}.md")

    def list_watched_files(self) -> list:
        """List all currently tracked files and their status."""
        result = []
        for path_key, mtime in self._file_mtimes.items():
            full_path = Path(path_key)
            result.append({
                "path": path_key,
                "exists": full_path.exists(),
                "mtime": mtime,
                "current_mtime": full_path.stat().st_mtime if full_path.exists() else None,
                "stale": full_path.exists() and full_path.stat().st_mtime != mtime,
            })
        return result

    def invalidate(self, rel_path: Optional[str] = None) -> None:
        """Invalidate cache for a specific file or all files."""
        if rel_path:
            full_path = str(_HARNESSES_DIR / rel_path)
            self._file_mtimes.pop(full_path, None)
            self._file_cache.pop(full_path, None)
        else:
            self._file_mtimes.clear()
            self._file_cache.clear()

    @staticmethod
    def _load_file(path: Path) -> Any:
        """Load a file — YAML parsed as dict, MD as raw text."""
        text = path.read_text(encoding="utf-8")
        if path.suffix in (".yaml", ".yml"):
            return yaml.safe_load(text) or {}
        return text


# Module-level singleton
_watcher = HarnessConfigWatcher()


def get_config_watcher() -> HarnessConfigWatcher:
    """Get the singleton config watcher instance."""
    return _watcher
