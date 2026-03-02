# Interviewer Agent v1

A CLI-based technical interview practice tool that draws from Chinese 八股文 knowledge notes, asks targeted questions, and evaluates your answers using an LLM.

---

## Setup

**1. Set Python version**
```bash
pyenv local 3.11.9
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure your LLM** — edit `.env` in the project root:
```
LLM_PROVIDER=anthropic          # anthropic | openai | ollama
MODEL_INTERVIEWER=claude-sonnet-4-6
ANTHROPIC_API_KEY=sk-ant-...    # your real key
```

**4. Build the concept index** (one-time, re-run if notes change)
```bash
python -m app build-index
```
Expected output: `Indexed 338 concepts → data/concepts_index.json`

---

## Running the Agent

**Dev mode** — offline, no API key needed, uses mock responses:
```bash
python -m app interview
```

**Prod mode** — real LLM, reads provider and key from `.env`:
```bash
python -m app interview --prod
```

---

## What the Agent Does

Each session runs one full interview cycle:

1. **Picks a random concept** from the index (338 concepts across 6 categories)
2. **Generates one interview question** based on a trigger from the notes
3. **Waits for your answer** via CLI input
4. **Evaluates your answer** using the LLM against the reference content
5. **Prints a structured result:**
   - Score (0–10)
   - Strengths — what you got right
   - Missing points — what you left out
   - Ideal answer — a concise 30-second spoken answer

---

## Supported LLM Providers

| Provider | `LLM_PROVIDER` | Key required | Example model |
|---|---|---|---|
| Anthropic (Claude) | `anthropic` | `ANTHROPIC_API_KEY` | `claude-sonnet-4-6` |
| OpenAI | `openai` | `OPENAI_API_KEY` | `gpt-4o` |
| Ollama (local) | `ollama` | none | `llama3` |

To switch providers, change `LLM_PROVIDER` and `MODEL_INTERVIEWER` in `.env`.

For Ollama, set the base URL if not using the default:
```
OLLAMA_BASE_URL=http://localhost:11434/v1
```

---

## Knowledge Base

Notes live in `notes_clean_v2/` across 6 categories:

| Category | Concepts |
|---|---|
| 数据库 (Database) | 69 |
| llm | 67 |
| 前端 (Frontend) | 54 |
| 操作系统 (OS) | 52 |
| 计算机网络 (Networking) | 49 |
| 设计模式 (Design Patterns) | 47 |

Each concept block contains interview triggers, question types, follow-up paths, and engineering hooks used to generate and evaluate questions.

---

## Running Tests

```bash
python -m pytest tests/ -v
```

32 tests covering block parsing, index building, and load correctness.

---

## Project Structure

```
app/                    CLI entry point (python -m app ...)
interviewer/            InterviewerAgent logic
knowledge/              Concept block parser + index builder/loader
llm/                    LLM abstraction (MockLLM, ClaudeLLM, OpenAILLM)
notes_clean_v2/         Knowledge base (338 concepts, 41 markdown files)
data/                   Generated index (gitignored, rebuilt by build-index)
tests/                  pytest test suite
.env                    LLM config and API keys (gitignored)
```
