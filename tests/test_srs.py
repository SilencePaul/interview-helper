"""Tests for SRS (SM-2) module."""
import pytest
from datetime import date, timedelta

from app.srs import compute_quality, _sm2, update_schedule, get_weakest_item


# ── compute_quality ────────────────────────────────────────────────────────────

class TestComputeQuality:
    def test_zero_max_returns_zero(self):
        assert compute_quality({}, {}, "topic") == 0.0

    def test_perfect_score_returns_5(self):
        scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        assert compute_quality(scores, max_scores, "topic") == 5.0

    def test_zero_score_returns_zero(self):
        scores = {"accuracy": 0, "completeness": 0, "clarity": 0}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        assert compute_quality(scores, max_scores, "topic") == 0.0

    def test_correctness_zero_caps_at_2(self):
        scores = {"recognize_pattern": 3, "correctness": 0, "complexity": 2,
                  "edge_cases": 1, "pattern_articulation": 2}
        max_scores = {"recognize_pattern": 3, "correctness": 4, "complexity": 2,
                      "edge_cases": 1, "pattern_articulation": 2}
        q = compute_quality(scores, max_scores, "algo")
        assert q <= 2.0

    def test_recognize_pattern_zero_caps_at_2(self):
        scores = {"recognize_pattern": 0, "correctness": 4, "complexity": 2,
                  "edge_cases": 1, "pattern_articulation": 2}
        max_scores = {"recognize_pattern": 3, "correctness": 4, "complexity": 2,
                      "edge_cases": 1, "pattern_articulation": 2}
        q = compute_quality(scores, max_scores, "algo")
        assert q <= 2.0

    def test_accuracy_zero_caps_at_2_via_alias(self):
        # "accuracy" is treated as alias for "correctness"
        scores = {"accuracy": 0, "completeness": 3, "clarity": 2}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        q = compute_quality(scores, max_scores, "topic")
        assert q <= 2.0

    def test_key_concepts_missed_3_caps_at_3_for_topic(self):
        scores = {"accuracy": 4, "completeness": 3, "clarity": 2, "key_concepts_missed": 3}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2, "key_concepts_missed": 0}
        q = compute_quality(scores, max_scores, "topic")
        assert q <= 3.0

    def test_key_concepts_missed_2_no_cap(self):
        # 2 < 3 threshold → the cap-at-3 does NOT apply.
        # Note: key_concepts_missed is included in sum(scores) but max=0, so
        # raw_quality inflates above 5 — the important thing is it stays > 3.0.
        scores = {"accuracy": 4, "completeness": 3, "clarity": 2, "key_concepts_missed": 2}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2, "key_concepts_missed": 0}
        q = compute_quality(scores, max_scores, "topic")
        assert q > 3.0  # cap at 3.0 does NOT fire when missed < 3

    def test_topic_cap_does_not_apply_to_algo_session(self):
        # key_concepts_missed>=3 cap only applies when session_type=="topic"
        scores = {"correctness": 4, "complexity": 2, "key_concepts_missed": 5}
        max_scores = {"correctness": 4, "complexity": 2, "key_concepts_missed": 0}
        q_algo = compute_quality(scores, max_scores, "algo")
        q_topic = compute_quality(scores, max_scores, "topic")
        assert q_topic <= 3.0
        # algo session: no topic cap (correctness>0, so no correctness cap either)
        assert q_algo > 3.0

    def test_partial_score_in_range(self):
        scores = {"accuracy": 2, "completeness": 2, "clarity": 1}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        q = compute_quality(scores, max_scores, "topic")
        assert 0.0 < q < 5.0

    def test_result_rounded_to_2_decimals(self):
        scores = {"a": 1}
        max_scores = {"a": 3}
        q = compute_quality(scores, max_scores, "topic")
        assert q == round(q, 2)

    def test_both_caps_applied_when_both_triggered(self):
        # correctness=0 AND key_concepts_missed=5 → quality should be ≤2 (strictest)
        scores = {"accuracy": 4, "completeness": 3, "clarity": 2,
                  "correctness": 0, "key_concepts_missed": 5}
        max_scores = {"accuracy": 4, "completeness": 3, "clarity": 2,
                      "correctness": 4, "key_concepts_missed": 0}
        q = compute_quality(scores, max_scores, "topic")
        assert q <= 2.0


# ── _sm2 ───────────────────────────────────────────────────────────────────────

