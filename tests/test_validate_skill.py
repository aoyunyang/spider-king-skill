from __future__ import annotations

import re
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import validate_skill  # noqa: E402


class ScriptSelfTestValidationTests(unittest.TestCase):
    def make_root(self, directory: str, overrides: dict[str, str] | None = None) -> Path:
        root = Path(directory)
        scripts = root / "scripts"
        scripts.mkdir()
        overrides = overrides or {}
        for script_name, marker in validate_skill.SCRIPT_SELF_TESTS:
            source = overrides.get(script_name, f"print({marker!r})\n")
            (scripts / script_name).write_text(source, encoding="utf-8")
        return root

    def run_trusted(self, root: Path, result: validate_skill.Validation) -> None:
        with mock.patch.object(validate_skill, "TRUSTED_SKILL_ROOT", root.resolve()):
            validate_skill.validate_script_self_tests(root, result)

    def test_accepts_all_expected_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            result = validate_skill.Validation()

            self.run_trusted(root, result)

            self.assertEqual(result.errors, [])

    def test_candidate_execution_is_disabled_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "candidate-code-ran.txt"
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "from pathlib import Path\n"
                        f"Path({str(sentinel)!r}).write_text('ran', encoding='utf-8')\n"
                        "print('self_test=PASS')\n"
                    )
                },
            )
            result = validate_skill.Validation()

            validate_skill.validate_root(root, result)

            self.assertFalse(sentinel.exists())

    def test_parser_requires_explicit_trusted_self_test_flag(self) -> None:
        args = validate_skill.build_parser().parse_args([])

        self.assertFalse(args.run_trusted_self_tests)

    def test_trusted_self_tests_do_not_inherit_arbitrary_environment(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "import os\n"
                        "if os.environ.get('SPIDER_TEST_SECRET'):\n"
                        "    raise SystemExit(9)\n"
                        "print('self_test=PASS')\n"
                    )
                },
            )
            result = validate_skill.Validation()

            with mock.patch.dict("os.environ", {"SPIDER_TEST_SECRET": "do-not-copy"}):
                self.run_trusted(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_missing_marker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(
                directory,
                {
                    "transcript_diff.py": (
                        "print('not-transcript_diff_self_test=PASS')\n"
                    )
                },
            )
            result = validate_skill.Validation()

            self.run_trusted(root, result)

            self.assertTrue(
                any("marker missing" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_nonzero_exit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(
                directory,
                {"practice_lab.py": "raise SystemExit(7)\n"},
            )
            result = validate_skill.Validation()

            self.run_trusted(root, result)

            self.assertTrue(
                any("exited with code 7" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_missing_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            (root / "scripts" / "evidence_normalizer.py").unlink()
            result = validate_skill.Validation()

            self.run_trusted(root, result)

            self.assertTrue(
                any("missing self-test script" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_execution_from_an_unreviewed_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            sentinel = Path(directory) / "candidate-code-ran.txt"
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "from pathlib import Path\n"
                        f"Path({str(sentinel)!r}).write_text('ran', encoding='utf-8')\n"
                        "print('self_test=PASS')\n"
                    )
                },
            )
            result = validate_skill.Validation()

            validate_skill.validate_script_self_tests(root, result)

            self.assertFalse(sentinel.exists())
            self.assertTrue(
                any("trusted skill root" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_symlinked_self_test_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            script = root / "scripts" / "evidence_normalizer.py"
            external = root.parent / f"{root.name}-external-self-test.py"
            script.unlink()
            external.write_text("print('self_test=PASS')\n", encoding="utf-8")
            try:
                script.symlink_to(external)
            except OSError as exc:
                external.unlink(missing_ok=True)
                self.skipTest(f"symlinks unavailable: {exc}")
            result = validate_skill.Validation()
            try:
                self.run_trusted(root, result)
            finally:
                external.unlink(missing_ok=True)

            self.assertTrue(
                any("unsafe self-test path" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_symlinked_self_test_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "import _bounded_input\n"
                        "print('self_test=PASS')\n"
                    )
                },
            )
            sentinel = root / "dependency-code-ran.txt"
            dependency = root / "scripts" / "_bounded_input.py"
            external = root.parent / f"{root.name}-external-dependency.py"
            external.write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('ran', encoding='utf-8')\n",
                encoding="utf-8",
            )
            try:
                dependency.symlink_to(external)
            except OSError as exc:
                external.unlink(missing_ok=True)
                self.skipTest(f"symlinks unavailable: {exc}")
            result = validate_skill.Validation()
            try:
                self.run_trusted(root, result)
            finally:
                external.unlink(missing_ok=True)

            self.assertFalse(sentinel.exists())
            self.assertTrue(
                any(
                    "unsafe trusted self-test dependency path" in error
                    for error in result.errors
                ),
                result.errors,
            )

    def test_rejects_mocked_reparse_point_self_test_dependency(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "import _bounded_input\n"
                        "print('self_test=PASS')\n"
                    )
                },
            )
            sentinel = root / "dependency-code-ran.txt"
            dependency = root / "scripts" / "_bounded_input.py"
            dependency.write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('ran', encoding='utf-8')\n",
                encoding="utf-8",
            )
            result = validate_skill.Validation()

            with mock.patch.object(
                validate_skill,
                "is_reparse_point",
                side_effect=lambda path: path == dependency,
            ):
                self.run_trusted(root, result)

            self.assertFalse(sentinel.exists())
            self.assertTrue(
                any(
                    "unsafe trusted self-test dependency path" in error
                    for error in result.errors
                ),
                result.errors,
            )

    def test_rejects_reparse_point_self_test_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            target = root / "scripts" / "evidence_normalizer.py"
            result = validate_skill.Validation()

            with (
                mock.patch.object(validate_skill, "TRUSTED_SKILL_ROOT", root.resolve()),
                mock.patch.object(
                    validate_skill,
                    "is_reparse_point",
                    side_effect=lambda path: path == target,
                ),
            ):
                validate_skill.validate_script_self_tests(root, result)

            self.assertTrue(
                any("unsafe self-test path" in error for error in result.errors),
                result.errors,
            )

    def test_timeout_terminates_descendants_holding_output_pipes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "escaped-child.txt"
            child_code = (
                "import pathlib,time; time.sleep(2.0); "
                f"pathlib.Path({str(marker)!r}).write_text('escaped', encoding='utf-8')"
            )
            root = self.make_root(
                directory,
                {
                    "evidence_normalizer.py": (
                        "import subprocess,sys,time\n"
                        f"subprocess.Popen([sys.executable, '-c', {child_code!r}])\n"
                        "time.sleep(30)\n"
                    )
                },
            )
            result = validate_skill.Validation()

            started = time.monotonic()
            with (
                mock.patch.object(
                    validate_skill,
                    "SCRIPT_SELF_TEST_TIMEOUT_SECONDS",
                    0.2,
                ),
                mock.patch.object(
                    validate_skill,
                    "SCRIPT_SELF_TESTS",
                    (("evidence_normalizer.py", "self_test=PASS"),),
                ),
            ):
                self.run_trusted(root, result)
            elapsed = time.monotonic() - started
            time.sleep(2.2)

            self.assertLess(elapsed, 3.0)
            self.assertFalse(marker.exists())
            self.assertTrue(
                any("self-test timed out" in error for error in result.errors),
                result.errors,
            )


class ProfileRouteValidationTests(unittest.TestCase):
    def make_profile(
        self,
        directory: str,
        index_text: str,
        *,
        references: tuple[str, ...] = (),
        scripts: tuple[str, ...] = (),
    ) -> Path:
        root = Path(directory)
        (root / "references").mkdir(parents=True)
        (root / "references" / "workflow-overview.md").write_text(
            "# Workflow\n",
            encoding="utf-8",
        )
        profile = root / "references" / "profiles" / "sample"
        profile.mkdir(parents=True)
        (profile / "index.md").write_text(index_text, encoding="utf-8")
        for name in references:
            path = profile / "references" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {name}\n", encoding="utf-8")
        for name in scripts:
            path = profile / "scripts" / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("// fixture\n", encoding="utf-8")
        return root

    def test_accepts_profile_local_and_skill_root_routes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(
                directory,
                "\n".join(
                    (
                        "`references/workflow-overview.md`",
                        "`references/network.md`",
                        "`scripts/hook.js`",
                    )
                ),
                references=("network.md",),
                scripts=("hook.js",),
            )
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_broken_profile_route(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(directory, "`references/missing.md`\n")
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertTrue(
                any("broken profile routed path" in error for error in result.errors),
                result.errors,
            )

    def test_ignores_routes_in_profile_tool_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(directory, "# Sample\n")
            cached = (
                root
                / "references"
                / "profiles"
                / "sample"
                / ".pytest_cache"
                / "cached.md"
            )
            cached.parent.mkdir(parents=True)
            cached.write_text("`references/missing.md`\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_unguarded_named_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(directory, "转 `future-js-reverse`。\n")
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertTrue(
                any("unguarded profile handoff" in error for error in result.errors),
                result.errors,
            )

    def test_accepts_capability_aware_named_handoff(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(
                directory,
                "capability snapshot 中 `future-js-reverse` 可用时转交；"
                "否则返回 Spider core loop。\n",
            )
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_unguarded_named_handoff_in_route_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(
                directory,
                "| Current goal | Route |\n"
                "|---|---|\n"
                "| Locate entry | `future-entry-skill` |\n",
            )
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertTrue(
                any("unguarded profile handoff" in error for error in result.errors),
                result.errors,
            )

    def test_accepts_local_tool_tokens_in_route_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(
                directory,
                "| Fallback | Tools |\n"
                "|---|---|\n"
                "| Browser evidence | `chrome-devtools` / `js-reverse` |\n",
            )
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_profile_package_without_test_script(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(directory, "# Sample\n")
            package = (
                root
                / "references"
                / "profiles"
                / "sample"
                / "package.json"
            )
            package.write_text('{"private": true}\n', encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertTrue(
                any("missing npm test" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_non_object_profile_package_without_crashing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_profile(directory, "# Sample\n")
            package = (
                root
                / "references"
                / "profiles"
                / "sample"
                / "package.json"
            )
            package.write_text("[]\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_profile_routes(root, result)

            self.assertTrue(
                any("must contain a JSON object" in error for error in result.errors),
                result.errors,
            )


class DirectoryHygieneValidationTests(unittest.TestCase):
    def test_validation_reads_are_bounded_and_utf8_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            oversized = Path(directory) / "oversized.md"
            invalid = Path(directory) / "invalid.md"
            oversized.write_bytes(b"1234")
            invalid.write_bytes(b"\xff")

            with mock.patch.object(validate_skill, "MAX_VALIDATION_FILE_BYTES", 3):
                with self.assertRaisesRegex(ValueError, "validation limit"):
                    validate_skill.read_text(oversized)
            with self.assertRaisesRegex(ValueError, "not valid UTF-8"):
                validate_skill.read_text(invalid)

    def test_accepts_skill_without_root_shadow_documents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(Path(directory), result)

            self.assertEqual(result.errors, [])

    def test_allows_root_github_landing_documents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Landing\n", encoding="utf-8")
            (root / "DISCLAIMER.md").write_text("# Legal\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            self.assertEqual(result.errors, [])

    def test_rejects_root_changelog_shadow_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CHANGELOG.md").write_text("# Duplicate\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            self.assertTrue(
                any("root shadow document" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_nested_readme_auxiliary_document(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            readme = root / "references" / "examples" / "README.md"
            readme.parent.mkdir(parents=True)
            readme.write_text("# Auxiliary\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            self.assertTrue(
                any("auxiliary skill document" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_tool_caches_without_duplicate_readme_errors(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for cache_name in validate_skill.VALIDATION_IGNORED_DIRS:
                readme = root / cache_name / "README.md"
                readme.parent.mkdir(parents=True)
                readme.write_text("# Generated cache metadata\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            cache_errors = [
                error
                for error in result.errors
                if "generated cache directory" in error
            ]
            self.assertEqual(len(cache_errors), len(validate_skill.VALIDATION_IGNORED_DIRS))
            for cache_name in validate_skill.VALIDATION_IGNORED_DIRS:
                self.assertTrue(
                    any(cache_name in error for error in cache_errors),
                    cache_errors,
                )
            self.assertFalse(
                any("auxiliary skill document" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_generated_test_runner_dumps(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tests = root / "tests"
            tests.mkdir()
            (tests / "_err_test_example.py.txt").write_text("boom\n", encoding="utf-8")
            (tests / "_out_test_example.py.txt").write_text("", encoding="utf-8")
            (tests / "keep_me.txt").write_text("ok\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            dump_errors = [
                error
                for error in result.errors
                if "generated test-runner dump" in error
            ]
            self.assertEqual(len(dump_errors), 2, result.errors)
            self.assertTrue(any("_err_test_example.py.txt" in error for error in dump_errors))
            self.assertTrue(any("_out_test_example.py.txt" in error for error in dump_errors))
            self.assertFalse(any("keep_me.txt" in error for error in result.errors), result.errors)

    def test_rejects_generated_local_noise_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "module.pyc").write_bytes(b"\0")
            (root / ".DS_Store").write_bytes(b"\0")
            (root / "notes.log").write_text("x\n", encoding="utf-8")
            (root / "keep.py").write_text("x = 1\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_directory_hygiene(root, result)

            noise_errors = [
                error
                for error in result.errors
                if "generated local noise file" in error
            ]
            self.assertEqual(len(noise_errors), 3, result.errors)
            self.assertFalse(any("keep.py" in error for error in result.errors), result.errors)

    def test_clean_package_hygiene_removes_known_dirt_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cache = root / "scripts" / "__pycache__"
            cache.mkdir(parents=True)
            (cache / "x.pyc").write_bytes(b"\0")
            dump = root / "tests" / "_err_test_example.py.txt"
            dump.parent.mkdir(parents=True)
            dump.write_text("boom\n", encoding="utf-8")
            keep = root / "tests" / "test_keep.py"
            keep.write_text("def test_ok():\n    assert True\n", encoding="utf-8")

            removed = validate_skill.clean_package_hygiene(root)

            self.assertTrue(any("__pycache__" in item for item in removed), removed)
            self.assertTrue(any("_err_test_example.py.txt" in item for item in removed), removed)
            self.assertFalse(cache.exists())
            self.assertFalse(dump.exists())
            self.assertTrue(keep.exists())
            result = validate_skill.Validation()
            validate_skill.validate_directory_hygiene(root, result)
            self.assertEqual(result.errors, [])


class OpenAIMetadataValidationTests(unittest.TestCase):
    valid_metadata = (
        "interface:\n"
        '  display_name: "Spider King"\n'
        '  short_description: "Protocol-first web reversal and Python delivery"\n'
        '  default_prompt: "Use $spider-king for sequential protocol analysis."\n'
        "policy:\n"
        "  allow_implicit_invocation: true\n"
    )

    def validate(self, text: str) -> validate_skill.Validation:
        result = validate_skill.Validation()
        validate_skill.validate_openai_metadata(text, result)
        return result

    def test_accepts_structured_openai_metadata(self) -> None:
        result = self.validate(self.valid_metadata)

        self.assertEqual(result.errors, [])

    def test_rejects_invalid_openai_yaml(self) -> None:
        result = self.validate("interface: [unterminated\n")

        self.assertTrue(
            any("invalid agents/openai.yaml" in error for error in result.errors),
            result.errors,
        )

    def test_rejects_missing_interface_mapping(self) -> None:
        result = self.validate("policy:\n  allow_implicit_invocation: true\n")

        self.assertTrue(
            any("interface mapping" in error for error in result.errors),
            result.errors,
        )

    def test_rejects_wrong_interface_field_type(self) -> None:
        text = self.valid_metadata.replace(
            '  short_description: "Protocol-first web reversal and Python delivery"',
            "  short_description: 42",
        )
        result = self.validate(text)

        self.assertTrue(
            any("short_description" in error for error in result.errors),
            result.errors,
        )

    def test_rejects_default_prompt_without_skill_token(self) -> None:
        text = self.valid_metadata.replace("$spider-king", "the skill")
        result = self.validate(text)

        self.assertTrue(
            any("must mention $spider-king" in error for error in result.errors),
            result.errors,
        )

    def test_rejects_non_boolean_implicit_invocation_policy(self) -> None:
        text = self.valid_metadata.replace(
            "  allow_implicit_invocation: true",
            '  allow_implicit_invocation: "true"',
        )
        result = self.validate(text)

        self.assertTrue(
            any("must be boolean" in error for error in result.errors),
            result.errors,
        )


class MarkerSemanticValidationTests(unittest.TestCase):
    def validate_markers(self, text: str, marker: str) -> validate_skill.Validation:
        result = validate_skill.Validation()
        validate_skill.require_marker_groups(
            text,
            ((marker,),),
            result,
            "positive contract",
        )
        return result

    def test_html_comment_does_not_satisfy_a_contract_marker(self) -> None:
        result = self.validate_markers(
            "<!-- capability snapshot -->\nNo contract remains.\n",
            "capability snapshot",
        )

        self.assertTrue(result.errors, result.errors)

    def test_direct_negation_does_not_satisfy_a_positive_contract(self) -> None:
        result = self.validate_markers(
            "DO NOT USE capability snapshot.\n",
            "capability snapshot",
        )

        self.assertTrue(result.errors, result.errors)

    def test_explicitly_negative_contract_marker_remains_valid(self) -> None:
        marker = "do not require this brief for `evidence`"
        result = self.validate_markers(f"- {marker}.\n", marker)

        self.assertEqual(result.errors, [])


class RecursivePythonValidationTests(unittest.TestCase):
    def make_root(self, directory: str) -> Path:
        root = Path(directory)
        (root / "scripts").mkdir()
        (root / "scripts" / "valid.py").write_text("value = 1\n", encoding="utf-8")
        return root

    def test_rejects_invalid_python_in_nested_tests(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            path = root / "tests" / "nested" / "broken.py"
            path.parent.mkdir(parents=True)
            path.write_text("def broken(:\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_python(root, result)

            self.assertTrue(
                any("tests/nested/broken.py" in error for error in result.errors),
                result.errors,
            )

    def test_rejects_invalid_python_in_distributed_examples(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            path = root / "references" / "examples" / "sample" / "broken.py"
            path.parent.mkdir(parents=True)
            path.write_text("def broken(:\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_python(root, result)

            self.assertTrue(
                any(
                    "references/examples/sample/broken.py" in error
                    for error in result.errors
                ),
                result.errors,
            )

    def test_rejects_invalid_python_in_profile_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            path = root / "references" / "profiles" / "sample" / "scripts" / "broken.py"
            path.parent.mkdir(parents=True)
            path.write_text("def broken(:\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_python(root, result)

            self.assertTrue(
                any(
                    "references/profiles/sample/scripts/broken.py" in error
                    for error in result.errors
                ),
                result.errors,
            )

    def test_ignores_invalid_python_in_tool_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            path = root / ".pytest_cache" / "broken.py"
            path.parent.mkdir(parents=True)
            path.write_text("def broken(:\n", encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_python(root, result)

            self.assertEqual(result.errors, [])

    def test_recursive_python_validation_never_executes_candidate_code(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            sentinel = root / "candidate-code-ran.txt"
            path = root / "references" / "examples" / "candidate.py"
            path.parent.mkdir(parents=True)
            path.write_text(
                "from pathlib import Path\n"
                f"Path({str(sentinel)!r}).write_text('ran', encoding='utf-8')\n",
                encoding="utf-8",
            )
            result = validate_skill.Validation()

            validate_skill.validate_python(root, result)

            self.assertEqual(result.errors, [])
            self.assertFalse(sentinel.exists())


class ReferenceContentsValidationTests(unittest.TestCase):
    def test_rejects_nested_long_markdown_without_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "references" / "nested" / "long.md"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join(["# Long"] + ["line"] * 100), encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_reference_contents(root, result)

            self.assertTrue(
                any("must retain a Contents section" in error for error in result.errors),
                result.errors,
            )

    def test_accepts_long_markdown_with_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "references" / "nested" / "long.md"
            path.parent.mkdir(parents=True)
            lines = ["# Long", "", "## Contents", "", "- [Topic](#topic)"]
            lines.extend(["line"] * 96)
            path.write_text("\n".join(lines), encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_reference_contents(root, result)

            self.assertEqual(result.errors, [])

    def test_exactly_one_hundred_lines_does_not_require_contents(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "references" / "short.md"
            path.parent.mkdir(parents=True)
            path.write_text("\n".join(["# Short"] + ["line"] * 99), encoding="utf-8")
            result = validate_skill.Validation()

            validate_skill.validate_reference_contents(root, result)

            self.assertEqual(result.errors, [])

    def test_ignores_long_markdown_in_tool_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            path = root / "references" / ".pytest_cache" / "generated.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "\n".join(["# Generated"] + ["line"] * 100),
                encoding="utf-8",
            )
            result = validate_skill.Validation()

            validate_skill.validate_reference_contents(root, result)

            self.assertEqual(result.errors, [])


class ClaudeFusionDocumentContractTests(unittest.TestCase):
    validation_inputs = (
        "SKILL.md",
        "references/startup-triage-playbook.md",
        "references/workflow-overview.md",
        "references/tool-playbook.md",
        "references/hook-techniques.md",
        "references/report-templates.md",
        "references/provider-work-order.md",
        "references/delivery-gate-playbook.md",
        "references/project-artifact-contract.md",
        "references/skill-maintenance.md",
        "references/mcp-routing-playbook.md",
        "agents/openai.yaml",
        "scripts/check_reverse_env.py",
    )

    def make_root(self, directory: str) -> Path:
        root = Path(directory)
        for relative in self.validation_inputs:
            source = ROOT / relative
            destination = root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, destination)
        return root

    def validate(self, root: Path) -> validate_skill.Validation:
        result = validate_skill.Validation()
        validate_skill.validate_intake_tools_and_reporting(root, result)
        return result

    def mutate_section_marker(
        self,
        root: Path,
        relative: str,
        heading: str,
        marker: str,
        *,
        move_to_sibling: bool = False,
    ) -> None:
        path = root / relative
        document = path.read_text(encoding="utf-8")
        section = validate_skill.extract_markdown_section(document, heading)
        self.assertTrue(section, heading)
        self.assertIn(marker, section)
        mutated_section = section.replace(marker, "removed-contract-marker")
        mutated = document.replace(section, mutated_section, 1)
        if move_to_sibling:
            mutated += f"\n## Mutation sink\n\n{marker}\n"
        path.write_text(mutated, encoding="utf-8")

    def remove_section(self, root: Path, relative: str, heading: str) -> None:
        path = root / relative
        document = path.read_text(encoding="utf-8")
        pattern = re.compile(
            rf"^##[ \t]+{re.escape(heading)}[ \t]*\n.*?(?=^##[ \t]+|\Z)",
            re.IGNORECASE | re.MULTILINE | re.DOTALL,
        )
        mutated, count = pattern.subn("", document, count=1)
        self.assertEqual(count, 1, heading)
        path.write_text(mutated, encoding="utf-8")

    def assert_contract_error(
        self,
        root: Path,
        expected_fragment: str,
    ) -> None:
        result = self.validate(root)
        self.assertTrue(
            any(expected_fragment in error for error in result.errors),
            result.errors,
        )

    def test_current_documents_satisfy_section_scoped_contracts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.validate(self.make_root(directory))

            self.assertEqual(result.errors, [])

    def test_rejects_deleted_browser_role_and_sequential_handoff_markers(self) -> None:
        mutations = (
            (
                "references/startup-triage-playbook.md",
                "Capability-aware evidence roles",
                "`cdp-bridge`",
                "startup browser acquisition roles",
            ),
            (
                "references/tool-playbook.md",
                "Capability-aware evidence route matrix",
                "after the handoff gate",
                "tool browser acquisition roles",
            ),
        )
        for relative, heading, marker, expected_error in mutations:
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as directory:
                root = self.make_root(directory)
                self.mutate_section_marker(root, relative, heading, marker)

                self.assert_contract_error(root, expected_error)

    def test_rejects_deleted_hook_timing_matrix(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.remove_section(
                root,
                "references/hook-techniques.md",
                "Hook timing and recovery matrix",
            )

            self.assert_contract_error(root, "hook timing fallbacks")

    def test_rejects_deleted_environment_coherence_and_strict_mode(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            path = root / "scripts" / "check_reverse_env.py"
            document = path.read_text(encoding="utf-8")
            marker = '"--require-project-venv"'
            self.assertIn(marker, document)
            path.write_text(document.replace(marker, '"--removed-venv-gate"'), encoding="utf-8")

            self.assert_contract_error(root, "check_reverse_env project coherence contract")

    def test_rejects_deleted_provider_brief_trigger(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.mutate_section_marker(
                root,
                "references/provider-work-order.md",
                "Conditional Implementation Brief",
                "at least one material choice remains",
            )

            self.assert_contract_error(root, "provider conditional implementation brief")

    def test_rejects_short_workflow_handoff_routing_moved_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.mutate_section_marker(
                root,
                "references/workflow-overview.md",
                "Phase 5: Deliver",
                "compact protocol handoff",
                move_to_sibling=True,
            )

            self.assert_contract_error(root, "workflow compact protocol handoff routing")

    def test_rejects_runtime_evidence_field_moved_elsewhere(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.mutate_section_marker(
                root,
                "references/project-artifact-contract.md",
                "Proof Manifest",
                '"runtimeEvidence"',
                move_to_sibling=True,
            )

            self.assert_contract_error(root, "project artifact runtime evidence contract")

    def test_rejects_report_brief_field_moved_to_another_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.mutate_section_marker(
                root,
                "references/report-templates.md",
                "Conditional implementation brief",
                "- Permission status:",
                move_to_sibling=True,
            )

            self.assert_contract_error(root, "report conditional implementation brief")

    def test_rejects_handoff_field_moved_to_another_section(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = self.make_root(directory)
            self.mutate_section_marker(
                root,
                "references/report-templates.md",
                "Compact protocol handoff",
                "- Real request:",
                move_to_sibling=True,
            )

            self.assert_contract_error(root, "compact protocol handoff")


class OfficialSuiteContractTests(unittest.TestCase):
    def suite_text(self) -> str:
        return (ROOT / "references" / "official-self-test-task-suite.md").read_text(
            encoding="utf-8"
        )

    def fusion_cases(self) -> dict[str, validate_skill.SelfTestCase]:
        suite = self.suite_text()
        cases = validate_skill.parse_self_test_suite(suite)
        return {
            case.heading: case
            for case in cases
            if case.heading in validate_skill.CLAUDE_PROJECT_FUSION_TASKS
        }

    def test_claude_project_fusion_tasks_are_structurally_present(self) -> None:
        suite = self.suite_text()
        cases = validate_skill.parse_self_test_suite(suite)
        headings = {case.heading for case in cases}

        self.assertGreaterEqual(len(cases), 92)
        self.assertEqual(
            validate_skill.CLAUDE_PROJECT_FUSION_TASKS - headings,
            set(),
        )

        indexed = {case.heading: case for case in cases}
        for heading in validate_skill.CLAUDE_PROJECT_FUSION_TASKS:
            case = indexed[heading]
            self.assertTrue(case.prompt)
            self.assertTrue(case.routes)
            self.assertTrue(case.conclusions)
            result = validate_skill.Validation()
            validate_skill.validate_claude_project_fusion_case(case, result)
            self.assertEqual(result.errors, [], heading)

    def test_claude_project_fusion_tasks_require_exact_routes(self) -> None:
        indexed = self.fusion_cases()
        for heading, (expected_routes, _) in (
            validate_skill.CLAUDE_PROJECT_FUSION_CONTRACTS.items()
        ):
            case = indexed[heading]
            self.assertEqual(case.routes, expected_routes)
            mutated = validate_skill.SelfTestCase(
                heading=case.heading,
                prompt=case.prompt,
                routes=tuple(reversed(case.routes)),
                conclusions=case.conclusions,
            )
            result = validate_skill.Validation()

            validate_skill.validate_claude_project_fusion_case(mutated, result)

            self.assertTrue(
                any("official task routes changed" in error for error in result.errors),
                result.errors,
            )

    def test_claude_project_fusion_tasks_reject_deleted_conclusion_markers(self) -> None:
        indexed = self.fusion_cases()
        for heading, (_, marker_groups) in (
            validate_skill.CLAUDE_PROJECT_FUSION_CONTRACTS.items()
        ):
            case = indexed[heading]
            for marker_group in marker_groups:
                with self.subTest(heading=heading, marker_group=marker_group):
                    pattern = re.compile(
                        "|".join(re.escape(marker) for marker in marker_group),
                        re.IGNORECASE,
                    )
                    mutated_conclusions = tuple(
                        pattern.sub("removed-contract-marker", conclusion)
                        for conclusion in case.conclusions
                    )
                    self.assertNotEqual(mutated_conclusions, case.conclusions)
                    mutated = validate_skill.SelfTestCase(
                        heading=case.heading,
                        prompt=case.prompt,
                        routes=case.routes,
                        conclusions=mutated_conclusions,
                    )
                    result = validate_skill.Validation()

                    validate_skill.validate_claude_project_fusion_case(mutated, result)

                    self.assertTrue(
                        any(
                            "official task conclusion contract" in error
                            for error in result.errors
                        ),
                        result.errors,
                    )

    def test_contract_fingerprint_accepts_crlf_without_losing_headings(self) -> None:
        suite = self.suite_text()
        crlf_suite = suite.replace("\n", "\r\n")

        self.assertEqual(
            validate_skill.official_suite_contract_digest(crlf_suite),
            validate_skill.OFFICIAL_SUITE_CONTRACT_SHA256,
        )
        self.assertEqual(
            len(validate_skill.TASK_HEADING_RE.findall(crlf_suite)),
            validate_skill.OFFICIAL_SUITE_TASK_COUNT,
        )
        self.assertEqual(
            len(validate_skill.parse_self_test_suite(crlf_suite)),
            validate_skill.OFFICIAL_SUITE_TASK_COUNT,
        )

    def test_contract_fingerprint_rejects_deletion_of_every_individual_task(self) -> None:
        suite = self.suite_text()
        task_matches = list(validate_skill.TASK_BLOCK_RE.finditer(suite))
        self.assertEqual(
            len(task_matches),
            validate_skill.OFFICIAL_SUITE_TASK_COUNT,
        )

        for match in task_matches:
            with self.subTest(heading=match.group("heading")):
                mutated = suite[: match.start()] + suite[match.end() :]
                self.assertNotEqual(
                    validate_skill.official_suite_contract_digest(mutated),
                    validate_skill.OFFICIAL_SUITE_CONTRACT_SHA256,
                )

    def test_contract_fingerprint_rejects_each_protected_surface(self) -> None:
        suite = self.suite_text()
        first_match = next(iter(validate_skill.TASK_BLOCK_RE.finditer(suite)))
        first_block = first_match.group(0)
        first_case = validate_skill.parse_self_test_suite(first_block)[0]
        self.assertTrue(first_case.prompt)
        self.assertTrue(first_case.routes)
        self.assertTrue(first_case.conclusions)

        prompt_block = first_block.replace(
            first_case.prompt,
            f"{first_case.prompt} mutated",
            1,
        )
        route_block = first_block.replace(
            first_case.routes[0],
            "references/mutated-contract.md",
            1,
        )
        conclusion_block = first_block.replace(
            first_case.conclusions[0],
            f"{first_case.conclusions[0]} mutated",
            1,
        )
        failure_mutation = suite.replace(
            "## Failure signals",
            "## Failure signals\n\n- mutated failure contract",
            1,
        )
        mutations = {
            "prompt": suite[: first_match.start()] + prompt_block + suite[first_match.end() :],
            "route": suite[: first_match.start()] + route_block + suite[first_match.end() :],
            "conclusion": (
                suite[: first_match.start()]
                + conclusion_block
                + suite[first_match.end() :]
            ),
            "failure-signals": failure_mutation,
        }

        for surface, mutated in mutations.items():
            with self.subTest(surface=surface):
                result = validate_skill.Validation()
                validate_skill.validate_official_suite_contract(mutated, result)

                self.assertTrue(
                    any("official suite contract fingerprint" in error for error in result.errors),
                    result.errors,
                )


if __name__ == "__main__":
    unittest.main()
