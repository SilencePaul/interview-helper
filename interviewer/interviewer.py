from __future__ import annotations

import json
import random
import sys
import warnings
from dataclasses import dataclass

from knowledge.indexer import ConceptEntry, load_index
from knowledge.loader import (
    MAX_CONCEPT_CHARS,
    Concept,
    load_block,
    parse_bullet_list,
)
from llm.base import BaseLLM
from llm.mock_llm import MockLLM

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

_QUESTION_PROMPT = """\
You are a technical interviewer. Based on the concept and trigger below, \
generate ONE natural interview question in Chinese.

Concept: {title}
Category: {category}
Trigger: {trigger}

Return ONLY the question text. No explanation, no preamble.\
"""

_EVAL_PROMPT = """\
You are a strict technical interviewer evaluating a candidate's answer in Chinese.

## Concept: {title}
## Category: {category}

## Reference Content:
{content}

## Question asked:
{question}

## Candidate's answer:
{user_answer}

Evaluate the answer. Respond with ONLY valid JSON — no markdown fences, no extra text:
{{
  "score": <integer 0-10>,
  "strengths": [<strength strings in Chinese>],
  "missing_points": [<missing point strings in Chinese>],
  "ideal_answer": "<concise 30-second spoken answer in Chinese>"
}}\
"""

_FOLLOWUP_PROMPT = """\
You are a technical interviewer. The candidate's first answer was incomplete (score < 6).

## Concept: {title}
## Original question: {question}
## Candidate's answer: {user_answer}
## Key points they missed:
{missing_points}

Generate ONE follow-up question in Chinese that:
- Provides a gentle hint pointing toward the missing points
- Narrows the scope to what they got wrong
- Does NOT reveal the answer directly

Return ONLY the follow-up question text. No explanation, no preamble.\
"""


# ---------------------------------------------------------------------------
# Result dataclass
# ---------------------------------------------------------------------------

@dataclass
class EvaluationResult:
    score: int
    strengths: list[str]
    missing_points: list[str]
    ideal_answer: str


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

