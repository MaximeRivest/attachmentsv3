"""
attachments: Turn any file or collection into LLM-ready artifacts (minimal core)

This minimal build implements:
- Unpacker: local directory, local files, ZIP, TAR.* (tgz/tbz2/txz), and
  GitHub repo cloning (via `git` CLI).
- Processors: catch-all text processor and an Excel (.xlsx) processor.
- Registry for processors and for custom unpack handlers.

Public API:
- att(input: str | PathLike, **options) -> list[dict]
- unpack(input: str, extra_handlers: dict[str, callable] | None = None)
  -> list[tuple[str, bytes]]
- processors (dict) and register_processor(ext, func)
- register_unpack_handler(prefix, func)
"""

from .core import att
from .processors import (
    get_processors_copy,
    processors,
    register_processor,
    reset_processors,
)
from .unpack import extra_unpack_handlers, register_unpack_handler, unpack

__all__ = [
    "att",
    "unpack",
    "processors",
    "register_processor",
    "reset_processors",
    "get_processors_copy",
    "register_unpack_handler",
    "extra_unpack_handlers",
]

# Managed via [tool.hatch.version] in pyproject.toml
__version__ = "0.1.0"
