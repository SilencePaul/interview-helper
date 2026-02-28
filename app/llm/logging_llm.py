"""LoggingLLM — wraps any LLMBase to add timing, structured logging, and call accumulation."""
from __future__ import annotations

import logging
import time

from app.llm.base import LLMBase, ChatResponse

logger = logging.getLogger(__name__)


class LoggingLLM(LLMBase):
    """Transparent wrapper that logs each chat() call and accumulates call records."""

    def __init__(self, inner: LLMBase) -> None:
        self._inner = inner
        self._calls: list[dict] = []

    def chat(
        self,
        model: str,
        system: str,
        messages: list[dict],
        max_tokens: int = 2048,
        tag: str = "",
    ) -> ChatResponse:
        start = time.perf_counter()
        response = self._inner.chat(model, system, messages, max_tokens, tag)
        latency_s = time.perf_counter() - start

        record = {
            "tag": tag,
            "model": model,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "latency_s": latency_s,
        }
        self._calls.append(record)

        logger.info(
            "llm_call tag=%r model=%s in=%d out=%d latency=%.3fs",
            tag, model, response.input_tokens, response.output_tokens, latency_s,
        )

        return response

    def session_summary(self) -> list[dict]:
        """Return all accumulated call records for this session."""
        return list(self._calls)

    def total_tokens(self) -> tuple[int, int]:
        """Return (total_input_tokens, total_output_tokens) across all calls."""
        total_in = sum(r["input_tokens"] for r in self._calls)
        total_out = sum(r["output_tokens"] for r in self._calls)
        return total_in, total_out
