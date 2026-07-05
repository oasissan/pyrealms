"""Run submitted code against a challenge's hidden pytest suite in a
subprocess with a timeout and (on Unix) a memory cap. Not a security sandbox —
acceptable for solo local use only, per the design spec.

Grading produces a structured per-test report (call made, expected value,
actual value, or crash details pointing at the learner's own code) by
injecting a small pytest reporter plugin (conftest.py) into the sandbox
directory. Raw pytest output is kept as a fallback."""

import json
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

TIMEOUT_SECONDS = 5
MEMORY_LIMIT_BYTES = 512 * 1024 * 1024

# Written into the sandbox next to solution.py/test_solution.py. Captures the
# real exception objects via hooks — far more reliable than regexing pytest's
# terminal output.
_REPORTER_CONFTEST = '''\
import json
import pytest

RESULTS = []


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "setup" and report.failed:
        RESULTS.append({
            "name": item.name,
            "outcome": "failed",
            "raw": str(report.longrepr),
        })
        return
    if report.when != "call":
        return
    entry = {"name": item.name, "outcome": "passed" if report.passed else "failed"}
    if report.failed and call.excinfo is not None:
        entry["error_type"] = call.excinfo.typename
        if call.excinfo.errisinstance(AssertionError):
            entry["assertion"] = str(call.excinfo.value)
        else:
            entry["error_message"] = str(call.excinfo.value)
            for tb_entry in reversed(call.excinfo.traceback):
                if str(tb_entry.path).endswith("solution.py"):
                    entry["user_line_no"] = tb_entry.lineno + 1
                    try:
                        entry["user_line"] = str(tb_entry.statement).strip()
                    except Exception:
                        pass
                    break
    RESULTS.append(entry)


def pytest_sessionfinish(session, exitstatus):
    with open("report.json", "w") as f:
        json.dump(RESULTS, f)
'''

# Matches pytest's rewritten-assertion explanation lines like
# " +  where 5 = solve([1, 2, 3])" or " +  and 6 = int('6')".
_WHERE_RE = re.compile(r"^\s*\+\s*(?:where|and)\s+(?P<value>.+?) = (?P<expr>.+)$")
_CMP_RE = re.compile(r"^assert (?P<left>.+?) == (?P<right>.+)$")


@dataclass
class SyntaxIssue:
    message: str
    line_no: int | None = None
    offset: int | None = None
    text: str = ""


@dataclass
class TestCaseResult:
    name: str
    outcome: str  # "passed" | "failed"
    call: str | None = None
    expected: str | None = None
    got: str | None = None
    error_type: str | None = None
    error_message: str | None = None
    user_line_no: int | None = None
    user_line: str | None = None
    detail: str | None = None

    @property
    def label(self) -> str:
        """Human name: test_basic_sum -> 'basic sum'."""
        return self.name.removeprefix("test_").replace("_", " ")


@dataclass
class GradeResult:
    passed: bool
    output: str
    failing_tests: list[str] = field(default_factory=list)
    timed_out: bool = False
    tests: list[TestCaseResult] = field(default_factory=list)
    syntax_error: SyntaxIssue | None = None

    @property
    def total(self) -> int:
        return len(self.tests)

    @property
    def passed_count(self) -> int:
        return sum(1 for t in self.tests if t.outcome == "passed")


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


def check_syntax(code: str) -> SyntaxIssue | None:
    """Compile (never execute) the learner's code to catch syntax errors
    before spawning pytest — gives exact line/offset for a caret pointer."""
    try:
        compile(code, "solution.py", "exec")
    except SyntaxError as exc:
        return SyntaxIssue(
            message=exc.msg or "invalid syntax",
            line_no=exc.lineno,
            offset=exc.offset,
            text=(exc.text or "").rstrip("\n"),
        )
    except ValueError as exc:
        return SyntaxIssue(message=str(exc))
    return None


def _parse_assertion(explanation: str) -> dict:
    """Turn pytest's rewritten-assert explanation into call/expected/got.

    'assert 5 == 6\\n +  where 5 = solve([1, 2, 3])' becomes
    {call: 'solve([1, 2, 3])', got: '5', expected: '6'}. Anything that
    doesn't fit the simple `assert <call> == <value>` shape falls back to
    the cleaned explanation text in `detail`.
    """
    lines = [line for line in explanation.splitlines() if line.strip()]
    assert_line = next(
        (line for line in lines if line.lstrip().startswith("assert ")), None
    )
    where = {}
    for line in lines:
        m = _WHERE_RE.match(line)
        if m:
            where[m.group("value").strip()] = m.group("expr").strip()

    if assert_line:
        m = _CMP_RE.match(assert_line.strip())
        if m:
            left, right = m.group("left").strip(), m.group("right").strip()
            if left in where and "(" in where[left]:
                return {"call": where[left], "got": left, "expected": right}
            if right in where and "(" in where[right]:
                return {"call": where[right], "got": right, "expected": left}
            return {"got": left, "expected": right}
    return {"detail": explanation.strip()}


def _build_test_results(entries: list[dict]) -> list[TestCaseResult]:
    results = []
    for entry in entries:
        result = TestCaseResult(
            name=entry.get("name", "?"), outcome=entry.get("outcome", "failed")
        )
        result.error_type = entry.get("error_type")
        result.error_message = entry.get("error_message")
        result.user_line_no = entry.get("user_line_no")
        result.user_line = entry.get("user_line")
        result.detail = entry.get("raw")
        if "assertion" in entry:
            parsed = _parse_assertion(entry["assertion"])
            result.call = parsed.get("call")
            result.expected = parsed.get("expected")
            result.got = parsed.get("got")
            result.detail = parsed.get("detail")
        results.append(result)
    return results


def run_hidden_tests(code: str, hidden_tests: str) -> GradeResult:
    syntax_error = check_syntax(code)
    if syntax_error is not None:
        return GradeResult(
            passed=False,
            output=f"SyntaxError: {syntax_error.message} (line {syntax_error.line_no})",
            syntax_error=syntax_error,
        )

    with tempfile.TemporaryDirectory() as tmp:
        tmpdir = Path(tmp)
        (tmpdir / "solution.py").write_text(code)
        (tmpdir / "test_solution.py").write_text(hidden_tests)
        (tmpdir / "conftest.py").write_text(_REPORTER_CONFTEST)
        try:
            proc = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pytest",
                    "test_solution.py",
                    "-q",
                    "--tb=short",
                    "--color=no",
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

        tests: list[TestCaseResult] = []
        report_file = tmpdir / "report.json"
        if report_file.exists():
            try:
                tests = _build_test_results(json.loads(report_file.read_text()))
            except (json.JSONDecodeError, OSError):
                tests = []

        if tests:
            failing = [t.name for t in tests if t.outcome != "passed"]
        else:
            failing = sorted(
                set(re.findall(r"(?:FAILED|ERROR) test_solution\.py::(\w+)", output))
            )
        return GradeResult(
            passed=proc.returncode == 0,
            output=output,
            failing_tests=failing,
            tests=tests,
        )
