"""Quiz answering + state derivation.

XP is awarded only when a question's *first* answer is correct — retries stay
consequence-free for learning but can't farm XP. Awards go through the same
idempotent XP ledger as coding challenges (`quiz_correct:{question_id}`), so a
resolved question never double-awards. A question is "resolved" once any
correct answer has been recorded; resolution is derived from the append-only
`QuizAnswer` log, never stored as a flag.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models import QuizAnswer, QuizQuestion
from . import xp


def resolved_question_ids(db: Session) -> set[int]:
    """Questions the learner has answered correctly at least once."""
    return set(
        db.execute(
            select(QuizAnswer.question_id)
            .where(QuizAnswer.correct.is_(True))
            .distinct()
        ).scalars()
    )


def record_answer(db: Session, question_id: int, chosen_index: int) -> dict:
    """Log an answer and, on a first-try correct pick, award XP.

    Returns a dict for the UI. The correct option and its explanation are
    revealed only once the question is resolved (a correct answer) — a wrong
    answer never leaks them, so the learner can genuinely retry.
    """
    question = db.get(QuizQuestion, question_id)
    if question is None:
        raise LookupError(f"unknown quiz question {question_id}")

    prior = (
        db.execute(
            select(QuizAnswer).where(QuizAnswer.question_id == question_id)
        )
        .scalars()
        .all()
    )
    already_resolved = any(a.correct for a in prior)
    is_correct = chosen_index == question.correct_index

    db.add(
        QuizAnswer(
            question_id=question_id,
            chosen_index=chosen_index,
            correct=is_correct,
        )
    )

    xp_result = None
    # First-try rule: award only when the very first answer is the correct one.
    if is_correct and not prior:
        xp_result = xp.award_xp(
            db,
            event_type="quiz_correct",
            delta=question.xp_reward,
            idempotency_key=f"quiz_correct:{question_id}",
            meta={"question_id": question_id, "quest_id": question.quest_id},
        )

    db.commit()

    resolved = is_correct or already_resolved
    return {
        "question": question,
        "correct": is_correct,
        "resolved": resolved,
        "chosen_index": chosen_index,
        "correct_index": question.correct_index if resolved else None,
        "explanation_md": question.explanation_md if resolved else None,
        "xp_result": xp_result,
    }


def quiz_state_for_quest(db: Session, quest_id: int) -> list[dict]:
    """Every question for a quest with its resolved state, for rendering the
    quest page's Knowledge Check."""
    questions = (
        db.execute(
            select(QuizQuestion)
            .where(QuizQuestion.quest_id == quest_id)
            .order_by(QuizQuestion.order)
        )
        .scalars()
        .all()
    )
    resolved = resolved_question_ids(db)
    return [{"question": q, "resolved": q.id in resolved} for q in questions]
