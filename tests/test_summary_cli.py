from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def test_summary_cli_text_and_json(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    summary_dir = tmp_path / "data" / "summaries"
    summary_dir.mkdir(parents=True)
    summary = {
        "completed": 2,
        "averageScore": 7.0,
        "lowScoreRounds": 0,
        "weakestDimension": {"key": "practicality", "label": "场景意识", "value": 1.0},
        "bestTopic": {"category": "数据库", "title": "索引", "score": 7},
        "worstTopic": {"category": "操作系统", "title": "进程", "score": 6},
        "topMissing": "缺少场景",
        "suggestion": "建议继续练场景题",
        "topics": [{"category": "数据库", "title": "索引", "score": 7}],
    }
    (summary_dir / "summary-20260102T000000-000000Z.json").write_text(json.dumps(summary), encoding="utf-8")

    module_name = "app.__main__"
    if module_name in sys.modules:
        del sys.modules[module_name]
    repo_root = Path(__file__).resolve().parents[1]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    module = importlib.import_module(module_name)

    module._cmd_summary(limit=10, latest=True, as_json=False)
    out = capsys.readouterr().out
    assert "interview-helper summary" in out
    assert "Best topic : [数据库] 索引 (7/10)" in out

    module._cmd_summary(limit=10, latest=True, as_json=True)
    out = capsys.readouterr().out
    data = json.loads(out)
    assert data["completed"] == 2
    assert data["topMissing"] == "缺少场景"
