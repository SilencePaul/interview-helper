"""Tests for db module — using temp SQLite files."""
import json
import sqlite3
import pytest
from pathlib import Path

import app.db as db_module


@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db_module, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(db_module, "DATA_DIR", tmp_path)
    db_module.init_db()


# ── sessions ───────────────────────────────────────────────────────────────────

class TestSessions:
    def test_insert_and_retrieve(self):
        db_module.insert_session(
            "sess1", "20240101_120000", "topic", "数据库_索引",
            7, 9, {"accuracy": 4, "completeness": 3}, ["missed X"]
        )
        rows = db_module.get_sessions()
        assert len(rows) == 1
        assert rows[0]["id"] == "sess1"
        assert rows[0]["item_id"] == "数据库_索引"
        assert rows[0]["total_score"] == 7
        assert rows[0]["max_score"] == 9

    def test_scores_stored_as_json(self):
        db_module.insert_session("s1", "ts", "topic", "item", 5, 9,
                                 {"accuracy": 4}, ["point"])
        rows = db_module.get_sessions()
        scores = json.loads(rows[0]["scores_json"])
        assert scores["accuracy"] == 4
        missed = json.loads(rows[0]["missed_json"])
        assert missed == ["point"]

    def test_get_sessions_returns_desc_order(self):
        db_module.insert_session("s1", "20240101_100000", "topic", "item1", 5, 9, {}, [])
        db_module.insert_session("s2", "20240101_110000", "topic", "item2", 7, 9, {}, [])
        rows = db_module.get_sessions()
        assert rows[0]["id"] == "s2"  # more recent first

    def test_get_sessions_respects_limit(self):
        for i in range(10):
            db_module.insert_session(f"s{i}", f"2024010{i:01d}", "algo",
                                     f"item{i}", i, 12, {}, [])
        rows = db_module.get_sessions(limit=5)
        assert len(rows) == 5

    def test_get_sessions_for_item_filters_correctly(self):
        db_module.insert_session("s1", "20240101", "topic", "target", 5, 9, {}, [])
        db_module.insert_session("s2", "20240102", "topic", "other", 7, 9, {}, [])
        rows = db_module.get_sessions_for_item("target")
        assert len(rows) == 1
        assert rows[0]["item_id"] == "target"

    def test_insert_replaces_on_same_id(self):
        db_module.insert_session("s1", "ts", "topic", "item", 5, 9, {}, [])
        db_module.insert_session("s1", "ts", "topic", "item", 8, 9, {}, [])
        rows = db_module.get_sessions()
        assert len(rows) == 1
        assert rows[0]["total_score"] == 8

    def test_empty_db_returns_empty_list(self):
        assert db_module.get_sessions() == []


# ── schedule ───────────────────────────────────────────────────────────────────

