"""Tests for TutorAgent, InterviewerAgent, GraderAgent — LLM injected via DI."""
import json
import pytest
from unittest.mock import MagicMock

from app.agents import TutorAgent, InterviewerAgent, GraderAgent, GradeResult
from app.llm.base import LLMBase, ChatResponse
from app.schemas import Problem


# ── helpers ─────────────────────────────────────────────────────────────────────

def _make_response(text: str) -> ChatResponse:
    return ChatResponse(text=text, input_tokens=len(text) // 4, output_tokens=len(text) // 4)


def _mock_llm(return_value: str = "") -> LLMBase:
    """Return a MagicMock LLM whose chat() returns a ChatResponse."""
    llm = MagicMock(spec=LLMBase)
    llm.chat.return_value = _make_response(return_value)
    return llm


# ── fixtures ───────────────────────────────────────────────────────────────────

SAMPLE_PROBLEM = Problem(
    id="lc_1",
    title="两数之和",
    difficulty="easy",
    tags=["hashmap"],
    description="给定 nums 和 target，找两数之和等于 target 的下标。",
    examples=["nums=[2,7], target=9 → [0,1]"],
    constraints=["2 <= nums.length <= 10^4"],
    rubric={
        "recognize_pattern": 3,
        "correctness": 4,
        "complexity": 2,
        "edge_cases": 1,
        "pattern_articulation": 2,
    },
)

VALID_TOPIC_GRADE = json.dumps({
    "score_breakdown": {"accuracy": 3, "completeness": 2, "clarity": 2},
    "missed_points": ["遗漏了聚簇索引的细节"],
    "model_answer_structure": "1. 索引定义 2. B+树原理 3. 使用场景",
    "next_drills": ["复习事务隔离级别", "练习SQL explain"],
})

VALID_ALGO_GRADE = json.dumps({
    "score_breakdown": {
        "recognize_pattern": 3, "correctness": 4,
        "complexity": 2, "edge_cases": 1, "pattern_articulation": 2,
    },
    "missed_points": [],
    "model_answer_structure": "哈希表一遍扫描，O(n)时间O(n)空间",
    "next_drills": ["LC 3 滑动窗口"],
})


# ── TutorAgent ─────────────────────────────────────────────────────────────────

class TestTutorAgent:
    def test_start_session_parses_numbered_questions(self):
        llm = _mock_llm(
            "1. 什么是B+树索引？\n"
            "2. 哈希索引的局限是什么？\n"
            "3. 聚簇与非聚簇索引的区别？"
        )
        agent = TutorAgent(llm)
        questions = agent.start_session("## 索引", "B+树...")
        assert len(questions) == 3
        assert all(q[0].isdigit() for q in questions)

    def test_start_session_fallback_when_no_numbered_lines(self):
        llm = _mock_llm("Please explain indexing.")
        agent = TutorAgent(llm)
        questions = agent.start_session("outline", "content")
        assert questions == ["Please explain indexing."]

    def test_start_session_sends_outline_and_chunks(self):
        llm = _mock_llm("1. Question?")
        agent = TutorAgent(llm)
        agent.start_session("MY_OUTLINE", "MY_CHUNKS")
        messages = llm.chat.call_args[0][2]
        user_content = messages[0]["content"]
        assert "MY_OUTLINE" in user_content
        assert "MY_CHUNKS" in user_content

    def test_answer_appends_exchange_to_history(self):
        llm = _mock_llm("1. Q?")
        agent = TutorAgent(llm)
        agent.start_session("outline", "content")

        llm.chat.return_value = _make_response("Good point! Consider also...")
        agent.answer("I think it's B+tree structure.")

        transcript = agent.get_transcript()
        user_msgs = [m["content"] for m in transcript if m["role"] == "user"]
        asst_msgs = [m["content"] for m in transcript if m["role"] == "assistant"]
        assert any("B+tree" in c for c in user_msgs)
        assert any("Good point" in c for c in asst_msgs)

    def test_answer_returns_tutor_reply(self):
        llm = _mock_llm("1. Q?")
        agent = TutorAgent(llm)
        agent.start_session("o", "c")
        llm.chat.return_value = _make_response("Tutor reply text")
        result = agent.answer("my answer")
        assert result == "Tutor reply text"

    def test_get_transcript_returns_copy_not_reference(self):
        llm = _mock_llm("1. Q?")
        agent = TutorAgent(llm)
        agent.start_session("o", "c")
        t1 = agent.get_transcript()
        original_len = len(t1)
        t1.append({"role": "injected", "content": "extra"})
        t2 = agent.get_transcript()
        assert len(t2) == original_len  # internal state not mutated

    def test_uses_model_tutor(self):
        llm = _mock_llm("1. Q?")
        from app.config import MODEL_TUTOR
        agent = TutorAgent(llm)
        agent.start_session("o", "c")
        model_used = llm.chat.call_args[0][0]
        assert model_used == MODEL_TUTOR


# ── InterviewerAgent ───────────────────────────────────────────────────────────

class TestInterviewerAgent:
    def test_present_returns_string(self):
        llm = _mock_llm("好的，我来介绍这道题...")
        agent = InterviewerAgent(llm)
        result = agent.present(SAMPLE_PROBLEM)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_present_sends_problem_title_to_model(self):
        llm = _mock_llm("presentation")
        agent = InterviewerAgent(llm)
        agent.present(SAMPLE_PROBLEM)
        messages = llm.chat.call_args[0][2]
        user_content = messages[0]["content"]
        assert "两数之和" in user_content

    def test_present_sends_examples_and_constraints(self):
        llm = _mock_llm("pres")
        agent = InterviewerAgent(llm)
        agent.present(SAMPLE_PROBLEM)
        messages = llm.chat.call_args[0][2]
        user_content = messages[0]["content"]
        assert "nums=[2,7]" in user_content
        assert "2 <= nums.length" in user_content

    def test_probe_normal_returns_string(self):
        llm = _mock_llm("Interesting approach.")
        agent = InterviewerAgent(llm)
        agent._problem = SAMPLE_PROBLEM
        agent._history = [{"role": "assistant", "content": "problem statement"}]
        result = agent.probe("I'll use a hash map", elapsed_sec=100)
        assert isinstance(result, str)

    def test_probe_at_time_limit_injects_timeout_marker(self):
        llm = _mock_llm("Time's up, summarize.")
        agent = InterviewerAgent(llm)
        agent._problem = SAMPLE_PROBLEM
        agent._history = []
        agent.probe("my answer", elapsed_sec=SAMPLE_PROBLEM.time_limit_sec + 1)
        # history is passed by reference; assistant reply appended after call,
        # but the [时间到] user message was appended before — scan all messages.
        messages = llm.chat.call_args[0][2]
        assert any("[时间到]" in m["content"] for m in messages)

    def test_probe_under_time_limit_no_timeout_marker(self):
        llm = _mock_llm("Follow-up question.")
        agent = InterviewerAgent(llm)
        agent._problem = SAMPLE_PROBLEM
        agent._history = []
        agent.probe("my answer", elapsed_sec=10)
        messages = llm.chat.call_args[0][2]
        last_user_content = messages[-1]["content"]
        assert "[时间到]" not in last_user_content

    def test_transcript_grows_with_each_turn(self):
        llm = _mock_llm("reply")
        agent = InterviewerAgent(llm)
        agent.present(SAMPLE_PROBLEM)
        assert len(agent.get_transcript()) == 2  # user + assistant
        agent.probe("answer 1", elapsed_sec=0)
        assert len(agent.get_transcript()) == 4
        agent.probe("answer 2", elapsed_sec=0)
        assert len(agent.get_transcript()) == 6

    def test_uses_model_interviewer(self):
        llm = _mock_llm("reply")
        from app.config import MODEL_INTERVIEWER
        agent = InterviewerAgent(llm)
        agent.present(SAMPLE_PROBLEM)
        model_used = llm.chat.call_args[0][0]
        assert model_used == MODEL_INTERVIEWER


# ── GraderAgent ────────────────────────────────────────────────────────────────

class TestGraderAgent:
    def test_grade_topic_valid_json_returns_grade_result(self):
        llm = _mock_llm(VALID_TOPIC_GRADE)
        agent = GraderAgent(llm)
        result = agent.grade_topic(
            "## 索引", "B+树...",
            [{"role": "user", "content": "B+树是平衡多叉树"}],
        )
        assert isinstance(result, GradeResult)
        assert result.total == 3 + 2 + 2  # 7
        assert result.max_score == 9       # 4+3+2
        assert result.missed_points == ["遗漏了聚簇索引的细节"]
        assert len(result.next_drills) == 2

    def test_grade_topic_fallback_on_invalid_json(self):
        llm = _mock_llm("这是一段非JSON的回复内容")
        agent = GraderAgent(llm)
        result = agent.grade_topic("outline", "chunks", [])
        assert result.total == 0
        assert "无法解析" in result.missed_points[0]
        assert result.model_answer_structure == "这是一段非JSON的回复内容"

    def test_grade_topic_json_embedded_in_prose(self):
        llm = _mock_llm("这是评分：\n" + VALID_TOPIC_GRADE + "\n以上。")
        agent = GraderAgent(llm)
        result = agent.grade_topic("outline", "content", [])
        assert result.total == 7

    def test_grade_algo_valid_json_returns_grade_result(self):
        llm = _mock_llm(VALID_ALGO_GRADE)
        agent = GraderAgent(llm)
        result = agent.grade_algo(
            SAMPLE_PROBLEM,
            [{"role": "user", "content": "用哈希表O(n)"}],
        )
        assert result.total == 12   # 3+4+2+1+2
        assert result.max_score == 12
        assert result.missed_points == []

    def test_grade_algo_fills_missing_rubric_keys_with_zero(self):
        partial = json.dumps({
            "score_breakdown": {"recognize_pattern": 2},  # only one key
            "missed_points": [],
            "model_answer_structure": "framework",
            "next_drills": [],
        })
        llm = _mock_llm(partial)
        agent = GraderAgent(llm)
        result = agent.grade_algo(SAMPLE_PROBLEM, [])
        # All rubric keys should appear, missing ones filled with 0
        for key in SAMPLE_PROBLEM.rubric:
            assert key in result.score_breakdown
        assert result.score_breakdown["correctness"] == 0

    def test_grade_algo_uses_problem_rubric(self):
        custom_problem = Problem(
            id="custom", title="Custom", difficulty="medium",
            tags=[], description="desc",
            rubric={"correctness": 10},
        )
        llm = _mock_llm(json.dumps({
            "score_breakdown": {"correctness": 8},
            "missed_points": [],
            "model_answer_structure": "approach",
            "next_drills": [],
        }))
        agent = GraderAgent(llm)
        result = agent.grade_algo(custom_problem, [])
        assert result.max_score == 10

    def test_grade_algo_fallback_rubric_when_empty(self):
        problem_no_rubric = Problem(
            id="x", title="X", difficulty="easy",
            tags=[], description="desc",
            rubric={},  # empty rubric → should use default
        )
        llm = _mock_llm(VALID_ALGO_GRADE)
        agent = GraderAgent(llm)
        result = agent.grade_algo(problem_no_rubric, [])
        # Default rubric: recognize_pattern(3)+correctness(4)+complexity(2)+edge_cases(1)+pattern_articulation(2)=12
        assert result.max_score == 12

    def test_grade_topic_sends_outline_and_chunks(self):
        llm = _mock_llm(VALID_TOPIC_GRADE)
        agent = GraderAgent(llm)
        agent.grade_topic("THE_OUTLINE", "THE_CHUNKS", [])
        messages = llm.chat.call_args[0][2]
        user_content = messages[0]["content"]
        assert "THE_OUTLINE" in user_content
        assert "THE_CHUNKS" in user_content

    def test_grade_uses_model_grader(self):
        llm = _mock_llm(VALID_TOPIC_GRADE)
        from app.config import MODEL_GRADER
        agent = GraderAgent(llm)
        agent.grade_topic("o", "c", [])
        model_used = llm.chat.call_args[0][0]
        assert model_used == MODEL_GRADER
