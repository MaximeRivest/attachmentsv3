from __future__ import annotations

import os
from collections.abc import Callable

from .processors import processors
from .unpack import unpack
from .utils import is_text_bytes


def _route_processor(filename: str, data: bytes) -> Callable[..., dict]:
    ext = os.path.splitext(filename)[1].lower()
    proc = processors.get(ext)
    if proc is None:
        # If bytes look like text, use the text catch-all
        if is_text_bytes(data):
            proc = processors.get("__text__")
    if proc is None:
        # Fallback: identity/empty artifact
        def _default(data: bytes, **opts) -> dict:
            return {
                "text": "",
                "images": [],
                "audio": [],
                "video": [],
                "flags": {"note": "no processor", "filename": filename},
            }

        return _default
    return proc


def _error_artifact(source: str, error: str) -> dict:
    """Create a standardized error artifact."""
    return {
        "text": "",
        "images": [],
        "audio": [],
        "video": [],
        "flags": {"source": source, "error": error},
    }


def att(input: str, **options) -> list[dict]:
    """High-level entrypoint: unpack -> route -> process -> collate.
    Returns a flat list of artifacts (dicts).

    All errors are captured in the returned artifacts rather than raised,
    providing consistent error handling. Check artifact["flags"]["error"]
    to detect failures.
    """
    try:
        pairs: list[tuple[str, bytes]] = unpack(input)
    except Exception as e:
        # Unpack failed - return single error artifact
        return [_error_artifact(input, f"unpack failed: {e}")]

    out: list[dict] = []
    for fname, data in pairs:
        proc = _route_processor(fname, data)
        try:
            artifact = proc(data, filename=fname, **options)
        except Exception as e:
            artifact = _error_artifact(fname, f"processing failed: {e}")
        # Normalize keys
        artifact.setdefault("text", "")
        artifact.setdefault("images", [])
        artifact.setdefault("audio", [])
        artifact.setdefault("video", [])
        artifact.setdefault("flags", {})
        artifact["flags"].setdefault("source", fname)
        out.append(artifact)
    return out
