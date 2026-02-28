"""LLM abstraction layer."""
from app.llm.base import LLMBase
from app.llm.factory import get_llm

__all__ = ["LLMBase", "get_llm"]
