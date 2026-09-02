#!/usr/bin/env python3
"""Validate Spider King's structure and behavior-preservation invariants."""

from __future__ import annotations

import argparse
import shutil
import ast
import hashlib
import json
import os
import re
import signal
import stat
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# Prevent this validator process from writing __pycache__ into the skill package.
sys.dont_write_bytecode = True

try:
    import yaml
except ImportError:  # pragma: no cover - exercised only in stripped environments
    yaml = None


TASK_HEADING_RE = re.compile(r"^## (Task [^\r\n]+)\r?$", re.MULTILINE)
TASK_BLOCK_RE = re.compile(
    r"^## (?P<heading>Task [^\r\n]+)\r?\n(?P<body>.*?)(?=^## Task |^## Failure signals|\Z)",
    re.MULTILINE | re.DOTALL,
)
PROMPT_RE = re.compile(r"Prompt:\s*```text\s*(?P<prompt>.*?)\s*```", re.DOTALL)
ROUTE_SECTION_RE = re.compile(r"Expected route:\s*(?P<section>.*?)(?=\nMust conclude:)", re.DOTALL)
CONCLUSION_SECTION_RE = re.compile(r"Must conclude:\s*(?P<section>.*?)(?=\n## |\Z)", re.DOTALL)
BACKTICK_PATH_RE = re.compile(r"`((?:references|scripts)/[A-Za-z0-9_.\/-]+)`")
BULLET_RE = re.compile(r"^- (.+)$", re.MULTILINE)
PATH_REF_RE = re.compile(r"(?P<path>(?:references|scripts)/[A-Za-z0-9_.\/-]+)")
FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.DOTALL)
PROFILE_SKILL_TOKEN_RE = re.compile(r"`(?P<name>[a-z0-9]+(?:-[a-z0-9]+)+)`", re.I)
HTML_COMMENT_RE = re.compile(r"<!--.*?-->", re.DOTALL)
FAILURE_SIGNALS_BLOCK_RE = re.compile(
    r"^## Failure signals\r?\n(?P<body>.*)\Z",
    re.MULTILINE | re.DOTALL,
)
NEGATIVE_CONTRACT_MARKER_RE = re.compile(
    r"^(?:do\s+not|don't|never|must\s+not|should\s+not|does\s+not|cannot|not\b|no\b)",
    re.IGNORECASE,
)
NEGATED_MARKER_PREFIX_RE = re.compile(
    r"(?:\bdo\s+not|\bdon't|\bnever|\bmust\s+not|\bshould\s+not|\bcannot)"
    r"\s+(?:use|require|retain|preserve|enforce|apply|follow|record|include|support)\s+$",
    re.IGNORECASE,
)
MAX_ENTRY_NONBLANK_LINES = 280
MAX_VALIDATION_FILE_BYTES = 16 * 1024 * 1024
MAX_SELF_TEST_OUTPUT_BYTES = 1024 * 1024
OFFICIAL_SUITE_TASK_COUNT = 160
OFFICIAL_SUITE_CONTRACT_SHA256 = (
    "fb40033033ecdbaf9b78f507fce48ffa8ce78ec388e6afcbc0740e23091f6a3d"
)
TRUSTED_SKILL_ROOT = Path(__file__).resolve().parents[1]
MarkerGroups = tuple[tuple[str, ...], ...]
PROFILE_LOCAL_ROUTE_TOKENS = frozenset(
    {
        "artifact-only",
        "chrome-devtools",
        "js-reverse",
        "live-target",
        "set-cookie",
        "spider-king",
    }
)
PROFILE_HANDOFF_CONTEXT_MARKERS = (
    "转",
    "delegate",
    "handoff",
    "primary",
    "route to",
)
PROFILE_SPECIAL_HANDOFF_TOKENS = (
    "`spider-king` AST profile",
)
PROFILE_AVAILABILITY_MARKERS = (
    "capability snapshot",
    "when available",
    "if available",
    "可用时",
    "若可用",
    "已安装时",
    "存在时",
)
PROFILE_FALLBACK_MARKERS = (
    "otherwise",
    "else",
    "fallback",
    "否则",
    "不可用时",
    "未安装时",
    "不存在时",
)
ROOT_SHADOW_DOCUMENTS = (
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
    "CHANGELOG.md",
)
ROOT_ALLOWED_LANDING_DOCUMENTS = (
    "README.md",
    "DISCLAIMER.md",
    "LICENSE",
)
VALIDATION_IGNORED_DIRS = frozenset(
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
GENERATED_RUNNER_DUMP_PREFIXES = ("_err_", "_out_")
GENERATED_NOISE_FILENAMES = frozenset(
    {
        ".coverage",
        ".ds_store",
        "coverage.xml",
        "desktop.ini",
        "thumbs.db",
    }
)
GENERATED_NOISE_SUFFIXES = (
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
LIFECYCLE_TASKS = {
    "Task 0F: Capability checks do not prewarm both target browsers",
    "Task 0G: Normal Chrome to js-reverse handoff",
    "Task 0H: Unreplayable session state uses a retained exception",
    "Task 0I: Parked is not closed",
    "Task 0J: Browser mode follows installed capabilities",
    "Task 0K: Returning from js-reverse to Chrome",
}
SECOND_PASS_TASKS = {
    "Task 0L: Artifact-only intake does not invent browser evidence",
    "Task 0M: Continuation intake reuses a current gate",
    "Task 0N: Missing optional tools use supported fallbacks",
    "Task 0O: Sensitive artifacts are redacted by default",
}
PRACTICE_TASKS = {
    "Task 19: Normalize a publishable evidence package",
    "Task 19A: Find the first divergence across matching final requests",
    "Task 19B: Require an offline oracle and negative control",
}
WEBSKILLS_FUSION_TASKS = {
    "Task 21: Supplied JavaScript uses the non-executing AST route",
    "Task 21A: AST parse failure preserves the exact source",
    "Task 21B: Dynamic rebuild requires a second independent sample",
    "Task 21C: CryptoJS cipher hooks remain metadata-only",
    "Task 21D: gRPC framing needs length and trailer negative controls",
    "Task 21E: Crypto primitive names do not define wire formats",
    "Task 21F: Narrow env runtime contracts stay explicit and bounded",
    "Task 21G: One successful job remains an experience candidate",
    "Task 21H: Specialist handoff cannot widen authority",
    "Task 21I: Evidence uses its own completion gate",
    "Task 21J: Provider write paths are an enforced allowlist",
    "Task 21K: Static AST dependencies stay task-local",
    "Task 21L: Static validation does not execute candidate code",
}
CLAUDE_PROJECT_FUSION_CONTRACTS: dict[
    str,
    tuple[tuple[str, ...], MarkerGroups],
] = {
    "Task 21M: Browser acquisition roles are capability-aware": (
        (
            "references/startup-triage-playbook.md",
            "references/tool-playbook.md",
        ),
        (
            ("fingerprint baseline",),
            ("debugger trace",),
            ("cdp bridge",),
            ("target_active",),
            ("sequentially",),
            ("evidence-only",),
            ("browser-free python",),
        ),
    ),
    "Task 21N: The implementation brief is conditional": (
        (
            "references/provider-work-order.md",
            "references/report-templates.md",
        ),
        (
            ("mandatory plan",),
            ("approval ceremony",),
            ("bounded evidence",),
            ("local-proof",),
            ("`compact-replay`",),
            ("`collector`",),
            ("material implementation ambiguity",),
            ("widen runtime",),
            ("dependency",),
            ("write",),
            ("live authority",),
            ("decision record",),
            ("never grants",),
            ("acceptance test",),
            ("unresolved risks",),
        ),
    ),
    "Task 21O: Project runtime coherence is explicit": (
        (
            "scripts/check_reverse_env.py",
            "references/project-artifact-contract.md",
        ),
        (
            ("project root",),
            ("interpreter",),
            ("virtual-environment state",),
            ("project-local environment coherence",),
            ("runtime versions",),
            ("explicitly supplied lockfiles",),
            ("relative to the bound project",),
            ("warn by default",),
            ("fail only",),
            ("never hardcode",),
        ),
    ),
    "Task 21P: Hook timing fallbacks preserve evidence limits": (
        (
            "references/tool-playbook.md",
            "references/hook-techniques.md",
        ),
        (
            ("preload support",),
            ("missing optional methods",),
            ("early supported breakpoint",),
            ("authorized controlled reload",),
            ("post-load observation",),
            ("clean baseline",),
            ("sibling transports",),
            ("page-owned world",),
        ),
    ),
    "Task 21Q: Collector handoff stays compact and auditable": (
        (
            "references/report-templates.md",
            "references/delivery-gate-playbook.md",
        ),
        (
            ("real endpoint",),
            ("dynamic field writer",),
            ("wire slot",),
            ("session issuance or refresh",),
            ("fixed-vector",),
            ("negative-control",),
            ("live replay count",),
            ("business acceptance oracle",),
            ("python and helper boundary",),
            ("browser-free and runtime-free truth",),
            ("saved artifact paths",),
            ("hashes",),
            ("remaining risks",),
            ("redact reusable secrets",),
            ("one canonical compact handoff",),
        ),
    ),
}
CLAUDE_PROJECT_FUSION_TASKS = set(CLAUDE_PROJECT_FUSION_CONTRACTS)

STARTUP_BROWSER_ROLE_MARKERS: MarkerGroups = (
    ("`fingerprint-baseline`",),
    ("`debugger-trace`",),
    ("`cdp-bridge`",),
    ("`sequential handoff`", "after the handoff gate"),
    ("target_active",),
    ("chrome baseline",),
    ("not permanent routes",),
    ("not a third concurrent owner",),
)
TOOL_BROWSER_ROLE_MARKERS: MarkerGroups = (
    ("`fingerprint-baseline`",),
    ("`debugger-trace`",),
    ("`cdp-bridge`",),
    ("`sequential handoff`", "after the handoff gate"),
    ("target_active",),
    ("not choose-once routes",),
    ("chrome baseline followed by `js-reverse` after the handoff gate",),
    ("required first-pass evidence surface",),
)
HOOK_TIMING_MARKERS: MarkerGroups = (
    ("`preload available`",),
    ("`preload unavailable`",),
    ("`page already initialized`",),
    ("`hook miss`",),
    ("`page-owned world`",),
    ("`sibling transport`",),
    ("clean baseline",),
    ("controlled refresh",),
    ("subsequent events only",),
    ("retained_exception",),
    ("silence on one channel is not whole-transport proof",),
)
TOOL_HOOK_ROUTING_MARKERS: MarkerGroups = (
    ("navigate_page(initscript=...)",),
    ("controlled refresh",),
    ("evidence only about that exact boundary",),
    ("sibling writers or alternate transport channels",),
    ("references/hook-techniques.md",),
    ("preload, initialized-page, hook-miss, page-owned-world, sibling-transport",),
)
STARTUP_ENVIRONMENT_MARKERS: MarkerGroups = (
    ("scripts/check_reverse_env.py --project-root",),
    ("--helper-lockfile",),
    ("project `.venv` coherence",),
    ("advisory by default",),
    ("--require-project-venv",),
)
ENVIRONMENT_COHERENCE_MARKERS: MarkerGroups = (
    ("def command_version(",),
    ("def discover_path_tool(",),
    ("def _diagnostic_subprocess_environment(",),
    ("def _trusted_windows_command_paths(",),
    ("def _read_bounded_process_output(",),
    ("limit_exceeded",),
    ("def detect_python_environment(",),
    ("def fingerprint_helper_lockfile(",),
    ("def _read_stable_lockfile(",),
    ("os.path.samestat",),
    ("backslashreplace",),
    ('"--project-root"',),
    ('"--helper-lockfile"',),
    ('"--require-project-venv"',),
    ("for value in args.helper_lockfile",),
    ("python_version",),
    ("node_version",),
    ("npm_version",),
    ("project_dot_venv_active",),
    ("project_dot_venv_requirement",),
    ("helper_lockfiles: none_requested",),
    ("relative_path=relative_path",),
    ("sha256=hashlib.sha256",),
    ("helper lockfile must stay under project root",),
    ("helper lockfile name is not a supported public lockfile",),
    ("if args.require_project_venv and not python_environment.project_dot_venv_active",),
)
PROVIDER_BRIEF_MARKERS: MarkerGroups = (
    ("`compact-replay`",),
    ("`collector`",),
    ("at least one material choice remains",),
    ("more than one implementation form",),
    ("dependency installation", "dependency choice or installation authority"),
    ("durable path",),
    ("meaningful permission choice",),
    ("do not require this brief for `evidence`, `local-proof`, or explicit no-write analysis",),
    ("decision record, not an automatic user-approval gate",),
    ("never grants authority",),
    ("does not replace or widen `permissions`, `budget`, scope, or `allowedpaths`",),
    ("real endpoint",),
    ("dynamic field",),
    ("wire slot",),
    ("chosen boundary",),
    ("acceptance oracle",),
    ("negative control",),
    ("residual risk",),
)
REPORT_BRIEF_MARKERS: MarkerGroups = (
    ("`compact-replay`",),
    ("`collector`",),
    ("multiple implementation forms", "competing implementation forms"),
    ("do not force it for `evidence`, `local-proof`",),
    ("explicit no-write analysis",),
    ("not approval",),
    ("cannot widen scope, budgets, permissions, or `allowedpaths`",),
    ("implementation brief",),
    ("- trigger:",),
    ("- real request:",),
    ("- dynamic fields:",),
    ("- candidate forms:",),
    ("- chosen boundary:",),
    ("- session contract:",),
    ("- acceptance:",),
    ("- planned durable paths:",),
    ("- permission status:",),
    ("- residual risk:",),
)
COMPACT_HANDOFF_MARKERS: MarkerGroups = (
    ("default final summary",),
    ("it summarizes proof; it does not replace that gate",),
    ("replay count `unproven`",),
    ("protocol handoff",),
    ("- capability:",),
    ("- real request:",),
    ("- protocol order:",),
    ("- dynamic fields:",),
    ("writer",),
    ("wire slot",),
    ("- evidence:",),
    ("- fixed vectors:",),
    ("- python/helper boundary:",),
    ("- session:",),
    ("issuance",),
    ("refresh",),
    ("- acceptance:",),
    ("negative control",),
    ("replay count",),
    ("- saved paths:",),
    ("sha-256",),
    ("- browser-free status:",),
    ("runtime-free status",),
    ("- residual risk:",),
)
WORKFLOW_BRIEF_MARKERS: MarkerGroups = (
    ("conditional implementation brief",),
    ("ambiguous or authority-widening",),
    ("do not impose it on bounded `evidence`, `local-proof`",),
)
WORKFLOW_HANDOFF_MARKERS: MarkerGroups = (
    ("compact protocol handoff",),
    ("canonical rerun and audit summary",),
    ("do not duplicate the same facts",),
)
ARTIFACT_RUNTIME_PACKAGING_MARKERS: MarkerGroups = (
    ("scripts/check_reverse_env.py --project-root",),
    ("--helper-lockfile",),
    ("relative paths",),
    ("byte lengths",),
    ("sha-256",),
)
ARTIFACT_RUNTIME_MANIFEST_MARKERS: MarkerGroups = (
    ('"runtimeevidence"',),
    ('"pythonversion"',),
    ('"nodeversion"',),
    ('"npmversion"',),
    ('"projectvenv"',),
    ('"helperlockfiles"',),
)
SCRIPT_SELF_TESTS = (
    ("evidence_normalizer.py", "self_test=PASS"),
    ("transcript_diff.py", "transcript_diff_self_test=PASS"),
    ("practice_lab.py", "practice_lab_self_test=PASS"),
    ("transform_trace_diff.py", "self_test=PASS"),
    ("transport_profile_diff.py", "self_test=PASS"),
    ("grpc_frame_inspector.py", "grpc_frame_inspector_self_test=PASS"),
    ("forward_test_report.py", "forward_test_report_self_test=PASS"),
)
SCRIPT_SELF_TEST_TIMEOUT_SECONDS = 30
SELF_TEST_ENV_ALLOWLIST = (
    "COMSPEC",
    "LANG",
    "LC_ALL",
    "PATH",
    "PATHEXT",
    "SYSTEMROOT",
    "TEMP",
    "TMP",
    "WINDIR",
)
FORWARD_TEST_BANNED_IMPORT_ROOTS = frozenset(
    {
        "anthropic",
        "httpx",
        "openai",
        "requests",
        "socket",
        "subprocess",
        "urllib",
        "urllib3",
    }
)
FORWARD_TEST_BANNED_CALLS = frozenset(
    {
        "__import__",
        "compile",
        "eval",
        "exec",
        "os.popen",
        "os.system",
    }
)


@dataclass
class Validation:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    def require(self, condition: bool, message: str) -> None:
        if not condition:
            self.errors.append(message)

    def warn(self, condition: bool, message: str) -> None:
        if not condition:
            self.warnings.append(message)


@dataclass(frozen=True)
class SelfTestCase:
    heading: str
    prompt: str
    routes: tuple[str, ...]
    conclusions: tuple[str, ...]


def read_text(path: Path) -> str:
    with path.open("rb") as handle:
        payload = handle.read(MAX_VALIDATION_FILE_BYTES + 1)
    if len(payload) > MAX_VALIDATION_FILE_BYTES:
        raise ValueError(
            f"{path.name} exceeds the {MAX_VALIDATION_FILE_BYTES}-byte validation limit"
        )
    try:
        return payload.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ValueError(f"{path.name} is not valid UTF-8") from exc


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    total = 0
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(chunk)
            if total > MAX_VALIDATION_FILE_BYTES:
                raise ValueError(
                    f"{path.name} exceeds the {MAX_VALIDATION_FILE_BYTES}-byte validation limit"
                )
            digest.update(chunk)
    return digest.hexdigest()


def normalized_ref(raw: str) -> str:
    return raw.rstrip(".,):;]}`")


def normalized_search_text(value: str) -> str:
    return " ".join(value.lower().split())


def strip_html_comments(document_text: str) -> str:
    return HTML_COMMENT_RE.sub(" ", document_text)


def marker_has_positive_occurrence(document_text: str, marker: str) -> bool:
    normalized_document = normalized_search_text(strip_html_comments(document_text))
    normalized_marker = normalized_search_text(marker)
    if not normalized_marker:
        return False

    marker_is_explicitly_negative = bool(
        NEGATIVE_CONTRACT_MARKER_RE.match(normalized_marker)
    )
    start = normalized_document.find(normalized_marker)
    while start != -1:
        if marker_is_explicitly_negative:
            return True
        prefix = normalized_document[max(0, start - 128) : start]
        if NEGATED_MARKER_PREFIX_RE.search(prefix) is None:
            return True
        start = normalized_document.find(normalized_marker, start + 1)
    return False


def extract_markdown_section(document_text: str, heading: str) -> str:
    document_text = strip_html_comments(document_text)
    match = re.search(
        rf"^##[ \t]+{re.escape(heading)}[ \t]*\r?\n(?P<body>.*?)(?=^##[ \t]+|\Z)",
        document_text,
        re.IGNORECASE | re.MULTILINE | re.DOTALL,
    )
    return match.group("body") if match else ""


def require_marker_groups(
    document_text: str,
    marker_groups: MarkerGroups,
    result: Validation,
    label: str,
) -> None:
    missing = [
        " | ".join(group)
        for group in marker_groups
        if not any(marker_has_positive_occurrence(document_text, marker) for marker in group)
    ]
    result.require(not missing, f"{label} is missing marker groups: {missing}")


def require_markdown_section_markers(
    document_text: str,
    heading: str,
    marker_groups: MarkerGroups,
    result: Validation,
    label: str,
) -> None:
    section = extract_markdown_section(document_text, heading)
    if not section.strip():
        result.errors.append(f"{label} section is missing or empty: ## {heading}")
        return
    require_marker_groups(section, marker_groups, result, label)


def profile_handoff_tokens(line: str) -> tuple[str, ...]:
    lower_line = line.lower()
    has_handoff_context = line.lstrip().startswith("|") or any(
        marker in lower_line for marker in PROFILE_HANDOFF_CONTEXT_MARKERS
    )
    tokens: set[str] = set()
    if has_handoff_context:
        tokens.update(
            match.group("name").lower()
            for match in PROFILE_SKILL_TOKEN_RE.finditer(line)
            if match.group("name").lower() not in PROFILE_LOCAL_ROUTE_TOKENS
        )
    tokens.update(
        token
        for token in PROFILE_SPECIAL_HANDOFF_TOKENS
        if token.lower() in lower_line
    )
    return tuple(sorted(tokens))


def parse_self_test_suite(suite_text: str) -> list[SelfTestCase]:
    cases: list[SelfTestCase] = []
    for match in TASK_BLOCK_RE.finditer(suite_text):
        heading = match.group("heading").strip()
        body = match.group("body")
        prompt_match = PROMPT_RE.search(body)
        route_match = ROUTE_SECTION_RE.search(body)
        conclusion_match = CONCLUSION_SECTION_RE.search(body)
        prompt = prompt_match.group("prompt").strip() if prompt_match else ""
        routes = (
            tuple(BACKTICK_PATH_RE.findall(route_match.group("section")))
            if route_match
            else ()
        )
        conclusions = (
            tuple(item.strip() for item in BULLET_RE.findall(conclusion_match.group("section")))
            if conclusion_match
            else ()
        )
        cases.append(
            SelfTestCase(
                heading=heading,
                prompt=prompt,
                routes=routes,
                conclusions=conclusions,
            )
        )
    return cases


def normalize_newlines(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\r", "\n")


def official_suite_contract_digest(suite_text: str) -> str:
    normalized = normalize_newlines(suite_text)
    task_blocks = [
        match.group(0).rstrip()
        for match in TASK_BLOCK_RE.finditer(normalized)
    ]
    failure_match = FAILURE_SIGNALS_BLOCK_RE.search(normalized)
    failure_signals = failure_match.group(0).rstrip() if failure_match else ""
    payload = json.dumps(
        {
            "tasks": task_blocks,
            "failure_signals": failure_signals,
        },
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def validate_official_suite_contract(
    suite_text: str,
    result: Validation,
) -> None:
    task_count = len(TASK_BLOCK_RE.findall(suite_text))
    result.require(
        task_count == OFFICIAL_SUITE_TASK_COUNT,
        f"official self-test suite has {task_count} parsed tasks; "
        f"expected exactly {OFFICIAL_SUITE_TASK_COUNT}",
    )
    result.require(
        FAILURE_SIGNALS_BLOCK_RE.search(suite_text) is not None,
        "official suite must retain Failure signals",
    )
    observed_digest = official_suite_contract_digest(suite_text)
    result.require(
        observed_digest == OFFICIAL_SUITE_CONTRACT_SHA256,
        "official suite contract fingerprint changed: "
        f"expected {OFFICIAL_SUITE_CONTRACT_SHA256}, observed {observed_digest}",
    )


def validate_claude_project_fusion_case(case: SelfTestCase, result: Validation) -> None:
    contract = CLAUDE_PROJECT_FUSION_CONTRACTS.get(case.heading)
    if contract is None:
        return
    expected_routes, conclusion_marker_groups = contract
    result.require(
        case.routes == expected_routes,
        f"official task routes changed: {case.heading}: "
        f"expected {expected_routes}, observed {case.routes}",
    )
    require_marker_groups(
        "\n".join(case.conclusions),
        conclusion_marker_groups,
        result,
        f"official task conclusion contract: {case.heading}",
    )


def task_headings(root: Path) -> set[str]:
    suite = root / "references" / "official-self-test-task-suite.md"
    if not suite.is_file():
        return set()
    return set(TASK_HEADING_RE.findall(read_text(suite)))


def validate_frontmatter(skill_text: str, result: Validation) -> None:
    match = FRONTMATTER_RE.search(skill_text)
    result.require(match is not None, "SKILL.md must start with YAML frontmatter")
    if match is None:
        return

    fields: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            result.errors.append(f"invalid frontmatter line: {line!r}")
            continue
        key, value = line.split(":", 1)
        fields[key.strip()] = value.strip()

    result.require(fields.get("name") == "spider-king", "frontmatter name must be spider-king")
    result.require(bool(fields.get("description")), "frontmatter description must be present")
    result.require(
        set(fields) == {"name", "description"},
        "frontmatter must contain only name and description",
    )


def validate_behavior(skill_text: str, result: Validation) -> None:
    lower = skill_text.lower()
    required_literals = {
        "chrome-devtools": "fresh-target startup must require chrome-devtools",
        "js-reverse": "fresh-target startup must require js-reverse",
        "signer-gated": "signer-gated family is missing",
        "verifier-gated": "verifier-gated family is missing",
        "decode-gated": "decode-gated family is missing",
        "session-gated": "session-gated family is missing",
        "transport-gated": "transport-gated secondary tag is missing",
        "canonical mutation point": "canonical wire mutation rule is missing",
        "fixed-input": "fixed-input validation is missing",
        "cookie provenance": "cookie provenance rule is missing",
        "session chain": "session-chain integrity rule is missing",
        "observer effect": "observer-effect handling is missing",
        "pure python": "pure Python must remain the first delivery choice",
        "browser-free": "browser-free final delivery rule is missing",
        "repeated live replay": "repeated live replay must remain an acceptance gate",
    }
    for literal, message in required_literals.items():
        result.require(literal in lower, message)

    result.require(
        bool(re.search(r"fresh web (?:live-)?target.*chrome-devtools.*js-reverse|Start every fresh web target classified as `live-target` with evidence from both\s+`?chrome-devtools`?\s+and\s+`?js-reverse`?", skill_text, re.I | re.S)),
        "fresh web live targets must explicitly require both first-pass tools",
    )

    result.require(
        ("out of scope" in lower or "out-of-scope" in lower or "pure-web" in lower)
        and ("apk" in lower or "mini-program" in lower or "non-web" in lower)
        and ("paired-browser" in lower or "paired browser" in lower or "ceremony" in lower),
        "pure-web scope must refuse APK/app/mini-program paired-browser ceremony",
    )
    result.require(
        bool(re.search(r"browser automation.*(?:not|never|forbidden|unacceptable)", lower))
        or bool(re.search(r"(?:do not|never).*browser automation", lower)),
        "browser automation must be explicitly rejected as final delivery",
    )
    result.require(
        "references/delivery-gate-playbook.md" in skill_text,
        "delivery-gate-playbook.md must be directly routed from SKILL.md",
    )
    result.require(
        "only for `artifact-only`" in lower
        and "classify it as `live-target`" in lower,
        "focused profiles must not bypass paired evidence for fresh live-target interaction",
    )


def validate_openai_metadata(metadata_text: str, result: Validation) -> None:
    if yaml is None:
        result.errors.append("PyYAML is required to validate agents/openai.yaml")
        return

    try:
        document = yaml.safe_load(metadata_text)
    except yaml.YAMLError as exc:
        result.errors.append(f"invalid agents/openai.yaml: {exc}")
        return
    if not isinstance(document, dict):
        result.errors.append("agents/openai.yaml must contain a YAML mapping")
        return

    interface = document.get("interface")
    if not isinstance(interface, dict):
        result.errors.append("agents/openai.yaml must contain an interface mapping")
        return

    values: dict[str, str] = {}
    for field_name in ("display_name", "short_description", "default_prompt"):
        value = interface.get(field_name)
        result.require(
            isinstance(value, str) and bool(value.strip()),
            f"agents/openai.yaml interface.{field_name} must be a non-empty string",
        )
        if isinstance(value, str):
            values[field_name] = value.strip()

    display_name = values.get("display_name", "")
    short_description = values.get("short_description", "")
    default_prompt = values.get("default_prompt", "")
    result.require(
        display_name == "Spider King",
        "agents/openai.yaml interface.display_name must match Spider King",
    )
    result.require(
        not short_description or 25 <= len(short_description) <= 64,
        "agents/openai.yaml interface.short_description must be 25-64 characters",
    )
    result.require(
        "$spider-king" in default_prompt,
        "agents/openai.yaml interface.default_prompt must mention $spider-king",
    )
    result.require(
        "sequential" in default_prompt.lower(),
        "agents/openai.yaml interface.default_prompt must retain sequential analysis",
    )

    policy = document.get("policy")
    if policy is not None:
        result.require(
            isinstance(policy, dict),
            "agents/openai.yaml policy must be a mapping",
        )
        if isinstance(policy, dict) and "allow_implicit_invocation" in policy:
            result.require(
                isinstance(policy["allow_implicit_invocation"], bool),
                "agents/openai.yaml policy.allow_implicit_invocation must be boolean",
            )


def validate_lifecycle(root: Path, result: Validation) -> None:
    paths = {
        "skill": root / "SKILL.md",
        "tool": root / "references" / "tool-playbook.md",
        "startup": root / "references" / "startup-triage-playbook.md",
        "workflow": root / "references" / "workflow-overview.md",
        "suite": root / "references" / "official-self-test-task-suite.md",
        "maintenance": root / "references" / "skill-maintenance.md",
        "metadata": root / "agents" / "openai.yaml",
    }
    documents: dict[str, str] = {}
    for name, path in paths.items():
        result.require(path.is_file(), f"missing lifecycle document: {path.relative_to(root)}")
        if path.is_file():
            documents[name] = read_text(path)

    combined = "\n".join(documents.values()).lower()
    skill_text = documents.get("skill", "").lower()
    tool_text = documents.get("tool", "").lower()
    startup_text = documents.get("startup", "").lower()
    workflow_text = documents.get("workflow", "").lower()
    maintenance_text = documents.get("maintenance", "").lower()
    metadata_text = documents.get("metadata", "")

    if metadata_text:
        validate_openai_metadata(metadata_text, result)

    result.require(
        "target_active" in combined,
        "browser lifecycle must define single TARGET_ACTIVE ownership",
    )
    result.require(
        "retained_exception" in combined,
        "browser lifecycle must preserve unreplayable state with RETAINED_EXCEPTION",
    )
    result.require(
        "parked" in tool_text and "closed" in tool_text,
        "tool playbook must distinguish PARKED from CLOSED",
    )
    result.require(
        "parallel tool batch" in skill_text or "parallel tool batch" in tool_text,
        "skill must forbid mixing both browser tool families in one parallel tool batch",
    )
    result.require(
        "must not open" in startup_text and "target" in startup_text,
        "startup capability checks must not open both target browsers",
    )
    result.require(
        "handoff" in workflow_text,
        "workflow overview must include a browser lifecycle handoff checkpoint",
    )
    result.require(
        "explicitly confirms" in tool_text,
        "CLOSED may be claimed only when the installed tool explicitly confirms termination",
    )
    result.require(
        "configured mode" in tool_text and "headless" in tool_text and "headful" in tool_text,
        "browser mode guidance must be capability-aware and cover headless/headful differences",
    )
    result.require(
        "target_active" in maintenance_text and "retained_exception" in maintenance_text,
        "maintenance gates must preserve lifecycle ownership and retained-state handling",
    )
    result.require(
        "capability-aware" in maintenance_text and "fallback" in maintenance_text,
        "maintenance gates must require capability-aware profile handoffs with fallbacks",
    )


def validate_intake_tools_and_reporting(root: Path, result: Validation) -> None:
    paths = {
        "skill": root / "SKILL.md",
        "startup": root / "references" / "startup-triage-playbook.md",
        "workflow": root / "references" / "workflow-overview.md",
        "tool": root / "references" / "tool-playbook.md",
        "hook": root / "references" / "hook-techniques.md",
        "report": root / "references" / "report-templates.md",
        "provider": root / "references" / "provider-work-order.md",
        "delivery": root / "references" / "delivery-gate-playbook.md",
        "artifact": root / "references" / "project-artifact-contract.md",
        "maintenance": root / "references" / "skill-maintenance.md",
        "metadata": root / "agents" / "openai.yaml",
        "environment": root / "scripts" / "check_reverse_env.py",
    }
    documents = {
        name: read_text(path)
        for name, path in paths.items()
        if path.is_file()
    }
    combined = "\n".join(documents.values()).lower()
    skill_text = documents.get("skill", "")
    startup_text = documents.get("startup", "")
    workflow_text = documents.get("workflow", "")
    tool_text = documents.get("tool", "")
    hook_text = documents.get("hook", "")
    report_text = documents.get("report", "")
    provider_text = documents.get("provider", "")
    delivery_text = documents.get("delivery", "")
    artifact_text = documents.get("artifact", "")
    metadata_text = documents.get("metadata", "")
    environment_text = documents.get("environment", "")
    tool_lower = tool_text.lower()
    report_lower = report_text.lower()
    provider_lower = provider_text.lower()
    delivery_lower = delivery_text.lower()
    metadata_lower = metadata_text.lower()
    environment_lower = environment_text.lower()

    for mode in ("live-target", "artifact-only", "continuation"):
        result.require(mode in combined, f"intake mode is missing: {mode}")

    result.require(
        "capability snapshot" in combined,
        "startup workflow must record an agent-side capability snapshot",
    )
    mcp_path = root / "references" / "mcp-routing-playbook.md"
    result.require(mcp_path.is_file(), "missing references/mcp-routing-playbook.md")
    if mcp_path.is_file():
        mcp_lower = read_text(mcp_path).lower()
        for token, msg in (
            ("available", "mcp routing must enforce available-only selection"),
            ("target_active", "mcp routing must keep single TARGET_ACTIVE ownership"),
            ("passive", "mcp routing must define passive wire stores"),
            ("environment provider", "mcp routing must define environment providers"),
            ("out of scope", "mcp routing must mark APK/app/mini-program primary work out of scope"),
        ):
            result.require(token in mcp_lower, msg)
    result.require(
        "web" in documents.get("maintenance", "").lower()
        and "chrome-devtools" in documents.get("maintenance", "").lower()
        and "js-reverse" in documents.get("maintenance", "").lower(),
        "skill-maintenance must keep web-scoped dual first-pass wording",
    )

    require_markdown_section_markers(
        startup_text,
        "Capability-aware evidence roles",
        STARTUP_BROWSER_ROLE_MARKERS,
        result,
        "startup browser acquisition roles",
    )
    require_markdown_section_markers(
        tool_text,
        "Capability-aware evidence route matrix",
        TOOL_BROWSER_ROLE_MARKERS,
        result,
        "tool browser acquisition roles",
    )
    require_markdown_section_markers(
        hook_text,
        "Hook timing and recovery matrix",
        HOOK_TIMING_MARKERS,
        result,
        "hook timing fallbacks",
    )
    require_markdown_section_markers(
        tool_text,
        "Dynamic validation",
        TOOL_HOOK_ROUTING_MARKERS,
        result,
        "tool hook recovery routing",
    )
    require_markdown_section_markers(
        startup_text,
        "Startup gate",
        STARTUP_ENVIRONMENT_MARKERS,
        result,
        "startup project environment contract",
    )
    require_marker_groups(
        environment_text,
        ENVIRONMENT_COHERENCE_MARKERS,
        result,
        "check_reverse_env project coherence contract",
    )
    require_markdown_section_markers(
        workflow_text,
        "Startup gate",
        WORKFLOW_BRIEF_MARKERS,
        result,
        "workflow conditional implementation brief routing",
    )
    require_markdown_section_markers(
        workflow_text,
        "Phase 5: Deliver",
        WORKFLOW_HANDOFF_MARKERS,
        result,
        "workflow compact protocol handoff routing",
    )
    require_markdown_section_markers(
        artifact_text,
        "Stable Delivery",
        ARTIFACT_RUNTIME_PACKAGING_MARKERS,
        result,
        "project artifact runtime packaging contract",
    )
    require_markdown_section_markers(
        artifact_text,
        "Proof Manifest",
        ARTIFACT_RUNTIME_MANIFEST_MARKERS,
        result,
        "project artifact runtime evidence contract",
    )
    for label, document_text in (
        ("startup triage", startup_text),
        ("tool playbook", tool_text),
        ("provider work order", provider_text),
        ("report templates", report_text),
        ("skill maintenance", documents.get("maintenance", "")),
        ("project artifact contract", artifact_text),
    ):
        result.require(
            bool(extract_markdown_section(document_text, "Contents").strip()),
            f"{label} must retain a Contents section",
        )
    result.require(
        "`trace_function`" not in tool_lower and "`inject_before_load`" not in tool_lower,
        "tool playbook contains stale unguarded methods: trace_function or inject_before_load",
    )
    for fallback in (
        "set_breakpoint_on_text",
        "get_paused_info",
        "step(direction=",
        "navigate_page(initScript=",
    ):
        result.require(
            fallback.lower() in tool_lower,
            f"tool playbook is missing supported fallback: {fallback}",
        )

    result.require(
        "redacted" in report_lower and "secret" in report_lower,
        "report templates must redact sensitive values by default",
    )
    require_markdown_section_markers(
        provider_text,
        "Conditional Implementation Brief",
        PROVIDER_BRIEF_MARKERS,
        result,
        "provider conditional implementation brief",
    )
    require_markdown_section_markers(
        report_text,
        "Conditional implementation brief",
        REPORT_BRIEF_MARKERS,
        result,
        "report conditional implementation brief",
    )
    result.require(
        "conditional implementation brief" in provider_lower
        and "decision record, not an automatic user-approval gate" in provider_lower
        and all(shape in provider_lower for shape in ("`evidence`", "`local-proof`")),
        "provider contract must keep the implementation brief conditional and capability-specific",
    )
    require_markdown_section_markers(
        report_text,
        "Compact protocol handoff",
        COMPACT_HANDOFF_MARKERS,
        result,
        "compact protocol handoff",
    )
    require_marker_groups(
        skill_text,
        (
            ("compact protocol handoff summary",),
            ("rather than creating redundant project documents",),
        ),
        result,
        "skill compact handoff routing",
    )
    result.require(
        "compact protocol handoff" in report_lower
        and "it summarizes proof; it does not replace that gate" in report_lower
        and "python/helper boundary" in report_lower
        and "negative control" in report_lower,
        "report templates must retain the compact auditable protocol handoff",
    )
    result.require(
        "proof_manifest.json" in report_lower and "proof_manifest.json" in delivery_lower,
        "reporting and delivery gates must require proof_manifest.json",
    )
    result.require(
        "artifact-only" in metadata_lower and "live target" in metadata_lower,
        "agents/openai.yaml must advertise live-target and artifact-only intake",
    )
    result.require(
        all(mode in environment_lower for mode in ("live-target", "artifact-only", "continuation"))
        and "depends_on_intake_mode" in environment_lower,
        "check_reverse_env.py must report intake-dependent capability requirements",
    )


def validate_references(root: Path, skill_text: str, result: Validation) -> None:
    for match in PATH_REF_RE.finditer(skill_text):
        rel = normalized_ref(match.group("path"))
        result.require((root / rel).is_file(), f"broken routed path: {rel}")

    reference_files = sorted((root / "references").glob("*.md"))
    result.require(bool(reference_files), "references directory must contain Markdown files")
    for path in reference_files:
        token = f"references/{path.name}"
        result.require(token in skill_text, f"reference is not directly routed by SKILL.md: {token}")

        document_text = strip_html_comments(read_text(path))
        for match in PATH_REF_RE.finditer(document_text):
            rel = normalized_ref(match.group("path"))
            if not Path(rel).suffix:
                continue
            result.require(
                (root / rel).is_file(),
                f"broken reference document path: {path.relative_to(root)}: {rel}",
            )


def validate_reference_contents(root: Path, result: Validation) -> None:
    references_root = root / "references"
    if not references_root.is_dir():
        return

    for path in sorted(references_root.rglob("*.md")):
        if is_validation_ignored(path):
            continue
        document_text = read_text(path)
        if len(document_text.splitlines()) <= 100:
            continue
        relative = path.relative_to(root).as_posix()
        result.require(
            bool(extract_markdown_section(document_text, "Contents").strip()),
            f"long Markdown reference must retain a Contents section: {relative}",
        )


def validate_profile_routes(root: Path, result: Validation) -> None:
    profiles_root = root / "references" / "profiles"
    if not profiles_root.is_dir():
        return

    for profile_root in sorted(path for path in profiles_root.iterdir() if path.is_dir()):
        index_path = profile_root / "index.md"
        result.require(
            index_path.is_file(),
            f"profile is missing index.md: {profile_root.relative_to(root)}",
        )
        if not index_path.is_file():
            continue

        index_text = read_text(index_path)
        package_path = profile_root / "package.json"
        if package_path.is_file():
            try:
                package_data = json.loads(read_text(package_path))
            except json.JSONDecodeError as exc:
                result.errors.append(
                    f"invalid profile package.json: {package_path.relative_to(root)}: {exc}"
                )
            else:
                if not isinstance(package_data, dict):
                    result.errors.append(
                        f"profile package.json must contain a JSON object: "
                        f"{package_path.relative_to(root)}"
                    )
                else:
                    scripts = package_data.get("scripts", {})
                    result.require(
                        isinstance(scripts, dict) and bool(scripts.get("test")),
                        f"profile package.json is missing npm test: "
                        f"{package_path.relative_to(root)}",
                    )
        local_references = sorted((profile_root / "references").glob("*.md"))
        for reference_path in local_references:
            token = f"references/{reference_path.name}"
            result.require(
                token in index_text,
                f"profile reference is not routed by index.md: "
                f"{reference_path.relative_to(root)}",
            )

        for document_path in sorted(profile_root.rglob("*.md")):
            if is_validation_ignored(document_path):
                continue
            document_text = read_text(document_path)
            for match in PATH_REF_RE.finditer(document_text):
                rel = normalized_ref(match.group("path"))
                candidates = (profile_root / rel, root / rel)
                result.require(
                    any(candidate.exists() for candidate in candidates),
                    f"broken profile routed path: "
                    f"{document_path.relative_to(root)}: {rel}",
                )

            for line_number, line in enumerate(document_text.splitlines(), start=1):
                lower_line = line.lower()
                for token in profile_handoff_tokens(line):
                    has_availability_check = any(
                        marker in lower_line for marker in PROFILE_AVAILABILITY_MARKERS
                    )
                    has_fallback = any(
                        marker in lower_line for marker in PROFILE_FALLBACK_MARKERS
                    )
                    result.require(
                        has_availability_check and has_fallback,
                        f"unguarded profile handoff: "
                        f"{document_path.relative_to(root)}:{line_number}: {token}",
                    )


def validate_entry_size(skill_text: str, result: Validation, legacy: bool) -> None:
    nonblank = sum(1 for line in skill_text.splitlines() if line.strip())
    if legacy:
        result.warnings.append(f"legacy entry size: {nonblank} nonblank lines")
        return
    result.require(
        nonblank <= MAX_ENTRY_NONBLANK_LINES,
        f"SKILL.md has {nonblank} nonblank lines; budget is {MAX_ENTRY_NONBLANK_LINES}",
    )



def is_generated_runner_dump(name: str) -> bool:
    """Return True for external pytest/runner dump files such as _err_*.txt."""
    lowered = name.casefold()
    return lowered.endswith(".txt") and any(
        lowered.startswith(prefix) for prefix in GENERATED_RUNNER_DUMP_PREFIXES
    )


def classify_generated_noise_file(name: str) -> str | None:
    """Return a hygiene error label for generated local noise files, else None."""
    lowered = name.casefold()
    if is_generated_runner_dump(name):
        return "generated test-runner dump"
    if lowered in GENERATED_NOISE_FILENAMES:
        return "generated local noise file"
    if any(lowered.endswith(suffix) for suffix in GENERATED_NOISE_SUFFIXES):
        return "generated local noise file"
    if lowered.endswith("~"):
        return "generated local noise file"
    if lowered.endswith(".egg-info"):
        return "generated local noise file"
    return None


def iter_package_hygiene_targets(root: Path) -> list[tuple[Path, str, str]]:
    """List generated dirt under root as (path, kind, relative_posix)."""
    cache_names = {name.casefold() for name in VALIDATION_IGNORED_DIRS}
    targets: list[tuple[Path, str, str]] = []

    def record_walk_error(exc: OSError) -> None:
        raise OSError(f"skill directory could not be inspected: {exc}") from exc

    for directory, child_directories, files in os.walk(
        root,
        topdown=True,
        onerror=record_walk_error,
        followlinks=False,
    ):
        parent = Path(directory)
        retained: list[str] = []
        for child_name in sorted(child_directories):
            child = parent / child_name
            relative = child.relative_to(root).as_posix()
            lowered = child_name.casefold()
            if lowered in cache_names or lowered.endswith(".egg-info"):
                targets.append((child, "generated cache directory", relative))
                continue
            retained.append(child_name)
        child_directories[:] = retained
        for file_name in sorted(files):
            label = classify_generated_noise_file(file_name)
            if label is None:
                continue
            path = parent / file_name
            relative = path.relative_to(root).as_posix()
            targets.append((path, label, relative))
    return targets


def clean_package_hygiene(root: Path) -> list[str]:
    """Remove known generated dirt. Returns relative paths that were removed."""
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"skill root is not a directory: {root}")

    targets = iter_package_hygiene_targets(root)
    # Remove files first, then directories deepest-first.
    files = [item for item in targets if item[0].is_file()]
    dirs = [item for item in targets if item[0].is_dir()]
    dirs.sort(key=lambda item: len(item[0].parts), reverse=True)

    removed: list[str] = []
    for path, _kind, relative in files + dirs:
        if is_reparse_point(path):
            # Never delete through reparse points / symlinks.
            continue
        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists() or path.is_symlink():
                path.unlink()
            else:
                continue
        except OSError:
            continue
        if not path.exists():
            removed.append(relative)
    return removed


def validate_directory_hygiene(root: Path, result: Validation) -> None:
    ignored_dir_names = {name.casefold() for name in VALIDATION_IGNORED_DIRS}
    if root.name.casefold() in ignored_dir_names:
        result.errors.append(
            f"generated cache directory is not allowed in the skill package: {root.name}"
        )

    try:
        targets = iter_package_hygiene_targets(root)
    except OSError as exc:
        result.errors.append(str(exc))
        targets = []

    for _path, kind, relative in targets:
        result.errors.append(f"{kind} is not allowed in the skill package: {relative}")

    scanned_names = tuple(dict.fromkeys((*ROOT_SHADOW_DOCUMENTS, *ROOT_ALLOWED_LANDING_DOCUMENTS)))
    allowed_root_names = {name.casefold() for name in ROOT_ALLOWED_LANDING_DOCUMENTS}
    for name in scanned_names:
        for path in sorted(root.rglob(name)):
            if is_validation_ignored(path):
                continue
            relative = path.relative_to(root).as_posix()
            if path.parent == root:
                if name.casefold() in allowed_root_names:
                    continue
                result.errors.append(
                    f"root shadow document duplicates SKILL.md or references: {name}"
                )
            else:
                result.errors.append(
                    f"auxiliary skill document is not allowed: {relative}"
                )


def is_reparse_point(path: Path) -> bool:
    try:
        attributes = getattr(os.lstat(path), "st_file_attributes", 0)
    except OSError:
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    return path.is_symlink() or bool(reparse_flag and attributes & reparse_flag)


def is_validation_ignored(path: Path) -> bool:
    ignored = {name.casefold() for name in VALIDATION_IGNORED_DIRS}
    return any(part.casefold() in ignored for part in path.parts)


def validate_python(root: Path, result: Validation) -> None:
    scripts_root = root / "scripts"
    script_paths = sorted(scripts_root.rglob("*.py")) if scripts_root.is_dir() else []
    result.require(bool(script_paths), "scripts directory must contain Python files")
    paths = sorted(
        path
        for path in root.rglob("*.py")
        if not is_validation_ignored(path)
    )
    canonical_root = root.resolve()
    for path in paths:
        relative = path.relative_to(root).as_posix()
        if is_reparse_point(path):
            result.errors.append(f"unsafe Python validation path: {relative}")
            continue
        try:
            canonical_path = path.resolve(strict=True)
        except OSError as exc:
            result.errors.append(f"Python validation path could not be resolved: {relative}: {exc}")
            continue
        if not is_relative_to(canonical_path, canonical_root):
            result.errors.append(f"Python validation path escapes skill root: {relative}")
            continue
        try:
            ast.parse(read_text(path), filename=str(path), feature_version=(3, 9))
        except SyntaxError as exc:
            result.errors.append(f"Python 3.9 syntax error in {relative}: {exc}")


def normalized_absolute_path(path: Path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def validate_trusted_self_test_root(root: Path, result: Validation) -> Path | None:
    if normalized_absolute_path(root) != normalized_absolute_path(TRUSTED_SKILL_ROOT):
        result.errors.append(
            "trusted self-tests may run only from the validator's reviewed trusted skill root"
        )
        return None

    try:
        canonical_root = root.resolve(strict=True)
        canonical_trusted_root = TRUSTED_SKILL_ROOT.resolve(strict=True)
    except OSError as exc:
        result.errors.append(f"trusted skill root could not be resolved: {exc}")
        return None
    if canonical_root != canonical_trusted_root:
        result.errors.append(
            "trusted self-tests may run only from the validator's reviewed trusted skill root"
        )
        return None
    for path in (root, root / "scripts"):
        if is_reparse_point(path):
            result.errors.append(
                f"unsafe trusted self-test root path: {path.relative_to(root.parent)}"
            )
            return None
    return canonical_root


def validate_trusted_self_test_tree(
    root: Path,
    canonical_root: Path,
    result: Validation,
) -> bool:
    stack = [root / "scripts"]
    valid = True
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0)
    self_test_entries = {
        f"scripts/{script_name}" for script_name, _marker in SCRIPT_SELF_TESTS
    }

    while stack:
        directory = stack.pop()
        try:
            with os.scandir(directory) as entries:
                children = list(entries)
        except OSError as exc:
            relative = directory.relative_to(root).as_posix()
            result.errors.append(
                f"trusted self-test dependency directory could not be read: "
                f"{relative}: {exc}"
            )
            valid = False
            continue

        for entry in children:
            path = Path(entry.path)
            relative = path.relative_to(root).as_posix()
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as exc:
                result.errors.append(
                    f"trusted self-test dependency path could not be inspected: "
                    f"{relative}: {exc}"
                )
                valid = False
                continue

            is_reparse = (
                stat.S_ISLNK(metadata.st_mode)
                or bool(
                    reparse_flag
                    and getattr(metadata, "st_file_attributes", 0) & reparse_flag
                )
                or is_reparse_point(path)
            )
            if is_reparse:
                if relative in self_test_entries:
                    result.errors.append(f"unsafe self-test path: {relative}")
                else:
                    result.errors.append(
                        f"unsafe trusted self-test dependency path: {relative}"
                    )
                valid = False
                continue

            if not stat.S_ISDIR(metadata.st_mode) and not stat.S_ISREG(metadata.st_mode):
                result.errors.append(
                    f"unsafe trusted self-test dependency file type: {relative}"
                )
                valid = False
                continue
            if stat.S_ISREG(metadata.st_mode) and metadata.st_nlink > 1:
                result.errors.append(
                    f"unsafe hard-linked trusted self-test dependency: {relative}"
                )
                valid = False
                continue

            try:
                canonical_path = path.resolve(strict=True)
            except OSError as exc:
                result.errors.append(
                    f"trusted self-test dependency path could not be resolved: "
                    f"{relative}: {exc}"
                )
                valid = False
                continue
            if not is_relative_to(canonical_path, canonical_root):
                result.errors.append(
                    f"trusted self-test dependency path escapes skill root: {relative}"
                )
                valid = False
                continue
            if stat.S_ISDIR(metadata.st_mode):
                stack.append(path)

    return valid


def windows_system_executable(name: str) -> Path | None:
    if os.name != "nt":
        return None
    try:
        import ctypes

        buffer = ctypes.create_unicode_buffer(32768)
        length = ctypes.windll.kernel32.GetSystemDirectoryW(buffer, len(buffer))
    except (AttributeError, OSError):
        return None
    if length <= 0 or length >= len(buffer):
        return None
    candidate = Path(buffer.value) / name
    if not candidate.is_file() or is_reparse_point(candidate):
        return None
    return candidate


def terminate_process_tree(process: subprocess.Popen[bytes]) -> None:
    if os.name == "nt":
        taskkill = windows_system_executable("taskkill.exe")
        if taskkill is not None:
            try:
                subprocess.run(
                    [str(taskkill), "/PID", str(process.pid), "/T", "/F"],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5,
                    check=False,
                )
            except (OSError, subprocess.TimeoutExpired):
                pass
    else:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass

    if process.poll() is None:
        try:
            process.kill()
        except OSError:
            pass


def run_self_test_process(
    command: list[str],
    *,
    root: Path,
    child_env: dict[str, str],
) -> subprocess.CompletedProcess[str]:
    creationflags = 0
    if os.name == "nt":
        creationflags = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)

    with (
        tempfile.TemporaryFile(mode="w+b") as stdout_file,
        tempfile.TemporaryFile(mode="w+b") as stderr_file,
    ):
        process = subprocess.Popen(
            command,
            cwd=root,
            stdin=subprocess.DEVNULL,
            stdout=stdout_file,
            stderr=stderr_file,
            env=child_env,
            creationflags=creationflags,
            start_new_session=os.name != "nt",
        )
        try:
            returncode = process.wait(timeout=SCRIPT_SELF_TEST_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            terminate_process_tree(process)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                terminate_process_tree(process)
            raise

        stdout_file.seek(0)
        stderr_file.seek(0)
        stdout = stdout_file.read(MAX_SELF_TEST_OUTPUT_BYTES + 1)
        stderr = stderr_file.read(MAX_SELF_TEST_OUTPUT_BYTES + 1)
        if len(stdout) > MAX_SELF_TEST_OUTPUT_BYTES:
            stdout = stdout[:MAX_SELF_TEST_OUTPUT_BYTES] + b"\n[stdout truncated]\n"
        if len(stderr) > MAX_SELF_TEST_OUTPUT_BYTES:
            stderr = stderr[:MAX_SELF_TEST_OUTPUT_BYTES] + b"\n[stderr truncated]\n"
        return subprocess.CompletedProcess(
            command,
            returncode,
            stdout.decode("utf-8", errors="replace"),
            stderr.decode("utf-8", errors="replace"),
        )


def validate_script_self_tests(root: Path, result: Validation) -> None:
    """Run self-tests from a root the caller has explicitly marked as trusted."""

    canonical_root = validate_trusted_self_test_root(root, result)
    if canonical_root is None:
        return
    if not validate_trusted_self_test_tree(root, canonical_root, result):
        return

    scripts_dir = root / "scripts"
    child_env = {
        name: os.environ[name]
        for name in SELF_TEST_ENV_ALLOWLIST
        if name in os.environ
    }
    child_env.update(
        {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUTF8": "1",
        }
    )
    for script_name, marker in SCRIPT_SELF_TESTS:
        script_path = scripts_dir / script_name
        if is_reparse_point(script_path):
            result.errors.append(f"unsafe self-test path: scripts/{script_name}")
            continue
        if not script_path.is_file():
            result.errors.append(f"missing self-test script: scripts/{script_name}")
            continue
        try:
            canonical_script = script_path.resolve(strict=True)
        except OSError as exc:
            result.errors.append(
                f"self-test path could not be resolved: scripts/{script_name}: {exc}"
            )
            continue
        if not is_relative_to(canonical_script, canonical_root):
            result.errors.append(f"unsafe self-test path: scripts/{script_name}")
            continue

        try:
            completed = run_self_test_process(
                [sys.executable, "-I", "-B", str(script_path), "--self-test"],
                root=root,
                child_env=child_env,
            )
        except subprocess.TimeoutExpired:
            result.errors.append(
                f"self-test timed out after {SCRIPT_SELF_TEST_TIMEOUT_SECONDS}s: "
                f"scripts/{script_name}"
            )
            continue
        except OSError as exc:
            result.errors.append(
                f"self-test could not start: scripts/{script_name}: {exc}"
            )
            continue

        output = f"{completed.stdout}\n{completed.stderr}"
        marker_seen = any(
            line == marker or line.startswith(f"{marker} ")
            for line in (candidate.strip() for candidate in output.splitlines())
        )
        if completed.returncode != 0:
            result.errors.append(
                f"self-test exited with code {completed.returncode}: "
                f"scripts/{script_name}"
            )
        if not marker_seen:
            result.errors.append(
                f"self-test marker missing for scripts/{script_name}: {marker}"
            )


def validate_suite(root: Path, result: Validation) -> None:
    suite_path = root / "references" / "official-self-test-task-suite.md"
    if not suite_path.is_file():
        result.errors.append(f"missing official self-test suite: {suite_path}")
        return

    suite_text = read_text(suite_path)
    validate_official_suite_contract(suite_text, result)
    cases = parse_self_test_suite(suite_text)
    tasks = {case.heading for case in cases}
    expected_tasks = (
        LIFECYCLE_TASKS
        | SECOND_PASS_TASKS
        | PRACTICE_TASKS
        | WEBSKILLS_FUSION_TASKS
        | CLAUDE_PROJECT_FUSION_TASKS
    )
    result.require(
        len(cases) == len(tasks),
        "official self-test suite contains duplicate task headings",
    )
    result.require(
        len(cases) == len(TASK_HEADING_RE.findall(suite_text)),
        "one or more official tasks could not be parsed structurally",
    )
    missing_lifecycle_tasks = sorted(expected_tasks - tasks)
    result.require(
        not missing_lifecycle_tasks,
        f"official self-test suite is missing required tasks: {missing_lifecycle_tasks}",
    )
    normalized_prompts: set[str] = set()
    for case in cases:
        result.require(bool(case.prompt), f"official task has no prompt: {case.heading}")
        result.require(bool(case.routes), f"official task has no expected route: {case.heading}")
        result.require(bool(case.conclusions), f"official task has no required conclusions: {case.heading}")
        validate_claude_project_fusion_case(case, result)
        normalized_prompt = " ".join(case.prompt.lower().split())
        result.require(
            normalized_prompt not in normalized_prompts,
            f"official task prompt is duplicated: {case.heading}",
        )
        normalized_prompts.add(normalized_prompt)
        for route in case.routes:
            result.require((root / route).is_file(), f"official task route is broken: {case.heading}: {route}")


def ast_dotted_name(node: ast.AST) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts)) if parts else ""


def validate_forward_testing_contract(
    root: Path,
    skill_text: str,
    result: Validation,
) -> None:
    playbook_path = root / "references" / "forward-testing-playbook.md"
    maintenance_path = root / "references" / "skill-maintenance.md"
    script_path = root / "scripts" / "forward_test_report.py"
    for label, path in (
        ("forward-testing playbook", playbook_path),
        ("skill-maintenance reference", maintenance_path),
        ("forward-test report validator", script_path),
    ):
        result.require(path.is_file(), f"missing {label}: {path.relative_to(root)}")
    if not all(path.is_file() for path in (playbook_path, maintenance_path, script_path)):
        return

    playbook_text = read_text(playbook_path)
    maintenance_text = read_text(maintenance_path)
    script_text = read_text(script_path)
    playbook_lower = playbook_text.lower()
    maintenance_lower = maintenance_text.lower()

    result.require(
        "references/forward-testing-playbook.md" in skill_text,
        "forward-testing-playbook.md must be directly routed from SKILL.md",
    )
    result.require(
        "scripts/forward_test_report.py" in skill_text,
        "forward_test_report.py must be directly routed from SKILL.md",
    )
    result.require(
        "scripts/forward_test_report.py" in playbook_text
        and "does not invoke a model" in playbook_lower
        and "arbitrary command" in playbook_lower,
        "forward-testing playbook must keep report validation read-only and model-independent",
    )
    result.require(
        all(marker in playbook_lower for marker in ("fresh_context", "independent", "smoke", "full", "160", "full_pass")),
        "forward-testing playbook must distinguish fresh independent smoke and full evidence",
    )
    result.require(
        all(marker in playbook_lower for marker in ("report directory", "symlink", "reparse point", "hard link")),
        "forward-testing playbook must retain response-artifact containment rules",
    )
    result.require(
        "static `validation=pass`" in maintenance_lower
        and "behavioral claims require" in maintenance_lower
        and "scripts/forward_test_report.py" in maintenance_text,
        "skill maintenance must distinguish static PASS from forward-test evidence",
    )
    result.require(
        ("forward_test_report.py", "forward_test_report_self_test=PASS")
        in SCRIPT_SELF_TESTS,
        "forward-test report validator must remain in trusted script self-tests",
    )

    try:
        tree = ast.parse(script_text, filename=str(script_path), feature_version=(3, 9))
    except SyntaxError:
        return
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots = {alias.name.split(".", 1)[0] for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported_roots = {node.module.split(".", 1)[0]} if node.module else set()
        else:
            imported_roots = set()
        banned_imports = sorted(imported_roots & FORWARD_TEST_BANNED_IMPORT_ROOTS)
        result.require(
            not banned_imports,
            f"forward-test report validator imports execution/network modules: {banned_imports}",
        )
        if isinstance(node, ast.Call):
            call_name = ast_dotted_name(node.func)
            result.require(
                call_name not in FORWARD_TEST_BANNED_CALLS,
                f"forward-test report validator contains a forbidden call: {call_name}",
            )

    for marker in (
        "def validate_report",
        "official_suite_contract_digest",
        "parse_self_test_suite",
        "bounded_sha256",
        "full_pass",
        "--self-test",
    ):
        result.require(
            marker in script_text,
            f"forward-test report validator is missing contract marker: {marker}",
        )


def export_tests(root: Path, output_path: Path) -> None:
    suite_text = read_text(root / "references" / "official-self-test-task-suite.md")
    payload = [
        {
            "heading": case.heading,
            "prompt": case.prompt,
            "expected_routes": list(case.routes),
            "must_conclude": list(case.conclusions),
        }
        for case in parse_self_test_suite(suite_text)
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def is_relative_to(path: Path, parent: Path) -> bool:
    try:
        path.relative_to(parent)
    except ValueError:
        return False
    return True


def validate_root(
    root: Path,
    result: Validation,
    *,
    legacy: bool = False,
    run_trusted_self_tests: bool = False,
) -> None:
    skill_path = root / "SKILL.md"
    result.require(skill_path.is_file(), f"missing SKILL.md: {skill_path}")

    if skill_path.is_file():
        skill_text = read_text(skill_path)
        validate_frontmatter(skill_text, result)
        validate_behavior(skill_text, result)
        validate_lifecycle(root, result)
        validate_intake_tools_and_reporting(root, result)
        validate_references(root, skill_text, result)
        validate_reference_contents(root, result)
        validate_profile_routes(root, result)
        validate_entry_size(skill_text, result, legacy=legacy)
        validate_forward_testing_contract(root, skill_text, result)

    validate_python(root, result)
    validate_directory_hygiene(root, result)
    if run_trusted_self_tests:
        validate_script_self_tests(root, result)
    validate_suite(root, result)


def compare_with_baseline(root: Path, baseline: Path, result: Validation) -> None:
    baseline_tasks = task_headings(baseline)
    candidate_tasks = task_headings(root)
    missing_tasks = sorted(baseline_tasks - candidate_tasks)
    result.require(not missing_tasks, f"official self-test tasks removed: {missing_tasks}")

    baseline_refs = {path.name: path for path in (baseline / "references").glob("*.md")}
    candidate_refs = {path.name: path for path in (root / "references").glob("*.md")}
    result.require(
        set(baseline_refs) == set(candidate_refs),
        "reference file set differs from the baseline",
    )
    for name, baseline_path in baseline_refs.items():
        candidate_path = candidate_refs.get(name)
        if candidate_path is None:
            continue
        result.require(
            sha256(baseline_path) == sha256(candidate_path),
            f"specialist reference changed during conservative optimization: references/{name}",
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        default=str(Path(__file__).resolve().parents[1]),
        help="Spider King skill directory",
    )
    parser.add_argument("--baseline", help="Original skill directory used for preservation checks")
    parser.add_argument(
        "--legacy",
        action="store_true",
        help="Validate legacy behavior without enforcing the new entry-size budget",
    )
    parser.add_argument(
        "--export-tests",
        help="Write the parsed suite to JSON outside the skill directory after validation passes",
    )
    parser.add_argument(
        "--run-trusted-self-tests",
        action="store_true",
        help=(
            "Execute candidate Python self-tests. Use only for a trusted current root; "
            "the subprocesses are isolated from user site packages and secret-like environment variables, "
            "but are not an operating-system sandbox."
        ),
    )
    parser.add_argument(
        "--clean-hygiene",
        action="store_true",
        help=(
            "Remove known generated cache/noise files from the skill package before validation. "
            "Only matches package-dirt patterns; does not delete source or references."
        ),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    root = Path(args.root).absolute()
    result = Validation()
    # Keep both this process and trusted self-test children from dirtying the package.
    sys.dont_write_bytecode = True
    os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
    try:
        if args.clean_hygiene:
            removed = clean_package_hygiene(root)
            for relative in removed:
                print(f"cleaned={relative}")
            print(f"cleaned_count={len(removed)}")
        validate_root(
            root,
            result,
            legacy=args.legacy,
            run_trusted_self_tests=args.run_trusted_self_tests,
        )

        if args.baseline:
            compare_with_baseline(root, Path(args.baseline).resolve(), result)
    except (OSError, UnicodeError, ValueError) as exc:
        result.errors.append(f"validation input rejected: {exc}")

    print(f"root={root}")
    for warning in result.warnings:
        print(f"WARN: {warning}")
    for error in result.errors:
        print(f"ERROR: {error}")
    print(f"warnings={len(result.warnings)} errors={len(result.errors)}")
    if result.errors:
        return 1
    if args.export_tests:
        export_path = Path(args.export_tests).resolve()
        if is_relative_to(export_path, root):
            print("ERROR: --export-tests must point outside the skill directory")
            return 1
        try:
            export_tests(root, export_path)
        except (OSError, UnicodeError, ValueError) as exc:
            print(f"ERROR: could not export tests: {exc}")
            return 1
        else:
            print(f"exported_tests={export_path}")
    print("validation=PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
