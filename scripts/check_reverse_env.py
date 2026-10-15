#!/usr/bin/env python3
"""Quick environment check for protocol-first reverse work."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import importlib.util
import os
import re
import signal
import stat
import subprocess
import sys
import threading
import time
import warnings
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO, Sequence


TOOL_NAMES = (
    "node",
    "npm",
    "curl",
    "git",
)

PYTHON_MODULES = [
    "iv8",
    "curl_cffi",
]

PYTHON_DISTRIBUTIONS = [
    "requests",
    "urllib3",
    "chardet",
    "charset-normalizer",
]

AGENT_CAPABILITIES = [
    "chrome-devtools",
    "js-reverse",
]

PROXY_ENV_VARS = [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "ALL_PROXY",
    "NO_PROXY",
]

MAX_COMMAND_OUTPUT_BYTES = 256
COMMAND_TIMEOUT_SECONDS = 3.0
MAX_LOCKFILE_BYTES = 16 * 1024 * 1024
PUBLIC_HELPER_LOCKFILES = frozenset(
    {
        "bun.lock",
        "bun.lockb",
        "cargo.lock",
        "composer.lock",
        "deno.lock",
        "gemfile.lock",
        "npm-shrinkwrap.json",
        "package-lock.json",
        "pipfile.lock",
        "pnpm-lock.yaml",
        "poetry.lock",
        "uv.lock",
        "yarn.lock",
    }
)
VERSION_PATTERN = re.compile(
    rb"(?<![0-9A-Za-z_])[vV]?\d+(?:\.\d+){1,3}(?:[-+][0-9A-Za-z.-]+)?(?![0-9A-Za-z_])"
)


class EnvironmentInputError(ValueError):
    """Raised for invalid user-selected diagnostic inputs."""


@dataclass(frozen=True)
class PythonEnvironment:
    virtual_environment_active: bool
    environment_kind: str
    project_dot_venv_active: bool
    project_dot_venv_exists: bool


@dataclass(frozen=True)
class LockfileFingerprint:
    relative_path: str
    byte_length: int
    sha256: str


def command_status(path: str | None) -> str:
    if not path:
        return "missing"
    try:
        return str(Path(path).resolve())
    except (OSError, RuntimeError):
        return "unavailable"


def module_status(name: str) -> str:
    try:
        return "available" if importlib.util.find_spec(name) else "missing"
    except (ImportError, AttributeError, ValueError):
        return "unavailable"


def distribution_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "missing"
    except Exception:  # pragma: no cover - broken local package metadata
        return "unavailable"


def _bounded_diagnostic(value: str, *, max_chars: int = 256) -> str:
    printable = "".join(character if character.isprintable() else " " for character in value)
    compact = " ".join(printable.split())
    if len(compact) <= max_chars:
        return compact
    return compact[:max_chars] + "..."


def requests_dependency_notes() -> list[str]:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        try:
            import requests  # noqa: F401
        except Exception as exc:  # pragma: no cover - diagnostic script
            return [f"requests_import_error: {type(exc).__name__}"]
    return [_bounded_diagnostic(str(item.message)) for item in caught]


def curl_cffi_default_chrome() -> str:
    if module_status("curl_cffi") != "available":
        return "missing"
    try:
        from curl_cffi.requests.impersonate import DEFAULT_CHROME
    except Exception as exc:  # pragma: no cover - diagnostic script
        return f"unavailable: {type(exc).__name__}"
    return _bounded_diagnostic(str(DEFAULT_CHROME), max_chars=64)


def _desktop_chrome_impersonate_major(name: str) -> int | None:
    lowered = name.strip().lower()
    if "android" in lowered or "ios" in lowered:
        return None
    match = re.fullmatch(r"chrome(\d+)[a-z]?", lowered)
    if match is None:
        return None
    return int(match.group(1))


def _max_desktop_chrome_impersonate(names: list[str]) -> str | None:
    ranked: list[tuple[int, str]] = []
    for name in names:
        major = _desktop_chrome_impersonate_major(name)
        if major is not None:
            ranked.append((major, name))
    if not ranked:
        return None
    return max(ranked, key=lambda item: (item[0], item[1]))[1]


def curl_cffi_chrome_impersonate_profile() -> str:
    if module_status("curl_cffi") != "available":
        return "missing"
    try:
        from curl_cffi.requests import impersonate as impersonate_mod
    except Exception as exc:  # pragma: no cover - diagnostic script
        return f"unavailable: {type(exc).__name__}"
    default_chrome = str(getattr(impersonate_mod, "DEFAULT_CHROME", "") or "").strip()
    names: set[str] = set()
    if default_chrome:
        names.add(default_chrome)
    browser_type = getattr(impersonate_mod, "BrowserType", None)
    try:
        for member in browser_type or []:
            names.add(str(getattr(member, "value", member)))
    except TypeError:
        members = getattr(browser_type, "__members__", {})
        for member in members.values():
            names.add(str(getattr(member, "value", member)))
    max_chrome = _max_desktop_chrome_impersonate(sorted(names))
    if not default_chrome and not max_chrome:
        return "unavailable"
    profile = f"default={default_chrome or 'unknown'}; max={max_chrome or default_chrome or 'unknown'}"
    return _bounded_diagnostic(profile, max_chars=96)


def _windows_api_directory(function_name: str) -> Path | None:
    if os.name != "nt":
        return None
    try:
        import ctypes

        function = getattr(ctypes.WinDLL("kernel32", use_last_error=True), function_name)
        buffer = ctypes.create_unicode_buffer(32768)
        length = function(buffer, len(buffer))
        if length == 0 or length >= len(buffer):
            return None
        directory = Path(buffer.value).resolve(strict=True)
    except (AttributeError, OSError, RuntimeError, ValueError):
        return None
    return directory if directory.is_dir() else None


def _trusted_windows_command_paths() -> tuple[Path, Path, Path] | None:
    windows_directory = _windows_api_directory("GetWindowsDirectoryW")
    system_directory = _windows_api_directory("GetSystemDirectoryW")
    if windows_directory is None or system_directory is None:
        return None
    command_processor = system_directory / "cmd.exe"
    taskkill = system_directory / "taskkill.exe"
    if not command_processor.is_file() or not taskkill.is_file():
        return None
    return windows_directory, command_processor, taskkill


def _diagnostic_subprocess_environment(executable: str) -> dict[str, str]:
    launcher_directory = Path(os.path.abspath(executable)).parent
    environment: dict[str, str] = {
        "PATH": str(launcher_directory),
        "NO_COLOR": "1",
    }
    trusted_windows_paths = _trusted_windows_command_paths()
    if trusted_windows_paths is not None:
        windows_directory, command_processor, _ = trusted_windows_paths
        environment.update(
            {
                "SystemRoot": str(windows_directory),
                "WINDIR": str(windows_directory),
                "COMSPEC": str(command_processor),
                "PATHEXT": ".COM;.EXE;.BAT;.CMD",
            }
        )
    return environment


def _create_windows_kill_job() -> int | None:
    if os.name != "nt":
        return None
    try:
        import ctypes
        from ctypes import wintypes

        class IoCounters(ctypes.Structure):
            _fields_ = [
                ("ReadOperationCount", ctypes.c_ulonglong),
                ("WriteOperationCount", ctypes.c_ulonglong),
                ("OtherOperationCount", ctypes.c_ulonglong),
                ("ReadTransferCount", ctypes.c_ulonglong),
                ("WriteTransferCount", ctypes.c_ulonglong),
                ("OtherTransferCount", ctypes.c_ulonglong),
            ]

        class BasicLimitInformation(ctypes.Structure):
            _fields_ = [
                ("PerProcessUserTimeLimit", ctypes.c_longlong),
                ("PerJobUserTimeLimit", ctypes.c_longlong),
                ("LimitFlags", wintypes.DWORD),
                ("MinimumWorkingSetSize", ctypes.c_size_t),
                ("MaximumWorkingSetSize", ctypes.c_size_t),
                ("ActiveProcessLimit", wintypes.DWORD),
                ("Affinity", ctypes.c_size_t),
                ("PriorityClass", wintypes.DWORD),
                ("SchedulingClass", wintypes.DWORD),
            ]

        class ExtendedLimitInformation(ctypes.Structure):
            _fields_ = [
                ("BasicLimitInformation", BasicLimitInformation),
                ("IoInfo", IoCounters),
                ("ProcessMemoryLimit", ctypes.c_size_t),
                ("JobMemoryLimit", ctypes.c_size_t),
                ("PeakProcessMemoryUsed", ctypes.c_size_t),
                ("PeakJobMemoryUsed", ctypes.c_size_t),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_job = kernel32.CreateJobObjectW
        create_job.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
        create_job.restype = wintypes.HANDLE
        set_job_information = kernel32.SetInformationJobObject
        set_job_information.argtypes = [
            wintypes.HANDLE,
            ctypes.c_int,
            ctypes.c_void_p,
            wintypes.DWORD,
        ]
        set_job_information.restype = wintypes.BOOL
        close_handle = kernel32.CloseHandle
        close_handle.argtypes = [wintypes.HANDLE]
        close_handle.restype = wintypes.BOOL

        job = create_job(None, None)
        if not job:
            return None
        information = ExtendedLimitInformation()
        information.BasicLimitInformation.LimitFlags = 0x00002000
        if not set_job_information(
            job,
            9,
            ctypes.byref(information),
            ctypes.sizeof(information),
        ):
            close_handle(job)
            return None
        return int(job)
    except (AttributeError, OSError, TypeError, ValueError):
        return None


def _close_windows_handle(handle: int | None) -> None:
    if os.name != "nt" or handle is None:
        return
    try:
        import ctypes
        from ctypes import wintypes

        close_handle = ctypes.WinDLL("kernel32", use_last_error=True).CloseHandle
        close_handle.argtypes = [wintypes.HANDLE]
        close_handle.restype = wintypes.BOOL
        close_handle(handle)
    except (AttributeError, OSError, TypeError, ValueError):
        pass


def _assign_and_resume_windows_process(
    process: subprocess.Popen[bytes],
    job_handle: int,
) -> bool:
    try:
        import ctypes
        from ctypes import wintypes

        process_handle = int(getattr(process, "_handle"))
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        assign_process = kernel32.AssignProcessToJobObject
        assign_process.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
        assign_process.restype = wintypes.BOOL
        if not assign_process(job_handle, process_handle):
            return False

        resume_process = ctypes.WinDLL("ntdll", use_last_error=True).NtResumeProcess
        resume_process.argtypes = [wintypes.HANDLE]
        resume_process.restype = ctypes.c_long
        return resume_process(process_handle) >= 0
    except (AttributeError, OSError, TypeError, ValueError):
        return False


def _terminate_process_tree(
    process: subprocess.Popen[bytes],
    environment: dict[str, str],
    windows_job_handle: int | None = None,
) -> None:
    if os.name == "nt" and windows_job_handle is not None:
        _close_windows_handle(windows_job_handle)
    elif os.name == "nt" and process.poll() is None:
        trusted_windows_paths = _trusted_windows_command_paths()
        if trusted_windows_paths is not None:
            _, _, taskkill = trusted_windows_paths
            try:
                subprocess.run(
                    [str(taskkill), "/PID", str(process.pid), "/T", "/F"],
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=1.0,
                    check=False,
                    env=environment,
                )
            except (OSError, subprocess.TimeoutExpired):
                pass
    elif os.name != "nt":
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except (OSError, ProcessLookupError):
            pass

    if process.poll() is not None:
        return
    try:
        process.kill()
    except OSError:
        pass
    try:
        process.wait(timeout=1.0)
    except (OSError, subprocess.TimeoutExpired):
        pass


def _read_bounded_process_output(
    stream: BinaryIO,
    max_output_bytes: int,
    output: bytearray,
    limit_exceeded: threading.Event,
    read_failed: threading.Event,
) -> None:
    try:
        file_descriptor = stream.fileno()
        while True:
            remaining = max_output_bytes + 1 - len(output)
            chunk = os.read(file_descriptor, max(1, min(4096, remaining)))
            if not chunk:
                return
            output.extend(chunk)
            if len(output) > max_output_bytes:
                limit_exceeded.set()
                return
    except (OSError, ValueError):
        read_failed.set()
    finally:
        try:
            stream.close()
        except (OSError, ValueError):
            pass


def command_version(
    executable: str | None,
    arguments: Sequence[str] = ("--version",),
    *,
    max_output_bytes: int = MAX_COMMAND_OUTPUT_BYTES,
    timeout_seconds: float = COMMAND_TIMEOUT_SECONDS,
) -> str:
    """Return one sanitized version token without retaining unbounded command output."""
    if not executable:
        return "missing"
    if max_output_bytes < 1 or timeout_seconds <= 0:
        return "unavailable(invalid_bounds)"

    environment = _diagnostic_subprocess_environment(executable)
    popen_command: Sequence[str] | str = [executable, *arguments]
    popen_executable: str | None = None
    if os.name == "nt" and Path(executable).suffix.lower() in {".bat", ".cmd"}:
        trusted_windows_paths = _trusted_windows_command_paths()
        if trusted_windows_paths is None:
            return "unavailable(trusted_command_processor_missing)"
        _, command_processor, _ = trusted_windows_paths
        if any(any(character in part for character in '"\x00\r\n') for part in arguments):
            return "unavailable(unsafe_batch_argument)"
        environment["SPIDER_KING_DIAGNOSTIC_BATCH"] = executable
        argument_variables: list[str] = []
        for index, argument in enumerate(arguments):
            variable_name = f"SPIDER_KING_DIAGNOSTIC_ARG_{index}"
            environment[variable_name] = argument
            argument_variables.append(f' "%{variable_name}%"')
        batch_command = '""%SPIDER_KING_DIAGNOSTIC_BATCH%"' + "".join(
            argument_variables
        ) + '"'
        popen_executable = str(command_processor)
        popen_command = (
            f'"{command_processor}" /d /v:off /s /c {batch_command}'
        )
    popen_options: dict[str, object] = {}
    windows_job_handle: int | None = None
    if os.name == "nt":
        windows_job_handle = _create_windows_kill_job()
        if windows_job_handle is None:
            return "unavailable(process_containment_failed)"
        popen_options["creationflags"] = getattr(
            subprocess,
            "CREATE_NEW_PROCESS_GROUP",
            0x00000200,
        ) | getattr(subprocess, "CREATE_SUSPENDED", 0x00000004)
        if popen_executable is not None:
            popen_options["executable"] = popen_executable
    else:
        popen_options["start_new_session"] = True

    try:
        process = subprocess.Popen(
            popen_command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=str(Path(os.path.abspath(executable)).parent),
            env=environment,
            **popen_options,
        )
    except (OSError, RuntimeError, ValueError):
        _close_windows_handle(windows_job_handle)
        return "unavailable(start_failed)"

    if windows_job_handle is not None and not _assign_and_resume_windows_process(
        process,
        windows_job_handle,
    ):
        try:
            process.kill()
            process.wait(timeout=1.0)
        except (OSError, subprocess.TimeoutExpired):
            pass
        _close_windows_handle(windows_job_handle)
        return "unavailable(process_containment_failed)"

    if process.stdout is None:  # pragma: no cover - PIPE always creates stdout
        _terminate_process_tree(process, environment, windows_job_handle)
        return "unavailable(no_output_pipe)"

    output_buffer = bytearray()
    limit_exceeded = threading.Event()
    read_failed = threading.Event()
    reader = threading.Thread(
        target=_read_bounded_process_output,
        args=(
            process.stdout,
            max_output_bytes,
            output_buffer,
            limit_exceeded,
            read_failed,
        ),
        daemon=True,
    )
    reader.start()

    deadline = time.monotonic() + timeout_seconds
    outcome: str | None = None
    while process.poll() is None:
        if limit_exceeded.wait(timeout=0.01):
            outcome = "unavailable(output_limit)"
            break
        if time.monotonic() >= deadline:
            outcome = "unavailable(timeout)"
            break

    _terminate_process_tree(process, environment, windows_job_handle)
    reader.join(timeout=1.0)
    if reader.is_alive():
        try:
            process.stdout.close()
        except (OSError, ValueError):
            pass
        reader.join(timeout=0.25)
    if reader.is_alive():
        return outcome or "unavailable(output_read_timeout)"
    if outcome is not None:
        return outcome
    if limit_exceeded.is_set():
        return "unavailable(output_limit)"
    if read_failed.is_set():
        return "unavailable(output_read_failed)"

    return_code = process.returncode
    if return_code != 0:
        return f"unavailable(exit_{return_code})"

    match = VERSION_PATTERN.search(bytes(output_buffer))
    if match is None:
        return "unavailable(unrecognized_output)"
    return match.group(0).decode("ascii")


def _strip_windows_extended_prefix(value: str) -> str:
    if os.name != "nt":
        return value
    if value.startswith("\\\\?\\UNC\\"):
        return "\\\\" + value[8:]
    if value.startswith("\\\\?\\"):
        return value[4:]
    return value


def _absolute_lexical_path(path: str | Path) -> Path:
    absolute = os.path.abspath(os.fspath(path))
    return Path(_strip_windows_extended_prefix(absolute))


def _normalized_path(path: Path) -> str:
    return os.path.normcase(os.path.normpath(os.fspath(_absolute_lexical_path(path))))


def _path_is_within(path: Path, parent: Path) -> bool:
    try:
        return os.path.commonpath((_normalized_path(path), _normalized_path(parent))) == _normalized_path(parent)
    except (OSError, RuntimeError, ValueError):
        return False


def _paths_equal(left: Path, right: Path) -> bool:
    try:
        return _normalized_path(left) == _normalized_path(right)
    except (OSError, RuntimeError, ValueError):
        return False


def _resolve_without_error(path: Path) -> Path:
    try:
        return _absolute_lexical_path(path.resolve(strict=False))
    except (OSError, RuntimeError, ValueError):
        try:
            return _absolute_lexical_path(path)
        except (OSError, RuntimeError, ValueError):
            return Path()


def discover_path_tool(
    name: str,
    project_root: Path,
    *,
    path_value: str | None = None,
) -> str | None:
    """Resolve a tool only from absolute PATH entries outside the bound project."""
    if Path(name).name != name or "/" in name or "\\" in name:
        return None

    if os.name == "nt":
        suffixes = (".COM", ".EXE", ".BAT", ".CMD")
        candidate_names = (
            (name,)
            if Path(name).suffix.upper() in suffixes
            else tuple(f"{name}{suffix}" for suffix in suffixes)
        )
    else:
        candidate_names = (name,)

    search_path = os.getenv("PATH", "") if path_value is None else path_value
    current_directory = _absolute_lexical_path(Path.cwd())
    for raw_directory in search_path.split(os.pathsep):
        directory_text = raw_directory.strip().strip('"')
        if not directory_text:
            continue
        directory = Path(os.path.expandvars(os.path.expanduser(directory_text)))
        if not directory.is_absolute():
            continue
        try:
            resolved_directory = directory.resolve(strict=True)
        except (OSError, RuntimeError):
            continue
        if _path_is_within(resolved_directory, project_root):
            continue

        for candidate_name in candidate_names:
            candidate = resolved_directory / candidate_name
            try:
                resolved_candidate = candidate.resolve(strict=True)
            except (OSError, RuntimeError):
                continue
            if _path_is_within(resolved_candidate, project_root):
                continue
            if _path_is_within(resolved_candidate, current_directory):
                continue
            if resolved_candidate.is_file() and os.access(resolved_candidate, os.X_OK):
                return str(candidate)
    return None


def resolve_project_root(value: str | Path) -> Path:
    try:
        project_root = _absolute_lexical_path(Path(value).resolve(strict=True))
    except (OSError, RuntimeError, ValueError) as exc:
        raise EnvironmentInputError("project root does not exist or cannot be resolved") from exc
    if not project_root.is_dir():
        raise EnvironmentInputError("project root must be a directory")
    return project_root


def _environment_variable_matches_prefix(name: str, prefix: Path) -> bool:
    value = os.getenv(name)
    if not value:
        return False
    return _paths_equal(_resolve_without_error(Path(value)), prefix)


def detect_python_environment(
    project_root: Path,
    *,
    executable: Path | None = None,
    prefix: Path | None = None,
    base_prefix: Path | None = None,
    has_real_prefix: bool | None = None,
) -> PythonEnvironment:
    active_executable = _resolve_without_error(executable or Path(sys.executable))
    active_prefix = _resolve_without_error(prefix or Path(sys.prefix))
    active_base_prefix = _resolve_without_error(base_prefix or Path(getattr(sys, "base_prefix", sys.prefix)))
    real_prefix_present = hasattr(sys, "real_prefix") if has_real_prefix is None else has_real_prefix
    conda_active = _environment_variable_matches_prefix("CONDA_PREFIX", active_prefix)
    virtual_env_active = _environment_variable_matches_prefix("VIRTUAL_ENV", active_prefix)
    prefix_isolated = not _paths_equal(active_prefix, active_base_prefix)
    environment_active = real_prefix_present or prefix_isolated or conda_active or virtual_env_active

    if conda_active:
        environment_kind = "conda"
    elif environment_active:
        environment_kind = "venv"
    else:
        environment_kind = "system"

    project_dot_venv = project_root / ".venv"
    resolved_project_dot_venv = _resolve_without_error(project_dot_venv)
    project_dot_venv_active = environment_active and (
        _path_is_within(active_executable, resolved_project_dot_venv)
        or _paths_equal(active_prefix, resolved_project_dot_venv)
    )
    return PythonEnvironment(
        virtual_environment_active=environment_active,
        environment_kind=environment_kind,
        project_dot_venv_active=project_dot_venv_active,
        project_dot_venv_exists=project_dot_venv.is_dir(),
    )


def _is_reparse_point(path: Path) -> bool:
    try:
        path_stat = os.lstat(path)
    except OSError as exc:
        raise EnvironmentInputError("helper lockfile path cannot be inspected") from exc
    attributes = getattr(path_stat, "st_file_attributes", 0)
    reparse_attribute = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(path_stat.st_mode) or bool(attributes & reparse_attribute)


def _reject_reparse_components(project_root: Path, lexical_path: Path) -> None:
    try:
        relative_parts = Path(os.path.relpath(lexical_path, project_root)).parts
    except ValueError as exc:
        raise EnvironmentInputError("helper lockfile must stay under project root") from exc
    current = project_root
    for part in relative_parts:
        if part in {"..", "."}:
            raise EnvironmentInputError("helper lockfile must stay under project root")
        current /= part
        if _is_reparse_point(current):
            raise EnvironmentInputError("helper lockfile path must not use symlinks or reparse points")


def _windows_extended_path(path: Path) -> str:
    value = os.fspath(path)
    if value.startswith("\\\\?\\"):
        return value
    if value.startswith("\\\\"):
        return "\\\\?\\UNC\\" + value[2:]
    return "\\\\?\\" + value


def _open_windows_lockfile(project_root: Path, lexical_path: Path) -> tuple[int, Path]:
    try:
        import ctypes
        import msvcrt
        from ctypes import wintypes

        class FileTime(ctypes.Structure):
            _fields_ = [
                ("dwLowDateTime", wintypes.DWORD),
                ("dwHighDateTime", wintypes.DWORD),
            ]

        class FileInformation(ctypes.Structure):
            _fields_ = [
                ("dwFileAttributes", wintypes.DWORD),
                ("ftCreationTime", FileTime),
                ("ftLastAccessTime", FileTime),
                ("ftLastWriteTime", FileTime),
                ("dwVolumeSerialNumber", wintypes.DWORD),
                ("nFileSizeHigh", wintypes.DWORD),
                ("nFileSizeLow", wintypes.DWORD),
                ("nNumberOfLinks", wintypes.DWORD),
                ("nFileIndexHigh", wintypes.DWORD),
                ("nFileIndexLow", wintypes.DWORD),
            ]

        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        create_file = kernel32.CreateFileW
        create_file.argtypes = [
            wintypes.LPCWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        create_file.restype = wintypes.HANDLE
        get_file_information = kernel32.GetFileInformationByHandle
        get_file_information.argtypes = [wintypes.HANDLE, ctypes.POINTER(FileInformation)]
        get_file_information.restype = wintypes.BOOL
        get_final_path = kernel32.GetFinalPathNameByHandleW
        get_final_path.argtypes = [
            wintypes.HANDLE,
            wintypes.LPWSTR,
            wintypes.DWORD,
            wintypes.DWORD,
        ]
        get_final_path.restype = wintypes.DWORD
        close_handle = kernel32.CloseHandle
        close_handle.argtypes = [wintypes.HANDLE]
        close_handle.restype = wintypes.BOOL

        invalid_handle = ctypes.c_void_p(-1).value
        file_read_attributes = 0x00000080
        generic_read = 0x80000000
        share_read = 0x00000001
        open_existing = 3
        file_attribute_directory = 0x00000010
        file_attribute_reparse_point = 0x00000400
        file_flag_open_reparse_point = 0x00200000
        file_flag_backup_semantics = 0x02000000
        file_flag_sequential_scan = 0x08000000

        def open_handle(path: Path, *, directory: bool) -> int:
            handle = create_file(
                _windows_extended_path(path),
                file_read_attributes if directory else generic_read,
                share_read,
                None,
                open_existing,
                file_flag_open_reparse_point
                | (file_flag_backup_semantics if directory else file_flag_sequential_scan),
                None,
            )
            if handle in (None, invalid_handle):
                raise EnvironmentInputError("helper lockfile cannot be opened safely")
            return int(handle)

        def inspect_handle(handle: int, *, directory: bool) -> FileInformation:
            information = FileInformation()
            if not get_file_information(handle, ctypes.byref(information)):
                raise EnvironmentInputError("helper lockfile path cannot be inspected")
            if information.dwFileAttributes & file_attribute_reparse_point:
                raise EnvironmentInputError(
                    "helper lockfile path must not use symlinks or reparse points"
                )
            is_directory = bool(information.dwFileAttributes & file_attribute_directory)
            if is_directory != directory:
                message = (
                    "helper lockfile path cannot be inspected"
                    if directory
                    else "helper lockfile must be a regular file"
                )
                raise EnvironmentInputError(message)
            return information

        def final_path_for_handle(handle: int) -> Path:
            required = get_final_path(handle, None, 0, 0)
            if required == 0:
                raise EnvironmentInputError("helper lockfile path cannot be inspected")
            buffer = ctypes.create_unicode_buffer(required + 1)
            written = get_final_path(handle, buffer, len(buffer), 0)
            if written == 0 or written >= len(buffer):
                raise EnvironmentInputError("helper lockfile path cannot be inspected")
            return _absolute_lexical_path(Path(buffer.value))

        relative_parent = Path(os.path.relpath(lexical_path.parent, project_root))
        directory_paths = [project_root]
        current = project_root
        if relative_parent != Path("."):
            for part in relative_parent.parts:
                if part in {".", ".."}:
                    raise EnvironmentInputError(
                        "helper lockfile must stay under project root"
                    )
                current /= part
                directory_paths.append(current)

        directory_handles: list[int] = []
        file_handle: int | None = None
        try:
            for directory_path in directory_paths:
                directory_handle = open_handle(directory_path, directory=True)
                directory_handles.append(directory_handle)
                inspect_handle(directory_handle, directory=True)
                if not _path_is_within(
                    final_path_for_handle(directory_handle),
                    project_root,
                ):
                    raise EnvironmentInputError(
                        "helper lockfile must stay under project root"
                    )

            file_handle = open_handle(lexical_path, directory=False)
            information = inspect_handle(file_handle, directory=False)
            if information.nNumberOfLinks != 1:
                raise EnvironmentInputError("helper lockfile must not be a hardlink")
            resolved_path = final_path_for_handle(file_handle)
            if not _path_is_within(resolved_path, project_root):
                raise EnvironmentInputError("helper lockfile must stay under project root")

            descriptor = msvcrt.open_osfhandle(
                file_handle,
                os.O_RDONLY | getattr(os, "O_BINARY", 0),
            )
            file_handle = None
            return descriptor, resolved_path
        finally:
            if file_handle is not None:
                close_handle(file_handle)
            for directory_handle in reversed(directory_handles):
                close_handle(directory_handle)
    except EnvironmentInputError:
        raise
    except (AttributeError, OSError, TypeError, ValueError) as exc:
        raise EnvironmentInputError("helper lockfile cannot be opened safely") from exc


def _open_posix_lockfile(project_root: Path, lexical_path: Path) -> tuple[int, Path]:
    nofollow = getattr(os, "O_NOFOLLOW", 0)
    directory_flag = getattr(os, "O_DIRECTORY", 0)
    if not nofollow or not directory_flag or os.open not in os.supports_dir_fd:
        raise EnvironmentInputError("secure helper lockfile traversal is unavailable")

    directory_flags = os.O_RDONLY | directory_flag | nofollow | getattr(os, "O_CLOEXEC", 0)
    file_flags = (
        os.O_RDONLY
        | nofollow
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_NONBLOCK", 0)
    )
    descriptors: list[int] = []
    file_descriptor: int | None = None
    try:
        root_descriptor = os.open(project_root, directory_flags)
        descriptors.append(root_descriptor)
        current_descriptor = root_descriptor
        relative_path = Path(os.path.relpath(lexical_path, project_root))
        if any(part in {".", ".."} for part in relative_path.parts):
            raise EnvironmentInputError("helper lockfile must stay under project root")

        for part in relative_path.parts[:-1]:
            component = os.stat(part, dir_fd=current_descriptor, follow_symlinks=False)
            if stat.S_ISLNK(component.st_mode):
                raise EnvironmentInputError(
                    "helper lockfile path must not use symlinks or reparse points"
                )
            next_descriptor = os.open(part, directory_flags, dir_fd=current_descriptor)
            if not stat.S_ISDIR(os.fstat(next_descriptor).st_mode):
                os.close(next_descriptor)
                raise EnvironmentInputError("helper lockfile path cannot be inspected")
            descriptors.append(next_descriptor)
            current_descriptor = next_descriptor

        final_name = relative_path.parts[-1]
        component = os.stat(final_name, dir_fd=current_descriptor, follow_symlinks=False)
        if stat.S_ISLNK(component.st_mode):
            raise EnvironmentInputError(
                "helper lockfile path must not use symlinks or reparse points"
            )
        file_descriptor = os.open(final_name, file_flags, dir_fd=current_descriptor)
        if not stat.S_ISREG(os.fstat(file_descriptor).st_mode):
            raise EnvironmentInputError("helper lockfile must be a regular file")
        descriptor = file_descriptor
        file_descriptor = None
        return descriptor, lexical_path
    except EnvironmentInputError:
        raise
    except OSError as exc:
        raise EnvironmentInputError("helper lockfile cannot be opened safely") from exc
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        for descriptor in reversed(descriptors):
            os.close(descriptor)


def _open_lockfile_descriptor(
    project_root: Path,
    lexical_path: Path,
) -> tuple[int, Path]:
    if os.name == "nt":
        return _open_windows_lockfile(project_root, lexical_path)
    return _open_posix_lockfile(project_root, lexical_path)


def _lockfile_stat_signature(file_stat: os.stat_result) -> tuple[int, ...]:
    return (
        file_stat.st_dev,
        file_stat.st_ino,
        file_stat.st_mode,
        file_stat.st_nlink,
        file_stat.st_size,
        file_stat.st_mtime_ns,
        file_stat.st_ctime_ns,
    )


def _read_lockfile_pass(descriptor: int, *, max_bytes: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks: list[bytes] = []
    remaining = max_bytes + 1
    while remaining:
        chunk = os.read(descriptor, min(64 * 1024, remaining))
        if not chunk:
            break
        chunks.append(chunk)
        remaining -= len(chunk)
    return b"".join(chunks)


def _read_stable_lockfile(descriptor: int, *, max_bytes: int) -> bytes:
    try:
        if os.name != "nt":
            try:
                import fcntl

                fcntl.flock(descriptor, fcntl.LOCK_SH | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise EnvironmentInputError(
                    "helper lockfile is being modified"
                ) from exc
            except (AttributeError, ImportError, OSError):
                pass

        opened_before = os.fstat(descriptor)
        if not stat.S_ISREG(opened_before.st_mode):
            raise EnvironmentInputError("helper lockfile must be a regular file")
        if opened_before.st_nlink != 1:
            raise EnvironmentInputError("helper lockfile must not be a hardlink")
        if opened_before.st_size > max_bytes:
            raise EnvironmentInputError(f"helper lockfile exceeds the {max_bytes}-byte limit")

        content = _read_lockfile_pass(descriptor, max_bytes=max_bytes)
        opened_between = os.fstat(descriptor)
        verification_content = _read_lockfile_pass(descriptor, max_bytes=max_bytes)
        opened_after = os.fstat(descriptor)

        if opened_between.st_nlink != 1 or opened_after.st_nlink != 1:
            raise EnvironmentInputError("helper lockfile must not be a hardlink")
        if (
            not os.path.samestat(opened_before, opened_between)
            or not os.path.samestat(opened_between, opened_after)
            or _lockfile_stat_signature(opened_before)
            != _lockfile_stat_signature(opened_between)
            or _lockfile_stat_signature(opened_between)
            != _lockfile_stat_signature(opened_after)
            or content != verification_content
            or len(content) != opened_before.st_size
        ):
            raise EnvironmentInputError("helper lockfile changed during validation")
    except EnvironmentInputError:
        raise
    except OSError as exc:
        raise EnvironmentInputError("helper lockfile cannot be read") from exc

    if len(content) > max_bytes:
        raise EnvironmentInputError(f"helper lockfile exceeds the {max_bytes}-byte limit")
    return content


def fingerprint_helper_lockfile(
    project_root: Path,
    value: str | Path,
    *,
    max_bytes: int = MAX_LOCKFILE_BYTES,
) -> LockfileFingerprint:
    if max_bytes < 1:
        raise EnvironmentInputError("helper lockfile byte limit must be positive")
    project_root = resolve_project_root(project_root)
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = project_root / candidate
    lexical_path = _absolute_lexical_path(candidate)
    if not _path_is_within(lexical_path, project_root):
        raise EnvironmentInputError("helper lockfile must stay under project root")
    if lexical_path.name.lower() not in PUBLIC_HELPER_LOCKFILES:
        raise EnvironmentInputError("helper lockfile name is not a supported public lockfile")

    descriptor, resolved_path = _open_lockfile_descriptor(project_root, lexical_path)
    try:
        if not _path_is_within(resolved_path, project_root):
            raise EnvironmentInputError("helper lockfile must stay under project root")
        content = _read_stable_lockfile(descriptor, max_bytes=max_bytes)
    finally:
        os.close(descriptor)

    relative_path = Path(os.path.relpath(lexical_path, project_root)).as_posix()
    return LockfileFingerprint(
        relative_path=relative_path,
        byte_length=len(content),
        sha256=hashlib.sha256(content).hexdigest(),
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        default=".",
        metavar="PATH",
        help="existing project directory to compare with its .venv (default: current directory)",
    )
    parser.add_argument(
        "--helper-lockfile",
        action="append",
        default=[],
        metavar="PATH",
        help="explicit public dependency lockfile under the project root; repeat as needed",
    )
    parser.add_argument(
        "--require-project-venv",
        action="store_true",
        help="return exit status 1 unless this interpreter is under PROJECT_ROOT/.venv",
    )
    return parser


def _yes_no(value: bool) -> str:
    return "yes" if value else "no"


def _configure_output_streams() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            try:
                reconfigure(errors="backslashreplace")
            except (OSError, ValueError):
                pass


def main(argv: Sequence[str] | None = None) -> int:
    _configure_output_streams()
    args = build_parser().parse_args(argv)
    try:
        project_root = resolve_project_root(args.project_root)
        lockfiles = [
            fingerprint_helper_lockfile(project_root, value)
            for value in args.helper_lockfile
        ]
    except EnvironmentInputError as exc:
        print(f"environment_check_error: {exc}", file=sys.stderr)
        return 2

    python_environment = detect_python_environment(project_root)
    discovered_tools = {
        name: discover_path_tool(name, project_root)
        for name in TOOL_NAMES
    }

    print("reverse environment")
    python_version = ".".join(str(item) for item in sys.version_info[:3])
    print(f"- python_version: {python_version}")
    print(f"- python: {command_status(sys.executable)}")
    for name in TOOL_NAMES:
        print(f"- {name}: {command_status(discovered_tools[name])}")
    print(f"- node_version: {command_version(discovered_tools['node'])}")
    print(f"- npm_version: {command_version(discovered_tools['npm'])}")
    print("project environment")
    print(f"- project_root: {project_root}")
    print(f"- virtual_environment_active: {_yes_no(python_environment.virtual_environment_active)}")
    print(f"- virtual_environment_kind: {python_environment.environment_kind}")
    print(f"- project_dot_venv_exists: {_yes_no(python_environment.project_dot_venv_exists)}")
    print(f"- project_dot_venv_active: {_yes_no(python_environment.project_dot_venv_active)}")
    print(f"- project_dot_venv_requirement: {'strict' if args.require_project_venv else 'advisory'}")
    if python_environment.project_dot_venv_active:
        print("- project_dot_venv_warning: none")
    else:
        print("- project_dot_venv_warning: active interpreter is not under the project .venv")
    print("helper lockfile fingerprints")
    if lockfiles:
        for item in lockfiles:
            print(
                f"- helper_lockfile: {item.relative_path} "
                f"bytes={item.byte_length} sha256={item.sha256}"
            )
    else:
        print("- helper_lockfiles: none_requested")
    for name in PYTHON_MODULES:
        print(f"- python_module_{name}: {module_status(name)}")
    print("python package compatibility")
    for name in PYTHON_DISTRIBUTIONS:
        print(f"- python_distribution_{name}: {distribution_version(name)}")
    notes = requests_dependency_notes()
    if notes:
        for note in notes:
            print(f"- requests_dependency_warning: {note}")
    else:
        print("- requests_dependency_warning: none")
    print("transport and proxy context")
    print(f"- curl_cffi_default_chrome: {curl_cffi_default_chrome()}")
    print(f"- curl_cffi_chrome_impersonate: {curl_cffi_chrome_impersonate_profile()}")
    for name in PROXY_ENV_VARS:
        configured = bool(os.getenv(name) or os.getenv(name.lower()))
        print(f"- proxy_env_{name}: {'set' if configured else 'unset'}")
    print("agent capability gate")
    for name in AGENT_CAPABILITIES:
        print(f"- {name}: not_checkable_from_local_python")
    print("intake mode gate")
    print("- live-target: probe both capabilities and record the active agent capability snapshot")
    print("- artifact-only: browser probing is not required unless the next claim depends on live evidence")
    print("- continuation: reuse the current capability snapshot unless the registry, browser mode, or target context changed")
    print("- startup_gate_complete: depends_on_intake_mode_and_required_evidence")
    print("notes")
    print("- pure Python protocol replay should work with Python alone")
    print("- node is useful for preserving tiny JS helpers")
    print("- iv8 or another embedded runtime is useful when JS needs host semantics without a real browser")
    print("- curl is useful for quick raw request diffs")
    print("- this script validates local dependencies only; it cannot complete an agent-side live-target capability snapshot")
    if args.require_project_venv and not python_environment.project_dot_venv_active:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
