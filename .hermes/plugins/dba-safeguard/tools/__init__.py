"""DBA SafeGuard tools package namespace."""

from importlib import import_module
from importlib.util import find_spec


def __getattr__(name):
	"""Lazy-load tool submodules for string-based monkeypatch lookups."""
	fullname = f"{__name__}.{name}"
	if find_spec(fullname) is None:
		raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
	module = import_module(fullname)
	globals()[name] = module
	return module


__all__ = []
