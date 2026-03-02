from __future__ import annotations

import openai

from llm.base import BaseLLM


class OpenAILLM(BaseLLM):
    """Supports any OpenAI-compatible API (OpenAI, Ollama, etc.)."""

    def __init__(self, model: str, api_key: str, base_url: str | None = None) -> None:
        self._client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self._model = model

    def complete(self, prompt: str) -> str:
        response = self._client.chat.completions.create(
            model=self._model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
