from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def test_history_latest_full(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    history_dir = tmp_path / "data" / "history"
    history_dir.mkdir(parents=True)
    session = {
        "saved_at": "2026-01-02T00:00:00Z",
        "final_score": 8,
        "final_dimensions": {"accuracy": 3, "completeness": 3, "practicality": 1, "clarity": 1},
        "scope": "Random",
        "concept": {"category": "操作系统", "title": "进程"},
        "rounds": [
            {
                "question": "什么是进程？",
                "answer": "进程是资源分配的基本单位。",
                "score": 8,
                "dimensions": {"accuracy": 3, "completeness": 3, "practicality": 1, "clarity": 1},
                "strengths": ["回答清晰"],
                "missing_points": ["缺少边界"],
                "ideal_answer": "理想答案",
            }
        ],
    }
    (history_dir / "session-20260102T000000Z.json").write_text(json.dumps(session), encoding="utf-8")

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module(module_name)

    module._cmd_history(limit=10, latest=True, low_score_only=False, full=True)
    out = capsys.readouterr().out
    assert "Round 1" in out
    assert "Answer   : 进程是资源分配的基本单位。" in out
    assert "Ideal    : 理想答案" in out
