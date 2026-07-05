from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Tier(Base):
    __tablename__ = "tiers"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    subtitle: Mapped[str] = mapped_column(String, default="")
    order: Mapped[int] = mapped_column(Integer)
    min_level: Mapped[int] = mapped_column(Integer, default=1)
    # Optional realms (e.g. the DSA proving grounds) never gate another tier;
    # they render with an "Optional" label and can be skipped entirely.
    optional: Mapped[bool] = mapped_column(Boolean, default=False)

    quests: Mapped[list["Quest"]] = relationship(
        back_populates="tier", order_by="Quest.order"
    )


class Quest(Base):
    __tablename__ = "quests"

    id: Mapped[int] = mapped_column(primary_key=True)
    tier_id: Mapped[int] = mapped_column(ForeignKey("tiers.id"))
    slug: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(Text, default="")
    order: Mapped[int] = mapped_column(Integer)
    is_boss_battle: Mapped[bool] = mapped_column(Boolean, default=False)

    tier: Mapped[Tier] = relationship(back_populates="quests")
    challenges: Mapped[list["Challenge"]] = relationship(
        back_populates="quest", order_by="Challenge.order"
    )


class Challenge(Base):
    __tablename__ = "challenges"

    id: Mapped[int] = mapped_column(primary_key=True)
    quest_id: Mapped[int] = mapped_column(ForeignKey("quests.id"))
    slug: Mapped[str] = mapped_column(String, unique=True)
    title: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    # 'standard' | 'boss' (end of quest, awards badge) | 'tier_boss' (gates next tier)
    kind: Mapped[str] = mapped_column(String, default="standard")
    lesson_md: Mapped[str] = mapped_column(Text, default="")
    prompt_md: Mapped[str] = mapped_column(Text)
    starter_code: Mapped[str] = mapped_column(Text, default="")
    hidden_tests: Mapped[str] = mapped_column(Text)
    # A small, *visible* set of example assertions shown on standard missions
    # so learners see expected input/output. Empty on bosses (fully hidden).
    example_tests: Mapped[str] = mapped_column(Text, default="")
    # Canonical solution + a short "why", markdown with one ```python fence.
    # Revealed only after the learner passes.
    solution_md: Mapped[str] = mapped_column(Text, default="")
    xp_reward: Mapped[int] = mapped_column(Integer, default=50)
    time_limit_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)

    quest: Mapped[Quest] = relationship(back_populates="challenges")
    submissions: Mapped[list["Submission"]] = relationship(back_populates="challenge")


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    challenge_id: Mapped[int] = mapped_column(ForeignKey("challenges.id"))
    code: Mapped[str] = mapped_column(Text)
    passed: Mapped[bool] = mapped_column(Boolean)
    output: Mapped[str] = mapped_column(Text, default="")
    failing_tests: Mapped[str] = mapped_column(Text, default="")  # comma-separated
    duration_seconds: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    challenge: Mapped[Challenge] = relationship(back_populates="submissions")


class SolutionReveal(Base):
    """Records that the learner 'gave up' and revealed a challenge's canonical
    solution. Independent of passing — the challenge stays unsolved (no XP,
    no badge) until actually passed, so you can still earn it afterward."""

    __tablename__ = "solution_reveals"

    id: Mapped[int] = mapped_column(primary_key=True)
    challenge_id: Mapped[int] = mapped_column(
        ForeignKey("challenges.id"), unique=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class XpEvent(Base):
    """Append-only XP ledger. Current XP is SUM(delta); never mutate rows."""

    __tablename__ = "xp_ledger"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String)
    delta: Mapped[int] = mapped_column(Integer)
    idempotency_key: Mapped[str] = mapped_column(String, unique=True)
    meta: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StreakState(Base):
    __tablename__ = "streak_state"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_active_local_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    current_streak: Mapped[int] = mapped_column(Integer, default=0)
    longest_streak: Mapped[int] = mapped_column(Integer, default=0)


class FreezeEvent(Base):
    """Grant/consume ledger for streak freeze tokens; balance is a SUM."""

    __tablename__ = "freeze_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String)  # 'grant' | 'consume'
    delta: Mapped[int] = mapped_column(Integer)  # +1 grant, -1 consume
    reason: Mapped[str] = mapped_column(String, default="")
    idempotency_key: Mapped[str] = mapped_column(String, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class AchievementRule(Base):
    __tablename__ = "achievement_rules"

    id: Mapped[int] = mapped_column(primary_key=True)
    badge_id: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    icon: Mapped[str] = mapped_column(String, default="🏅")
    description: Mapped[str] = mapped_column(String, default="")
    trigger_event: Mapped[str] = mapped_column(String)  # 'challenge_passed' | 'streak_updated'
    condition_json: Mapped[str] = mapped_column(Text)  # JSON condition, see achievements service


class AchievementEarned(Base):
    __tablename__ = "achievements_earned"

    id: Mapped[int] = mapped_column(primary_key=True)
    badge_id: Mapped[str] = mapped_column(String, unique=True)
    earned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Settings(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    show_gamification: Mapped[bool] = mapped_column(Boolean, default=True)
