"""Full-page routes: skill-tree map, quest pages, mission pages."""

import time

import markdown
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import levels
from ..database import get_db
from ..models import AchievementEarned, AchievementRule, Challenge, Quest, Settings
from ..services import progress, streak, xp
from ..templating import templates

router = APIRouter()


def render_md(text: str) -> str:
    return markdown.markdown(text, extensions=["fenced_code", "tables"])


def hud_context(db: Session) -> dict:
    settings = db.execute(select(Settings)).scalar_one()
    state = streak.get_state(db)
    return {
        "show_gamification": settings.show_gamification,
        "progress": levels.level_progress(xp.total_xp(db)),
        "streak": state,
        "freeze_balance": streak.freeze_balance(db),
    }


@router.get("/")
def world_map(request: Request, db: Session = Depends(get_db)):
    hud = hud_context(db)
    map_state = progress.build_map(db, hud["progress"]["level"])
    earned_ids = {a.badge_id for a in db.execute(select(AchievementEarned)).scalars()}
    rules = db.execute(select(AchievementRule)).scalars().all()
    badges = [
        {"rule": r, "earned": r.badge_id in earned_ids}
        for r in sorted(rules, key=lambda r: r.badge_id not in earned_ids)
    ]
    return templates.TemplateResponse(
        request,
        "map.html",
        {"map_state": map_state, "badges": badges, **hud},
    )


@router.get("/quest/{slug}")
def quest_page(slug: str, request: Request, db: Session = Depends(get_db)):
    quest = db.execute(select(Quest).where(Quest.slug == slug)).scalar_one_or_none()
    if quest is None:
        raise HTTPException(404, "Unknown quest")
    hud = hud_context(db)
    map_state = progress.build_map(db, hud["progress"]["level"])
    quest_state = next(
        qs
        for ts in map_state
        for qs in ts["quests"]
        if qs["quest"].id == quest.id
    )
    return templates.TemplateResponse(
        request,
        "quest.html",
        {"quest_state": quest_state, **hud},
    )


@router.get("/mission/{slug}")
def mission_page(slug: str, request: Request, db: Session = Depends(get_db)):
    challenge = db.execute(
        select(Challenge).where(Challenge.slug == slug)
    ).scalar_one_or_none()
    if challenge is None:
        raise HTTPException(404, "Unknown mission")
    hud = hud_context(db)
    state = progress.challenge_state(db, challenge, hud["progress"]["level"])
    if not state["unlocked"]:
        raise HTTPException(403, "This mission is still locked")
    is_boss = challenge.kind in ("boss", "tier_boss")
    return templates.TemplateResponse(
        request,
        "mission.html",
        {
            "challenge": challenge,
            "passed": state["passed"],
            "is_boss": is_boss,
            "lesson_html": render_md(challenge.lesson_md) if not is_boss else "",
            "prompt_html": render_md(challenge.prompt_md),
            "best": progress.personal_best(db, challenge.id),
            "attempts": progress.attempts_count(db, challenge.id),
            "started_at": time.time(),
            **hud,
        },
    )
