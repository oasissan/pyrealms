"""Mock Interview Arena: models, round selection, grading, scoring.

Runs against a throwaway in-memory SQLite DB seeded with a tiny curriculum,
never app.db — same approach as the other service tests.
"""

import json

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import app.models as m
from app.services import arena


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    m.Base.metadata.create_all(engine)
    session = sessionmaker(bind=engine)()
    _seed_minimal(session)
    yield session
    session.close()


def _seed_minimal(db):
    """Two tiers so difficulty filtering has something to choose from:
    tier 2 (standard pool) and tier 5 (expert pool). Each has one boss coding
    challenge and one MCQ."""
    for order, slug in ((2, "t2"), (5, "t5")):
        tier = m.Tier(slug=slug, title=slug, subtitle="", order=order, min_level=1)
        db.add(tier)
        db.flush()
        quest = m.Quest(tier_id=tier.id, slug=f"{slug}-q", title="Q", order=1)
        db.add(quest)
        db.flush()
        db.add(
            m.Challenge(
                quest_id=quest.id,
                slug=f"{slug}-boss",
                title="Boss",
                order=1,
                kind="boss",
                prompt_md="Write f() returning 1.",
                hidden_tests="from solution import f\n\ndef test_f():\n    assert f() == 1\n",
                solution_md="```python\ndef f():\n    return 1\n```",
                xp_reward=50,
            )
        )
        db.add(
            m.QuizQuestion(
                quest_id=quest.id,
                order=1,
                prompt_md=f"{slug} question?",
                options_json=json.dumps(["wrong", "right"]),
                correct_index=1,
                explanation_md="because",
                xp_reward=10,
            )
        )
    db.add(m.Settings(show_gamification=True))
    db.commit()


def test_session_rounds_ordered(db):
    s = m.InterviewSession(difficulty="expert", num_questions=2, total=2)
    db.add(s)
    db.flush()
    db.add(m.InterviewRound(session_id=s.id, order=2, kind="mcq", ref_id=1))
    db.add(m.InterviewRound(session_id=s.id, order=1, kind="coding", ref_id=1))
    db.flush()
    assert [r.order for r in s.rounds] == [1, 2]


def test_standard_difficulty_draws_only_standard_tiers(db):
    s = arena.start_session(db, "standard", 2)
    # every coding round must reference a tier-2 challenge (slug 't2-boss'),
    # every mcq a tier-2 question — nothing from tier 5.
    for r in s.rounds:
        if r.kind == "coding":
            ch = db.get(m.Challenge, r.ref_id)
            assert ch.slug == "t2-boss"
        else:
            q = db.get(m.QuizQuestion, r.ref_id)
            assert q.quest.tier.slug == "t2"


def test_start_session_persists_rounds(db):
    s = arena.start_session(db, "expert", 3)
    assert s.num_questions == 3
    assert s.total == 3
    assert len(s.rounds) == 3
    assert [r.order for r in s.rounds] == [1, 2, 3]


def test_current_round_advances(db):
    s = arena.start_session(db, "standard", 2)
    first = arena.current_round(db, s)
    assert first.order == 1
    # answer the first correctly, next current_round should be the 2nd
    answer = _correct_answer_for(db, first)
    arena.grade_round(db, first, answer)
    second = arena.current_round(db, s)
    assert second.order == 2


def test_mcq_grading_correct_and_incorrect(db):
    s = arena.start_session(db, "standard", 5)
    mcq = next(r for r in s.rounds if r.kind == "mcq")
    assert arena.grade_round(db, mcq, "1") is True
    assert mcq.correct is True
    mcq2 = m.InterviewRound(session_id=s.id, order=99, kind="mcq", ref_id=mcq.ref_id)
    db.add(mcq2)
    db.flush()
    assert arena.grade_round(db, mcq2, "0") is False
    assert mcq2.correct is False


def test_coding_grading_via_hidden_tests(db):
    s = arena.start_session(db, "standard", 5)
    coding = next(r for r in s.rounds if r.kind == "coding")
    assert arena.grade_round(db, coding, "def f():\n    return 1\n") is True
    assert coding.correct is True


def test_coding_grading_wrong_answer(db):
    s = arena.start_session(db, "standard", 5)
    coding = next(r for r in s.rounds if r.kind == "coding")
    assert arena.grade_round(db, coding, "def f():\n    return 2\n") is False


def test_finish_computes_score(db):
    s = arena.start_session(db, "standard", 2)
    for r in list(s.rounds):
        arena.grade_round(db, r, _correct_answer_for(db, r))
        arena.finish_if_done(db, s)
    assert s.finished_at is not None
    assert s.score == 2


def test_personal_best(db):
    assert arena.personal_best(db) is None
    s = arena.start_session(db, "standard", 1)
    r = arena.current_round(db, s)
    arena.grade_round(db, r, _correct_answer_for(db, r))
    arena.finish_if_done(db, s)
    assert arena.personal_best(db) == 1


def _correct_answer_for(db, round_):
    if round_.kind == "mcq":
        q = db.get(m.QuizQuestion, round_.ref_id)
        return str(q.correct_index)
    ch = db.get(m.Challenge, round_.ref_id)
    from app.content import solution_code

    return solution_code(ch.solution_md)
