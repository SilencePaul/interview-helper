from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def test_load_history_and_stats_output(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    history_dir = tmp_path / "data" / "history"
    history_dir.mkdir(parents=True)

    sample = {
        "final_score": 5,
        "final_dimensions": {
            "accuracy": 2,
            "completeness": 1,
            "practicality": 1,
            "clarity": 1,
        },
        "concept": {"category": "数据库"},
        "rounds": [
            {
                "missing_points": ["缺少场景", "不够完整"]
            }
        ],
    }
    sample2 = {
        "final_score": 8,
        "final_dimensions": {
            "accuracy": 3,
            "completeness": 3,
            "practicality": 1,
            "clarity": 1,
        },
        "concept": {"category": "操作系统"},
        "rounds": [
            {
                "missing_points": ["缺少场景"]
            }
        ],
    }

    (history_dir / "session-20260101T000000Z.json").write_text(json.dumps(sample), encoding="utf-8")
    (history_dir / "session-20260102T000000Z.json").write_text(json.dumps(sample2), encoding="utf-8")

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module(module_name)

    sessions = module._load_history(10)
    assert len(sessions) == 2

    module._cmd_stats(10)
    out = capsys.readouterr().out
    assert "Average score" in out
    assert "Weakest dimension" in out
    assert "数据库" in out
    assert "缺少场景" in out

    module._cmd_stats(10, as_json=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["samples"] == 2
    assert data["weakestDimension"]["label"]
