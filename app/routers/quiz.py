"""HTMX action route for answering a quest's Knowledge Check questions.

A single question is submitted per click; the response re-renders just that
question card (correct/wrong marking, explanation on success) plus an
out-of-band HUD refresh and XP toast, mirroring the challenge-submit flow.
"""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from sqlalchemy.orm import Session

from ..database import get_db
from ..services import quiz
from ..templating import templates
from .pages import hud_context

router = APIRouter()


@router.post("/quiz/{question_id}/answer")
def answer_quiz(
    question_id: int,
    request: Request,
    chosen: int = Form(...),
    db: Session = Depends(get_db),
):
    try:
        result = quiz.record_answer(db, question_id, chosen)
    except LookupError:
        raise HTTPException(404, "Unknown question")

    question = result["question"]
    return templates.TemplateResponse(
        request,
        "partials/quiz_result.html",
        {
            "q": {
                "question": question,
                "index": question.order,
                "resolved": result["resolved"],
                "chosen_index": result["chosen_index"],
                "correct": result["correct"],
            },
            "xp_result": result["xp_result"],
            **hud_context(db),
        },
    )
