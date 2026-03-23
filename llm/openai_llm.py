from __future__ import annotations

import openai

from llm.base import BaseLLM


class OpenAILLM(BaseLLM):
    """Supports any OpenAI-compatible API (OpenAI, Ollama, SiliconFlow, etc.)."""

    def __init__(self, model: str, api_key: str, base_url: str | None = None) -> None:
        self._client = openai.OpenAI(api_key=api_key, base_url=base_url)
        self._model = model
        self._base_url = base_url

    def complete(self, prompt: str) -> str:
        try:
            response = self._client.chat.completions.create(
                model=self._model,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except openai.AuthenticationError as exc:
            raise RuntimeError(
                "Authentication failed for OpenAI-compatible provider. "
                "Check your API key and provider account permissions."
            ) from exc
        except openai.NotFoundError as exc:
            raise RuntimeError(
                f"Model not found or unavailable: {self._model}. "
                "Check MODEL_INTERVIEWER and provider model access."
            ) from exc
        except openai.RateLimitError as exc:
            raise RuntimeError(
                "Rate limit reached from OpenAI-compatible provider. Try again later."
            ) from exc
        except openai.APIConnectionError as exc:
            target = self._base_url or "provider API"
            raise RuntimeError(
                f"Could not connect to {target}. Check network access and base URL."
            ) from exc
        except openai.BadRequestError as exc:
            raise RuntimeError(
                f"Provider rejected the request for model {self._model}. "
                "Check model name, request format, or provider compatibility."
            ) from exc
        except openai.OpenAIError as exc:
            raise RuntimeError(f"OpenAI-compatible provider error: {exc}") from exc
