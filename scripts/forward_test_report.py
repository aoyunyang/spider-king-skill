#!/usr/bin/env python3
"""Validate an externally produced fresh-agent forward-test report.

This tool is deliberately read-only. It does not call a model, execute a runner,
or execute commands named by a report.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

# Keep normal CLI validation from depositing Python caches in the skill tree.
sys.dont_write_bytecode = True

from _bounded_input import (  # noqa: E402
    BoundedInputError,
    parse_json_text,
)
from validate_skill import (  # noqa: E402
    official_suite_contract_digest,
    parse_self_test_suite,
    sha256 as bounded_sha256,
)


SCHEMA_VERSION = 1
OFFICIAL_SUITE_TASK_COUNT = 160
OFFICIAL_SUITE_CONTRACT_SHA256 = (
    "fb40033033ecdbaf9b78f507fce48ffa8ce78ec388e6afcbc0740e23091f6a3d"
)
DEFAULT_SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_SUITE_RELATIVE_PATH = Path("references/official-self-test-task-suite.md")
DEFAULT_SKILL_RELATIVE_PATH = Path("SKILL.md")
RESPONSES_DIRECTORY_NAME = "responses"
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
MAX_TOTAL_RESPONSE_BYTES = 64 * 1024 * 1024
MAX_PACKAGE_BYTES = 128 * 1024 * 1024
MAX_EVIDENCE_QUOTE_CHARS = 16 * 1024
MIN_EVIDENCE_QUOTE_CHARS = 12
MIN_REVIEW_RATIONALE_CHARS = 12
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")
PACKAGE_CACHE_DIRECTORIES = frozenset(
    {
        "__pycache__",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        ".cache",
        ".tox",
        ".eggs",
        ".hypothesis",
        "htmlcov",
        "node_modules",
        ".venv",
        "venv",
    }
)
PACKAGE_NOISE_FILENAMES = frozenset(
    {
        ".coverage",
        ".ds_store",
        "coverage.xml",
        "desktop.ini",
        "thumbs.db",
    }
)
PACKAGE_NOISE_SUFFIXES = (
    ".bak",
    ".log",
    ".pyc",
    ".pyd",
    ".pyo",
    ".swp",
    ".swo",
    ".temp",
    ".tmp",
)
PACKAGE_RUNNER_DUMP_PREFIXES = ("_err_", "_out_")
WINDOWS_RESERVED_NAMES = frozenset(
    {
        "AUX",
        "CON",
        "NUL",
        "PRN",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
)


class ForwardTestError(ValueError):
    """Raised when a report or an artifact cannot be inspected safely."""


@dataclass(frozen=True)
class SuiteCase:
    heading: str
    prompt: str
    routes: tuple[str, ...]
    conclusions: tuple[str, ...]


@dataclass
class Validation:
    errors: list[str]

    def require(self, condition: bool, message: str) -> bool:
        if not condition:
            self.errors.append(message)
        return condition


@dataclass(frozen=True)
class StableFile:
    path: Path
    payload: bytes
    sha256: str
    size: int
    identity: tuple[int, int]


@dataclass(frozen=True)
class ItemArtifact:
    summary: dict[str, str]
    path: Optional[Path] = None
    identity: Optional[tuple[int, int]] = None
    size: int = 0


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _is_reparse_point(metadata: os.stat_result) -> bool:
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(getattr(metadata, "st_file_attributes", 0) & reparse_flag)


def _reject_linked_components(path: Path, *, label: str) -> None:
    """Reject links/reparse points in every existing component of path."""

    current = _absolute(path)
    while True:
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise ForwardTestError(f"{label}: cannot inspect path component") from exc
        else:
            if stat.S_ISLNK(metadata.st_mode) or _is_reparse_point(metadata):
                raise ForwardTestError(
                    f"{label}: symlink or reparse-point paths are not allowed"
                )
            if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink > 1:
                raise ForwardTestError(f"{label}: hard-linked files are not allowed")
        if current.parent == current:
            return
        current = current.parent


def _safe_existing_file(path: Path, *, label: str) -> Path:
    absolute = _absolute(path)
    _reject_linked_components(absolute, label=label)
    try:
        metadata = os.lstat(absolute)
    except FileNotFoundError as exc:
        raise ForwardTestError(f"{label}: file does not exist") from exc
    except OSError as exc:
        raise ForwardTestError(f"{label}: cannot inspect file") from exc
    if not stat.S_ISREG(metadata.st_mode):
        raise ForwardTestError(f"{label}: expected a regular file")
    if metadata.st_nlink > 1:
        raise ForwardTestError(f"{label}: hard-linked files are not allowed")
    return absolute


def _safe_existing_directory(path: Path, *, label: str) -> Path:
    absolute = _absolute(path)
    _reject_linked_components(absolute, label=label)
    try:
        metadata = os.lstat(absolute)
    except FileNotFoundError as exc:
        raise ForwardTestError(f"{label}: directory does not exist") from exc
    except OSError as exc:
        raise ForwardTestError(f"{label}: cannot inspect directory") from exc
    if not stat.S_ISDIR(metadata.st_mode):
        raise ForwardTestError(f"{label}: expected a directory")
    return absolute


def _read_stable_file(path: Path, *, label: str, max_bytes: int) -> StableFile:
    """Read and hash one regular file through one verified, no-follow handle."""

    safe_path = _safe_existing_file(path, label=label)
    flags = os.O_RDONLY
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_NOINHERIT", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(safe_path, flags)
    except OSError as exc:
        raise ForwardTestError(f"{label}: cannot open file safely") from exc

    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            raise ForwardTestError(f"{label}: expected a regular file")
        if before.st_nlink > 1:
            raise ForwardTestError(f"{label}: hard-linked files are not allowed")
        if before.st_size > max_bytes:
            raise ForwardTestError(f"{label}: input exceeds {max_bytes} bytes")

        chunks: list[bytes] = []
        remaining = max_bytes + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(1024 * 1024, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        payload = b"".join(chunks)
        if len(payload) > max_bytes:
            raise ForwardTestError(f"{label}: input exceeds {max_bytes} bytes")

        after = os.fstat(descriptor)
        try:
            final_path_metadata = os.lstat(safe_path)
        except OSError as exc:
            raise ForwardTestError(f"{label}: path changed while being read") from exc
        _reject_linked_components(safe_path, label=label)
        if not os.path.samestat(before, after) or not os.path.samestat(
            after, final_path_metadata
        ):
            raise ForwardTestError(f"{label}: file identity changed while being read")
        if before.st_size != after.st_size or after.st_size != len(payload):
            raise ForwardTestError(f"{label}: file size changed while being read")
        if any(
            getattr(before, field, None) != getattr(after, field, None)
            for field in ("st_mtime_ns", "st_ctime_ns")
        ):
            raise ForwardTestError(f"{label}: file timestamps changed while being read")
    except OSError as exc:
        raise ForwardTestError(f"{label}: file read failed") from exc
    finally:
        os.close(descriptor)

    return StableFile(
        path=safe_path,
        payload=payload,
        sha256=hashlib.sha256(payload).hexdigest(),
        size=len(payload),
        identity=(int(after.st_dev), int(after.st_ino)),
    )


def _decode_utf8(payload: bytes, *, label: str) -> str:
    try:
        return payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ForwardTestError(f"{label}: input is not valid UTF-8") from exc


def _is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def _contained_response_path(
    report_path: Path,
    raw_path: Any,
    *,
    skill_root: Path,
    label: str,
) -> Path:
    if not isinstance(raw_path, str) or not raw_path.strip():
        raise ForwardTestError(f"{label}: response path must be a non-empty string")
    if "\x00" in raw_path:
        raise ForwardTestError(f"{label}: response path contains a NUL byte")

    relative = Path(raw_path)
    if relative.is_absolute() or relative.drive or relative.root:
        raise ForwardTestError(f"{label}: response path must be relative")
    if any(part == ".." for part in relative.parts):
        raise ForwardTestError(f"{label}: response path must not contain '..'")
    if (
        len(relative.parts) < 2
        or relative.parts[0].casefold() != RESPONSES_DIRECTORY_NAME
    ):
        raise ForwardTestError(
            f"{label}: response path must begin with '{RESPONSES_DIRECTORY_NAME}/'"
        )
    if os.name == "nt":
        for part in relative.parts:
            # Win32 collapses trailing dots/spaces and supports alternate streams.
            if part.rstrip(". ") != part:
                raise ForwardTestError(
                    f"{label}: response path components must not end in a dot or space"
                )
            if ":" in part:
                raise ForwardTestError(
                    f"{label}: response path must not use a data stream"
                )
            device_stem = part.split(".", 1)[0].rstrip(". ").upper()
            if device_stem in WINDOWS_RESERVED_NAMES:
                raise ForwardTestError(
                    f"{label}: response path must not use a reserved device name"
                )

    report_directory = _safe_existing_directory(
        report_path.parent,
        label="report directory",
    )
    response_directory = _safe_existing_directory(
        report_directory / RESPONSES_DIRECTORY_NAME,
        label="response directory",
    )
    candidate = _safe_existing_file(
        report_directory / relative,
        label=label,
    )
    try:
        resolved_directory = response_directory.resolve(strict=True)
        resolved_candidate = candidate.resolve(strict=True)
    except OSError as exc:
        raise ForwardTestError(f"{label}: cannot resolve response path") from exc
    if not _is_relative_to(resolved_candidate, resolved_directory):
        raise ForwardTestError(f"{label}: response path escapes the report directory")
    try:
        resolved_skill_root = skill_root.resolve(strict=True)
    except OSError as exc:
        raise ForwardTestError(
            "skill root: cannot resolve while checking response scope"
        ) from exc
    if _is_relative_to(resolved_candidate, resolved_skill_root):
        raise ForwardTestError(
            f"{label}: response path must stay outside the skill root"
        )

    try:
        same_as_report = os.path.samefile(candidate, report_path)
    except OSError:
        same_as_report = candidate == report_path
    if same_as_report:
        raise ForwardTestError(f"{label}: report JSON is not a response artifact")
    return candidate


def _read_document(path: Path, *, label: str) -> Any:
    try:
        stable = _read_stable_file(path, label=label, max_bytes=16 * 1024 * 1024)
        return parse_json_text(_decode_utf8(stable.payload, label=label), label=label)
    except (BoundedInputError, ForwardTestError) as exc:
        raise ForwardTestError(str(exc)) from exc


def _read_response(
    path: Path,
    *,
    label: str,
    remaining_budget: int,
) -> tuple[str, StableFile]:
    if remaining_budget < 1:
        raise ForwardTestError(
            f"{label}: aggregate response budget exceeds {MAX_TOTAL_RESPONSE_BYTES} bytes"
        )
    stable = _read_stable_file(
        path,
        label=label,
        max_bytes=min(MAX_RESPONSE_BYTES, remaining_budget),
    )
    return _decode_utf8(stable.payload, label=label), stable


def _recorded_hash(value: Any, *, label: str, validation: Validation) -> Optional[str]:
    if not validation.require(
        isinstance(value, str) and SHA256_RE.fullmatch(value) is not None,
        f"{label}: expected a 64-character SHA-256",
    ):
        return None
    return value.lower()


def _actor_id(
    document: dict[str, Any],
    name: str,
    validation: Validation,
) -> Optional[str]:
    actor = document.get(name)
    if not validation.require(isinstance(actor, dict), f"{name}: expected an object"):
        return None
    assert isinstance(actor, dict)
    identifier = actor.get("id")
    if not validation.require(
        isinstance(identifier, str) and bool(identifier.strip()),
        f"{name}.id: expected a non-empty string",
    ):
        identifier = None
    validation.require(
        actor.get("fresh_context") is True,
        f"{name}.fresh_context must be true",
    )
    validation.require(
        actor.get("independent") is True,
        f"{name}.independent must be true",
    )
    return identifier.strip() if isinstance(identifier, str) else None


def _scope(
    document: dict[str, Any],
    item_count: int,
    validation: Validation,
) -> str:
    raw_scope = document.get("scope")
    if isinstance(raw_scope, dict):
        raw_kind = raw_scope.get("kind")
        kind = raw_kind.strip().lower() if isinstance(raw_kind, str) else ""
        declared_count = raw_scope.get("task_count")
    else:
        kind = ""
        declared_count = None

    validation.require(isinstance(raw_scope, dict), "scope: expected an object")
    validation.require(
        kind in {"smoke", "full"}, "scope.kind must be 'smoke' or 'full'"
    )
    validation.require(
        isinstance(declared_count, int) and not isinstance(declared_count, bool),
        "scope.task_count must be an integer",
    )
    if isinstance(declared_count, int) and not isinstance(declared_count, bool):
        validation.require(
            declared_count == item_count,
            f"scope.task_count is {declared_count}; report contains {item_count} items",
        )
    if kind == "full":
        validation.require(
            item_count == OFFICIAL_SUITE_TASK_COUNT,
            f"full scope requires all {OFFICIAL_SUITE_TASK_COUNT} tasks; found {item_count}",
        )
    elif kind == "smoke":
        validation.require(item_count > 0, "smoke scope requires at least one task")
        validation.require(
            item_count < OFFICIAL_SUITE_TASK_COUNT,
            "a 160-task report must use full scope, not smoke scope",
        )
    return kind or "unknown"


def _evidence_quotes(
    value: Any,
    response_text: str,
    *,
    label: str,
    validation: Validation,
    used_spans: set[tuple[int, int]],
) -> list[str]:
    if not isinstance(value, list):
        validation.errors.append(f"{label}: evidence must be a list of span objects")
        return []

    quotes: list[str] = []
    if not value:
        validation.errors.append(f"{label}: at least one evidence span is required")
    for index, raw_span in enumerate(value):
        span_label = f"{label}[{index}]"
        if not isinstance(raw_span, dict):
            validation.errors.append(f"{span_label}: expected an object")
            continue
        raw_quote = raw_span.get("quote")
        start = raw_span.get("start")
        end = raw_span.get("end")
        if not isinstance(raw_quote, str) or not raw_quote.strip():
            validation.errors.append(f"{span_label}.quote: expected a non-empty string")
            continue
        if len(raw_quote) > MAX_EVIDENCE_QUOTE_CHARS:
            validation.errors.append(
                f"{span_label}.quote: quote exceeds {MAX_EVIDENCE_QUOTE_CHARS} characters"
            )
            continue
        if (
            len(raw_quote.strip()) < MIN_EVIDENCE_QUOTE_CHARS
            or sum(character.isalnum() for character in raw_quote) < 4
        ):
            validation.errors.append(
                f"{span_label}.quote: evidence is too short to be substantive"
            )
            continue
        if not (
            isinstance(start, int)
            and not isinstance(start, bool)
            and isinstance(end, int)
            and not isinstance(end, bool)
            and 0 <= start < end <= len(response_text)
        ):
            validation.errors.append(
                f"{span_label}: start/end must select a valid response character range"
            )
            continue
        if response_text[start:end] != raw_quote:
            validation.errors.append(
                f"{span_label}: quote does not match the original response at start/end"
            )
            continue
        span_key = (start, end)
        if span_key in used_spans:
            validation.errors.append(
                f"{span_label}: an evidence span must not be reused across checks"
            )
            continue
        used_spans.add(span_key)
        quotes.append(raw_quote)
    return quotes


def _validate_checks(
    raw_checks: Any,
    expected_values: tuple[str, ...],
    response_text: str,
    *,
    kind: str,
    item_label: str,
    validation: Validation,
    used_spans: set[tuple[int, int]],
) -> None:
    if not validation.require(
        isinstance(raw_checks, list),
        f"{item_label}.review.{kind}: expected a list",
    ):
        return
    assert isinstance(raw_checks, list)
    validation.require(
        len(raw_checks) == len(expected_values),
        f"{item_label}.review.{kind}: expected {len(expected_values)} checks, "
        f"found {len(raw_checks)}",
    )

    for index, expected in enumerate(expected_values):
        check_label = f"{item_label}.review.{kind}[{index}]"
        if index >= len(raw_checks):
            continue
        check = raw_checks[index]
        if not validation.require(
            isinstance(check, dict), f"{check_label}: expected an object"
        ):
            continue
        assert isinstance(check, dict)
        observed = check.get("expected")
        validation.require(
            observed == expected,
            f"{check_label}: expected contract value does not match the official suite",
        )
        validation.require(
            check.get("passed") is True, f"{check_label}.passed must be true"
        )
        rationale = check.get("rationale")
        validation.require(
            isinstance(rationale, str)
            and len(rationale.strip()) >= MIN_REVIEW_RATIONALE_CHARS,
            f"{check_label}.rationale must record the independent review reasoning",
        )
        evidence = check.get("evidence")
        quotes = _evidence_quotes(
            evidence,
            response_text,
            label=f"{check_label}.evidence",
            validation=validation,
            used_spans=used_spans,
        )
        if kind == "routes":
            validation.require(
                any(expected in quote for quote in quotes),
                f"{check_label}: route evidence must quote the expected route",
            )


def _item_response_fields(item: dict[str, Any]) -> tuple[Any, Any]:
    response = item.get("response")
    if isinstance(response, dict):
        raw_path = response.get("path")
        raw_hash = response.get("sha256")
    else:
        raw_path = None
        raw_hash = None
    return raw_path, raw_hash


def _validate_item(
    item: Any,
    index: int,
    report_path: Path,
    cases_by_heading: dict[str, SuiteCase],
    reviewer_id: Optional[str],
    skill_root: Path,
    remaining_budget: int,
    validation: Validation,
) -> Optional[ItemArtifact]:
    item_label = f"items[{index}]"
    if not validation.require(
        isinstance(item, dict), f"{item_label}: expected an object"
    ):
        return None
    assert isinstance(item, dict)
    heading = item.get("heading")
    if not validation.require(
        isinstance(heading, str) and bool(heading.strip()),
        f"{item_label}.heading: expected a non-empty string",
    ):
        return None
    assert isinstance(heading, str)
    case = cases_by_heading.get(heading)
    if not validation.require(
        case is not None,
        f"{item_label}.heading is not present in the official suite: {heading!r}",
    ):
        return ItemArtifact(
            {"heading": heading, "response_path": "", "response_sha256": ""}
        )
    assert case is not None

    recorded_prompt_hash = _recorded_hash(
        item.get("prompt_sha256"),
        label=f"{item_label}.prompt_sha256",
        validation=validation,
    )
    expected_prompt_hash = hashlib.sha256(case.prompt.encode("utf-8")).hexdigest()
    if recorded_prompt_hash is not None:
        validation.require(
            recorded_prompt_hash == expected_prompt_hash,
            f"{item_label}.prompt_sha256 does not match the official prompt",
        )

    raw_path, raw_hash = _item_response_fields(item)
    validation.require(
        isinstance(item.get("response"), dict),
        f"{item_label}.response: expected an object",
    )
    recorded_response_hash = _recorded_hash(
        raw_hash,
        label=f"{item_label}.response.sha256",
        validation=validation,
    )
    try:
        response_path = _contained_response_path(
            report_path,
            raw_path,
            skill_root=skill_root,
            label=f"{item_label}.response.path",
        )
        response_text, stable_response = _read_response(
            response_path,
            label=f"{item_label}.response",
            remaining_budget=remaining_budget,
        )
    except ForwardTestError as exc:
        validation.errors.append(str(exc))
        return ItemArtifact(
            {
                "heading": heading,
                "response_path": str(raw_path) if isinstance(raw_path, str) else "",
                "response_sha256": "",
            }
        )

    if recorded_response_hash is not None:
        validation.require(
            recorded_response_hash == stable_response.sha256,
            f"{item_label}.response.sha256 does not match the response file",
        )

    review = item.get("review")
    if not validation.require(
        isinstance(review, dict), f"{item_label}.review: expected an object"
    ):
        review = {}
    assert isinstance(review, dict)
    validation.require(
        review.get("passed") is True, f"{item_label}.review.passed must be true"
    )
    if item.get("passed") is not None:
        validation.require(
            item.get("passed") is True, f"{item_label}.passed must be true"
        )
    if reviewer_id is not None:
        validation.require(
            review.get("reviewer_id") == reviewer_id,
            f"{item_label}.review.reviewer_id must match reviewer.id",
        )
    used_spans: set[tuple[int, int]] = set()
    _validate_checks(
        review.get("routes"),
        case.routes,
        response_text,
        kind="routes",
        item_label=item_label,
        validation=validation,
        used_spans=used_spans,
    )
    _validate_checks(
        review.get("conclusions"),
        case.conclusions,
        response_text,
        kind="conclusions",
        item_label=item_label,
        validation=validation,
        used_spans=used_spans,
    )
    return ItemArtifact(
        {
            "heading": heading,
            "response_path": str(raw_path),
            "response_sha256": stable_response.sha256,
        },
        path=stable_response.path,
        identity=stable_response.identity,
        size=stable_response.size,
    )


def _skill_package_digest(skill_root: Path) -> str:
    digest = hashlib.sha256()
    total_bytes = 0

    def walk_error(exc: OSError) -> None:
        raise ForwardTestError(f"skill package cannot be walked: {exc}")

    for directory, child_directories, file_names in os.walk(
        skill_root,
        topdown=True,
        onerror=walk_error,
        followlinks=False,
    ):
        parent = Path(directory)
        retained_directories: list[str] = []
        for child_name in sorted(child_directories):
            child = parent / child_name
            lowered_child = child_name.casefold()
            if lowered_child in PACKAGE_CACHE_DIRECTORIES or lowered_child.endswith(
                ".egg-info"
            ):
                raise ForwardTestError(
                    "skill package contains a generated cache directory: "
                    f"{child.relative_to(skill_root).as_posix()}"
                )
            _safe_existing_directory(child, label="skill package directory")
            retained_directories.append(child_name)
        child_directories[:] = retained_directories

        for file_name in sorted(file_names):
            path = parent / file_name
            relative = path.relative_to(skill_root).as_posix()
            lowered = file_name.casefold()
            if lowered.endswith(".txt") and any(
                lowered.startswith(prefix) for prefix in PACKAGE_RUNNER_DUMP_PREFIXES
            ):
                raise ForwardTestError(
                    "skill package contains a generated test-runner dump: "
                    f"{relative}"
                )
            if (
                lowered in PACKAGE_NOISE_FILENAMES
                or any(lowered.endswith(suffix) for suffix in PACKAGE_NOISE_SUFFIXES)
                or lowered.endswith("~")
                or lowered.endswith(".egg-info")
            ):
                raise ForwardTestError(
                    "skill package contains generated local noise: "
                    f"{relative}"
                )
            remaining = MAX_PACKAGE_BYTES - total_bytes
            if remaining < 1:
                raise ForwardTestError(
                    f"skill package exceeds {MAX_PACKAGE_BYTES} bytes"
                )
            stable = _read_stable_file(
                path,
                label=f"skill package file {relative}",
                max_bytes=remaining,
            )
            total_bytes += stable.size
            relative_bytes = relative.encode("utf-8")
            digest.update(len(relative_bytes).to_bytes(4, "big"))
            digest.update(relative_bytes)
            digest.update(stable.size.to_bytes(8, "big"))
            digest.update(bytes.fromhex(stable.sha256))
    return digest.hexdigest()


def _load_suite(
    skill_root: Path, validation: Validation
) -> tuple[list[SuiteCase], str, str, str]:
    suite_file = _read_stable_file(
        skill_root / DEFAULT_SUITE_RELATIVE_PATH,
        label="official suite",
        max_bytes=16 * 1024 * 1024,
    )
    skill_file = _read_stable_file(
        skill_root / DEFAULT_SKILL_RELATIVE_PATH,
        label="SKILL.md",
        max_bytes=16 * 1024 * 1024,
    )
    try:
        suite_text = _decode_utf8(suite_file.payload, label="official suite")
        suite_digest = official_suite_contract_digest(suite_text)
        parsed = parse_self_test_suite(suite_text)
    except (OSError, ValueError) as exc:
        raise ForwardTestError(f"cannot load current skill contract: {exc}") from exc
    skill_digest = skill_file.sha256
    package_digest = _skill_package_digest(skill_root)

    cases = [
        SuiteCase(
            heading=case.heading,
            prompt=case.prompt,
            routes=tuple(case.routes),
            conclusions=tuple(case.conclusions),
        )
        for case in parsed
    ]
    validation.require(
        len(cases) == OFFICIAL_SUITE_TASK_COUNT,
        f"current official suite has {len(cases)} tasks; expected {OFFICIAL_SUITE_TASK_COUNT}",
    )
    validation.require(
        len({case.heading for case in cases}) == len(cases),
        "current official suite contains duplicate task headings",
    )
    validation.require(
        all(case.prompt and case.routes and case.conclusions for case in cases),
        "current official suite contains an incomplete task contract",
    )
    validation.require(
        suite_digest == OFFICIAL_SUITE_CONTRACT_SHA256,
        "current official-suite contract digest is not the reviewed digest",
    )
    return cases, suite_digest, skill_digest, package_digest


def validate_report(
    report_path: Path, *, skill_root: Optional[Path] = None
) -> dict[str, Any]:
    """Validate report_path without executing anything named by its contents."""

    errors: list[str] = []
    validation = Validation(errors)
    scope = "unknown"
    item_summaries: list[dict[str, str]] = []
    suite_digest = ""
    skill_digest = ""
    package_digest = ""
    report_path = _absolute(Path(report_path))
    root = _absolute(Path(skill_root)) if skill_root is not None else DEFAULT_SKILL_ROOT

    try:
        root = _safe_existing_directory(root, label="skill root")
        report_path = _safe_existing_file(report_path, label="forward-test report")
        if _is_relative_to(
            report_path.resolve(strict=True),
            root.resolve(strict=True),
        ):
            raise ForwardTestError(
                "forward-test report must be stored outside the skill directory"
            )
        document = _read_document(report_path, label=str(report_path))
        if not isinstance(document, dict):
            raise ForwardTestError("forward-test report: expected a JSON object")
        cases, suite_digest, skill_digest, package_digest = _load_suite(
            root, validation
        )
    except ForwardTestError as exc:
        errors.append(str(exc))
        return {
            "schema_version": SCHEMA_VERSION,
            "valid": False,
            "status": "FAIL",
            "scope": scope,
            "full_pass": False,
            "reported_items": 0,
            "official_items": OFFICIAL_SUITE_TASK_COUNT,
            "suite_contract_sha256": suite_digest,
            "skill_sha256": skill_digest,
            "skill_package_sha256": package_digest,
            "items": item_summaries,
            "errors": errors,
        }

    assert isinstance(document, dict)
    validation.require(
        type(document.get("schema_version")) is int
        and document.get("schema_version") == SCHEMA_VERSION,
        f"schema_version must be {SCHEMA_VERSION}",
    )

    suite_metadata = document.get("suite")
    if not validation.require(
        isinstance(suite_metadata, dict), "suite: expected an object"
    ):
        suite_metadata = {}
    assert isinstance(suite_metadata, dict)
    validation.require(
        suite_metadata.get("path") == DEFAULT_SUITE_RELATIVE_PATH.as_posix(),
        "suite.path must name the canonical official suite",
    )
    reported_suite_hash = _recorded_hash(
        suite_metadata.get("contract_sha256"),
        label="suite.contract_sha256",
        validation=validation,
    )
    if reported_suite_hash is not None:
        validation.require(
            reported_suite_hash == suite_digest,
            "suite.contract_sha256 does not match the current official-suite contract",
        )
    reported_suite_count = suite_metadata.get("task_count")
    validation.require(
        type(reported_suite_count) is int
        and reported_suite_count == OFFICIAL_SUITE_TASK_COUNT,
        f"suite.task_count must be {OFFICIAL_SUITE_TASK_COUNT}",
    )

    skill_metadata = document.get("skill")
    if not validation.require(
        isinstance(skill_metadata, dict), "skill: expected an object"
    ):
        skill_metadata = {}
    assert isinstance(skill_metadata, dict)
    validation.require(
        skill_metadata.get("path") == DEFAULT_SKILL_RELATIVE_PATH.as_posix(),
        "skill.path must name SKILL.md",
    )
    reported_skill_hash = _recorded_hash(
        skill_metadata.get("sha256"),
        label="skill.sha256",
        validation=validation,
    )
    if reported_skill_hash is not None:
        validation.require(
            reported_skill_hash == skill_digest,
            "skill.sha256 does not match the current SKILL.md",
        )
    reported_package_hash = _recorded_hash(
        skill_metadata.get("package_sha256"),
        label="skill.package_sha256",
        validation=validation,
    )
    if reported_package_hash is not None:
        validation.require(
            reported_package_hash == package_digest,
            "skill.package_sha256 does not match the current skill package",
        )

    runner_id = _actor_id(document, "runner", validation)
    reviewer_id = _actor_id(document, "reviewer", validation)
    if runner_id is not None and reviewer_id is not None:
        validation.require(
            runner_id.casefold() != reviewer_id.casefold(),
            "runner.id and reviewer.id must identify different agents",
        )

    items = document.get("items")
    if not validation.require(isinstance(items, list), "items: expected a list"):
        items = []
    assert isinstance(items, list)
    if len(items) > OFFICIAL_SUITE_TASK_COUNT:
        validation.errors.append(
            f"items may contain at most {OFFICIAL_SUITE_TASK_COUNT} tasks"
        )
        items_to_validate = items[:OFFICIAL_SUITE_TASK_COUNT]
    else:
        items_to_validate = items
    scope = _scope(document, len(items), validation)
    claimed_full_pass = document.get("full_pass")
    if claimed_full_pass is not None:
        validation.require(
            claimed_full_pass is False
            or (
                claimed_full_pass is True
                and scope == "full"
                and len(items) == OFFICIAL_SUITE_TASK_COUNT
            ),
            "full_pass may be true only for a 160-task full-scope report",
        )

    cases_by_heading = {case.heading: case for case in cases}
    headings: list[str] = []
    seen_headings: set[str] = set()
    seen_identities: set[tuple[int, int]] = set()
    seen_paths: list[Path] = []
    remaining_budget = MAX_TOTAL_RESPONSE_BYTES
    for index, item in enumerate(items_to_validate):
        if isinstance(item, dict) and isinstance(item.get("heading"), str):
            candidate_heading = item["heading"]
            if candidate_heading in seen_headings:
                validation.errors.append(
                    f"items[{index}].heading is duplicated: {candidate_heading!r}"
                )
                continue
            seen_headings.add(candidate_heading)
        artifact = _validate_item(
            item,
            index,
            report_path,
            cases_by_heading,
            reviewer_id,
            root,
            remaining_budget,
            validation,
        )
        if artifact is None:
            continue
        item_summaries.append(artifact.summary)
        headings.append(artifact.summary["heading"])
        remaining_budget -= artifact.size
        if artifact.path is not None:
            if artifact.identity is not None and artifact.identity != (0, 0):
                validation.require(
                    artifact.identity not in seen_identities,
                    f"items[{index}].response must identify a distinct physical file",
                )
                seen_identities.add(artifact.identity)
            for prior_path in seen_paths:
                try:
                    same_file = os.path.samefile(artifact.path, prior_path)
                except OSError:
                    same_file = False
                if same_file:
                    validation.errors.append(
                        f"items[{index}].response must identify a distinct physical file"
                    )
                    break
            seen_paths.append(artifact.path)
    validation.require(
        len(headings) == len(set(headings)),
        "items contain duplicate task headings",
    )
    if scope == "full":
        missing = sorted(set(cases_by_heading) - set(headings))
        validation.require(
            not missing,
            "full scope is missing official tasks: "
            + repr(missing[:10])
            + (" ..." if len(missing) > 10 else ""),
        )

    valid = not errors
    full_pass = valid and scope == "full" and len(headings) == OFFICIAL_SUITE_TASK_COUNT
    return {
        "schema_version": SCHEMA_VERSION,
        "valid": valid,
        "status": "PASS" if valid else "FAIL",
        "scope": scope,
        "full_pass": full_pass,
        "reported_items": len(items),
        "official_items": OFFICIAL_SUITE_TASK_COUNT,
        "suite_contract_sha256": suite_digest,
        "skill_sha256": skill_digest,
        "skill_package_sha256": package_digest,
        "items": item_summaries,
        "errors": errors,
    }


def _checks(
    expected_values: tuple[str, ...],
    response_text: str,
    *,
    kind: str,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    cursor = 0
    for value in expected_values:
        value_start = response_text.find(value, cursor)
        if value_start < 0:
            continue
        line_start = response_text.rfind("\n", 0, value_start) + 1
        line_end = response_text.find("\n", value_start + len(value))
        if line_end < 0:
            line_end = len(response_text)
        quote = response_text[line_start:line_end]
        checks.append(
            {
                "expected": value,
                "passed": True,
                "rationale": (
                    f"Independent reviewer confirms this expected {kind} "
                    "from the cited response span."
                ),
                "evidence": [{"quote": quote, "start": line_start, "end": line_end}],
            }
        )
        cursor = line_end + 1
    return checks


def run_self_test() -> None:
    validation = Validation([])
    root = _safe_existing_directory(DEFAULT_SKILL_ROOT, label="self-test skill root")
    cases, suite_digest, skill_digest, package_digest = _load_suite(root, validation)
    if validation.errors:
        raise AssertionError("; ".join(validation.errors))
    case = cases[0]
    response_text = "\n".join((*case.routes, *case.conclusions)) + "\n"

    with tempfile.TemporaryDirectory(prefix="spider-forward-test-") as temporary:
        report_directory = Path(temporary)
        response_path = report_directory / "responses" / "task-000.md"
        response_path.parent.mkdir()
        response_path.write_bytes(response_text.encode("utf-8"))
        response_hash = bounded_sha256(response_path)
        report = {
            "schema_version": SCHEMA_VERSION,
            "scope": {"kind": "smoke", "task_count": 1},
            "suite": {
                "path": DEFAULT_SUITE_RELATIVE_PATH.as_posix(),
                "contract_sha256": suite_digest,
                "task_count": OFFICIAL_SUITE_TASK_COUNT,
            },
            "skill": {
                "path": DEFAULT_SKILL_RELATIVE_PATH.as_posix(),
                "sha256": skill_digest,
                "package_sha256": package_digest,
            },
            "runner": {
                "id": "self-test-fresh-runner",
                "fresh_context": True,
                "independent": True,
            },
            "reviewer": {
                "id": "self-test-independent-reviewer",
                "fresh_context": True,
                "independent": True,
            },
            "items": [
                {
                    "heading": case.heading,
                    "prompt_sha256": hashlib.sha256(
                        case.prompt.encode("utf-8")
                    ).hexdigest(),
                    "response": {
                        "path": response_path.relative_to(report_directory).as_posix(),
                        "sha256": response_hash,
                    },
                    "review": {
                        "passed": True,
                        "reviewer_id": "self-test-independent-reviewer",
                        "routes": _checks(case.routes, response_text, kind="route"),
                        "conclusions": _checks(
                            case.conclusions, response_text, kind="conclusion"
                        ),
                    },
                }
            ],
        }
        report_path = report_directory / "forward-test-report.json"
        report_path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        result = validate_report(report_path, skill_root=root)
        if not result["valid"] or result["full_pass"]:
            raise AssertionError(f"valid smoke report was rejected: {result['errors']}")

        full_claim = json.loads(json.dumps(report))
        full_claim["scope"] = {"kind": "full", "task_count": 1}
        report_path.write_text(json.dumps(full_claim), encoding="utf-8")
        full_result = validate_report(report_path, skill_root=root)
        if full_result["valid"] or full_result["full_pass"]:
            raise AssertionError("partial report was accepted as full")

        report_path.write_text(json.dumps(report), encoding="utf-8")
        response_path.write_bytes((response_text + "tampered\n").encode("utf-8"))
        tampered_result = validate_report(report_path, skill_root=root)
        if tampered_result["valid"]:
            raise AssertionError("tampered response hash was accepted")

        response_path.write_bytes(response_text.encode("utf-8"))
        traversal = json.loads(json.dumps(report))
        traversal["items"][0]["response"]["path"] = "../outside.md"
        report_path.write_text(json.dumps(traversal), encoding="utf-8")
        traversal_result = validate_report(report_path, skill_root=root)
        if traversal_result["valid"]:
            raise AssertionError("response path traversal was accepted")

        package_mismatch = json.loads(json.dumps(report))
        package_mismatch["skill"]["package_sha256"] = "0" * 64
        report_path.write_text(json.dumps(package_mismatch), encoding="utf-8")
        package_result = validate_report(report_path, skill_root=root)
        if package_result["valid"]:
            raise AssertionError("skill package hash mismatch was accepted")

        weak_types = json.loads(json.dumps(report))
        weak_types["schema_version"] = True
        weak_types["suite"]["task_count"] = 160.0
        report_path.write_text(json.dumps(weak_types), encoding="utf-8")
        weak_type_result = validate_report(report_path, skill_root=root)
        if weak_type_result["valid"]:
            raise AssertionError("non-integer contract fields were accepted")

        fake_skill_root = response_path.parent / "fake-skill"
        fake_skill_root.mkdir()
        (fake_skill_root / "SKILL.md").write_text("fake skill", encoding="utf-8")
        try:
            _contained_response_path(
                report_path,
                "responses/fake-skill/SKILL.md",
                skill_root=fake_skill_root,
                label="self-test response scope",
            )
        except ForwardTestError as exc:
            if "outside the skill root" not in str(exc):
                raise AssertionError(f"unexpected response scope error: {exc}")
        else:
            raise AssertionError("response inside the skill root was accepted")

        weak_evidence = json.loads(json.dumps(report))
        first_span = weak_evidence["items"][0]["review"]["routes"][0]["evidence"][0]
        first_span.update({"quote": response_text[0:1], "start": 0, "end": 1})
        report_path.write_text(json.dumps(weak_evidence), encoding="utf-8")
        weak_result = validate_report(report_path, skill_root=root)
        if weak_result["valid"]:
            raise AssertionError("trivial reviewer evidence was accepted")

        try:
            hard_link = report_directory / "responses" / "hard-link.md"
            os.link(response_path, hard_link)
        except OSError:
            hard_link = None
        if hard_link is not None:
            linked_report = json.loads(json.dumps(report))
            linked_report["items"][0]["response"]["path"] = hard_link.relative_to(
                report_directory
            ).as_posix()
            report_path.write_text(json.dumps(linked_report), encoding="utf-8")
            linked_result = validate_report(report_path, skill_root=root)
            if linked_result["valid"]:
                raise AssertionError("hard-linked response was accepted")
            hard_link.unlink()

        if os.name == "nt":
            trailing_dot = json.loads(json.dumps(report))
            trailing_dot["items"][0]["response"]["path"] += "."
            report_path.write_text(json.dumps(trailing_dot), encoding="utf-8")
            trailing_dot_result = validate_report(report_path, skill_root=root)
            if trailing_dot_result["valid"]:
                raise AssertionError("Windows trailing-dot response alias was accepted")


def render_text(result: dict[str, Any]) -> str:
    lines = [
        f"status={result['status']}",
        f"scope={result['scope']}",
        f"reported_items={result['reported_items']}",
        f"official_items={result['official_items']}",
        f"full_pass={str(result['full_pass']).lower()}",
        f"suite_contract_sha256={result['suite_contract_sha256']}",
        f"skill_sha256={result['skill_sha256']}",
        f"skill_package_sha256={result['skill_package_sha256']}",
    ]
    lines.extend(f"error={error}" for error in result["errors"])
    return "\n".join(lines)


def current_contract(*, skill_root: Optional[Path] = None) -> dict[str, Any]:
    root = _absolute(Path(skill_root)) if skill_root is not None else DEFAULT_SKILL_ROOT
    root = _safe_existing_directory(root, label="skill root")
    validation = Validation([])
    cases, suite_digest, skill_digest, package_digest = _load_suite(root, validation)
    if validation.errors:
        raise ForwardTestError("; ".join(validation.errors))
    return {
        "schema_version": SCHEMA_VERSION,
        "suite": {
            "path": DEFAULT_SUITE_RELATIVE_PATH.as_posix(),
            "contract_sha256": suite_digest,
            "task_count": len(cases),
        },
        "skill": {
            "path": DEFAULT_SKILL_RELATIVE_PATH.as_posix(),
            "sha256": skill_digest,
            "package_sha256": package_digest,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", nargs="?", help="Existing forward-test report JSON")
    parser.add_argument(
        "--skill-root",
        help="Skill root whose suite, SKILL.md, and package hashes must match",
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit machine-readable JSON"
    )
    parser.add_argument(
        "--print-contract",
        action="store_true",
        help="Print current suite and skill hashes without running a model",
    )
    parser.add_argument(
        "--self-test", action="store_true", help="Run deterministic internal checks"
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.self_test:
        try:
            run_self_test()
        except (AssertionError, ForwardTestError, OSError, ValueError) as exc:
            print(f"forward_test_report_self_test=FAIL: {exc}", file=sys.stderr)
            return 1
        print("forward_test_report_self_test=PASS")
        return 0
    if args.print_contract:
        try:
            contract = current_contract(
                skill_root=Path(args.skill_root) if args.skill_root else None
            )
        except (ForwardTestError, OSError, ValueError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(contract, ensure_ascii=False, indent=2))
        else:
            print(f"suite_contract_sha256={contract['suite']['contract_sha256']}")
            print(f"suite_task_count={contract['suite']['task_count']}")
            print(f"skill_sha256={contract['skill']['sha256']}")
            print(f"skill_package_sha256={contract['skill']['package_sha256']}")
        return 0
    if not args.report:
        print(
            "error: report path is required unless --self-test or --print-contract is used",
            file=sys.stderr,
        )
        return 2

    result = validate_report(
        Path(args.report),
        skill_root=Path(args.skill_root) if args.skill_root else None,
    )
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(render_text(result))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
