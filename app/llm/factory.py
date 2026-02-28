"""LLM factory — selects implementation based on APP_ENV."""
from __future__ import annotations

from app.llm.logging_llm import LoggingLLM


def get_llm() -> LoggingLLM:
    """Return a LoggingLLM-wrapped MockLLM (dev) or ClaudeLLM (prod).

    Fail fast if APP_ENV=prod and ANTHROPIC_API_KEY is missing.
    """
    from app.config import APP_ENV, ANTHROPIC_API_KEY

    if APP_ENV == "dev":
        from app.llm.mock_llm import MockLLM
        return LoggingLLM(MockLLM())

    # prod mode
    if not ANTHROPIC_API_KEY:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is required in prod mode. "
            "Set it in your .env file or export it as an environment variable."
        )
    from app.llm.claude_llm import ClaudeLLM
    return LoggingLLM(ClaudeLLM(api_key=ANTHROPIC_API_KEY))
