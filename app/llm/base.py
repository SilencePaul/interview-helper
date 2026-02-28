"""Abstract LLM interface."""
from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class ChatResponse:
    text: str
    input_tokens: int
    output_tokens: int


class LLMBase(ABC):
    @abstractmethod
    def chat(
        self,
        model: str,
        system: str,
        messages: list[dict],
        max_tokens: int = 2048,
        tag: str = "",
    ) -> ChatResponse:
        """Send a chat request and return a ChatResponse with text and token counts."""
        ...
