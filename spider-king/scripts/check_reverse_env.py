#!/usr/bin/env python3
"""
Quick environment check for protocol-first reverse work.
"""

from __future__ import annotations

import shutil
import sys


TOOLS = [
    ("python", sys.executable),
    ("node", shutil.which("node")),
    ("npm", shutil.which("npm")),
    ("curl", shutil.which("curl")),
    ("git", shutil.which("git")),
]


def main() -> None:
    print("reverse environment")
    print(f"- python_version: {sys.version.split()[0]}")
    for name, path in TOOLS:
        status = path or "missing"
        print(f"- {name}: {status}")
    print("notes")
    print("- pure Python protocol replay should work with Python alone")
    print("- node is useful for preserving tiny JS helpers")
    print("- curl is useful for quick raw request diffs")


if __name__ == "__main__":
    main()
