from __future__ import annotations

import json

from llm.base import BaseLLM

_MOCK_QUESTION = "请解释一下这个概念的核心原理，并说明它在实际工程中的应用场景？"

_MOCK_FOLLOWUP_ACCURACY = "你刚才的表述有点泛。先别展开场景，能不能先更准确地定义一下这个概念，并说明它和相近概念的边界区别？"
_MOCK_FOLLOWUP_COMPLETENESS = "你已经说到一部分了。如果让我按要点检查，这个问题你还漏了哪些关键点？可以再补全一下。"
_MOCK_FOLLOWUP_PRACTICALITY = "如果把它放到真实工程里，你会在什么场景下用它？有什么收益、代价或风险需要权衡？"
_MOCK_FOLLOWUP_CLARITY = "你知道这个点，但表达还可以更清楚一些。你能按“定义-原理-场景”这三个层次重新组织一下回答吗？"

_MOCK_EVALUATION_LOW = {
    "score": 4,
    "dimensions": {
        "accuracy": 2,
        "completeness": 1,
        "practicality": 0,
        "clarity": 1,
    },
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
    "dimensions": {
        "accuracy": 3,
        "completeness": 2,
        "practicality": 1,
        "clarity": 1,
    },
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
    def __init__(self) -> None:
        self._eval_count = 0

    def complete(self, prompt: str) -> str:
        if "Lowest scoring dimension" in prompt:
            if "场景意识" in prompt:
                return _MOCK_FOLLOWUP_PRACTICALITY
            if "完整性" in prompt:
                return _MOCK_FOLLOWUP_COMPLETENESS
            if "表达清晰度" in prompt:
                return _MOCK_FOLLOWUP_CLARITY
            return _MOCK_FOLLOWUP_ACCURACY
        if "valid JSON" in prompt or '"score"' in prompt:
            self._eval_count += 1
            if self._eval_count == 1:
                return json.dumps(_MOCK_EVALUATION_LOW, ensure_ascii=False)
            return json.dumps(_MOCK_EVALUATION_HIGH, ensure_ascii=False)
        return _MOCK_QUESTION
