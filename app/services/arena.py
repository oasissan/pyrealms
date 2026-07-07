"""Mock Interview Arena: build a timed, randomized session from the existing
question banks and grade its rounds.

Rounds are drawn from content that already exists — MCQ rounds from the
``QuizQuestion`` bank, coding rounds from boss/tier-boss ``Challenge`` rows —
filtered by difficulty to a set of tiers. Coding rounds are graded through the
same ``run_hidden_tests`` path as normal missions. A correct round awards a
little XP through the idempotent ledger (keyed by session + round), and the
session score is recomputed from its rounds rather than incremented.
"""

import random
from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import (
    Challenge,
    InterviewRound,
    InterviewSession,
    Quest,
    QuizQuestion,
    Tier,
)
from . import xp

# Which tier orders each difficulty draws from.
DIFFICULTY_TIERS: dict[str, list[int]] = {
    "standard": [2, 3],
    "expert": [4, 5, 6],
}
CODING_KINDS = ("boss", "tier_boss")
XP_PER_ROUND = 15


def _coding_pool(db: Session, tier_orders: list[int]) -> list[int]:
    return list(
        db.execute(
            select(Challenge.id)
            .join(Quest, Challenge.quest_id == Quest.id)
            .join(Tier, Quest.tier_id == Tier.id)
            .where(Challenge.kind.in_(CODING_KINDS), Tier.order.in_(tier_orders))
        ).scalars()
    )


def _mcq_pool(db: Session, tier_orders: list[int]) -> list[int]:
    return list(
        db.execute(
            select(QuizQuestion.id)
            .join(Quest, QuizQuestion.quest_id == Quest.id)
            .join(Tier, Quest.tier_id == Tier.id)
            .where(Tier.order.in_(tier_orders))
        ).scalars()
    )


def _select_rounds(
    coding: list[int], mcq: list[int], n: int
) -> list[tuple[str, int]]:
    """Pick ``n`` (kind, ref_id) rounds, guaranteeing a mix when both pools
    exist. Picks with replacement so a small question bank can still fill a
    longer session; a large bank makes repeats vanishingly unlikely."""
    picks: list[tuple[str, int]] = []
    if coding and len(picks) < n:
        picks.append(("coding", random.choice(coding)))
    if mcq and len(picks) < n:
        picks.append(("mcq", random.choice(mcq)))
    combined = [("coding", c) for c in coding] + [("mcq", q) for q in mcq]
    while len(picks) < n and combined:
        picks.append(random.choice(combined))
    random.shuffle(picks)
    return picks[:n]


def start_session(
    db: Session, difficulty: str, num_questions: int
) -> InterviewSession:
    tier_orders = DIFFICULTY_TIERS.get(difficulty, DIFFICULTY_TIERS["standard"])
    picks = _select_rounds(
        _coding_pool(db, tier_orders), _mcq_pool(db, tier_orders), num_questions
    )
    session = InterviewSession(
        difficulty=difficulty,
        num_questions=len(picks),
        total=len(picks),
    )
    db.add(session)
    db.flush()
    for order, (kind, ref_id) in enumerate(picks, start=1):
        db.add(
            InterviewRound(
                session_id=session.id,
                order=order,
                kind=kind,
                ref_id=ref_id,
                points=1,
            )
        )
    db.commit()
    return session


def current_round(db: Session, session: InterviewSession) -> InterviewRound | None:
    """The next unanswered round (lowest order), or None when the session is
    complete."""
    for round_ in session.rounds:
        if round_.answer is None:
            return round_
    return None


def _safe_int(value: str | None) -> int | None:
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def grade_round(
    db: Session,
    round_: InterviewRound,
    answer: str,
    elapsed_seconds: float | None = None,
) -> bool:
    """Grade a round, record the answer, and award XP once on a correct pick."""
    round_.answer = answer if answer is not None else ""
    round_.elapsed_seconds = elapsed_seconds

    if round_.kind == "mcq":
        question = db.get(QuizQuestion, round_.ref_id)
        correct = question is not None and _safe_int(answer) == question.correct_index
    else:
        from ..grading import run_hidden_tests

        challenge = db.get(Challenge, round_.ref_id)
        correct = challenge is not None and run_hidden_tests(
            answer or "", challenge.hidden_tests
        ).passed

    round_.correct = correct
    if correct:
        xp.award_xp(
            db,
            event_type="arena_round",
            delta=XP_PER_ROUND,
            idempotency_key=f"arena:{round_.session_id}:{round_.order}",
            meta={"kind": round_.kind, "ref_id": round_.ref_id},
        )
    db.commit()
    return correct


def finish_if_done(db: Session, session: InterviewSession) -> None:
    """Once every round is answered, stamp finished_at and recompute the score
    from the rounds. No-op while rounds remain."""
    if any(r.answer is None for r in session.rounds):
        return
    session.score = sum(r.points for r in session.rounds if r.correct)
    session.total = sum(r.points for r in session.rounds)
    if session.finished_at is None:
        session.finished_at = datetime.utcnow()
    db.commit()


def personal_best(db: Session) -> int | None:
    """Highest score among finished sessions, or None if none finished yet."""
    return db.execute(
        select(func.max(InterviewSession.score)).where(
            InterviewSession.finished_at.is_not(None)
        )
    ).scalar()


def recent_sessions(db: Session, limit: int = 10) -> list[InterviewSession]:
    return list(
        db.execute(
            select(InterviewSession)
            .where(InterviewSession.finished_at.is_not(None))
            .order_by(InterviewSession.created_at.desc())
            .limit(limit)
        ).scalars()
    )
