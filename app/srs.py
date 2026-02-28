"""SM-2 spaced repetition with quality caps; SQLite backend."""
from __future__ import annotations
from datetime import date, timedelta
from typing import Any

from app import db


# ---------- quality computation ----------

def compute_quality(
    scores: dict[str, int],
    max_scores: dict[str, int],
    session_type: str,  # "topic" | "algo"
) -> float:
    """Normalise raw scores to 0-5 SM-2 quality, then apply caps."""
    total = sum(scores.values())
    maximum = sum(max_scores.values())
    if maximum == 0:
        return 0.0

    raw_quality = (total / maximum) * 5

    # Hard caps
    correctness = scores.get("correctness", scores.get("accuracy", None))
    recognize_pattern = scores.get("recognize_pattern", scores.get("pattern_recognition", None))

    if correctness == 0 or (recognize_pattern is not None and recognize_pattern == 0):
        raw_quality = min(raw_quality, 2.0)

    if session_type == "topic":
        key_concepts_missed = scores.get("key_concepts_missed", 0)
        if key_concepts_missed >= 3:
            raw_quality = min(raw_quality, 3.0)

    return round(raw_quality, 2)


# ---------- SM-2 algorithm ----------

def _sm2(
    quality: float,
    repetitions: int,
    ease_factor: float,
    interval_days: float,
) -> tuple[int, float, float]:
    """Return (new_repetitions, new_ease_factor, new_interval_days)."""
    if quality < 3:
        repetitions = 0
        interval_days = 1
    else:
        if repetitions == 0:
            interval_days = 1
        elif repetitions == 1:
            interval_days = 6
        else:
            interval_days = round(interval_days * ease_factor)
        repetitions += 1

    ease_factor = max(1.3, ease_factor + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    return repetitions, ease_factor, float(interval_days)


# ---------- public API ----------

def update_schedule(
    item_id: str,
    item_type: str,
    scores: dict[str, int],
    max_scores: dict[str, int],
    session_type: str,
) -> date:
    """Update schedule for item and return next review date."""
    db.init_db()
    quality = compute_quality(scores, max_scores, session_type)

    existing = db.get_schedule(item_id)
    if existing:
        reps = existing["repetitions"]
        ef = existing["ease_factor"]
        interval = existing["interval_days"]
    else:
        reps, ef, interval = 0, 2.5, 1.0

    reps, ef, interval = _sm2(quality, reps, ef, interval)
    next_review = date.today() + timedelta(days=int(interval))

    db.upsert_schedule(
        item_id=item_id,
        item_type=item_type,
        next_review=next_review.isoformat(),
        interval_days=interval,
        ease_factor=ef,
        repetitions=reps,
        last_quality=quality,
    )
    return next_review


def get_due_items() -> list[dict]:
    db.init_db()
    return db.get_due_items(date.today().isoformat())


def get_weakest_item(item_ids: list[str]) -> str | None:
    """Return item_id with lowest last_quality among candidates, or None."""
    db.init_db()
    best_id = None
    best_q = 999.0
    for iid in item_ids:
        row = db.get_schedule(iid)
        if row and row["last_quality"] < best_q:
            best_q = row["last_quality"]
            best_id = iid
    return best_id
