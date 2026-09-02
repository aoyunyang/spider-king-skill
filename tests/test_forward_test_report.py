from __future__ import annotations

import hashlib
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import forward_test_report  # noqa: E402
import validate_skill  # noqa: E402


class ForwardTestReportValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.suite_text = (
            ROOT / "references" / "official-self-test-task-suite.md"
        ).read_text(encoding="utf-8")
        cls.cases = validate_skill.parse_self_test_suite(cls.suite_text)
        cls.suite_digest = validate_skill.official_suite_contract_digest(
            cls.suite_text
        )
        cls.contract = forward_test_report.current_contract(skill_root=ROOT)

    @staticmethod
    def build_checks(
        expected_values: Iterable[str],
        response_text: str,
        *,
        kind: str,
    ) -> list[dict[str, Any]]:
        checks: list[dict[str, Any]] = []
        cursor = 0
        for expected in expected_values:
            start = response_text.find(expected, cursor)
            if start < 0:
                raise AssertionError(f"missing expected {kind}: {expected}")
            line_start = response_text.rfind("\n", 0, start) + 1
            line_end = response_text.find("\n", start + len(expected))
            if line_end < 0:
                line_end = len(response_text)
            quote = response_text[line_start:line_end]
            checks.append(
                {
                    "expected": expected,
                    "passed": True,
                    "rationale": (
                        f"Independent reviewer confirms this expected {kind} "
                        "from the cited response span."
                    ),
                    "evidence": [
                        {"quote": quote, "start": line_start, "end": line_end}
                    ],
                }
            )
            cursor = line_end + 1
        return checks

    def build_report(
        self,
        directory: str,
        cases: Iterable[validate_skill.SelfTestCase],
        *,
        scope: str = "smoke",
    ) -> tuple[Path, dict[str, Any], list[Path]]:
        report_directory = Path(directory)
        response_directory = report_directory / "responses"
        response_directory.mkdir()
        items: list[dict[str, Any]] = []
        response_paths: list[Path] = []
        selected_cases = list(cases)

        for index, case in enumerate(selected_cases):
            response_text = "\n".join((*case.routes, *case.conclusions)) + "\n"
            response_path = response_directory / f"task-{index:03d}.md"
            response_path.write_bytes(response_text.encode("utf-8"))
            response_paths.append(response_path)
            items.append(
                {
                    "heading": case.heading,
                    "prompt_sha256": hashlib.sha256(
                        case.prompt.encode("utf-8")
                    ).hexdigest(),
                    "response": {
                        "path": response_path.relative_to(report_directory).as_posix(),
                        "sha256": validate_skill.sha256(response_path),
                    },
                    "review": {
                        "passed": True,
                        "reviewer_id": "independent-reviewer",
                        "routes": self.build_checks(
                            case.routes,
                            response_text,
                            kind="route",
                        ),
                        "conclusions": self.build_checks(
                            case.conclusions,
                            response_text,
                            kind="conclusion",
                        ),
                    },
                }
            )

        report: dict[str, Any] = {
            "schema_version": 1,
            "scope": {"kind": scope, "task_count": len(items)},
            "suite": {
                "path": "references/official-self-test-task-suite.md",
                "contract_sha256": self.suite_digest,
                "task_count": len(self.cases),
            },
            "skill": {
                "path": "SKILL.md",
                "sha256": validate_skill.sha256(ROOT / "SKILL.md"),
                "package_sha256": self.contract["skill"]["package_sha256"],
            },
            "runner": {
                "id": "fresh-runner",
                "fresh_context": True,
                "independent": True,
            },
            "reviewer": {
                "id": "independent-reviewer",
                "fresh_context": True,
                "independent": True,
            },
            "items": items,
        }
        report_path = report_directory / "forward-test-report.json"
        self.write_report(report_path, report)
        return report_path, report, response_paths

    @staticmethod
    def write_report(path: Path, report: dict[str, Any]) -> None:
        path.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def validate(self, path: Path) -> dict[str, Any]:
        return forward_test_report.validate_report(path, skill_root=ROOT)

    def test_accepts_smoke_report_without_executing_report_content(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            sentinel = Path(directory) / "report-command-ran.txt"
            report["command"] = [
                sys.executable,
                "-c",
                f"from pathlib import Path; Path({str(sentinel)!r}).write_text('ran')",
            ]
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertTrue(result["valid"], result["errors"])
            self.assertFalse(result["full_pass"])
            self.assertFalse(sentinel.exists())

    def test_accepts_full_report_only_with_all_official_tasks(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, _report, _responses = self.build_report(
                directory,
                self.cases,
                scope="full",
            )

            result = self.validate(report_path)

            self.assertTrue(result["valid"], result["errors"])
            self.assertTrue(result["full_pass"])
            self.assertEqual(result["reported_items"], 160)

    def test_rejects_partial_full_scope_and_full_pass_claim(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory,
                self.cases[:1],
                scope="full",
            )
            report["full_pass"] = True
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertFalse(result["full_pass"])
            self.assertTrue(
                any("full scope requires all 160" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_stale_skill_and_response_hashes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            report["skill"]["sha256"] = "0" * 64
            report["items"][0]["response"]["sha256"] = "f" * 64
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("does not match the current SKILL.md" in error for error in result["errors"]),
                result["errors"],
            )
            self.assertTrue(
                any("does not match the response file" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_evidence_not_present_in_original_response(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            evidence = report["items"][0]["review"]["routes"][0]["evidence"][0]
            evidence["quote"] = "not-present-in-the-response"
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("quote does not match" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_runner_reviewer_identity_reuse(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            report["reviewer"]["id"] = "FRESH-RUNNER"
            report["items"][0]["review"]["reviewer_id"] = "FRESH-RUNNER"
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("different agents" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_item_without_independent_reviewer_binding(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            del report["items"][0]["review"]["reviewer_id"]
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("reviewer_id must match reviewer.id" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_response_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:1]
            )
            report["items"][0]["response"]["path"] = "../outside.md"
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("must not contain '..'" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_duplicate_response_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, report, _responses = self.build_report(
                directory, self.cases[:2]
            )
            report["items"][1]["response"] = dict(report["items"][0]["response"])
            self.write_report(report_path, report)

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("distinct physical file" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_hard_linked_response(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, _report, responses = self.build_report(
                directory, self.cases[:1]
            )
            hard_link = Path(directory) / "response-hard-link.md"
            try:
                os.link(responses[0], hard_link)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"hard links unavailable: {exc}")

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("hard-linked" in error for error in result["errors"]),
                result["errors"],
            )

    def test_rejects_symlinked_response(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            report_path, _report, responses = self.build_report(
                directory, self.cases[:1]
            )
            response_path = responses[0]
            target = Path(directory) / "real-response.md"
            response_path.replace(target)
            try:
                response_path.symlink_to(target)
            except OSError as exc:
                target.replace(response_path)
                self.skipTest(f"symlinks unavailable: {exc}")

            result = self.validate(report_path)

            self.assertFalse(result["valid"])
            self.assertTrue(
                any("symlink or reparse-point" in error for error in result["errors"]),
                result["errors"],
            )


if __name__ == "__main__":
    unittest.main()
