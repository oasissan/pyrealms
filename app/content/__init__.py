import re

from . import tier1, tier2, tier3, tier4

ALL_TIERS = [tier1.TIER, tier2.TIER, tier3.TIER, tier4.TIER]

_CODE_FENCE_RE = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)


def iter_missions():
    """Yield every mission dict across all tiers, for seeding and tests."""
    for tier in ALL_TIERS:
        for quest in tier["quests"]:
            for mission in quest["missions"]:
                yield mission


def solution_code(solution_md: str) -> str | None:
    """Extract the runnable Python from a mission's ``solution_md`` — the
    first ```python fenced block. Returns None if there isn't one."""
    if not solution_md:
        return None
    match = _CODE_FENCE_RE.search(solution_md)
    return match.group(1) if match else None

META_ACHIEVEMENTS = [
    {
        "badge_id": "first-blood",
        "name": "First Blood",
        "icon": "🩸",
        "description": "Pass your first challenge.",
        "trigger_event": "challenge_passed",
        "condition": {"passed_count": 1},
    },
    {
        "badge_id": "double-digits",
        "name": "Double Digits",
        "icon": "🔟",
        "description": "Pass 10 distinct challenges.",
        "trigger_event": "challenge_passed",
        "condition": {"passed_count": 10},
    },
    {
        "badge_id": "week-warrior",
        "name": "Week Warrior",
        "icon": "🔥",
        "description": "Keep a 7-day practice streak.",
        "trigger_event": "streak_updated",
        "condition": {"streak": 7},
    },
]