class InterviewerAgent:
    def __init__(self, llm: BaseLLM, notes_dir: str, index_path: str) -> None:
        self.llm = llm
        self.notes_dir = notes_dir
        # Index loaded once at construction time — never re-read during a session
        self._index: list[ConceptEntry] = load_index(index_path)

    # ------------------------------------------------------------------
    # Core methods
    # ------------------------------------------------------------------

    def pick_concept(self) -> Concept:
        """Select a random concept from the cached index and load its block."""
        if not self._index:
            raise RuntimeError(
                "Concept index is empty. "
                "Run `python -m app build-index` to populate it."
            )
        entry = random.choice(self._index)
        content = load_block(entry.file_path, entry.start_line, entry.end_line)

        # Apply same size guard as parse_concept_blocks
        if len(content) > MAX_CONCEPT_CHARS:
            warnings.warn(
                f"Concept '{entry.title}' is {len(content)} chars "
                f"(>{MAX_CONCEPT_CHARS}), truncating before sending to LLM.",
                stacklevel=2,
            )
            content = content[:MAX_CONCEPT_CHARS]

        return Concept(
            title=entry.title,
            category=entry.category,
            content=content,
            triggers=entry.triggers,            # from index (already parsed)
            question_type=entry.question_type,  # from index
            follow_up_paths=parse_bullet_list(content, "🔥"),
            engineering_hooks=parse_bullet_list(content, "🛠"),
            file_path=entry.file_path,
            start_line=entry.start_line,
            end_line=entry.end_line,
        )

    def generate_question(self, concept: Concept) -> str:
        """Pick one trigger and ask the LLM to rephrase it as a natural question."""
        if not concept.triggers:
            return f"请介绍一下{concept.title}的核心概念和实际应用场景？"
        trigger = random.choice(concept.triggers)
        prompt = _QUESTION_PROMPT.format(
            title=concept.title,
            category=concept.category,
            trigger=trigger,
        )
        return self.llm.complete(prompt).strip()

    def generate_followup(
        self,
        concept: Concept,
        question: str,
        user_answer: str,
        missing_points: list[str],
    ) -> str:
        """Generate a single follow-up question hinting at what was missed."""
        bullets = "\n".join(f"- {p}" for p in missing_points) if missing_points else "- 回答缺少深度"
        prompt = _FOLLOWUP_PROMPT.format(
            title=concept.title,
            question=question,
            user_answer=user_answer,
            missing_points=bullets,
        )
        return self.llm.complete(prompt).strip()

    def evaluate_answer(
        self,
        question: str,
        user_answer: str,
        concept: Concept,
    ) -> EvaluationResult:
        """Evaluate the user's answer. Retries once on JSON parse failure (prod only)."""
        prompt = _EVAL_PROMPT.format(
            title=concept.title,
            category=concept.category,
            content=concept.content,
            question=question,
            user_answer=user_answer,
        )
        raw = self.llm.complete(prompt)
        result = _parse_evaluation(raw)

        if result is None:
            # Retry once — only worth attempting in prod (MockLLM is always valid)
            if not isinstance(self.llm, MockLLM):
                raw = self.llm.complete(prompt)
                result = _parse_evaluation(raw)

            if result is None:
                print(
                    "\nError: LLM returned invalid evaluation JSON. "
                    "Cannot grade answer."
                )
                print(f"\nRaw LLM response:\n{raw}")
                sys.exit(1)

        return result

    # ------------------------------------------------------------------
    # CLI loop
    # ------------------------------------------------------------------

    def run(self) -> None:
        print("\n=== Interviewer Agent v2 ===\n")

        concept = self.pick_concept()
        print(f"Topic : [{concept.category}] {concept.title}\n")

        question = self.generate_question(concept)
        print(f"Question: {question}\n")

        user_answer = input("Your answer: ").strip()
        if not user_answer:
            print("No answer provided. Exiting.")
            return

        print("\nEvaluating...\n")
        result = self.evaluate_answer(question, user_answer, concept)

        if result.score >= 6:
            _print_result(result)
            return

        # Round 1 score < 6 — one follow-up round
        print(f"Score: {result.score}/10 — Answer needs more depth. Here's a follow-up:\n")
        followup = self.generate_followup(concept, question, user_answer, result.missing_points)
        print(f"Follow-up: {followup}\n")

        second_answer = input("Your answer: ").strip()
        if not second_answer:
            print("No answer provided.")
            _print_result(result)
            return

        print("\nEvaluating...\n")
        final_result = self.evaluate_answer(followup, second_answer, concept)
        _print_result(final_result)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_evaluation(raw: str) -> EvaluationResult | None:
    """Parse LLM output into EvaluationResult. Returns None on any failure."""
    try:
        text = raw.strip()
        # Strip markdown code fences if the LLM wrapped the JSON
        if text.startswith("```"):
            lines = text.splitlines()
            # Drop first line (```json or ```) and last line (```)
            inner = lines[1:-1] if lines[-1].strip() == "```" else lines[1:]
            text = "\n".join(inner)

        data = json.loads(text)
        return EvaluationResult(
            score=int(data["score"]),
            strengths=list(data["strengths"]),
            missing_points=list(data["missing_points"]),
            ideal_answer=str(data["ideal_answer"]),
        )
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def _print_result(result: EvaluationResult) -> None:
    bar = "─" * 40
    print(f"{bar}")
    print(f"Score : {result.score}/10\n")

    print("Strengths:")
    for s in result.strengths:
        print(f"  ✓ {s}")

    print("\nMissing Points:")
    for m in result.missing_points:
        print(f"  ✗ {m}")

    print(f"\nIdeal Answer (30s):\n  {result.ideal_answer}")
    print(f"{bar}\n")
