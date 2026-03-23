from __future__ import annotations

import json
import random
import sys
import warnings
from collections import defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from knowledge.indexer import ConceptEntry, load_index
from knowledge.loader import MAX_CONCEPT_CHARS, Concept, load_block, parse_bullet_list
from llm.base import BaseLLM
from llm.mock_llm import MockLLM

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
  "dimensions": {{
    "accuracy": <integer 0-4>,
    "completeness": <integer 0-3>,
    "practicality": <integer 0-2>,
    "clarity": <integer 0-1>
  }},
  "strengths": [<strength strings in Chinese>],
  "missing_points": [<missing point strings in Chinese>],
  "ideal_answer": "<concise 30-second spoken answer in Chinese>"
}}

Scoring rules:
- accuracy: 0-4
- completeness: 0-3
- practicality: 0-2
- clarity: 0-1
- score must equal the sum of the four dimensions
- Keep strengths and missing_points concise and practical
\
"""

_FOLLOWUP_PROMPT = """\
You are a technical interviewer. The candidate's first answer was incomplete (score < 6).

## Concept: {title}
## Original question: {question}
## Candidate's answer: {user_answer}
## Lowest scoring dimension: {focus_dimension}
## Follow-up intent: {followup_intent}
## Key points they missed:
{missing_points}

Generate ONE follow-up question in Chinese that:
- Focuses primarily on the lowest scoring dimension
- Provides a gentle hint pointing toward the missing points
- Narrows the scope to what they got wrong
- Does NOT reveal the answer directly
- Sounds like a real interviewer asking a targeted follow-up

