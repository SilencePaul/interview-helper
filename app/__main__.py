from __future__ import annotations

import os
import sys
from pathlib import Path


def _load_dotenv() -> None:
    """Load .env from project root into os.environ (stdlib only, no dotenv pkg)."""
    env_file = Path(".env")
    if not env_file.exists():
        return
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        value = value.split(" #")[0].strip()  # strip inline comments
        os.environ.setdefault(key.strip(), value)


_load_dotenv()

_NOTES_DIR = "notes_clean_v2"
_INDEX_PATH = "data/concepts_index.json"


def main() -> None:
    args = sys.argv[1:]

    if not args:
        _usage()
        sys.exit(1)

    command = args[0]

    if command == "build-index":
        _cmd_build_index()
    elif command == "interview":
        mode = "prod" if "--prod" in args else "dev"
        _cmd_interview(mode)
    else:
        print(f"Unknown command: {command!r}")
        _usage()
        sys.exit(1)


def _cmd_build_index() -> None:
    from knowledge.indexer import build_index
    count = build_index(_NOTES_DIR, _INDEX_PATH)
    print(f"Indexed {count} concepts → {_INDEX_PATH}")


def _cmd_interview(mode: str) -> None:
    from interviewer.interviewer import InterviewerAgent
    from llm.factory import get_llm

    llm = get_llm(mode)
    agent = InterviewerAgent(llm=llm, notes_dir=_NOTES_DIR, index_path=_INDEX_PATH)
    agent.run()


def _usage() -> None:
    print("Usage:")
    print("  python -m app build-index")
    print("  python -m app interview           # dev mode (MockLLM, offline)")
    print("  python -m app interview --prod    # prod mode (reads LLM_PROVIDER from .env)")
    print()
    print("Providers (set LLM_PROVIDER in .env):")
    print("  anthropic  — ANTHROPIC_API_KEY required")
    print("  openai     — OPENAI_API_KEY required")
    print("  ollama     — local, no API key needed")


if __name__ == "__main__":
    main()
