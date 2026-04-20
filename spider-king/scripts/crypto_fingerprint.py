#!/usr/bin/env python3
"""
Heuristic fingerprint helper for suspicious crypto or encoding outputs.
"""

from __future__ import annotations

import argparse
import re


HEX_RE = re.compile(r"^[0-9a-fA-F]+$")
BASE64_RE = re.compile(r"^[A-Za-z0-9+/=]+$")
URLSAFE_BASE64_RE = re.compile(r"^[A-Za-z0-9_-]+={0,2}$")


def guess_kind(value: str) -> list[str]:
    hints: list[str] = []
    length = len(value)
    is_hex = bool(HEX_RE.fullmatch(value))

    if is_hex:
        hints.append("hex")
        if length == 32:
            hints.append("md5-like length")
        elif length == 40:
            hints.append("sha1-like length")
        elif length == 64:
            hints.append("sha256-like length")

    if not is_hex and BASE64_RE.fullmatch(value):
        hints.append("base64-like alphabet")

    if not is_hex and URLSAFE_BASE64_RE.fullmatch(value):
        hints.append("urlsafe-base64-like alphabet")

    if not hints:
        hints.append("custom alphabet or mixed encoding")

    return hints


def main() -> None:
    parser = argparse.ArgumentParser(description="Fingerprint suspicious crypto-like strings.")
    parser.add_argument("value", help="Value to inspect")
    args = parser.parse_args()

    print(f"value_length={len(args.value)}")
    for hint in guess_kind(args.value):
        print(f"- {hint}")


if __name__ == "__main__":
    main()
