"""Idempotent curriculum + achievement-rule seeding from app.content.

Seeding is additive and safe to re-run: tiers are seeded by slug (so adding a
new realm to `ALL_TIERS` backfills it on next startup without wiping learner
progress), and quizzes are seeded per-quest. Neither touches existing rows.
"""

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from .content import ALL_TIERS, META_ACHIEVEMENTS, iter_quiz_questions
from .models import (
    AchievementRule,
    Challenge,
    Quest,
    QuizQuestion,
    Settings,
    Tier,
)


def _seed_tier(db: Session, tier_data: dict) -> None:
    """Insert one tier with its quests, challenges, and badge rules. Assumes
    the tier's slug does not already exist. Does not commit."""
    tier = Tier(
        slug=tier_data["slug"],
        title=tier_data["title"],
        subtitle=tier_data["subtitle"],
        order=tier_data["order"],
        min_level=tier_data["min_level"],
        optional=tier_data.get("optional", False),
    )
    db.add(tier)
    db.flush()

    for q_order, quest_data in enumerate(tier_data["quests"], start=1):
        quest = Quest(
            tier_id=tier.id,
            slug=quest_data["slug"],
            title=quest_data["title"],
            description=quest_data.get("description", ""),
            order=q_order,
            is_boss_battle=quest_data.get("is_boss_battle", False),
        )
        db.add(quest)
        db.flush()

        for m_order, mission in enumerate(quest_data["missions"], start=1):
            db.add(
                Challenge(
                    quest_id=quest.id,
                    slug=mission["slug"],
                    title=mission["title"],
                    order=m_order,
                    kind=mission["kind"],
                    lesson_md=mission.get("lesson_md", ""),
                    prompt_md=mission["prompt_md"],
                    starter_code=mission.get("starter_code", ""),
                    hidden_tests=mission["hidden_tests"],
                    example_tests=mission.get("example_tests", ""),
                    solution_md=mission.get("solution_md", ""),
                    xp_reward=mission["xp"],
                    time_limit_seconds=mission.get("time_limit_seconds"),
                )
            )

        # Badges gate on the quest's boss (or tier-boss) challenge.
        badge = quest_data.get("badge")
        if badge:
            boss_mission = next(
                m
                for m in quest_data["missions"]
                if m["kind"] in ("boss", "tier_boss")
            )
            db.add(
                AchievementRule(
                    badge_id=badge["id"],
                    name=badge["name"],
                    icon=badge["icon"],
                    description=f"Defeat the boss of “{quest_data['title']}”.",
                    trigger_event="challenge_passed",
                    condition_json=json.dumps(
                        {"challenge_slug": boss_mission["slug"]}
                    ),
                )
            )


def seed_missing_tiers(db: Session) -> None:
    """Seed any tier in ALL_TIERS whose slug isn't in the DB yet. Lets a new
    realm added to the content files land on the next startup while leaving
    every existing tier — and all learner progress — untouched."""
    existing = set(db.execute(select(Tier.slug)).scalars())
    added = False
    for tier_data in ALL_TIERS:
        if tier_data["slug"] not in existing:
            _seed_tier(db, tier_data)
            added = True
    if added:
        db.commit()


def seed_quizzes(db: Session) -> None:
    """Seed MCQ questions for any quest that has none yet. Idempotent and
    per-quest, so both a fresh install and a realm added later pick up their
    quizzes without a wipe (and without losing learner progress)."""
    quest_ids = {
        slug: qid
        for slug, qid in db.execute(select(Quest.slug, Quest.id)).all()
    }
    quests_with_quiz = set(
        db.execute(select(QuizQuestion.quest_id)).scalars()
    )
    added = False
    for quest, order, question in iter_quiz_questions():
        quest_id = quest_ids.get(quest["slug"])
        if quest_id is None or quest_id in quests_with_quiz:
            continue
        db.add(
            QuizQuestion(
                quest_id=quest_id,
                order=order,
                prompt_md=question["prompt_md"],
                options_json=json.dumps(question["options"]),
                correct_index=question["correct"],
                explanation_md=question["explanation_md"],
                xp_reward=question.get("xp", 10),
            )
        )
        added = True
    if added:
        db.commit()


def seed(db: Session) -> None:
    if db.execute(select(Tier.id)).first() is not None:
        # Existing install: backfill any newly-added realms and their quizzes
        # without disturbing existing tiers or learner progress.
        seed_missing_tiers(db)
        seed_quizzes(db)
        return

    for tier_data in ALL_TIERS:
        _seed_tier(db, tier_data)

    for meta in META_ACHIEVEMENTS:
        db.add(
            AchievementRule(
                badge_id=meta["badge_id"],
                name=meta["name"],
                icon=meta["icon"],
                description=meta["description"],
                trigger_event=meta["trigger_event"],
                condition_json=json.dumps(meta["condition"]),
            )
        )

    if db.execute(select(Settings.id)).first() is None:
        db.add(Settings(show_gamification=True))

    db.commit()
    seed_quizzes(db)  # quests now exist; attach their quizzes
