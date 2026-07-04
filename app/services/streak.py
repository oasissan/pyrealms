"""Streak logic, evaluated lazily on each qualifying action with local dates
(no midnight cron). Freeze tokens live in their own grant/consume ledger and
are earned through practice (one per 7 consecutive days), never purchased."""

from datetime import date

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ..models import FreezeEvent, StreakState

FREEZE_EARN_EVERY_DAYS = 7
MAX_FREEZE_BALANCE = 2


def get_state(db: Session) -> StreakState:
    state = db.execute(select(StreakState)).scalar_one_or_none()
    if state is None:
        state = StreakState(current_streak=0, longest_streak=0)
        db.add(state)
        db.flush()
    return state


def freeze_balance(db: Session) -> int:
    return db.execute(
        select(func.coalesce(func.sum(FreezeEvent.delta), 0))
    ).scalar_one()


def _append_freeze(db: Session, kind: str, delta: int, reason: str, key: str) -> bool:
    existing = db.execute(
        select(FreezeEvent).where(FreezeEvent.idempotency_key == key)
    ).scalar_one_or_none()
    if existing is not None:
        return False
    db.add(FreezeEvent(kind=kind, delta=delta, reason=reason, idempotency_key=key))
    db.flush()
    return True


def record_activity(db: Session, today: date | None = None) -> dict:
    """Update the streak for a qualifying action happening on `today`
    (local date). Returns what happened so the UI can toast it."""
    today = today or date.today()
    state = get_state(db)
    result = {
        "extended": False,
        "reset": False,
        "froze": False,
        "freeze_earned": False,
    }

    last = state.last_active_local_date
    if last == today:
        pass  # already counted today
    elif last is None:
        state.current_streak = 1
        result["extended"] = True
    else:
        gap = (today - last).days
        if gap == 1:
            state.current_streak += 1
            result["extended"] = True
        elif gap == 2 and freeze_balance(db) > 0:
            # Explicit, logged consumption covering the single missed day.
            _append_freeze(
                db,
                "consume",
                -1,
                f"covered missed day {last.isoformat()}+1",
                f"consume:{today.isoformat()}",
            )
            state.current_streak += 1
            result["froze"] = True
            result["extended"] = True
        else:
            state.current_streak = 1
            result["reset"] = True

    state.last_active_local_date = today
    state.longest_streak = max(state.longest_streak, state.current_streak)

    if (
        result["extended"]
        and state.current_streak > 0
        and state.current_streak % FREEZE_EARN_EVERY_DAYS == 0
        and freeze_balance(db) < MAX_FREEZE_BALANCE
    ):
        result["freeze_earned"] = _append_freeze(
            db,
            "grant",
            1,
            f"{state.current_streak}-day streak",
            f"grant:streak:{state.current_streak}:{today.isoformat()}",
        )

    db.flush()
    result.update(
        current_streak=state.current_streak,
        longest_streak=state.longest_streak,
        freeze_balance=freeze_balance(db),
    )
    return result
