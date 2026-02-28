"""Pydantic v2 data models."""
from __future__ import annotations
from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, Field


class Problem(BaseModel):
    id: str
    title: str
    difficulty: str  # easy | medium | hard
    tags: list[str]
    description: str
    examples: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    time_limit_sec: int = 1800  # 30 minutes default
    rubric: dict[str, int] = Field(default_factory=dict)


class ReviewResult(BaseModel):
    session_id: str
    item_id: str
    score_breakdown: dict[str, int]
    total: int
    max_score: int
    missed_points: list[str]
    model_answer_structure: str
    next_drills: list[str]


class ScheduleEntry(BaseModel):
    item_id: str
    item_type: str  # topic | algo
    next_review: date
    interval_days: float
    ease_factor: float
    repetitions: int
    last_quality: float


class MistakeEntry(BaseModel):
    session_id: str
    item_id: str
    prompt_subject: str
    first_reaction: str
    trigger_words: str
    self_questions: list[str]
    next_review_date: date
