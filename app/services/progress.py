"""Unlock and progress computation for the skill-tree map.

Rules (from the design spec):
- Tier 1 is always unlocked. Tier N unlocks when tier N-1's Boss Battle is
  passed AND the current level meets the tier's min_level.
- Within an unlocked tier, regular quests are all open (Free Spirit
  autonomy); the tier's Boss Battle quest unlocks once every other quest in
  the tier is complete.
- Within a quest, challenges unlock sequentially.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ..models import Challenge, Quest, Submission, Tier


def passed_challenge_ids(db: Session) -> set[int]:
    return set(
        db.execute(
            select(Submission.challenge_id).where(Submission.passed.is_(True)).distinct()
        ).scalars()
    )


def attempts_count(db: Session, challenge_id: int) -> int:
    return len(
        db.execute(
            select(Submission.id).where(Submission.challenge_id == challenge_id)
        ).scalars().all()
    )


def personal_best(db: Session, challenge_id: int) -> dict | None:
    """Best (fastest) passing solve and attempts-to-first-pass."""
    passes = (
        db.execute(
            select(Submission)
            .where(
                Submission.challenge_id == challenge_id,
                Submission.passed.is_(True),
            )
            .order_by(Submission.created_at)
        )
        .scalars()
        .all()
    )
    if not passes:
        return None
    first_pass = passes[0]
    attempts_to_first = len(
        db.execute(
            select(Submission.id).where(
                Submission.challenge_id == challenge_id,
                Submission.created_at <= first_pass.created_at,
            )
        ).scalars().all()
    )
    timed = [p.duration_seconds for p in passes if p.duration_seconds is not None]
    return {
        "attempts_to_first_pass": attempts_to_first,
        "best_time_seconds": min(timed) if timed else None,
        "times_solved": len(passes),
    }


def build_map(db: Session, current_level: int) -> list[dict]:
    """Full map state: every tier/quest/challenge with unlock + progress."""
    tiers = (
        db.execute(
            select(Tier)
            .options(selectinload(Tier.quests).selectinload(Quest.challenges))
            .order_by(Tier.order)
        )
        .scalars()
        .all()
    )
    passed = passed_challenge_ids(db)

    map_state = []
    previous_tier_boss_passed = True  # nothing gates tier 1
    for tier in tiers:
        tier_unlocked = previous_tier_boss_passed and current_level >= tier.min_level
        regular_quests = [q for q in tier.quests if not q.is_boss_battle]
        regular_complete = all(
            all(c.id in passed for c in q.challenges) for q in regular_quests
        )

        quest_states = []
        tier_total = 0
        tier_passed = 0
        tier_boss_passed = False
        for quest in tier.quests:
            quest_unlocked = tier_unlocked and (
                not quest.is_boss_battle or regular_complete
            )
            challenge_states = []
            prev_passed = True
            for challenge in quest.challenges:
                is_passed = challenge.id in passed
                challenge_states.append(
                    {
                        "challenge": challenge,
                        "passed": is_passed,
                        "unlocked": quest_unlocked and prev_passed,
                    }
                )
                prev_passed = is_passed
                tier_total += 1
                tier_passed += is_passed
                if challenge.kind == "tier_boss" and is_passed:
                    tier_boss_passed = True
            done = sum(c["passed"] for c in challenge_states)
            quest_states.append(
                {
                    "quest": quest,
                    "unlocked": quest_unlocked,
                    "done": done,
                    "total": len(challenge_states),
                    "complete": done == len(challenge_states),
                    "challenges": challenge_states,
                }
            )

        map_state.append(
            {
                "tier": tier,
                "unlocked": tier_unlocked,
                "locked_by_level": previous_tier_boss_passed
                and current_level < tier.min_level,
                "done": tier_passed,
                "total": tier_total,
                "percent": round(100 * tier_passed / tier_total) if tier_total else 0,
                "quests": quest_states,
            }
        )
        previous_tier_boss_passed = tier_boss_passed

    return map_state


def challenge_state(db: Session, challenge: Challenge, current_level: int) -> dict:
    """Unlock/progress state for one challenge, reusing the map computation."""
    for tier_state in build_map(db, current_level):
        for quest_state in tier_state["quests"]:
            for c_state in quest_state["challenges"]:
                if c_state["challenge"].id == challenge.id:
                    return c_state
    raise ValueError(f"challenge {challenge.slug} not found in map")