class TestSM2:
    def test_quality_lt_3_resets_repetitions_and_interval(self):
        reps, ef, interval = _sm2(quality=2.0, repetitions=5, ease_factor=2.5, interval_days=30)
        assert reps == 0
        assert interval == 1.0

    def test_quality_gte_3_first_repetition(self):
        reps, ef, interval = _sm2(quality=4.0, repetitions=0, ease_factor=2.5, interval_days=1)
        assert reps == 1
        assert interval == 1.0

    def test_quality_gte_3_second_repetition(self):
        reps, ef, interval = _sm2(quality=4.0, repetitions=1, ease_factor=2.5, interval_days=1)
        assert reps == 2
        assert interval == 6.0

    def test_quality_gte_3_later_repetitions_scales_by_ef(self):
        reps, ef, interval = _sm2(quality=4.0, repetitions=2, ease_factor=2.5, interval_days=6)
        assert reps == 3
        assert interval == round(6 * 2.5)

    def test_ease_factor_increases_at_perfect_quality(self):
        _, ef, _ = _sm2(quality=5.0, repetitions=0, ease_factor=2.5, interval_days=1)
        assert ef > 2.5

    def test_ease_factor_decreases_at_low_quality(self):
        _, ef, _ = _sm2(quality=3.0, repetitions=0, ease_factor=2.5, interval_days=1)
        assert ef < 2.5

    def test_ease_factor_never_below_1_3(self):
        _, ef, _ = _sm2(quality=0.0, repetitions=0, ease_factor=1.3, interval_days=1)
        assert ef >= 1.3

    def test_interval_is_float(self):
        _, _, interval = _sm2(quality=4.0, repetitions=0, ease_factor=2.5, interval_days=1)
        assert isinstance(interval, float)


# ── update_schedule (integration with real SQLite, temp file) ─────────────────

@pytest.fixture()
def tmp_db(tmp_path, monkeypatch):
    import app.db as db_mod
    monkeypatch.setattr(db_mod, "DB_PATH", tmp_path / "test.db")
    monkeypatch.setattr(db_mod, "DATA_DIR", tmp_path)


class TestUpdateSchedule:
    def test_returns_date_object(self, tmp_db):
        result = update_schedule(
            "item_a", "topic",
            {"accuracy": 4, "completeness": 3, "clarity": 2},
            {"accuracy": 4, "completeness": 3, "clarity": 2},
            "topic",
        )
        assert isinstance(result, date)

    def test_perfect_score_schedules_at_least_today(self, tmp_db):
        result = update_schedule(
            "item_perfect", "topic",
            {"accuracy": 4, "completeness": 3, "clarity": 2},
            {"accuracy": 4, "completeness": 3, "clarity": 2},
            "topic",
        )
        assert result >= date.today()

    def test_zero_score_schedules_tomorrow(self, tmp_db):
        result = update_schedule(
            "item_zero", "topic",
            {"accuracy": 0, "completeness": 0, "clarity": 0},
            {"accuracy": 4, "completeness": 3, "clarity": 2},
            "topic",
        )
        assert result == date.today() + timedelta(days=1)

    def test_repeated_perfect_scores_increase_interval(self, tmp_db):
        scores = {"accuracy": 4, "completeness": 3, "clarity": 2}
        max_s = {"accuracy": 4, "completeness": 3, "clarity": 2}
        d1 = update_schedule("item_rep", "topic", scores, max_s, "topic")
        d2 = update_schedule("item_rep", "topic", scores, max_s, "topic")
        d3 = update_schedule("item_rep", "topic", scores, max_s, "topic")
        assert d2 >= d1
        assert d3 >= d2

    def test_algo_type_stored_correctly(self, tmp_db):
        import app.db as db_mod
        db_mod.init_db()
        update_schedule(
            "lc_1", "algo",
            {"recognize_pattern": 3, "correctness": 4},
            {"recognize_pattern": 3, "correctness": 4},
            "algo",
        )
        row = db_mod.get_schedule("lc_1")
        assert row is not None
        assert row["item_type"] == "algo"


# ── get_weakest_item ───────────────────────────────────────────────────────────

class TestGetWeakestItem:
    def test_returns_none_when_no_data(self, tmp_db):
        result = get_weakest_item(["a", "b", "c"])
        assert result is None

    def test_returns_weakest_among_scheduled_items(self, tmp_db):
        update_schedule("strong", "topic",
                        {"accuracy": 4, "completeness": 3, "clarity": 2},
                        {"accuracy": 4, "completeness": 3, "clarity": 2}, "topic")
        update_schedule("weak", "topic",
                        {"accuracy": 0, "completeness": 1, "clarity": 0},
                        {"accuracy": 4, "completeness": 3, "clarity": 2}, "topic")
        result = get_weakest_item(["strong", "weak"])
        assert result == "weak"

    def test_ignores_items_not_in_candidate_list(self, tmp_db):
        update_schedule("item_a", "topic",
                        {"accuracy": 4, "completeness": 3, "clarity": 2},
                        {"accuracy": 4, "completeness": 3, "clarity": 2}, "topic")
        update_schedule("item_b", "topic",
                        {"accuracy": 0, "completeness": 0, "clarity": 0},
                        {"accuracy": 4, "completeness": 3, "clarity": 2}, "topic")
        # Only candidate is item_a; item_b is weaker but not in list
        result = get_weakest_item(["item_a"])
        assert result == "item_a"

    def test_empty_candidate_list_returns_none(self, tmp_db):
        assert get_weakest_item([]) is None
