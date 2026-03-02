# Interviewer Agent v2

A CLI-based technical interview practice tool that draws from Chinese 八股文 knowledge notes, asks targeted questions, evaluates your answers, and guides you with follow-up questions when needed.

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
Expected output: `Indexed 256 concepts → data/concepts_index.json`

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

**Restrict to a category:**
```bash
python -m app interview --module 数据库
```

**Restrict to a single file:**
```bash
python -m app interview --file 索引.md
```

Flags can be combined:
```bash
python -m app interview --prod --module 计算机网络
```

---

## What the Agent Does

Each session runs one interview cycle (max 2 rounds):

1. **Picks a random concept** from the index (256 concepts across 6 categories)
2. **Generates one interview question** based on a trigger from the notes
3. **Waits for your answer** via CLI input
4. **Evaluates your answer** using the LLM against the reference content
5. **If score ≥ 6** — prints full result and finishes
6. **If score < 6** — generates one follow-up question that hints at what you missed (without revealing the answer), accepts a second answer, then prints the final evaluation

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
| 数据库 (Database) | 53 |
| llm | 49 |
| 前端 (Frontend) | 42 |
| 操作系统 (OS) | 40 |
| 计算机网络 (Networking) | 38 |
| 设计模式 (Design Patterns) | 34 |

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
notes_clean_v2/         Knowledge base (256 concepts, 41 markdown files)
data/                   Generated index (gitignored, rebuilt by build-index)
tests/                  pytest test suite
.env                    LLM config and API keys (gitignored)
```