class TestSchedule:
    def test_upsert_and_get(self):
        db_module.upsert_schedule("item1", "topic", "2026-03-01", 6.0, 2.5, 1, 4.0)
        row = db_module.get_schedule("item1")
        assert row is not None
        assert row["item_id"] == "item1"
        assert row["item_type"] == "topic"
        assert row["next_review"] == "2026-03-01"
        assert row["ease_factor"] == pytest.approx(2.5)
        assert row["repetitions"] == 1
        assert row["last_quality"] == pytest.approx(4.0)

    def test_upsert_overwrites_existing(self):
        db_module.upsert_schedule("item1", "topic", "2026-03-01", 6.0, 2.5, 1, 4.0)
        db_module.upsert_schedule("item1", "topic", "2026-03-15", 15.0, 2.6, 2, 4.5)
        row = db_module.get_schedule("item1")
        assert row["interval_days"] == pytest.approx(15.0)
        assert row["repetitions"] == 2
        assert row["next_review"] == "2026-03-15"

    def test_get_schedule_returns_none_for_missing(self):
        assert db_module.get_schedule("nonexistent") is None

    def test_get_due_items_includes_past_and_today(self):
        db_module.upsert_schedule("past",   "algo", "2020-01-01", 1.0, 2.5, 0, 3.0)
        db_module.upsert_schedule("today",  "algo", "2026-02-27", 1.0, 2.5, 0, 3.5)
        db_module.upsert_schedule("future", "algo", "2099-01-01", 1.0, 2.5, 0, 4.0)
        due = db_module.get_due_items("2026-02-27")
        ids = {d["item_id"] for d in due}
        assert "past" in ids
        assert "today" in ids
        assert "future" not in ids

    def test_get_due_items_empty_when_nothing_due(self):
        db_module.upsert_schedule("future", "topic", "2099-01-01", 1.0, 2.5, 0, 4.0)
        due = db_module.get_due_items("2026-02-27")
        assert due == []

    def test_get_all_schedule_ordered_by_next_review(self):
        db_module.upsert_schedule("b_item", "topic", "2026-03-10", 1.0, 2.5, 0, 3.0)
        db_module.upsert_schedule("a_item", "topic", "2026-03-01", 1.0, 2.5, 0, 3.0)
        rows = db_module.get_all_schedule()
        assert rows[0]["item_id"] == "a_item"
        assert rows[1]["item_id"] == "b_item"

    def test_get_all_schedule_empty(self):
        assert db_module.get_all_schedule() == []


# ── mistakes ───────────────────────────────────────────────────────────────────

class TestMistakes:
    def _count_mistakes(self):
        con = sqlite3.connect(db_module.DB_PATH)
        count = con.execute("SELECT COUNT(*) FROM mistakes").fetchone()[0]
        con.close()
        return count

    def _fetch_all_mistakes(self):
        con = sqlite3.connect(db_module.DB_PATH)
        rows = con.execute("SELECT * FROM mistakes").fetchall()
        con.close()
        return rows

    def test_insert_single_mistake(self):
        db_module.insert_mistake(
            "sess1", "item1", "subject", "first reaction",
            "trigger words", ["q1", "q2"], "2026-03-01"
        )
        assert self._count_mistakes() == 1

    def test_mistake_fields_stored_correctly(self):
        db_module.insert_mistake(
            "sess1", "lc_1", "两数之和", "暴力解法",
            "哈希表", ["为什么用哈希表？"], "2026-03-05"
        )
        rows = self._fetch_all_mistakes()
        row = rows[0]
        assert row[1] == "sess1"          # session_id
        assert row[2] == "lc_1"           # item_id
        assert row[3] == "两数之和"        # prompt_subject
        assert row[4] == "暴力解法"        # first_reaction
        assert row[5] == "哈希表"          # trigger_words
        assert json.loads(row[6]) == ["为什么用哈希表？"]  # self_questions_json
        assert row[7] == "2026-03-05"     # next_review_date

    def test_insert_multiple_mistakes_each_gets_own_row(self):
        db_module.insert_mistake("s1", "i1", "sub1", "r1", "tw1", ["q1"], "2026-03-01")
        db_module.insert_mistake("s2", "i2", "sub2", "r2", "tw2", ["q2"], "2026-03-02")
        assert self._count_mistakes() == 2

    def test_mistakes_have_autoincrement_id(self):
        db_module.insert_mistake("s1", "i1", "s", "r", "t", [], "2026-03-01")
        db_module.insert_mistake("s2", "i2", "s", "r", "t", [], "2026-03-02")
        rows = self._fetch_all_mistakes()
        ids = [r[0] for r in rows]
        assert ids[0] != ids[1]


# ── init_db idempotency ────────────────────────────────────────────────────────

def test_init_db_is_idempotent():
    # Calling init_db multiple times should not raise
    db_module.init_db()
    db_module.init_db()
    db_module.init_db()
    # Tables should still be there
    db_module.insert_session("s1", "ts", "topic", "item", 0, 9, {}, [])
    assert len(db_module.get_sessions()) == 1
