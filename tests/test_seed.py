"""Seeding: quizzes seed idempotently and independently of the tier/quest
content, so an already-seeded database picks them up without a wipe.
"""

import pytest
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.content import ALL_TIERS, iter_quiz_questions, teaching_quests
from app.database import Base
from app.models import Quest, QuizQuestion
from app.seed import seed, seed_quizzes


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


def _expected_question_count():
    return len(list(iter_quiz_questions()))


def test_seed_creates_all_quiz_questions(db):
    seed(db)
    count = db.execute(select(func.count()).select_from(QuizQuestion)).scalar_one()
    assert count == _expected_question_count()


def test_seed_is_idempotent_for_quizzes(db):
    seed(db)
    seed(db)  # second run must not duplicate
    count = db.execute(select(func.count()).select_from(QuizQuestion)).scalar_one()
    assert count == _expected_question_count()


def test_quiz_questions_link_to_correct_quest(db):
    seed(db)
    # Spot-check: the first teaching quest of tier 1 owns its five questions.
    quest_slug = teaching_quests(ALL_TIERS[0])[0]["slug"]
    quest = db.execute(
        select(Quest).where(Quest.slug == quest_slug)
    ).scalar_one()
    assert len(quest.quiz_questions) == 5
    assert quest.quiz_questions[0].order == 1


def test_seed_quizzes_backfills_when_content_predates_quizzes(db):
    """Simulate an existing install: tiers/quests seeded, but the quiz table
    empty. Running seed_quizzes alone must populate it."""
    seed(db)
    db.query(QuizQuestion).delete()
    db.commit()

    seed_quizzes(db)
    count = db.execute(select(func.count()).select_from(QuizQuestion)).scalar_one()
    assert count == _expected_question_count()
