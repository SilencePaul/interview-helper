"""SQLite helpers: init schema, upsert, query."""
import json
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from app.config import DB_PATH, DATA_DIR

SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id          TEXT PRIMARY KEY,
    timestamp   TEXT NOT NULL,
    session_type TEXT NOT NULL,          -- topic | algo
    item_id     TEXT NOT NULL,
    total_score INTEGER NOT NULL,
    max_score   INTEGER NOT NULL,
    scores_json TEXT NOT NULL,           -- JSON object
    missed_json TEXT NOT NULL            -- JSON array
);

CREATE TABLE IF NOT EXISTS schedule (
    item_id      TEXT PRIMARY KEY,
    item_type    TEXT NOT NULL,          -- topic | algo
    next_review  TEXT NOT NULL,          -- ISO date
    interval_days REAL NOT NULL DEFAULT 1,
    ease_factor  REAL NOT NULL DEFAULT 2.5,
    repetitions  INTEGER NOT NULL DEFAULT 0,
    last_quality REAL NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS mistakes (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id         TEXT NOT NULL,
    item_id            TEXT NOT NULL,
    prompt_subject     TEXT NOT NULL,
    first_reaction     TEXT NOT NULL,
    trigger_words      TEXT NOT NULL,
    self_questions_json TEXT NOT NULL,   -- JSON array
    next_review_date   TEXT NOT NULL
);
"""


def init_db() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with _conn() as con:
        con.executescript(SCHEMA)


@contextmanager
def _conn():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    try:
        yield con
        con.commit()
    finally:
        con.close()


# ---------- sessions ----------

def insert_session(
    session_id: str,
    timestamp: str,
    session_type: str,
    item_id: str,
    total_score: int,
    max_score: int,
    scores: dict,
    missed: list,
) -> None:
    with _conn() as con:
        con.execute(
            """INSERT OR REPLACE INTO sessions
               (id, timestamp, session_type, item_id, total_score, max_score, scores_json, missed_json)
               VALUES (?,?,?,?,?,?,?,?)""",
            (session_id, timestamp, session_type, item_id,
             total_score, max_score, json.dumps(scores), json.dumps(missed)),
        )


def get_sessions(limit: int = 50) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM sessions ORDER BY timestamp DESC LIMIT ?", (limit,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_sessions_for_item(item_id: str) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM sessions WHERE item_id=? ORDER BY timestamp DESC",
            (item_id,),
        ).fetchall()
    return [dict(r) for r in rows]


# ---------- schedule ----------

def upsert_schedule(
    item_id: str,
    item_type: str,
    next_review: str,
    interval_days: float,
    ease_factor: float,
    repetitions: int,
    last_quality: float,
) -> None:
    with _conn() as con:
        con.execute(
            """INSERT OR REPLACE INTO schedule
               (item_id, item_type, next_review, interval_days, ease_factor, repetitions, last_quality)
               VALUES (?,?,?,?,?,?,?)""",
            (item_id, item_type, next_review, interval_days,
             ease_factor, repetitions, last_quality),
        )


def get_schedule(item_id: str) -> dict | None:
    with _conn() as con:
        row = con.execute(
            "SELECT * FROM schedule WHERE item_id=?", (item_id,)
        ).fetchone()
    return dict(row) if row else None


def get_due_items(today: str) -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM schedule WHERE next_review <= ?", (today,)
        ).fetchall()
    return [dict(r) for r in rows]


def get_all_schedule() -> list[dict]:
    with _conn() as con:
        rows = con.execute(
            "SELECT * FROM schedule ORDER BY next_review"
        ).fetchall()
    return [dict(r) for r in rows]


# ---------- mistakes ----------

def insert_mistake(
    session_id: str,
    item_id: str,
    prompt_subject: str,
    first_reaction: str,
    trigger_words: str,
    self_questions: list[str],
    next_review_date: str,
) -> None:
    with _conn() as con:
        con.execute(
            """INSERT INTO mistakes
               (session_id, item_id, prompt_subject, first_reaction,
                trigger_words, self_questions_json, next_review_date)
               VALUES (?,?,?,?,?,?,?)""",
            (session_id, item_id, prompt_subject, first_reaction,
             trigger_words, json.dumps(self_questions), next_review_date),
        )
