from __future__ import annotations

import json

from llm.base import BaseLLM

_MOCK_QUESTION = "请解释一下这个概念的核心原理，并说明它在实际工程中的应用场景？"

_MOCK_FOLLOWUP = "你提到了基本原理，但能具体说说底层实现机制是什么吗？比如它是如何处理边界条件的？"

_MOCK_EVALUATION_LOW = {
    "score": 4,
    "strengths": [
        "提到了基本概念",
    ],
    "missing_points": [
        "未提及具体的边界条件和异常情况处理",
        "对底层实现机制的解释不够深入",
        "缺少实际工程应用场景举例",
    ],
    "ideal_answer": (
        "这个概念的核心是将问题分层处理，通过明确的接口隔离职责。"
        "在实际工程中，通常在需要解耦、扩展性要求高的场景下使用，"
        "需要特别注意线程安全和资源释放等关键问题。"
    ),
}

_MOCK_EVALUATION_HIGH = {
    "score": 7,
    "strengths": [
        "理解了核心概念，能够清晰描述基本原理",
        "举了相关的工程实例，说明了使用场景",
    ],
    "missing_points": [
        "未提及具体的边界条件和异常情况处理",
        "对底层实现机制的解释不够深入",
    ],
    "ideal_answer": (
        "这个概念的核心是将问题分层处理，通过明确的接口隔离职责。"
        "在实际工程中，通常在需要解耦、扩展性要求高的场景下使用，"
        "需要特别注意线程安全和资源释放等关键问题。"
    ),
}


class MockLLM(BaseLLM):
    """Offline mock LLM for dev mode. Returns canned responses. No API calls.

    Evaluation cycle in dev mode:
      - First eval call  → low score (4) to exercise the follow-up branch.
      - Second eval call → high score (7) as the final result.
    """

    def __init__(self) -> None:
        self._eval_count = 0

    def complete(self, prompt: str) -> str:
        # Follow-up question generation (contains the unique marker from _FOLLOWUP_PROMPT)
        if "Key points they missed" in prompt:
            return _MOCK_FOLLOWUP
        # Evaluation requests
        if "valid JSON" in prompt or '"score"' in prompt:
            self._eval_count += 1
            if self._eval_count == 1:
                return json.dumps(_MOCK_EVALUATION_LOW, ensure_ascii=False)
            return json.dumps(_MOCK_EVALUATION_HIGH, ensure_ascii=False)
        return _MOCK_QUESTION
