"""Quiz service: answer recording, first-try-correct XP, idempotency, and
resolved-state derivation. XP flows through the same append-only ledger as
coding challenges, so re-answering a resolved question never double-awards.
"""

import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import QuizQuestion
from app.services import quiz, xp


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, expire_on_commit=False)
    with Session() as session:
        yield session


def _question(db, correct=1, xp_reward=10):
    q = QuizQuestion(
        quest_id=1,
        order=1,
        prompt_md="What does `7 // 2` give?",
        options_json=json.dumps(["3.5", "3", "4"]),
        correct_index=correct,
        explanation_md="`//` floors the result.",
        xp_reward=xp_reward,
    )
    db.add(q)
    db.commit()
    return q


def test_first_try_correct_awards_xp_and_resolves(db):
    q = _question(db)
    result = quiz.record_answer(db, q.id, 1)
    assert result["correct"] is True
    assert result["resolved"] is True
    assert result["correct_index"] == 1
    assert result["explanation_md"] == "`//` floors the result."
    assert result["xp_result"]["awarded"] is True
    assert xp.total_xp(db) == 10


def test_wrong_answer_does_not_reveal_or_resolve(db):
    q = _question(db)
    result = quiz.record_answer(db, q.id, 0)
    assert result["correct"] is False
    assert result["resolved"] is False
    # A wrong answer must not leak the correct option or its explanation.
    assert result["correct_index"] is None
    assert result["explanation_md"] is None
    assert result["xp_result"] is None
    assert xp.total_xp(db) == 0


def test_wrong_then_correct_awards_no_xp(db):
    q = _question(db)
    quiz.record_answer(db, q.id, 0)  # wrong first
    result = quiz.record_answer(db, q.id, 1)  # then correct
    assert result["correct"] is True
    assert result["resolved"] is True
    assert result["xp_result"] is None  # first-try rule: no XP after a miss
    assert xp.total_xp(db) == 0


def test_repeated_correct_is_idempotent(db):
    q = _question(db)
    quiz.record_answer(db, q.id, 1)
    second = quiz.record_answer(db, q.id, 1)
    assert second["resolved"] is True
    assert second["xp_result"] is None  # already awarded once
    assert xp.total_xp(db) == 10


def test_resolved_question_ids(db):
    q = _question(db)
    assert quiz.resolved_question_ids(db) == set()
    quiz.record_answer(db, q.id, 0)  # wrong keeps it unresolved
    assert quiz.resolved_question_ids(db) == set()
    quiz.record_answer(db, q.id, 1)
    assert quiz.resolved_question_ids(db) == {q.id}


def test_unknown_question_raises(db):
    with pytest.raises(LookupError):
        quiz.record_answer(db, 999, 0)


def test_quiz_state_for_quest_reports_resolution(db):
    q1 = _question(db)
    q2 = QuizQuestion(
        quest_id=1,
        order=2,
        prompt_md="second",
        options_json=json.dumps(["a", "b"]),
        correct_index=0,
        explanation_md="because a",
        xp_reward=10,
    )
    db.add(q2)
    db.commit()
    quiz.record_answer(db, q1.id, 1)  # resolve q1 only

    state = quiz.quiz_state_for_quest(db, quest_id=1)
    assert [s["question"].id for s in state] == [q1.id, q2.id]
    assert state[0]["resolved"] is True
    assert state[0]["question"].options == ["3.5", "3", "4"]
    assert state[1]["resolved"] is False


# --- Answer route integration --------------------------------------------


@pytest.fixture()
def api(monkeypatch):
    """TestClient backed by a seeded in-memory DB. Yields (client, question)
    where `question` is a real seeded QuizQuestion. Lifespan is not run, so
    the real app.db is untouched."""
    from fastapi.testclient import TestClient
    from sqlalchemy import select
    from sqlalchemy.pool import StaticPool

    from app.database import Base, get_db
    from app.main import app
    from app.models import QuizQuestion
    from app.seed import seed

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, expire_on_commit=False)
    with TestingSession() as db:
        seed(db)
        question = db.execute(
            select(QuizQuestion).order_by(QuizQuestion.id)
        ).scalars().first()

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), question
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_answer_route_correct_reveals_explanation(api):
    client, question = api
    resp = client.post(
        f"/quiz/{question.id}/answer", data={"chosen": question.correct_index}
    )
    assert resp.status_code == 200
    assert "quiz-explanation" in resp.text
    assert "resolved" in resp.text
    assert "+" in resp.text and "XP" in resp.text  # OOB toast fired


def test_answer_route_wrong_keeps_retryable(api):
    client, question = api
    wrong = (question.correct_index + 1) % len(question.options)
    resp = client.post(f"/quiz/{question.id}/answer", data={"chosen": wrong})
    assert resp.status_code == 200
    assert "quiz-nudge" in resp.text
    assert "quiz-explanation" not in resp.text  # answer not revealed
    # Buttons remain (still interactive)
    assert "hx-post" in resp.text


def test_answer_route_unknown_question_404(api):
    client, _ = api
    resp = client.post("/quiz/999999/answer", data={"chosen": 0})
    assert resp.status_code == 404
