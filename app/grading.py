"""Run submitted code against a challenge's hidden pytest suite in a
subprocess with a timeout and (on Unix) a memory cap. Not a security sandbox —
acceptable for solo local use only, per the design spec."""

import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

TIMEOUT_SECONDS = 5
MEMORY_LIMIT_BYTES = 512 * 1024 * 1024


@dataclass
class GradeResult:
    passed: bool
    output: str
    failing_tests: list[str] = field(default_factory=list)
    timed_out: bool = False


def _set_limits():  # pragma: no cover - runs in the child process
    try:
        import resource

        resource.setrlimit(
            resource.RLIMIT_AS, (MEMORY_LIMIT_BYTES, MEMORY_LIMIT_BYTES)
        )
        resource.setrlimit(resource.RLIMIT_CPU, (TIMEOUT_SECONDS, TIMEOUT_SECONDS + 1))
    except (ImportError, ValueError, OSError):
        # RLIMIT_AS is unreliable on macOS; the wall-clock timeout still applies.
        pass


def run_hidden_tests(code: str, hidden_tests: str) -> GradeResult:
    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        (tmpdir / "solution.py").write_text(code)
        (tmpdir / "test_solution.py").write_text(hidden_tests)
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "test_solution.py",
                    "-q",
                    "--tb=short",
                    "-p",
                    "no:cacheprovider",
                ],
                cwd=tmpdir,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                preexec_fn=_set_limits if sys.platform != "win32" else None,
            )
        except subprocess.TimeoutExpired:
            return GradeResult(
                passed=False,
                output=f"⏱ Time limit exceeded ({TIMEOUT_SECONDS}s). "
                "Check for infinite loops or blocking calls.",
                timed_out=True,
            )

        output = (proc.stdout + "\n" + proc.stderr).strip()
        failing = re.findall(r"(?:FAILED|ERROR) test_solution\.py::(\w+)", output)
        return GradeResult(
            passed=proc.returncode == 0,
            output=output,
            failing_tests=sorted(set(failing)),
        )
