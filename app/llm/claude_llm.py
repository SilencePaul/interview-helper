"""ClaudeLLM — real Anthropic API implementation for PROD mode."""
from __future__ import annotations

import anthropic

from app.llm.base import LLMBase


class ClaudeLLM(LLMBase):
    def __init__(self, api_key: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)

    def chat(
        self,
        model: str,
        system: str,
        messages: list[dict],
        max_tokens: int = 2048,
    ) -> str:
        response = self._client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )
        return response.content[0].text
