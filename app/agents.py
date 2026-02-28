"""TutorAgent, InterviewerAgent, GraderAgent — receive LLM via dependency injection."""
from __future__ import annotations
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from app.config import MODEL_TUTOR, MODEL_INTERVIEWER, MODEL_GRADER, PROMPTS_DIR
from app.llm.base import LLMBase
from app.schemas import Problem


# ---------- helpers ----------

def _load_prompt(name: str) -> str:
    path = PROMPTS_DIR / name
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


# ---------- GradeResult ----------

@dataclass
class GradeResult:
    score_breakdown: dict[str, int]
    total: int
    max_score: int
    missed_points: list[str]
    model_answer_structure: str
    next_drills: list[str]


# ---------- TutorAgent ----------

class TutorAgent:
    def __init__(self, llm: LLMBase) -> None:
        self._llm = llm
        self._system = _load_prompt("tutor.txt")
        self._model = MODEL_TUTOR
        self._history: list[dict] = []

    def start_session(self, outline: str, chunks_text: str) -> list[str]:
        """Send outline + selected chunks; return 2-3 recall questions."""
        prompt = (
            f"这是笔记的目录结构：\n\n{outline}\n\n"
            f"以下是本次复习的具体内容：\n\n{chunks_text}\n\n"
            "请根据以上内容生成2-3道主动回忆问题。"
            "每道问题单独一行，用数字编号（1. 2. 3.）。"
        )
        self._history = [{"role": "user", "content": prompt}]
        r = self._llm.chat(self._model, self._system, self._history, tag="tutor.start_session")
        reply = r.text
        self._history.append({"role": "assistant", "content": reply})
        # Parse numbered questions
        questions = []
        for line in reply.splitlines():
            line = line.strip()
            if line and line[0].isdigit() and '.' in line:
                questions.append(line)
        return questions if questions else [reply]

    def answer(self, user_answer: str) -> str:
        """Send user's answer; return tutor follow-up or readiness signal."""
        self._history.append({"role": "user", "content": user_answer})
        r = self._llm.chat(self._model, self._system, self._history, tag="tutor.answer")
        reply = r.text
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def get_transcript(self) -> list[dict]:
        return list(self._history)


# ---------- InterviewerAgent ----------

class InterviewerAgent:
    def __init__(self, llm: LLMBase) -> None:
        self._llm = llm
        self._system = _load_prompt("interviewer.txt")
        self._model = MODEL_INTERVIEWER
        self._history: list[dict] = []
        self._problem: Problem | None = None

    def present(self, problem: Problem) -> str:
        self._problem = problem
        prompt = (
            f"题目：{problem.title}（{problem.difficulty}）\n\n"
            f"{problem.description}\n\n"
        )
        if problem.examples:
            prompt += "示例：\n" + "\n".join(problem.examples) + "\n\n"
        if problem.constraints:
            prompt += "约束：\n" + "\n".join(problem.constraints) + "\n\n"
        prompt += "请以面试官身份呈现这道题，并等待候选人的回答。"
        self._history = [{"role": "user", "content": prompt}]
        r = self._llm.chat(self._model, self._system, self._history, tag="interviewer.present")
        reply = r.text
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def probe(self, user_input: str, elapsed_sec: int) -> str:
        """Probe or wrap up based on elapsed time."""
        content = user_input
        if self._problem and elapsed_sec >= self._problem.time_limit_sec:
            content = f"[时间到] 候选人说: {user_input}\n请给出总结性追问或结束面试。"
        self._history.append({"role": "user", "content": content})
        r = self._llm.chat(self._model, self._system, self._history, tag="interviewer.probe")
        reply = r.text
        self._history.append({"role": "assistant", "content": reply})
        return reply

    def get_transcript(self) -> list[dict]:
        return list(self._history)


# ---------- GraderAgent ----------

