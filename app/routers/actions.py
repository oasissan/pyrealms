"""HTMX action routes: code submission (the reward moment) and settings."""

import time

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..grading import run_hidden_tests
from ..models import Challenge, Settings, Submission
from ..services import achievements, progress, streak, xp
from ..templating import templates
from .pages import hud_context, render_md

router = APIRouter()


@router.post("/challenge/{slug}/submit")
def submit_challenge(
    slug: str,
    request: Request,
    code: str = Form(...),
    started_at: float = Form(0.0),
    db: Session = Depends(get_db),
):
    challenge = db.execute(
        select(Challenge).where(Challenge.slug == slug)
    ).scalar_one_or_none()
    if challenge is None:
        raise HTTPException(404, "Unknown challenge")

    elapsed = max(0.0, time.time() - started_at) if started_at else None
    timed_out_battle = (
        challenge.time_limit_seconds is not None
        and elapsed is not None
        and elapsed > challenge.time_limit_seconds
    )

    if timed_out_battle:
        result = None
        passed = False
    else:
        result = run_hidden_tests(code, challenge.hidden_tests)
        passed = result.passed

    submission = Submission(
        challenge_id=challenge.id,
        code=code,
        passed=passed,
        output="⏱ Boss battle time limit exceeded — the gate stays shut. Try again!"
        if timed_out_battle
        else result.output,
        failing_tests=",".join(result.failing_tests) if result else "",
        duration_seconds=elapsed,
    )
    db.add(submission)
    db.flush()

    xp_result = None
    streak_result = None
    new_badges = []
    if passed:
        xp_result = xp.award_xp(
            db,
            event_type="challenge_passed",
            delta=challenge.xp_reward,
            idempotency_key=f"challenge_passed:{challenge.id}",
            meta={"challenge": challenge.slug},
        )
        streak_result = streak.record_activity(db)
        context = {
            "challenge_slug": challenge.slug,
            "kind": challenge.kind,
            "current_streak": streak_result["current_streak"],
        }
        new_badges = achievements.evaluate(db, "challenge_passed", context)
        new_badges += achievements.evaluate(db, "streak_updated", context)

    db.commit()

    return templates.TemplateResponse(
        request,
        "partials/result.html",
        {
            "challenge": challenge,
            "passed": passed,
            "output": submission.output,
            "grade": result,
            "failing_tests": result.failing_tests if result else [],
            "xp_result": xp_result,
            "streak_result": streak_result,
            "new_badges": new_badges,
            "best": progress.personal_best(db, challenge.id),
            "elapsed": elapsed,
            # Reveal the canonical solution as part of the reward moment.
            "solution_html": render_md(challenge.solution_md)
            if passed and challenge.solution_md
            else "",
            **hud_context(db),
        },
    )


@router.post("/challenge/{slug}/reveal")
def reveal_solution(slug: str, request: Request, db: Session = Depends(get_db)):
    """Give up: record the reveal and return the canonical solution partial.
    Does not mark the challenge passed — no XP is awarded here."""
    challenge = db.execute(
        select(Challenge).where(Challenge.slug == slug)
    ).scalar_one_or_none()
    if challenge is None:
        raise HTTPException(404, "Unknown challenge")

    progress.reveal_solution(db, challenge.id)
    db.commit()

    return templates.TemplateResponse(
        request,
        "partials/solution.html",
        {
            "solution_html": render_md(challenge.solution_md)
            if challenge.solution_md
            else "",
            "gave_up": True,
        },
    )


@router.post("/settings/toggle-gamification")
def toggle_gamification(request: Request, db: Session = Depends(get_db)):
    settings = db.execute(select(Settings)).scalar_one()
    settings.show_gamification = not settings.show_gamification
    db.commit()
    return templates.TemplateResponse(
        request, "partials/hud.html", {**hud_context(db), "oob": False}
    )