Return ONLY the follow-up question text. No explanation, no preamble.\
"""

_LOW_SCORE_THRESHOLD = 6
_DEFAULT_DIMENSIONS = {"accuracy": 0, "completeness": 0, "practicality": 0, "clarity": 0}
_DIMENSION_LABELS = {"accuracy": "准确性", "completeness": "完整性", "practicality": "场景意识", "clarity": "表达清晰度"}
_DIMENSION_MAX = {"accuracy": 4, "completeness": 3, "practicality": 2, "clarity": 1}
_FOLLOWUP_INTENTS = {
    "accuracy": "追问核心定义、关键机制或概念边界，确认理解是否准确",
    "completeness": "追问回答中漏掉的关键点、步骤、对比项或约束条件",
    "practicality": "追问工程场景、适用条件、权衡、风险或实践经验",
    "clarity": "追问更有条理的表达，要求按层次、步骤或对比方式重述",
}


@dataclass
class EvaluationResult:
    score: int
    dimensions: dict[str, int]
    strengths: list[str]
    missing_points: list[str]
    ideal_answer: str


@dataclass
class HistoryRound:
    round: int
    question: str
    answer: str
    score: int
    dimensions: dict[str, int]
    strengths: list[str]
    missing_points: list[str]
    ideal_answer: str


@dataclass
class SessionOutcome:
    topic: str
    category: str
    final_score: int
    final_dimensions: dict[str, int]
    low_score: bool
    missing_points: list[str]


class InterviewerAgent:
    def __init__(self, llm: BaseLLM, notes_dir: str, index_path: str) -> None:
        self.llm = llm
        self.notes_dir = notes_dir
        self.index_path = index_path
        data_dir = Path(index_path).parent
        self.history_dir = data_dir / "history"
        self.summary_dir = data_dir / "summaries"
        self._index: list[ConceptEntry] = load_index(index_path)

    def pick_concept(self, pool: list[ConceptEntry] | None = None) -> Concept:
        candidates = pool if pool is not None else self._index
        if not candidates:
            raise RuntimeError("Concept index is empty. Run `python -m app build-index` to populate it.")
        return self.load_concept_from_entry(random.choice(candidates))

    def load_concept_from_entry(self, entry: ConceptEntry) -> Concept:
        content = load_block(entry.file_path, entry.start_line, entry.end_line)
        if len(content) > MAX_CONCEPT_CHARS:
            warnings.warn(f"Concept '{entry.title}' is {len(content)} chars (>{MAX_CONCEPT_CHARS}), truncating before sending to LLM.", stacklevel=2)
            content = content[:MAX_CONCEPT_CHARS]
        return Concept(entry.title, entry.category, content, entry.triggers, entry.question_type, parse_bullet_list(content, "🔥"), parse_bullet_list(content, "🛠"), entry.file_path, entry.start_line, entry.end_line)

    def generate_question(self, concept: Concept) -> str:
        if not concept.triggers:
            return f"请介绍一下{concept.title}的核心概念和实际应用场景？"
        return self.llm.complete(_QUESTION_PROMPT.format(title=concept.title, category=concept.category, trigger=random.choice(concept.triggers))).strip()

    def generate_followup(self, concept: Concept, question: str, user_answer: str, missing_points: list[str], dimensions: dict[str, int]) -> str:
        focus_key = _pick_followup_dimension(dimensions)
        bullets = "\n".join(f"- {p}" for p in missing_points) if missing_points else "- 回答缺少深度"
        return self.llm.complete(_FOLLOWUP_PROMPT.format(title=concept.title, question=question, user_answer=user_answer, focus_dimension=_DIMENSION_LABELS[focus_key], followup_intent=_FOLLOWUP_INTENTS[focus_key], missing_points=bullets)).strip()

    def evaluate_answer(self, question: str, user_answer: str, concept: Concept) -> EvaluationResult:
        prompt = _EVAL_PROMPT.format(title=concept.title, category=concept.category, content=concept.content, question=question, user_answer=user_answer)
        raw = self.llm.complete(prompt)
        result = _parse_evaluation(raw)
        if result is None and not isinstance(self.llm, MockLLM):
            raw = self.llm.complete(prompt)
            result = _parse_evaluation(raw)
        if result is None:
            print("\nError: LLM returned invalid evaluation JSON. Cannot grade answer.")
            print(f"\nRaw LLM response:\n{raw}")
            sys.exit(1)
        return result

    def save_history(self, *, mode: str, scope: str, concept: Concept, rounds: list[HistoryRound]) -> Path:
        self.history_dir.mkdir(parents=True, exist_ok=True)
        safe_timestamp = _make_timestamp_slug()
        file_path = self.history_dir / f"session-{safe_timestamp}.json"
        payload = {
            "version": 2,
            "saved_at": datetime.now(timezone.utc).isoformat(),
            "mode": mode,
            "scope": scope,
            "concept": {"title": concept.title, "category": concept.category, "file_path": concept.file_path, "start_line": concept.start_line, "end_line": concept.end_line},
            "round_count": len(rounds),
            "final_score": rounds[-1].score if rounds else None,
            "final_dimensions": rounds[-1].dimensions if rounds else None,
            "rounds": [asdict(r) for r in rounds],
        }
        file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return file_path

    def save_summary(self, payload: dict) -> Path:
        self.summary_dir.mkdir(parents=True, exist_ok=True)
        file_path = self.summary_dir / f"summary-{_make_timestamp_slug()}.json"
        file_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return file_path

    def load_review_candidates(self, pool: list[ConceptEntry]) -> list[ConceptEntry]:
        if not self.history_dir.exists():
            return []
        by_key = {(e.file_path, e.start_line, e.end_line): e for e in pool}
        seen: set[tuple[str, int, int]] = set()
        out: list[ConceptEntry] = []
        for history_file in sorted(self.history_dir.glob("session-*.json"), reverse=True):
            try:
                data = json.loads(history_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                continue
            if int(data.get("final_score", 0) or 0) >= _LOW_SCORE_THRESHOLD:
                continue
            concept = data.get("concept", {})
            key = (concept.get("file_path"), concept.get("start_line"), concept.get("end_line"))
            if key in seen or key not in by_key:
                continue
            seen.add(key)
            out.append(by_key[key])
        return out

    def run_one(self, *, mode: str = "dev", module: str | None = None, file: str | None = None, review_wrong: bool = False, no_followup: bool = False, session_label: str | None = None) -> SessionOutcome | None:
        pool = self._index
        scope = "Random"
        if module:
            pool = [e for e in pool if e.category == module]
            scope = module
        elif file:
            pool = [e for e in pool if Path(e.file_path).name == file]
            scope = file
        review_pool: list[ConceptEntry] = []
        if review_wrong:
            review_pool = self.load_review_candidates(pool)
            if review_pool:
                pool = review_pool
                scope = f"Wrong-first ({scope})"
            else:
                scope = f"Wrong-first ({scope}, no history hit → fallback random)"
        print(f"\n=== {session_label or 'Interviewer Agent v2'} ===\n")
        print(f"Training scope: {scope}\n")
        if not pool:
            print(f"Error: no concepts found for scope {scope!r}.")
            print("Check --module / --file value and ensure the index is up to date.")
            return None
        concept = self.pick_concept(pool)
        print(f"Topic : [{concept.category}] {concept.title}\n")
        if review_wrong and review_pool:
            print("Review mode: picked from low-score history.\n")
        question = self.generate_question(concept)
        print(f"Question: {question}\n")
        answer = input("Your answer: ").strip()
        if not answer:
            print("No answer provided. Exiting current round.")
            return None
        history_rounds: list[HistoryRound] = []
        print("\nEvaluating...\n")
        result = self.evaluate_answer(question, answer, concept)
        history_rounds.append(HistoryRound(1, question, answer, result.score, result.dimensions, result.strengths, result.missing_points, result.ideal_answer))
        final_result = result
        if result.score < _LOW_SCORE_THRESHOLD and not no_followup:
            print(f"Score: {result.score}/10 — Answer needs more depth. Here's a follow-up:\n")
            followup = self.generate_followup(concept, question, answer, result.missing_points, result.dimensions)
            print(f"Follow-up: {followup}\n")
            second_answer = input("Your answer: ").strip()
            if second_answer:
                print("\nEvaluating...\n")
                final_result = self.evaluate_answer(followup, second_answer, concept)
                history_rounds.append(HistoryRound(2, followup, second_answer, final_result.score, final_result.dimensions, final_result.strengths, final_result.missing_points, final_result.ideal_answer))
            else:
                print("No answer provided.")
        elif result.score < _LOW_SCORE_THRESHOLD and no_followup:
            print(f"Score: {result.score}/10 — no-followup mode, skipping follow-up.\n")
        _print_result(final_result)
        saved = self.save_history(mode=mode, scope=scope, concept=concept, rounds=history_rounds)
        print(f"History saved: {saved}")
        return SessionOutcome(topic=concept.title, category=concept.category, final_score=final_result.score, final_dimensions=final_result.dimensions, low_score=final_result.score < _LOW_SCORE_THRESHOLD, missing_points=final_result.missing_points)

    def run(self, mode: str = "dev", module: str | None = None, file: str | None = None, review_wrong: bool = False, no_followup: bool = False, count: int = 1) -> None:
        outcomes: list[SessionOutcome] = []
        for idx in range(count):
            outcome = self.run_one(mode=mode, module=module, file=file, review_wrong=review_wrong, no_followup=no_followup, session_label=f"Interviewer Agent v2 ({idx + 1}/{count})" if count > 1 else None)
            if outcome is None:
                if count > 1:
                    print("Stopped early.")
                break
            outcomes.append(outcome)
        if count > 1 and outcomes:
            summary = _build_session_summary(outcomes)
            _print_session_summary(summary)
            saved = self.save_summary(summary)
            print(f"Summary saved   : {saved}")


def _make_timestamp_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ").replace('.', '-')


def _pick_followup_dimension(dimensions: dict[str, int]) -> str:
    ratios = [(int(dimensions.get(k, 0)) / m if m else 1.0, int(dimensions.get(k, 0)), k) for k, m in _DIMENSION_MAX.items()]
    ratios.sort(key=lambda item: (item[0], item[1]))
    return ratios[0][2]


def _parse_evaluation(raw: str) -> EvaluationResult | None:
    try:
        text = raw.strip()
        if text.startswith("```"):
            lines = text.splitlines()
            text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
        data = json.loads(text)
        dimensions = dict(_DEFAULT_DIMENSIONS)
        dimensions.update({k: int(v) for k, v in data.get("dimensions", {}).items() if k in _DEFAULT_DIMENSIONS})
        score = sum(dimensions.values())
        return EvaluationResult(score, dimensions, list(data["strengths"]), list(data["missing_points"]), str(data["ideal_answer"]))
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        return None


def _build_session_summary(outcomes: list[SessionOutcome]) -> dict:
    total = len(outcomes)
    avg_score = sum(o.final_score for o in outcomes) / total
    low_count = sum(1 for o in outcomes if o.low_score)
    dim_totals = defaultdict(float)
    missing_counter = defaultdict(int)
    for o in outcomes:
        for key, value in o.final_dimensions.items():
            dim_totals[key] += value
        for item in o.missing_points:
            missing_counter[item] += 1
    weakest_key = min(_DIMENSION_LABELS, key=lambda k: dim_totals[k] / total)
    best = max(outcomes, key=lambda o: o.final_score)
    worst = min(outcomes, key=lambda o: o.final_score)
    top_missing = max(missing_counter.items(), key=lambda kv: kv[1])[0] if missing_counter else "无"
    if low_count > 0:
        suggestion = "下次建议优先开启 --review-wrong，先回补低分题。"
    elif weakest_key == "practicality":
        suggestion = "下次建议重点补工程场景与取舍，多回答“什么时候用、为什么用、代价是什么”。"
    elif weakest_key == "accuracy":
        suggestion = "下次建议先把定义、边界、核心机制讲准，再展开细节。"
    elif weakest_key == "completeness":
        suggestion = "下次建议按“定义-原理-步骤/对比-场景”结构回答，减少漏点。"
    else:
        suggestion = "下次建议把表达再结构化一点，先总后分，尽量分点回答。"
    return {
        "completed": total,
        "averageScore": avg_score,
        "lowScoreRounds": low_count,
        "weakestDimension": {"key": weakest_key, "label": _DIMENSION_LABELS[weakest_key], "value": dim_totals[weakest_key] / total},
        "bestTopic": {"category": best.category, "title": best.topic, "score": best.final_score},
        "worstTopic": {"category": worst.category, "title": worst.topic, "score": worst.final_score},
        "topMissing": top_missing,
        "suggestion": suggestion,
        "topics": [{"category": o.category, "title": o.topic, "score": o.final_score} for o in outcomes],
    }


def _print_result(result: EvaluationResult) -> None:
    bar = "─" * 40
    print(f"{bar}")
    print(f"Score : {result.score}/10\n")
    print("Dimensions:")
    print(f"  - 准确性: {result.dimensions['accuracy']}/4")
    print(f"  - 完整性: {result.dimensions['completeness']}/3")
    print(f"  - 场景意识: {result.dimensions['practicality']}/2")
    print(f"  - 表达清晰度: {result.dimensions['clarity']}/1")
    print("\nStrengths:")
    for s in result.strengths:
        print(f"  ✓ {s}")
    print("\nMissing Points:")
    for m in result.missing_points:
        print(f"  ✗ {m}")
    print(f"\nIdeal Answer (30s):\n  {result.ideal_answer}")
    print(f"{bar}\n")


def _print_session_summary(summary: dict) -> None:
    print("== Session summary ==")
    print(f"Completed       : {summary['completed']}")
    print(f"Average score   : {summary['averageScore']:.2f}/10")
    print(f"Low-score rounds: {summary['lowScoreRounds']}/{summary['completed']}")
    print(f"Weakest dim     : {summary['weakestDimension']['label']} ({summary['weakestDimension']['value']:.2f})")
    print(f"Best topic      : [{summary['bestTopic']['category']}] {summary['bestTopic']['title']} ({summary['bestTopic']['score']}/10)")
    print(f"Worst topic     : [{summary['worstTopic']['category']}] {summary['worstTopic']['title']} ({summary['worstTopic']['score']}/10)")
    print(f"Top missing     : {summary['topMissing']}")
    print(f"Suggestion      : {summary['suggestion']}")
    topics = "、".join(f"[{t['category']}] {t['title']}" for t in summary['topics'])
    print(f"Topics          : {topics}")
