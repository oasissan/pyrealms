"""Mock Interview Arena routes: a timed, randomized practice run.

Landing page (config + history), a per-round view (MCQ or coding, with a
countdown), an HTMX answer endpoint that grades and swaps in the next round or
the results, and a full results page. Round selection and grading live in
``app.services.arena``.
"""

import time

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Challenge, InterviewSession, QuizQuestion
from ..services import arena
from ..templating import templates
from .pages import hud_context, render_md

router = APIRouter(prefix="/arena")

# Per-round countdown (seconds), by round kind — coding rounds get more time.
ROUND_SECONDS = {"mcq": 45, "coding": 300}


def _round_view(db: Session, round_) -> dict:
    """Template context for a single round, resolving its referenced question
    or challenge."""
    ctx = {
        "round": round_,
        "seconds": ROUND_SECONDS.get(round_.kind, 60),
    }
    if round_.kind == "mcq":
        question = db.get(QuizQuestion, round_.ref_id)
        ctx["question"] = question
        ctx["prompt_html"] = render_md(question.prompt_md)
        ctx["options"] = question.options
    else:
        challenge = db.get(Challenge, round_.ref_id)
        ctx["challenge"] = challenge
        ctx["prompt_html"] = render_md(challenge.prompt_md)
        ctx["starter_code"] = challenge.starter_code
    return ctx


@router.get("")
def arena_home(request: Request, db: Session = Depends(get_db)):
    hud = hud_context(db)
    return templates.TemplateResponse(
        request,
        "arena.html",
        {
            "difficulties": list(arena.DIFFICULTY_TIERS.keys()),
            "personal_best": arena.personal_best(db),
            "recent": arena.recent_sessions(db),
            **hud,
        },
    )


@router.post("/start")
def arena_start(
    request: Request,
    difficulty: str = Form("expert"),
    num_questions: int = Form(5),
    db: Session = Depends(get_db),
):
    if difficulty not in arena.DIFFICULTY_TIERS:
        raise HTTPException(400, "Unknown difficulty")
    num_questions = max(1, min(num_questions, 15))
    session = arena.start_session(db, difficulty, num_questions)
    if not session.rounds:
        raise HTTPException(409, "No questions available for that difficulty yet")
    return RedirectResponse(f"/arena/round/{session.id}", status_code=303)


@router.get("/round/{session_id}")
def arena_round(session_id: int, request: Request, db: Session = Depends(get_db)):
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(404, "Unknown session")
    current = arena.current_round(db, session)
    if current is None:
        return RedirectResponse(f"/arena/results/{session.id}", status_code=303)
    hud = hud_context(db)
    return templates.TemplateResponse(
        request,
        "arena_round.html",
        {
            "session": session,
            "answered": sum(1 for r in session.rounds if r.answer is not None),
            "started_at": time.time(),
            **_round_view(db, current),
            **hud,
        },
    )


@router.post("/answer/{session_id}")
def arena_answer(
    session_id: int,
    request: Request,
    answer: str = Form(""),
    started_at: float = Form(0.0),
    db: Session = Depends(get_db),
):
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(404, "Unknown session")
    current = arena.current_round(db, session)
    if current is None:
        raise HTTPException(409, "Session already complete")

    elapsed = max(0.0, time.time() - started_at) if started_at else None
    correct = arena.grade_round(db, current, answer, elapsed)
    arena.finish_if_done(db, session)

    nxt = arena.current_round(db, session)
    if nxt is None:
        return templates.TemplateResponse(
            request,
            "partials/arena_result.html",
            {
                "session": session,
                "personal_best": arena.personal_best(db),
                "just_correct": correct,
                **hud_context(db),
            },
        )
    return templates.TemplateResponse(
        request,
        "partials/arena_round_body.html",
        {
            "session": session,
            "answered": sum(1 for r in session.rounds if r.answer is not None),
            "started_at": time.time(),
            "just_correct": correct,
            **_round_view(db, nxt),
            **hud_context(db),
        },
    )


@router.get("/results/{session_id}")
def arena_results(session_id: int, request: Request, db: Session = Depends(get_db)):
    session = db.get(InterviewSession, session_id)
    if session is None:
        raise HTTPException(404, "Unknown session")
    return templates.TemplateResponse(
        request,
        "arena_results.html",
        {
            "session": session,
            "personal_best": arena.personal_best(db),
            **hud_context(db),
        },
    )
