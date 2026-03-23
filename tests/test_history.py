from __future__ import annotations

import json
from pathlib import Path

from interviewer.interviewer import HistoryRound, InterviewerAgent
from llm.mock_llm import MockLLM


def test_save_history_writes_session_file(tmp_path):
    notes_dir = tmp_path / "notes_clean_v2"
    notes_dir.mkdir()
    category_dir = notes_dir / "数据库"
    category_dir.mkdir()
    note_file = category_dir / "a.md"
    note_file.write_text("## 测试概念\n\n内容\n\n---\n", encoding="utf-8")
    index_path = tmp_path / "data" / "concepts_index.json"
    index_path.parent.mkdir(parents=True)
    index_path.write_text(
        json.dumps(
            {
                "version": 1,
                "count": 1,
                "concepts": [
                    {
                        "title": "测试概念",
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
    concept = agent.pick_concept()
    rounds = [
        HistoryRound(
            round=1,
            question="什么是测试概念？",
            answer="这是一个测试回答。",
            score=7,
            dimensions={"accuracy": 3, "completeness": 2, "practicality": 1, "clarity": 1},
            strengths=["说到了基本概念"],
            missing_points=["缺少例子"],
            ideal_answer="理想答案",
        )
    ]

    saved_path = agent.save_history(mode="prod", scope="Random", concept=concept, rounds=rounds)
    assert saved_path.exists()
    assert saved_path.parent.name == "history"

    data = json.loads(saved_path.read_text(encoding="utf-8"))
    assert data["mode"] == "prod"
    assert data["scope"] == "Random"
    assert data["final_score"] == 7
    assert data["final_dimensions"] == {"accuracy": 3, "completeness": 2, "practicality": 1, "clarity": 1}
    assert data["round_count"] == 1
    assert data["concept"]["title"] == "测试概念"
    assert data["rounds"][0]["question"] == "什么是测试概念？"
    assert data["rounds"][0]["dimensions"]["accuracy"] == 3
