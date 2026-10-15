from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import check_reverse_env as environment_check  # noqa: E402


SCRIPT = ROOT / "scripts" / "check_reverse_env.py"


def run_check(
    *arguments: str,
    env: dict[str, str] | None = None,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-B", str(SCRIPT), *arguments],
        capture_output=True,
        text=True,
        check=False,
        env=env,
        cwd=cwd,
    )


@pytest.mark.parametrize(
    ("strict", "expected_return_code", "requirement"),
    [
        (False, 0, "advisory"),
        (True, 1, "strict"),
    ],
)
def test_project_venv_mismatch_warns_by_default_and_only_fails_in_strict_mode(
    tmp_path: Path,
    strict: bool,
    expected_return_code: int,
    requirement: str,
) -> None:
    project_root = tmp_path / "project root with spaces"
    project_root.mkdir()
    arguments = ["--project-root", str(project_root)]
    if strict:
        arguments.append("--require-project-venv")

    completed = run_check(*arguments)

    assert completed.returncode == expected_return_code, completed.stderr or completed.stdout
    assert f"- project_root: {project_root.resolve()}" in completed.stdout
    assert "- project_dot_venv_active: no" in completed.stdout
    assert f"- project_dot_venv_requirement: {requirement}" in completed.stdout
    assert "active interpreter is not under the project .venv" in completed.stdout
    assert "Traceback" not in completed.stdout + completed.stderr


def test_detects_an_active_interpreter_under_project_dot_venv_with_spaces(tmp_path: Path) -> None:
    project_root = tmp_path / "project root with spaces"
    project_venv = project_root / ".venv"
    scripts_directory = project_venv / ("Scripts" if os.name == "nt" else "bin")
    scripts_directory.mkdir(parents=True)
    executable = scripts_directory / ("python.exe" if os.name == "nt" else "python")
    executable.touch()

    result = environment_check.detect_python_environment(
        project_root,
        executable=executable,
        prefix=project_venv,
        base_prefix=tmp_path / "base python",
        has_real_prefix=False,
    )

    assert result.virtual_environment_active is True
    assert result.environment_kind == "venv"
    assert result.project_dot_venv_exists is True
    assert result.project_dot_venv_active is True


