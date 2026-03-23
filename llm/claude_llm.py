from __future__ import annotations

import anthropic

from llm.base import BaseLLM


class ClaudeLLM(BaseLLM):
    def __init__(self, model: str, api_key: str) -> None:
        self._client = anthropic.Anthropic(api_key=api_key)
        self._model = model

    def complete(self, prompt: str) -> str:
        try:
            message = self._client.messages.create(
                model=self._model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except anthropic.AuthenticationError as exc:
            raise RuntimeError(
                "Authentication failed for Anthropic. Check ANTHROPIC_API_KEY."
            ) from exc
        except anthropic.NotFoundError as exc:
            raise RuntimeError(
                f"Model not found or unavailable: {self._model}."
            ) from exc
        except anthropic.RateLimitError as exc:
            raise RuntimeError("Anthropic rate limit reached. Try again later.") from exc
        except anthropic.APIConnectionError as exc:
            raise RuntimeError(
                "Could not connect to Anthropic API. Check network access."
            ) from exc
        except anthropic.BadRequestError as exc:
            raise RuntimeError(
                f"Anthropic rejected the request for model {self._model}."
            ) from exc
        except anthropic.APIError as exc:
            raise RuntimeError(f"Anthropic API error: {exc}") from exc
