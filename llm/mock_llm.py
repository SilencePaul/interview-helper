from __future__ import annotations

import json

from llm.base import BaseLLM

_MOCK_QUESTION = "请解释一下这个概念的核心原理，并说明它在实际工程中的应用场景？"

_MOCK_EVALUATION = {
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
    """Offline mock LLM for dev mode. Returns canned responses. No API calls."""

    def complete(self, prompt: str) -> str:
        # Detect evaluation requests by the JSON format instruction in the prompt
        if "valid JSON" in prompt or '"score"' in prompt:
            return json.dumps(_MOCK_EVALUATION, ensure_ascii=False)
        return _MOCK_QUESTION
