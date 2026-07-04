"""XP -> level math. Level 1 starts at 0 XP; the XP needed to advance grows
by 50 per level (100, 150, 200, ...), a gentle goal-gradient curve."""

MAX_LEVEL = 50


def xp_to_advance(level: int) -> int:
    """XP required to go from `level` to `level + 1`."""
    return 100 + 50 * (level - 1)


def threshold_for_level(level: int) -> int:
    """Cumulative XP required to reach `level`."""
    return sum(xp_to_advance(l) for l in range(1, level))


def level_for_xp(xp: int) -> int:
    level = 1
    while level < MAX_LEVEL and xp >= threshold_for_level(level + 1):
        level += 1
    return level


def level_progress(xp: int) -> dict:
    """Progress within the current level, for the XP bar."""
    level = level_for_xp(xp)
    floor = threshold_for_level(level)
    ceiling = threshold_for_level(level + 1)
    span = ceiling - floor
    into = xp - floor
    return {
        "level": level,
        "xp": xp,
        "into_level": into,
        "level_span": span,
        "percent": min(100, round(100 * into / span)) if span else 100,
        "next_level_at": ceiling,
    }
