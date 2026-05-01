#!/usr/bin/env python3
"""Watch the prayer source files and regenerate prayers/index.html on changes."""

from __future__ import annotations

import subprocess
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRAYERS_SRC = ROOT.parent / "sein_prayers" / "src"
WATCHED_PATTERNS = ("SUMMARY.md", "weekly/*.md")


def snapshot() -> dict[Path, float]:
    files: list[Path] = []
    for pattern in WATCHED_PATTERNS:
        files.extend(PRAYERS_SRC.glob(pattern))
    return {path: path.stat().st_mtime for path in files if path.exists()}


def update() -> None:
    subprocess.run(["python3", "tools/update_prayers.py"], cwd=ROOT, check=True)


def main() -> None:
    previous = snapshot()
    update()
    print("Watching prayer sources. Press Ctrl+C to stop.")

    while True:
        time.sleep(2)
        current = snapshot()
        if current != previous:
            update()
            previous = current


if __name__ == "__main__":
    main()
