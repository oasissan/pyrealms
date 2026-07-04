"""Declarative achievement rule engine, evaluated on domain events instead of
scattered `if` checks in the grading path.

Condition JSON shapes:
  {"challenge_slug": "..."}   -> a specific challenge was just passed
  {"kind": "boss"}            -> any challenge of that kind was just passed
  {"passed_count": N}         -> total distinct challenges passed >= N
  {"streak": N}               -> current streak >= N
"""

import json

from sqlalchemy import distinct, func, select
from sqlalchemy.orm import Session

from ..models import AchievementEarned, AchievementRule, Submission


def earned_badge_ids(db: Session) -> set[str]:
    return set(db.execute(select(AchievementEarned.badge_id)).scalars())


def _distinct_passed_count(db: Session) -> int:
    return db.execute(
        select(func.count(distinct(Submission.challenge_id))).where(
            Submission.passed.is_(True)
        )
    ).scalar_one()


def _condition_met(db: Session, condition: dict, context: dict) -> bool:
    if "challenge_slug" in condition:
        return context.get("challenge_slug") == condition["challenge_slug"]
    if "kind" in condition:
        return context.get("kind") == condition["kind"]
    if "passed_count" in condition:
        return _distinct_passed_count(db) >= condition["passed_count"]
    if "streak" in condition:
        return context.get("current_streak", 0) >= condition["streak"]
    return False


def evaluate(db: Session, trigger_event: str, context: dict) -> list[AchievementRule]:
    """Check unearned rules for this event; award and return newly earned."""
    earned = earned_badge_ids(db)
    rules = db.execute(
        select(AchievementRule).where(AchievementRule.trigger_event == trigger_event)
    ).scalars()

    newly_earned = []
    for rule in rules:
        if rule.badge_id in earned:
            continue
        if _condition_met(db, json.loads(rule.condition_json), context):
            db.add(AchievementEarned(badge_id=rule.badge_id))
            newly_earned.append(rule)
    if newly_earned:
        db.flush()
    return newly_earned
