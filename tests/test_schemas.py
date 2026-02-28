"""Tests for Pydantic v2 schemas."""
import pytest
from datetime import date
from pydantic import ValidationError

from app.schemas import Problem, ReviewResult, ScheduleEntry, MistakeEntry


# ── Problem ────────────────────────────────────────────────────────────────────

class TestProblem:
    def test_valid_minimal_problem(self):
        p = Problem(
            id="lc_1", title="Two Sum", difficulty="easy",
            tags=["hashmap"], description="Find two numbers",
        )
        assert p.id == "lc_1"
        assert p.difficulty == "easy"
        assert p.time_limit_sec == 1800  # default
        assert p.examples == []
        assert p.constraints == []
        assert p.rubric == {}

    def test_problem_with_all_fields(self):
        p = Problem(
            id="lc_76",
            title="Minimum Window Substring",
            difficulty="hard",
            tags=["sliding_window", "hashmap"],
            description="Find min window covering t",
            examples=["s=ADOBECODEBANC, t=ABC → BANC"],
            constraints=["1 <= m, n <= 10^5"],
            time_limit_sec=2400,
            rubric={"recognize_pattern": 3, "correctness": 4},
        )
        assert p.time_limit_sec == 2400
        assert len(p.tags) == 2
        assert p.rubric["recognize_pattern"] == 3

    def test_problem_missing_required_id_raises(self):
        with pytest.raises(ValidationError):
            Problem(title="Missing id", difficulty="easy",
                    tags=[], description="desc")

    def test_problem_missing_required_title_raises(self):
        with pytest.raises(ValidationError):
            Problem(id="x", difficulty="easy", tags=[], description="desc")

    def test_problem_tags_default_empty(self):
        p = Problem(id="x", title="X", difficulty="easy",
                    tags=[], description="desc")
        assert p.tags == []

    def test_problem_rubric_values_are_ints(self):
        p = Problem(
            id="x", title="X", difficulty="easy", tags=[], description="desc",
            rubric={"correctness": 4, "complexity": 2},
        )
        assert isinstance(p.rubric["correctness"], int)


# ── ReviewResult ───────────────────────────────────────────────────────────────

class TestReviewResult:
    def test_valid_review_result(self):
        r = ReviewResult(
            session_id="s1", item_id="数据库_索引",
            score_breakdown={"accuracy": 4, "completeness": 3, "clarity": 2},
            total=9, max_score=9,
            missed_points=[],
            model_answer_structure="1. 索引定义 2. 实现",
            next_drills=["复习事务"],
        )
        assert r.total == 9
        assert r.max_score == 9

    def test_review_result_with_missed_points(self):
        r = ReviewResult(
            session_id="s1", item_id="item",
            score_breakdown={"accuracy": 2},
            total=2, max_score=9,
            missed_points=["遗漏B+树高度分析", "遗漏聚簇索引"],
            model_answer_structure="",
            next_drills=[],
        )
        assert len(r.missed_points) == 2

    def test_review_result_missing_required_fields_raises(self):
        with pytest.raises(ValidationError):
            ReviewResult(session_id="s1")  # missing many fields


# ── ScheduleEntry ──────────────────────────────────────────────────────────────

class TestScheduleEntry:
    def test_valid_schedule_entry(self):
        s = ScheduleEntry(
            item_id="数据库_索引",
            item_type="topic",
            next_review=date(2026, 3, 5),
            interval_days=6.0,
            ease_factor=2.5,
            repetitions=1,
            last_quality=4.0,
        )
        assert s.next_review == date(2026, 3, 5)
        assert s.ease_factor == 2.5
        assert s.repetitions == 1

    def test_schedule_entry_algo_type(self):
        s = ScheduleEntry(
            item_id="lc_1", item_type="algo",
            next_review=date(2026, 3, 1),
            interval_days=1.0, ease_factor=2.5,
            repetitions=0, last_quality=0.0,
        )
        assert s.item_type == "algo"

    def test_schedule_entry_missing_required_raises(self):
        with pytest.raises(ValidationError):
            ScheduleEntry(item_id="x")


# ── MistakeEntry ───────────────────────────────────────────────────────────────

class TestMistakeEntry:
    def test_valid_mistake_entry(self):
        m = MistakeEntry(
            session_id="s1", item_id="lc_1",
            prompt_subject="两数之和",
            first_reaction="用暴力双重循环",
            trigger_words="哈希表, complement",
            self_questions=["为什么用哈希表？", "如何处理重复元素？"],
            next_review_date=date(2026, 3, 5),
        )
        assert len(m.self_questions) == 2
        assert m.next_review_date == date(2026, 3, 5)

    def test_mistake_entry_empty_self_questions(self):
        m = MistakeEntry(
            session_id="s1", item_id="item",
            prompt_subject="subject",
            first_reaction="reaction",
            trigger_words="words",
            self_questions=[],
            next_review_date=date(2026, 3, 1),
        )
        assert m.self_questions == []

    def test_mistake_entry_missing_required_raises(self):
        with pytest.raises(ValidationError):
            MistakeEntry(session_id="s1")
