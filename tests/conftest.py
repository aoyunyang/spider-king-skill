"""Test session hygiene for the skill package."""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

# Force no bytecode before collection/imports so tests never drop __pycache__.
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True

SKILL_ROOT = Path(__file__).resolve().parents[1]
_CACHE_DIR_NAMES = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
}


def pytest_configure() -> None:
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    sys.dont_write_bytecode = True


def _is_runner_dump(name: str) -> bool:
    lowered = name.casefold()
    return lowered.endswith(".txt") and (
        lowered.startswith("_err_") or lowered.startswith("_out_")
    )


def _clean_skill_hygiene(skill_root: Path) -> list[str]:
    """Remove known local dirt created by test tooling under the skill root."""
    removed: list[str] = []
    if not skill_root.is_dir():
        return removed

    # Delete deepest cache dirs first.
    cache_dirs: list[Path] = []
    for dirpath, dirnames, filenames in os.walk(skill_root, topdown=False, followlinks=False):
        parent = Path(dirpath)
        if parent.name in _CACHE_DIR_NAMES:
            cache_dirs.append(parent)
            continue
        for file_name in filenames:
            path = parent / file_name
            if _is_runner_dump(file_name) or file_name.endswith((".pyc", ".pyo")):
                try:
                    path.unlink(missing_ok=True)
                    removed.append(path.relative_to(skill_root).as_posix())
                except OSError:
                    pass

    for cache_dir in sorted(cache_dirs, key=lambda p: len(p.parts), reverse=True):
        try:
            shutil.rmtree(cache_dir, ignore_errors=False)
            removed.append(cache_dir.relative_to(skill_root).as_posix())
        except OSError:
            shutil.rmtree(cache_dir, ignore_errors=True)
            if not cache_dir.exists():
                try:
                    removed.append(cache_dir.relative_to(skill_root).as_posix())
                except ValueError:
                    pass
    return removed


def pytest_sessionfinish(session, exitstatus) -> None:  # noqa: ARG001
    """Keep the skill package clean after the test session."""
    _clean_skill_hygiene(SKILL_ROOT)
