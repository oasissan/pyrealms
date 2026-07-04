from . import tier1, tier2, tier3

ALL_TIERS = [tier1.TIER, tier2.TIER, tier3.TIER]

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
