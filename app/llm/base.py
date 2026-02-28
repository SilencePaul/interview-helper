"""Abstract LLM interface."""
from __future__ import annotations
from abc import ABC, abstractmethod


class LLMBase(ABC):
    @abstractmethod
    def chat(
        self,
        model: str,
        system: str,
        messages: list[dict],
        max_tokens: int = 2048,
    ) -> str:
        """Send a chat request and return the assistant's text response."""
        ...
