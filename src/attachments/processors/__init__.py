# ruff: noqa: I001
from __future__ import annotations

from collections.abc import Callable


# Global registry for processors (extension -> callable)
# Keys are lowercase extensions like ".pdf" or sentinel keys like "__text__".
processors: dict[str, Callable[[bytes], dict]] = {}


def _normalize_key(key: str) -> str:
    k = key.strip()
    if k.startswith("__"):
        return k
    if not k.startswith("."):
        k = "." + k
    return k.lower()


def register_processor(key: str, func: Callable[[bytes], dict]) -> None:
    processors[_normalize_key(key)] = func


# Import modules to trigger self-registration
from . import text as _text  # noqa: E402,F401
from . import xlsx as _xlsx  # noqa: E402,F401

__all__ = ["processors", "register_processor"]
