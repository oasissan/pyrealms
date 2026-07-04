"""Idempotent curriculum + achievement-rule seeding from app.content."""

import json

from sqlalchemy import select
from sqlalchemy.orm import Session

from .content import ALL_TIERS, META_ACHIEVEMENTS
from .models import AchievementRule, Challenge, Quest, Settings, Tier


def seed(db: Session) -> None:
    if db.execute(select(Tier.id)).first() is not None:
        return  # already seeded

    for tier_data in ALL_TIERS:
        tier = Tier(
            slug=tier_data["slug"],
            title=tier_data["title"],
            subtitle=tier_data["subtitle"],
            order=tier_data["order"],
            min_level=tier_data["min_level"],
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
