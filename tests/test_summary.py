from __future__ import annotations

from interviewer.interviewer import SessionOutcome, _build_session_summary, _print_session_summary


def test_print_session_summary(capsys):
    outcomes = [
        SessionOutcome("索引", "数据库", 7, {"accuracy": 3, "completeness": 2, "practicality": 1, "clarity": 1}, False, ["缺少场景", "边界不清"]),
        SessionOutcome("进程", "操作系统", 5, {"accuracy": 2, "completeness": 1, "practicality": 1, "clarity": 1}, True, ["缺少场景"]),
    ]
    summary = _build_session_summary(outcomes)
    _print_session_summary(summary)
    out = capsys.readouterr().out
    assert "Session summary" in out
    assert "Average score   : 6.00/10" in out
    assert "Low-score rounds: 1/2" in out
    assert "Best topic      : [数据库] 索引 (7/10)" in out
    assert "Worst topic     : [操作系统] 进程 (5/10)" in out
    assert "Top missing     : 缺少场景" in out
    assert "Suggestion      : 下次建议优先开启 --review-wrong，先回补低分题。" in out
    assert "Topics          : [数据库] 索引、[操作系统] 进程" in out


def test_build_session_summary_payload():
    outcomes = [
        SessionOutcome("索引", "数据库", 7, {"accuracy": 3, "completeness": 2, "practicality": 1, "clarity": 1}, False, ["缺少场景"]),
        SessionOutcome("进程", "操作系统", 7, {"accuracy": 3, "completeness": 2, "practicality": 1, "clarity": 1}, False, ["缺少场景", "缺少边界"]),
    ]
    summary = _build_session_summary(outcomes)
    assert summary["completed"] == 2
    assert summary["weakestDimension"]["key"] == "practicality"
    assert summary["topMissing"] == "缺少场景"
    assert summary["topics"][0]["title"] == "索引"
