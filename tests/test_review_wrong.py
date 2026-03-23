from __future__ import annotations

import json

from interviewer.interviewer import InterviewerAgent
from llm.mock_llm import MockLLM


def test_load_review_candidates_filters_low_scores_and_dedupes(tmp_path):
    notes_dir = tmp_path / "notes_clean_v2"
    notes_dir.mkdir()
    category_dir = notes_dir / "数据库"
    category_dir.mkdir()
    note_file = category_dir / "a.md"
    note_file.write_text("## 概念A\n\n内容\n\n---\n", encoding="utf-8")

    index_path = tmp_path / "data" / "concepts_index.json"
    index_path.parent.mkdir(parents=True)
    index_path.write_text(
        json.dumps(
            {
                "version": 1,
                "count": 1,
                "concepts": [
                    {
                        "title": "概念A",
                        "category": "数据库",
                        "file_path": str(note_file),
                        "start_line": 1,
                        "end_line": 5,
                        "triggers": ["触发器"],
                        "question_type": ["comparison"],
                    }
                ],
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )

    agent = InterviewerAgent(llm=MockLLM(), notes_dir=str(notes_dir), index_path=str(index_path))
    agent.history_dir.mkdir(parents=True, exist_ok=True)

    low_score = {
        "final_score": 4,
        "concept": {
            "file_path": str(note_file),
            "start_line": 1,
            "end_line": 5,
        },
    }
    high_score = {
        "final_score": 8,
        "concept": {
            "file_path": str(note_file),
            "start_line": 1,
            "end_line": 5,
        },
    }

    (agent.history_dir / "session-20260101T000000Z.json").write_text(json.dumps(low_score), encoding="utf-8")
    (agent.history_dir / "session-20260102T000000Z.json").write_text(json.dumps(high_score), encoding="utf-8")

    review = agent.load_review_candidates(agent._index)
    assert len(review) == 1
    assert review[0].title == "概念A"
