from __future__ import annotations

import os

from llm.base import BaseLLM

_DEFAULTS = {
    "anthropic": "claude-sonnet-4-6",
    "openai": "gpt-4o",
    "ollama": "llama3",
    "siliconflow": "Qwen/Qwen2.5-7B-Instruct",
}


def get_llm(mode: str = "dev") -> BaseLLM:
    """Return the appropriate LLM for the given mode.

    dev  → MockLLM (offline, no API key)
    prod → dispatches on LLM_PROVIDER env var:
             anthropic   (default) — requires ANTHROPIC_API_KEY
             openai                — requires OPENAI_API_KEY
             ollama                — local, no key needed
             siliconflow           — requires SILICONFLOW_API_KEY
    """
    if mode == "dev":
        from llm.mock_llm import MockLLM
        return MockLLM()

    if mode == "prod":
        provider = os.environ.get("LLM_PROVIDER", "anthropic").lower()
        model = os.environ.get("MODEL_INTERVIEWER", _DEFAULTS.get(provider, ""))

        if provider == "anthropic":
            api_key = os.environ.get("ANTHROPIC_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "ANTHROPIC_API_KEY is not set. Add it to .env or export it."
                )
            from llm.claude_llm import ClaudeLLM
            return ClaudeLLM(model=model, api_key=api_key)

        if provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "OPENAI_API_KEY is not set. Add it to .env or export it."
                )
            from llm.openai_llm import OpenAILLM
            return OpenAILLM(model=model, api_key=api_key)

        if provider == "ollama":
            base_url = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434/v1")
            from llm.openai_llm import OpenAILLM
            return OpenAILLM(model=model, api_key="ollama", base_url=base_url)

        if provider == "siliconflow":
            api_key = os.environ.get("SILICONFLOW_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "SILICONFLOW_API_KEY is not set. Add it to .env or export it."
                )
            base_url = os.environ.get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")
            from llm.openai_llm import OpenAILLM
            return OpenAILLM(model=model, api_key=api_key, base_url=base_url)

        raise ValueError(
            f"Unknown LLM_PROVIDER: {provider!r}. "
            "Choose: anthropic | openai | ollama | siliconflow"
        )

    raise ValueError(f"Unknown mode: {mode!r}. Use 'dev' or 'prod'.")
