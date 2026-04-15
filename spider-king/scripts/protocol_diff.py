#!/usr/bin/env python3
"""
Compare two captured protocol samples and surface meaningful deltas.
"""

from __future__ import annotations

import argparse
import difflib
import json
import sys
from pathlib import Path
from typing import Any


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def try_load_json(text: str) -> Any | None:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def flatten_json(value: Any, prefix: str = "$") -> dict[str, str]:
    rows: dict[str, str] = {}
    if isinstance(value, dict):
        for key in sorted(value):
            rows.update(flatten_json(value[key], f"{prefix}.{key}"))
        return rows
    if isinstance(value, list):
        for index, item in enumerate(value):
            rows.update(flatten_json(item, f"{prefix}[{index}]"))
        return rows
    rows[prefix] = json.dumps(value, ensure_ascii=False, sort_keys=True)
    return rows


def compare_json(left: Any, right: Any, max_diffs: int) -> None:
    left_map = flatten_json(left)
    right_map = flatten_json(right)
    keys = sorted(set(left_map) | set(right_map))

    only_left = [key for key in keys if key not in right_map]
    only_right = [key for key in keys if key not in left_map]
    changed = [key for key in keys if key in left_map and key in right_map and left_map[key] != right_map[key]]

    print("mode=json")
    print(f"left_only={len(only_left)}")
    print(f"right_only={len(only_right)}")
    print(f"changed={len(changed)}")

    for key in only_left[:max_diffs]:
        print(f"- left_only {key} = {left_map[key]}")
    for key in only_right[:max_diffs]:
        print(f"- right_only {key} = {right_map[key]}")
    for key in changed[:max_diffs]:
        print(f"- changed {key}")
        print(f"  left:  {left_map[key]}")
        print(f"  right: {right_map[key]}")


def compare_text(left_text: str, right_text: str, max_diffs: int) -> None:
    print("mode=text")
    diff = list(
        difflib.unified_diff(
            left_text.splitlines(),
            right_text.splitlines(),
            fromfile="left",
            tofile="right",
            lineterm="",
        )
    )
    shown = diff[:max_diffs]
    print(f"diff_lines={len(diff)}")
    for line in shown:
        safe = line.encode(sys.stdout.encoding or "utf-8", errors="replace").decode(
            sys.stdout.encoding or "utf-8",
            errors="replace",
        )
        print(safe)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare two captured protocol samples.")
    parser.add_argument("left", help="Left sample path")
    parser.add_argument("right", help="Right sample path")
    parser.add_argument("--max-diffs", type=int, default=40, help="Maximum diff rows to print")
    args = parser.parse_args()

    left_path = Path(args.left)
    right_path = Path(args.right)

    left_text = load_text(left_path)
    right_text = load_text(right_path)
    left_json = try_load_json(left_text)
    right_json = try_load_json(right_text)

    print(f"left={left_path}")
    print(f"right={right_path}")

    if left_json is not None and right_json is not None:
        compare_json(left_json, right_json, args.max_diffs)
        return

    compare_text(left_text, right_text, args.max_diffs)


if __name__ == "__main__":
    main()
