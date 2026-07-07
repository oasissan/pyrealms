import re

from . import tier1, tier2, tier3, tier4, tier5, tier6

ALL_TIERS = [tier1.TIER, tier2.TIER, tier3.TIER, tier4.TIER, tier5.TIER, tier6.TIER]

_CODE_FENCE_RE = re.compile(r"```(?:python)?\n(.*?)```", re.DOTALL)


def iter_missions():
    """Yield every mission dict across all tiers, for seeding and tests."""
    for tier in ALL_TIERS:
        for quest in tier["quests"]:
            for mission in quest["missions"]:
                yield mission


def teaching_quests(tier):
    """The quests in a tier that carry a lesson and therefore a quiz — every
    quest except the single-mission boss-battle quest that gates the tier."""
    return [q for q in tier["quests"] if not q.get("is_boss_battle")]


def iter_quiz_questions():
    """Yield (quest, order, question_dict) for every MCQ across all tiers, for
    seeding and tests. Order is 1-based within each quest."""
    for tier in ALL_TIERS:
        for quest in teaching_quests(tier):
            for order, question in enumerate(quest.get("quiz", []), start=1):
                yield quest, order, question


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