class GraderAgent:
    def __init__(self, llm: LLMBase) -> None:
        self._llm = llm
        self._system = _load_prompt("grader.txt")
        self._model = MODEL_GRADER

    def _grade(self, user_prompt: str, rubric: dict[str, int]) -> GradeResult:
        messages = [{"role": "user", "content": user_prompt}]
        r = self._llm.chat(self._model, self._system, messages, tag="grader.grade")
        reply = r.text

        # Attempt JSON extraction
        try:
            json_start = reply.find('{')
            json_end = reply.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                data = json.loads(reply[json_start:json_end])
                breakdown = data.get("score_breakdown", {})
                # Fill zeros for missing rubric keys
                for k in rubric:
                    if k not in breakdown:
                        breakdown[k] = 0
                total = sum(breakdown.values())
                return GradeResult(
                    score_breakdown=breakdown,
                    total=total,
                    max_score=sum(rubric.values()),
                    missed_points=data.get("missed_points", []),
                    model_answer_structure=data.get("model_answer_structure", ""),
                    next_drills=data.get("next_drills", []),
                )
        except (json.JSONDecodeError, KeyError):
            pass

        # Fallback: zero scores, raw reply as model answer
        breakdown = {k: 0 for k in rubric}
        return GradeResult(
            score_breakdown=breakdown,
            total=0,
            max_score=sum(rubric.values()),
            missed_points=["无法解析评分结果，请查看原始回复"],
            model_answer_structure=reply,
            next_drills=[],
        )

    def grade_topic(
        self,
        outline: str,
        chunks_text: str,
        transcript: list[dict],
    ) -> GradeResult:
        rubric = {"accuracy": 4, "completeness": 3, "clarity": 2}
        transcript_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in transcript
        )
        prompt = (
            "你是一个严格的技术面试评分官。请根据以下参考资料和考生回答进行评分。\n\n"
            f"【笔记目录】\n{outline}\n\n"
            f"【参考内容】\n{chunks_text}\n\n"
            f"【对话记录】\n{transcript_text}\n\n"
            "请按以下维度评分，并以JSON格式返回结果：\n"
            "accuracy(0-4): 事实准确性\n"
            "completeness(0-3): 内容完整性\n"
            "clarity(0-2): 表达清晰度\n"
            "key_concepts_missed(整数): 遗漏的关键概念数量\n\n"
            "返回格式（严格JSON）：\n"
            "{\n"
            '  "score_breakdown": {"accuracy": N, "completeness": N, "clarity": N, "key_concepts_missed": N},\n'
            '  "missed_points": ["..."],\n'
            '  "model_answer_structure": "标准答题框架...",\n'
            '  "next_drills": ["推荐练习1", "推荐练习2"]\n'
            "}"
        )
        return self._grade(prompt, rubric)

    def grade_algo(
        self,
        problem: Problem,
        transcript: list[dict],
    ) -> GradeResult:
        rubric = problem.rubric if problem.rubric else {
            "recognize_pattern": 3,
            "correctness": 4,
            "complexity": 2,
            "edge_cases": 1,
            "pattern_articulation": 2,
        }
        transcript_text = "\n".join(
            f"{m['role'].upper()}: {m['content']}" for m in transcript
        )
        rubric_desc = "\n".join(f"{k}(0-{v})" for k, v in rubric.items())
        prompt = (
            "你是一个严格的算法面试评分官。请根据题目和候选人的作答记录进行评分。\n\n"
            f"【题目】{problem.title}（{problem.difficulty}）\n"
            f"{problem.description}\n\n"
            f"【对话记录】\n{transcript_text}\n\n"
            f"请按以下维度评分：\n{rubric_desc}\n\n"
            "返回格式（严格JSON）：\n"
            "{\n"
            '  "score_breakdown": {' + ", ".join(f'"{k}": N' for k in rubric) + '},\n'
            '  "missed_points": ["..."],\n'
            '  "model_answer_structure": "标准解题思路...",\n'
            '  "next_drills": ["推荐练习1", "推荐练习2"]\n'
            "}"
        )
        return self._grade(prompt, rubric)
