from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def test_history_cli_latest_and_low_score(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    history_dir = tmp_path / "data" / "history"
    history_dir.mkdir(parents=True)

    s1 = {
        "saved_at": "2026-01-01T00:00:00Z",
        "final_score": 5,
        "final_dimensions": {"accuracy": 2, "completeness": 1, "practicality": 1, "clarity": 1},
        "scope": "Random",
        "round_count": 1,
        "concept": {"category": "数据库", "title": "索引"},
        "rounds": [{"question": "什么是索引？", "missing_points": ["缺少场景"]}],
    }
    s2 = {
        "saved_at": "2026-01-02T00:00:00Z",
        "final_score": 8,
        "final_dimensions": {"accuracy": 3, "completeness": 3, "practicality": 1, "clarity": 1},
        "scope": "Random",
        "round_count": 1,
        "concept": {"category": "操作系统", "title": "进程"},
        "rounds": [{"question": "什么是进程？", "missing_points": ["缺少边界"]}],
    }

    (history_dir / "session-20260101T000000Z.json").write_text(json.dumps(s1), encoding="utf-8")
    (history_dir / "session-20260102T000000Z.json").write_text(json.dumps(s2), encoding="utf-8")

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module(module_name)

    module._cmd_history(limit=10, latest=True, low_score_only=False)
    out = capsys.readouterr().out
    assert "操作系统" in out
    assert "数据库" not in out

    module._cmd_history(limit=10, latest=False, low_score_only=True)
    out = capsys.readouterr().out
    assert "数据库" in out
    assert "操作系统" not in out

    module._cmd_history(limit=10, latest=True, low_score_only=False, as_json=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["topic"]["category"] == "操作系统"
    assert data["score"] == 8
