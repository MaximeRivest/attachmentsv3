# ruff: noqa: I001
from __future__ import annotations

from collections.abc import Callable


# Global registry for processors (extension -> callable)
# Keys are lowercase extensions like ".pdf" or sentinel keys like "__text__".
processors: dict[str, Callable[[bytes], dict]] = {}

# Snapshot of default processors after initial registration (populated lazily)
_default_processors: dict[str, Callable[[bytes], dict]] | None = None


def _normalize_key(key: str) -> str:
    k = key.strip()
    if k.startswith("__"):
        return k
    if not k.startswith("."):
        k = "." + k
    return k.lower()


def register_processor(
    key: str,
    func: Callable[[bytes], dict],
    registry: dict[str, Callable[[bytes], dict]] | None = None,
) -> None:
    """Register a processor for a file extension.

    Args:
        key: File extension (e.g., ".pdf") or sentinel key (e.g., "__text__")
        func: Processor function that takes bytes and returns an artifact dict
        registry: Optional custom registry dict. If None, uses the global registry.
    """
    target = registry if registry is not None else processors
    target[_normalize_key(key)] = func


def _snapshot_defaults() -> None:
    """Capture current processors as defaults (called once after initial imports)."""
    global _default_processors
    if _default_processors is None:
        _default_processors = dict(processors)


def reset_processors() -> None:
    """Reset the global processor registry to its default state.

    Useful for testing to ensure test isolation. Restores only the
    built-in processors (text, pdf, xlsx) and removes any custom processors.
    """
    global processors
    if _default_processors is not None:
        processors.clear()
        processors.update(_default_processors)


def get_processors_copy() -> dict[str, Callable[[bytes], dict]]:
    """Return a shallow copy of the current processor registry.

    Useful for creating isolated registries for testing or custom pipelines.
    """
    return dict(processors)


# Import modules to trigger self-registration
from . import text as _text  # noqa: E402,F401
from . import xlsx as _xlsx  # noqa: E402,F401
from . import pdf as _pdf  # noqa: E402,F401

# Capture defaults after built-in processors are registered
_snapshot_defaults()


__all__ = [
    "processors",
    "register_processor",
    "reset_processors",
    "get_processors_copy",
]
