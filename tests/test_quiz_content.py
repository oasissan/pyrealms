"""Quiz content integrity — the MCQ analogue of test_content's solution-rot
checks. Every teaching quest (anything that isn't a single-mission boss-battle
quest) must ship a well-formed 5-question Knowledge Check, and CI enforces it.
"""

import pytest

from app.content import ALL_TIERS, iter_quiz_questions, teaching_quests

QUESTIONS_PER_QUEST = 5

TEACHING_QUESTS = [
    pytest.param(q, id=f"{t['slug']}/{q['slug']}")
    for t in ALL_TIERS
    for q in teaching_quests(t)
]


@pytest.mark.parametrize("quest", TEACHING_QUESTS)
def test_quest_has_five_questions(quest):
    quiz = quest.get("quiz")
    assert quiz, f"{quest['slug']} has no quiz"
    assert len(quiz) == QUESTIONS_PER_QUEST, (
        f"{quest['slug']} has {len(quiz)} questions, expected {QUESTIONS_PER_QUEST}"
    )


@pytest.mark.parametrize("quest", TEACHING_QUESTS)
def test_questions_are_well_formed(quest):
    for i, question in enumerate(quest["quiz"]):
        where = f"{quest['slug']}[{i}]"
        assert question.get("prompt_md"), f"{where} missing prompt_md"
        options = question.get("options")
        assert options and len(options) >= 2, f"{where} needs >= 2 options"
        assert len(set(options)) == len(options), f"{where} has duplicate options"
        correct = question.get("correct")
        assert isinstance(correct, int) and 0 <= correct < len(options), (
            f"{where} correct index {correct!r} out of range"
        )
        assert question.get("explanation_md"), f"{where} missing explanation_md"


def test_boss_battle_quests_have_no_quiz():
    """Single-mission boss-battle quests are pure fights — no Knowledge Check."""
    for tier in ALL_TIERS:
        for quest in tier["quests"]:
            if quest.get("is_boss_battle"):
                assert not quest.get("quiz"), (
                    f"{quest['slug']} is a boss battle but has a quiz"
                )


def test_iter_quiz_questions_covers_every_teaching_quest():
    expected = sum(len(q["quiz"]) for t in ALL_TIERS for q in teaching_quests(t))
    assert len(list(iter_quiz_questions())) == expected
