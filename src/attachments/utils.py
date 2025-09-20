from __future__ import annotations


def is_text_bytes(data: bytes) -> bool:
    """Heuristic to decide whether bytes are (mostly) text.
    - Reject if NUL bytes are present.
    - Otherwise, consider text if >= 95% of bytes are printable/control whitespace.
    """
    if not data:
        return True
    if b"\x00" in data:
        return False
    # Printable byte set + common control whitespace
    textchars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)))
    nontext = data.translate(None, textchars)
    return (len(nontext) / max(1, len(data))) < 0.05


def guess_decode(data: bytes) -> tuple[str, str]:
    """Return (encoding, text) using a small, dependency-free strategy.
    Try utf-8, utf-8-sig, latin-1, cp1252, then utf-8 with 'replace' fallback.
    """
    for enc in ("utf-8", "utf-8-sig", "latin-1", "cp1252"):
        try:
            return enc, data.decode(enc)
        except UnicodeDecodeError:
            continue
    return "utf-8", data.decode("utf-8", "replace")
