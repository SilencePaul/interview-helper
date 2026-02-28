"""MockLLM — deterministic fake responses for DEV mode (no real API calls)."""
from __future__ import annotations

from app.llm.base import LLMBase, ChatResponse


_TOPIC_GRADE_JSON = """{
  "score_breakdown": {"accuracy": 3, "completeness": 2, "clarity": 2, "key_concepts_missed": 1},
  "missed_points": ["未详细说明底层实现机制"],
  "model_answer_structure": "1. 定义概念  2. 核心机制与原理  3. 常见应用场景与注意事项",
  "next_drills": ["手写核心代码示例", "对比相关概念的异同"]
}"""

_ALGO_GRADE_JSON = """{
  "score_breakdown": {"recognize_pattern": 2, "correctness": 3, "complexity": 1, "edge_cases": 1, "pattern_articulation": 1},
  "missed_points": ["边界条件处理不完整", "未分析空间复杂度"],
  "model_answer_structure": "1. 识别模式  2. 双指针/滑窗初始化  3. 循环逻辑  4. 时间O(n) 空间O(1)",
  "next_drills": ["练习同类型滑动窗口题", "手写完整含注释代码"]
}"""

_TUTOR_QUESTIONS = (
    "1. 请解释该技术的核心概念及其工作原理。\n"
    "2. 该机制与相关技术相比有何优缺点？\n"
    "3. 列举两个典型的实际应用场景。"
)

_INTERVIEWER_PRESENT = (
    "[Mock 面试官] 好的，我来给你出一道题目。\n"
    "请仔细阅读题意，先说思路再写代码。准备好了请告诉我。"
)

_FIGURE_REPLACEMENT = (
    "```\n"
    "[Mock Diagram]\n"
    "  ┌─────┐     ┌─────┐     ┌─────┐\n"
    "  │  A  │────►│  B  │────►│  C  │\n"
    "  └─────┘     └──┬──┘     └─────┘\n"
    "                 │\n"
    "                 ▼\n"
    "              ┌─────┐\n"
    "              │  D  │\n"
    "              └─────┘\n"
    "```"
)


class MockLLM(LLMBase):
    """Returns deterministic canned responses — no real API calls made."""

    def chat(
        self,
        model: str,
        system: str,
        messages: list[dict],
        max_tokens: int = 2048,
        tag: str = "",
    ) -> ChatResponse:
        last = messages[-1]["content"] if messages else ""

        # Grader: JSON response
        if "score_breakdown" in last or "严格JSON" in last:
            if "recognize_pattern" in last:
                text = _ALGO_GRADE_JSON
            else:
                text = _TOPIC_GRADE_JSON
        # Tutor: generate recall questions
        elif "生成2-3道" in last or "recall" in last.lower():
            text = _TUTOR_QUESTIONS
        # Interviewer: present problem
        elif "以面试官" in last or "面试官身份" in last:
            text = _INTERVIEWER_PRESENT
        # Figures: diagram generation (small max_tokens or diagram-related system)
        elif max_tokens <= 512 or "图表" in system or "图表" in last:
            text = _FIGURE_REPLACEMENT
        else:
            # Default conversational reply
            text = "[Mock] 这是 DEV 模式下的模拟回复。切换到 PROD 模式以使用真实 Claude API。"

        input_tokens = sum(len(m["content"]) for m in messages) // 4
        output_tokens = len(text) // 4
        return ChatResponse(text=text, input_tokens=input_tokens, output_tokens=output_tokens)