def test_fingerprints_explicit_public_lockfile_without_printing_content(tmp_path: Path) -> None:
    project_root = tmp_path / "public helper project"
    helper_root = project_root / "helper with spaces"
    helper_root.mkdir(parents=True)
    lockfile = helper_root / "package-lock.json"
    content = b'{"name":"public-helper","lockfileVersion":3}'
    lockfile.write_bytes(content)

    completed = run_check(
        "--project-root",
        str(project_root),
        "--helper-lockfile",
        str(lockfile),
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    expected_hash = hashlib.sha256(content).hexdigest()
    assert (
        f"- helper_lockfile: helper with spaces/package-lock.json "
        f"bytes={len(content)} sha256={expected_hash}"
    ) in completed.stdout
    assert "public-helper" not in completed.stdout


def test_does_not_scan_existing_lockfiles_without_explicit_selection(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    lockfile = project_root / "package-lock.json"
    content = b'{"private-marker":"must-not-be-read"}'
    lockfile.write_bytes(content)

    completed = run_check("--project-root", str(project_root))

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "- helper_lockfiles: none_requested" in completed.stdout
    assert hashlib.sha256(content).hexdigest() not in completed.stdout
    assert "must-not-be-read" not in completed.stdout + completed.stderr


def test_rejects_oversized_and_non_lockfile_inputs(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    oversized = project_root / "package-lock.json"
    oversized.write_bytes(b"1234")

    with pytest.raises(environment_check.EnvironmentInputError, match="3-byte limit"):
        environment_check.fingerprint_helper_lockfile(project_root, oversized, max_bytes=3)

    invalid = project_root / "settings.json"
    invalid.write_text("{}", encoding="utf-8")
    completed = run_check(
        "--project-root",
        str(project_root),
        "--helper-lockfile",
        str(invalid),
    )
    assert completed.returncode == 2
    assert completed.stdout == ""
    assert completed.stderr.strip() == (
        "environment_check_error: helper lockfile name is not a supported public lockfile"
    )
    assert str(project_root) not in completed.stderr
    assert "Traceback" not in completed.stderr

    outside = tmp_path / "package-lock.json"
    outside.write_text("{}", encoding="utf-8")
    escaped = run_check(
        "--project-root",
        str(project_root),
        "--helper-lockfile",
        str(outside),
    )
    assert escaped.returncode == 2
    assert escaped.stderr.strip() == (
        "environment_check_error: helper lockfile must stay under project root"
    )
    assert str(tmp_path) not in escaped.stderr


def test_missing_node_and_npm_have_stable_fallbacks(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    environment = os.environ.copy()
    environment["PATH"] = ""
    environment["HTTP_PROXY"] = "http://private-user:private-password@proxy.invalid"
    environment["VIRTUAL_ENV"] = str(tmp_path / "private environment value")

    completed = run_check("--project-root", str(project_root), env=environment)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "- node: missing" in completed.stdout
    assert "- npm: missing" in completed.stdout
    assert "- node_version: missing" in completed.stdout
    assert "- npm_version: missing" in completed.stdout
    assert "- proxy_env_HTTP_PROXY: set" in completed.stdout
    assert "private-user" not in completed.stdout + completed.stderr
    assert "private environment value" not in completed.stdout + completed.stderr
    assert "Traceback" not in completed.stdout + completed.stderr


def test_current_directory_cannot_supply_version_commands(tmp_path: Path) -> None:
    project_root = tmp_path / "untrusted project"
    project_root.mkdir()
    trusted_empty_path = tmp_path / "trusted empty path"
    trusted_empty_path.mkdir()
    marker = project_root / "version-command-ran.txt"
    environment = os.environ.copy()
    environment["PATH"] = str(trusted_empty_path)

    if os.name == "nt":
        for name in ("node.cmd", "npm.cmd"):
            (project_root / name).write_text(
                f'@echo ran>"{marker}"\n@echo 9.9.9\n',
                encoding="utf-8",
            )
    else:
        for name in ("node", "npm"):
            path = project_root / name
            path.write_text(
                f"#!/bin/sh\nprintf ran > '{marker}'\nprintf '9.9.9\\n'\n",
                encoding="utf-8",
            )
            path.chmod(0o755)

    completed = run_check(
        "--project-root",
        str(project_root),
        env=environment,
        cwd=project_root,
    )

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "- node: missing" in completed.stdout
    assert "- npm: missing" in completed.stdout
    assert not marker.exists()


@pytest.mark.skipif(os.name != "nt", reason="Windows command processor contract")
def test_untrusted_windows_command_environment_is_ignored(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    marker = project_root / "untrusted-command-processor-ran.txt"
    command_processor = project_root / "untrusted-comspec.cmd"
    command_processor.write_text(
        f'@echo ran>"{marker}"\n@exit /b 17\n',
        encoding="utf-8",
    )
    environment = os.environ.copy()
    environment["COMSPEC"] = str(command_processor)
    environment["SystemRoot"] = str(project_root / "untrusted-windows")
    environment["WINDIR"] = str(project_root / "untrusted-windows")

    completed = run_check("--project-root", str(project_root), env=environment)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "unavailable(start_failed)" not in completed.stdout
    assert not marker.exists()


def test_command_version_uses_a_sanitized_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NODE_OPTIONS", "--require=private-target-helper.js")
    monkeypatch.setenv("VIRTUAL_ENV", "private-environment-path")

    result = environment_check.command_version(
        sys.executable,
        (
            "-c",
            "import os; print('9.8.7' if 'NODE_OPTIONS' not in os.environ "
            "and 'VIRTUAL_ENV' not in os.environ else '0.0.0')",
        ),
    )

    assert result == "9.8.7"


def test_command_version_rejects_output_beyond_its_read_limit() -> None:
    result = environment_check.command_version(
        sys.executable,
        ("-c", "print('9.8.7'); print('x' * 512)"),
        max_output_bytes=32,
    )

    assert result == "unavailable(output_limit)"


def test_command_version_bounds_high_volume_output_without_disk_capture() -> None:
    started = time.monotonic()
    result = environment_check.command_version(
        sys.executable,
        ("-c", "import os; os.write(1, b'x' * (8 * 1024 * 1024))"),
        max_output_bytes=32,
    )
    elapsed = time.monotonic() - started

    assert result == "unavailable(output_limit)"
    assert elapsed < 3.0


def test_command_version_timeout_is_not_held_open_by_a_child_process() -> None:
    started = time.monotonic()
    result = environment_check.command_version(
        sys.executable,
        (
            "-c",
            "import subprocess, sys, time; "
            "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(8)']); "
            "time.sleep(8)",
        ),
        timeout_seconds=0.1,
    )
    elapsed = time.monotonic() - started

    assert result == "unavailable(timeout)"
    assert elapsed < 3.0


def test_command_version_kills_a_child_after_the_parent_exits_successfully(
    tmp_path: Path,
) -> None:
    marker = tmp_path / "escaped-child.txt"
    child_code = (
        "import pathlib, time; time.sleep(0.8); "
        f"pathlib.Path({str(marker)!r}).write_text('escaped', encoding='utf-8')"
    )
    parent_code = (
        "import subprocess, sys; "
        f"subprocess.Popen([sys.executable, '-c', {child_code!r}]); "
        "print('9.8.7')"
    )

    result = environment_check.command_version(
        sys.executable,
        ("-c", parent_code),
        timeout_seconds=2.0,
    )
    time.sleep(1.0)

    assert result == "9.8.7"
    assert not marker.exists()


@pytest.mark.skipif(os.name != "nt", reason="Windows batch quoting contract")
def test_command_version_accepts_legal_batch_path_metacharacters(tmp_path: Path) -> None:
    launcher_directory = tmp_path / "Program Files (x86) & 100%!"
    launcher_directory.mkdir()
    launcher = launcher_directory / "npm.cmd"
    launcher.write_text("@echo 9.8.7\n", encoding="utf-8")

    result = environment_check.command_version(str(launcher))

    assert result == "9.8.7"


def test_rejects_hardlinked_helper_lockfile(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    source = tmp_path / "outside-package-lock.json"
    source.write_text("{}", encoding="utf-8")
    lockfile = project_root / "package-lock.json"
    os.link(source, lockfile)

    with pytest.raises(environment_check.EnvironmentInputError, match="hardlink"):
        environment_check.fingerprint_helper_lockfile(project_root, lockfile)


def test_rechecks_hardlink_count_after_read(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lockfile = tmp_path / "package-lock.json"
    lockfile.write_text("{}", encoding="utf-8")
    real_fstat = os.fstat
    calls = 0

    def changing_fstat(descriptor: int) -> os.stat_result | SimpleNamespace:
        nonlocal calls
        calls += 1
        observed = real_fstat(descriptor)
        if calls == 1:
            return observed
        return SimpleNamespace(
            st_dev=observed.st_dev,
            st_ino=observed.st_ino,
            st_mode=observed.st_mode,
            st_nlink=2,
            st_size=observed.st_size,
            st_mtime_ns=observed.st_mtime_ns,
            st_ctime_ns=observed.st_ctime_ns,
        )

    monkeypatch.setattr(environment_check.os, "fstat", changing_fstat)

    descriptor = os.open(lockfile, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    try:
        with pytest.raises(environment_check.EnvironmentInputError, match="hardlink"):
            environment_check._read_stable_lockfile(descriptor, max_bytes=1024)
    finally:
        os.close(descriptor)


def test_rejects_changed_ctime_even_when_size_and_mtime_match(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lockfile = tmp_path / "package-lock.json"
    lockfile.write_text('{"lockfileVersion":3}', encoding="utf-8")
    real_fstat = os.fstat
    calls = 0

    def changed_ctime(descriptor: int) -> os.stat_result | SimpleNamespace:
        nonlocal calls
        calls += 1
        observed = real_fstat(descriptor)
        if calls == 1:
            return observed
        return SimpleNamespace(
            st_dev=observed.st_dev,
            st_ino=observed.st_ino,
            st_mode=observed.st_mode,
            st_nlink=observed.st_nlink,
            st_size=observed.st_size,
            st_mtime_ns=observed.st_mtime_ns,
            st_ctime_ns=observed.st_ctime_ns + 1,
        )

    monkeypatch.setattr(environment_check.os, "fstat", changed_ctime)
    descriptor = os.open(lockfile, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    try:
        with pytest.raises(environment_check.EnvironmentInputError, match="changed"):
            environment_check._read_stable_lockfile(descriptor, max_bytes=1024)
    finally:
        os.close(descriptor)


def test_rejects_two_different_reads_with_unchanged_metadata(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    lockfile = tmp_path / "package-lock.json"
    lockfile.write_text('{"lockfileVersion":3}', encoding="utf-8")
    reads = iter((b"old-and-new", b"all-new-now"))
    monkeypatch.setattr(
        environment_check,
        "_read_lockfile_pass",
        lambda descriptor, *, max_bytes: next(reads),
    )

    descriptor = os.open(lockfile, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    try:
        with pytest.raises(environment_check.EnvironmentInputError, match="changed"):
            environment_check._read_stable_lockfile(descriptor, max_bytes=1024)
    finally:
        os.close(descriptor)


@pytest.mark.skipif(os.name != "nt", reason="Windows sharing contract")
def test_windows_lockfile_snapshot_denies_a_concurrent_writer(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    lockfile = project_root / "package-lock.json"
    original = b'{"lockfileVersion":3}'
    lockfile.write_bytes(original)
    real_read_pass = environment_check._read_lockfile_pass
    write_failures: list[OSError] = []

    def read_with_write_attempt(descriptor: int, *, max_bytes: int) -> bytes:
        if not write_failures:
            try:
                lockfile.write_bytes(b'{"lockfileVersion":4}')
            except OSError as exc:
                write_failures.append(exc)
        return real_read_pass(descriptor, max_bytes=max_bytes)

    monkeypatch.setattr(
        environment_check,
        "_read_lockfile_pass",
        read_with_write_attempt,
    )

    result = environment_check.fingerprint_helper_lockfile(project_root, lockfile)

    assert write_failures
    assert lockfile.read_bytes() == original
    assert result.sha256 == hashlib.sha256(original).hexdigest()


def test_rejects_symlink_before_lockfile_resolution(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    target = project_root / "actual-lock.json"
    target.write_text("{}", encoding="utf-8")
    lockfile = project_root / "package-lock.json"
    try:
        lockfile.symlink_to(target)
    except OSError as exc:
        pytest.skip(f"symlink creation unavailable: {exc}")

    with pytest.raises(
        environment_check.EnvironmentInputError,
        match="symlinks or reparse points",
    ):
        environment_check.fingerprint_helper_lockfile(project_root, lockfile)


def test_rejects_symlinked_parent_before_lockfile_open(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "package-lock.json").write_text("{}", encoding="utf-8")
    linked_parent = project_root / "helper"
    try:
        linked_parent.symlink_to(outside, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"directory symlink creation unavailable: {exc}")

    with pytest.raises(
        environment_check.EnvironmentInputError,
        match="symlinks or reparse points",
    ):
        environment_check.fingerprint_helper_lockfile(
            project_root,
            linked_parent / "package-lock.json",
        )


@pytest.mark.skipif(os.name == "nt", reason="Unix launcher symlink contract")
def test_tool_discovery_preserves_a_validated_symlink_launcher(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    path_directory = tmp_path / "bin"
    path_directory.mkdir()
    target = tmp_path / "real-node"
    target.write_text("#!/bin/sh\nprintf '9.8.7\\n'\n", encoding="utf-8")
    target.chmod(0o755)
    launcher = path_directory / "node"
    launcher.symlink_to(target)

    discovered = environment_check.discover_path_tool(
        "node",
        project_root,
        path_value=str(path_directory),
    )

    assert discovered == str(launcher)


@pytest.mark.skipif(os.name != "nt", reason="Windows extended path contract")
def test_windows_extended_lockfile_path_matches_project_root(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    lockfile = project_root / "package-lock.json"
    lockfile.write_text("{}", encoding="utf-8")
    extended_path = Path("\\\\?\\" + str(lockfile.resolve()))

    result = environment_check.fingerprint_helper_lockfile(
        project_root.resolve(),
        extended_path,
    )

    assert result.relative_path == "package-lock.json"


def test_non_ascii_project_path_survives_ascii_console(tmp_path: Path) -> None:
    project_root = tmp_path / "project_\U0001f680"
    project_root.mkdir()
    environment = os.environ.copy()
    environment["PATH"] = ""
    environment["PYTHONIOENCODING"] = "ascii:strict"

    completed = run_check("--project-root", str(project_root), env=environment)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "project_\\U0001f680" in completed.stdout
    assert "UnicodeEncodeError" not in completed.stdout + completed.stderr


def test_lowercase_proxy_environment_is_reported_without_its_value(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    environment = os.environ.copy()
    environment["PATH"] = ""
    environment.pop("HTTP_PROXY", None)
    environment["http_proxy"] = "http://private-user:private-password@proxy.invalid"

    completed = run_check("--project-root", str(project_root), env=environment)

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "- proxy_env_HTTP_PROXY: set" in completed.stdout
    assert "private-user" not in completed.stdout + completed.stderr


def test_invalid_project_root_is_a_bounded_cli_error(tmp_path: Path) -> None:
    missing = tmp_path / "private path" / "missing"
    completed = run_check("--project-root", str(missing))

    assert completed.returncode == 2
    assert completed.stdout == ""
    assert completed.stderr.strip() == (
        "environment_check_error: project root does not exist or cannot be resolved"
    )
    assert str(tmp_path) not in completed.stderr
    assert "Traceback" not in completed.stderr


def test_desktop_chrome_impersonate_selector_ignores_android_and_picks_max() -> None:
    assert environment_check._desktop_chrome_impersonate_major("chrome146") == 146
    assert environment_check._desktop_chrome_impersonate_major("chrome133a") == 133
    assert environment_check._desktop_chrome_impersonate_major("chrome131_android") is None
    assert (
        environment_check._max_desktop_chrome_impersonate(
            ["chrome136", "chrome146", "chrome131_android", "chrome133a"]
        )
        == "chrome146"
    )


def test_reports_curl_cffi_chrome_impersonate_profile(tmp_path: Path) -> None:
    project_root = tmp_path / "project"
    project_root.mkdir()
    completed = run_check("--project-root", str(project_root))

    assert completed.returncode == 0, completed.stderr or completed.stdout
    assert "- curl_cffi_chrome_impersonate:" in completed.stdout
    profile = environment_check.curl_cffi_chrome_impersonate_profile()
    if environment_check.module_status("curl_cffi") == "available":
        assert "default=" in profile
        assert "max=" in profile
    else:
        assert profile == "missing"
