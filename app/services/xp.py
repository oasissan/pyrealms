"""XP service backed by the append-only ledger. Awards are idempotent via
`idempotency_key`, so re-passing a challenge never double-awards."""

import json

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .. import levels
from ..models import XpEvent


def total_xp(db: Session) -> int:
    return db.execute(select(func.coalesce(func.sum(XpEvent.delta), 0))).scalar_one()


def award_xp(
    db: Session, event_type: str, delta: int, idempotency_key: str, meta: dict | None = None
) -> dict:
    """Append an XP event unless one with this key exists.

    Returns {awarded, delta, xp_before, xp_after, level_before, level_after,
    leveled_up}.
    """
    xp_before = total_xp(db)
    existing = db.execute(
        select(XpEvent).where(XpEvent.idempotency_key == idempotency_key)
    ).scalar_one_or_none()
    if existing is not None:
        level = levels.level_for_xp(xp_before)
        return {
            "awarded": False,
            "delta": 0,
            "xp_before": xp_before,
            "xp_after": xp_before,
            "level_before": level,
            "level_after": level,
            "leveled_up": False,
        }

    db.add(
        XpEvent(
            event_type=event_type,
            delta=delta,
            idempotency_key=idempotency_key,
            meta=json.dumps(meta or {}),
        )
    )
    db.flush()
    xp_after = xp_before + delta
    level_before = levels.level_for_xp(xp_before)
    level_after = levels.level_for_xp(xp_after)
    return {
        "awarded": True,
        "delta": delta,
        "xp_before": xp_before,
        "xp_after": xp_after,
        "level_before": level_before,
        "level_after": level_after,
        "leveled_up": level_after > level_before,
    }
