from __future__ import annotations

from app import web


def test_html_contains_dashboard_title():
    assert "interview-helper UI" in web.HTML
    assert "/api/stats" in web.HTML
    assert "/api/history" in web.HTML
    assert "/api/summary" in web.HTML
    assert "/api/session/start" in web.HTML
    assert "/api/session/answer" in web.HTML
    assert "需要追问" in web.HTML
    assert "Ideal Answer" in web.HTML
    assert "Session Summary" in web.HTML
    assert "await refreshDashboard(false)" in web.HTML
    assert "第 2 轮（追问）" in web.HTML
    assert "下一题" in web.HTML
    assert "提交中..." in web.HTML
    assert "维度分" in web.HTML
    assert "score-grid" in web.HTML


def test_history_item_extracts_summary():
    session = {
        "saved_at": "2026-01-01T00:00:00Z",
        "__path": "data/history/a.json",
        "concept": {"category": "数据库", "title": "索引"},
        "final_score": 7,
        "final_dimensions": {"accuracy": 3},
        "scope": "Random",
        "rounds": [{"missing_points": ["缺少场景"]}],
    }
    item = web._history_item(session)
    assert item["topic"]["title"] == "索引"
    assert item["topMissing"] == "缺少场景"
