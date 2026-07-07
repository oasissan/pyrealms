"""Curriculum integrity tests.

The important one: every mission's *canonical solution* (the code revealed
after a pass, stored in ``solution_md``) is run against that mission's own
hidden pytest suite and must pass. This makes solution rot impossible — if a
model answer stops matching its tests, CI goes red.
"""

import pytest

from app.content import ALL_TIERS, META_ACHIEVEMENTS, iter_missions, solution_code
from app.grading import run_hidden_tests

MISSIONS = [
    pytest.param(m, id=f"{t['slug']}/{m['slug']}")
    for t in ALL_TIERS
    for q in t["quests"]
    for m in q["missions"]
]


@pytest.mark.parametrize("mission", MISSIONS)
def test_every_mission_has_a_canonical_solution(mission):
    assert mission.get("solution_md"), f"{mission['slug']} is missing solution_md"
    assert solution_code(mission["solution_md"]), (
        f"{mission['slug']} solution_md has no ```python code block"
    )


@pytest.mark.parametrize("mission", MISSIONS)
def test_canonical_solution_passes_hidden_suite(mission):
    code = solution_code(mission["solution_md"])
    result = run_hidden_tests(code, mission["hidden_tests"])
    assert result.passed, (
        f"canonical solution for {mission['slug']} failed its own suite: "
        f"{result.failing_tests or result.output}"
    )


@pytest.mark.parametrize("mission", MISSIONS)
def test_example_tests_only_on_non_boss(mission):
    """Bosses stay fully hidden — no visible example tests."""
    if mission["kind"] in ("boss", "tier_boss"):
        assert not mission.get("example_tests"), (
            f"{mission['slug']} is a boss but exposes example_tests"
        )


@pytest.mark.parametrize("mission", MISSIONS)
def test_visible_example_tests_are_consistent(mission):
    """If a standard mission shows example tests, the canonical solution must
    satisfy them too (they're a genuine subset of the real checks)."""
    example = mission.get("example_tests")
    if not example:
        return
    code = solution_code(mission["solution_md"])
    result = run_hidden_tests(code, example)
    assert result.passed, (
        f"example tests for {mission['slug']} don't pass the canonical solution"
    )


def test_all_slugs_unique():
    slugs = [m["slug"] for m in iter_missions()]
    assert len(slugs) == len(set(slugs)), "duplicate mission slug"


def test_all_badge_ids_unique():
    """badge_id is UNIQUE in the DB — a collision across quests/meta would make
    seeding an AchievementRule blow up. Catch it in content, not at runtime."""
    badge_ids = [
        q["badge"]["id"]
        for t in ALL_TIERS
        for q in t["quests"]
        if q.get("badge")
    ]
    badge_ids += [m["badge_id"] for m in META_ACHIEVEMENTS]
    dupes = {b for b in badge_ids if badge_ids.count(b) > 1}
    assert not dupes, f"duplicate badge_id(s): {dupes}"
