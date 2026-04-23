#!/usr/bin/env python3
"""Tools package namespace.

Keep package import side effects minimal. Importing ``tools`` should not
eagerly import the full tool stack, because several subsystems load tools while
``hermes_cli.config`` is still initializing.

Callers should import concrete submodules directly, for example:

    import tools.web_tools
    from tools import browser_tool

Python will resolve those submodules via the package path without needing them
to be re-exported here.
"""

from importlib import import_module
from importlib.util import find_spec


def check_file_requirements():
    """File tools only require terminal backend availability."""
    from .terminal_tool import check_terminal_requirements

    return check_terminal_requirements()


def __getattr__(name):
    """Lazy-load tool submodules for string-based monkeypatch/patch lookups."""
    fullname = f"{__name__}.{name}"
    if find_spec(fullname) is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = import_module(fullname)
    globals()[name] = module
    return module


__all__ = ["check_file_requirements"]
