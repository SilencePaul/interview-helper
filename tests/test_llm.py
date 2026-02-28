"""Tests for LoggingLLM — delegation, accumulation, and session summary."""
from unittest.mock import MagicMock

from app.llm.base import LLMBase, ChatResponse
from app.llm.logging_llm import LoggingLLM


def _make_inner(text: str, input_tokens: int = 10, output_tokens: int = 5) -> LLMBase:
    inner = MagicMock(spec=LLMBase)
    inner.chat.return_value = ChatResponse(
        text=text, input_tokens=input_tokens, output_tokens=output_tokens
    )
    return inner


class TestLoggingLLM:
    def test_delegates_to_inner_and_returns_chat_response(self):
        inner = _make_inner("hello", input_tokens=20, output_tokens=8)
        llm = LoggingLLM(inner)
        response = llm.chat("model-x", "system", [{"role": "user", "content": "hi"}])
        assert isinstance(response, ChatResponse)
        assert response.text == "hello"
        assert response.input_tokens == 20
        assert response.output_tokens == 8

    def test_passes_all_args_to_inner(self):
        inner = _make_inner("ok")
        llm = LoggingLLM(inner)
        messages = [{"role": "user", "content": "test"}]
        llm.chat("my-model", "my-system", messages, max_tokens=512, tag="test.tag")
        inner.chat.assert_called_once_with("my-model", "my-system", messages, 512, "test.tag")

    def test_accumulates_call_records(self):
        inner = _make_inner("reply", input_tokens=10, output_tokens=4)
        llm = LoggingLLM(inner)
        llm.chat("m", "s", [], tag="call.one")
        llm.chat("m", "s", [], tag="call.two")
        summary = llm.session_summary()
        assert len(summary) == 2
        assert summary[0]["tag"] == "call.one"
        assert summary[1]["tag"] == "call.two"

    def test_session_summary_returns_copy(self):
        inner = _make_inner("r")
        llm = LoggingLLM(inner)
        llm.chat("m", "s", [])
        s1 = llm.session_summary()
        s1.append({"injected": True})
        s2 = llm.session_summary()
        assert len(s2) == 1  # internal state not mutated

    def test_total_tokens_sums_across_calls(self):
        inner = MagicMock(spec=LLMBase)
        inner.chat.side_effect = [
            ChatResponse(text="a", input_tokens=10, output_tokens=3),
            ChatResponse(text="b", input_tokens=20, output_tokens=7),
        ]
        llm = LoggingLLM(inner)
        llm.chat("m", "s", [])
        llm.chat("m", "s", [])
        total_in, total_out = llm.total_tokens()
        assert total_in == 30
        assert total_out == 10

    def test_total_tokens_zero_when_no_calls(self):
        inner = _make_inner("x")
        llm = LoggingLLM(inner)
        assert llm.total_tokens() == (0, 0)

    def test_record_contains_latency(self):
        inner = _make_inner("x")
        llm = LoggingLLM(inner)
        llm.chat("m", "s", [], tag="latency.test")
        record = llm.session_summary()[0]
        assert "latency_s" in record
        assert record["latency_s"] >= 0.0

    def test_record_contains_model(self):
        inner = _make_inner("x")
        llm = LoggingLLM(inner)
        llm.chat("special-model", "s", [], tag="tag1")
        record = llm.session_summary()[0]
        assert record["model"] == "special-model"
        assert record["tag"] == "tag1"
