from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

from attachments import att


def build_demo_dir(root: Path) -> None:
    # Plain text
    (root / "hello.txt").write_text("Hello from Attachments!\n", encoding="utf-8")
    (root / "readme.md").write_text("# Demo\nThis is a small demo.\n", encoding="utf-8")

    # Nested zip with an inner text file
    with zipfile.ZipFile(
        root / "nested.zip", "w", compression=zipfile.ZIP_DEFLATED
    ) as zf:
        zf.writestr("inner/inner.txt", "Hello from inside the zip!\n")

    # Placeholder xlsx
    # (processor parses via pandas/openpyxl or emits a helpful error flag)
    (root / "table.xlsx").write_bytes(b"not-a-real-xlsx\n")


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="attachments_demo_") as td:
        demo = Path(td)
        build_demo_dir(demo)
        artifacts = att(str(demo))

        print(f"Processed {len(artifacts)} artifacts:\n")
        for art in artifacts:
            src = art.get("flags", {}).get("source")
            kind = art.get("flags", {}).get("kind")
            err = art.get("flags", {}).get("error")
            text_preview = art.get("text", "").strip().splitlines()[:2]
            text_lines = len(art.get("text", "").splitlines())
            print(f"- {src} | kind={kind} | text_lines={text_lines}")
            if err:
                print(f"    error: {err}")
            for line in text_preview:
                print(f"    > {line}")


if __name__ == "__main__":
    main()
