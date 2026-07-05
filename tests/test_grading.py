"""Tests for the structured grading report: parsing pytest results into
per-test cards (call / expected / got), crash details pointing at the
learner's code, syntax-error pre-checks, and timeouts."""

import pytest

from app import grading
from app.grading import run_hidden_tests

HIDDEN = """\
from solution import solve

def test_basic_sum():
    assert solve([1, 2, 3]) == 6

def test_empty_list():
    assert solve([]) == 0
"""


def test_all_pass_reports_every_test():
    result = run_hidden_tests(
        "def solve(nums):\n    return sum(nums)\n", HIDDEN
    )
    assert result.passed
    assert result.syntax_error is None
    assert len(result.tests) == 2
    assert all(t.outcome == "passed" for t in result.tests)
    assert result.passed_count == 2
    assert result.total == 2


def test_wrong_answer_parses_call_expected_got():
    result = run_hidden_tests(
        "def solve(nums):\n    return sum(nums) + 1\n", HIDDEN
    )
    assert not result.passed
    failed = {t.name: t for t in result.tests if t.outcome == "failed"}
    assert set(failed) == {"test_basic_sum", "test_empty_list"}
    basic = failed["test_basic_sum"]
    assert basic.call == "solve([1, 2, 3])"
    assert basic.expected == "6"
    assert basic.got == "7"
    assert result.failing_tests == ["test_basic_sum", "test_empty_list"]


def test_exception_reports_user_line():
    result = run_hidden_tests(
        "def solve(nums):\n    total = nums[0]\n    return total\n", HIDDEN
    )
    failed = {t.name: t for t in result.tests if t.outcome == "failed"}
    crash = failed["test_empty_list"]
    assert crash.error_type == "IndexError"
    assert "out of range" in crash.error_message
    assert crash.user_line_no == 2
    assert crash.user_line == "total = nums[0]"


def test_syntax_error_precheck_short_circuits():
    result = run_hidden_tests("def solve(nums:\n    return 0\n", HIDDEN)
    assert not result.passed
    assert result.tests == []
    assert result.syntax_error is not None
    assert result.syntax_error.line_no == 1
    assert "def solve(nums:" in result.syntax_error.text


def test_non_comparison_assert_falls_back_to_detail():
    hidden = """\
from solution import solve

def test_returns_float():
    assert isinstance(solve(0), float)
"""
    result = run_hidden_tests("def solve(x):\n    return 3\n", hidden)
    failed = result.tests[0]
    assert failed.outcome == "failed"
    assert failed.call is None
    assert failed.detail and "isinstance" in failed.detail


def test_timeout(monkeypatch):
    monkeypatch.setattr(grading, "TIMEOUT_SECONDS", 2)
    result = run_hidden_tests(
        "def solve(nums):\n    while True:\n        pass\n", HIDDEN
    )
    assert not result.passed
    assert result.timed_out
