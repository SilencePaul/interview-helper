from __future__ import annotations

from interviewer.interviewer import InterviewerAgent
from llm.mock_llm import MockLLM


def test_run_one_no_followup_skips_second_round(tmp_path, monkeypatch, capsys):
    notes_dir = tmp_path / "notes_clean_v2"
    notes_dir.mkdir()
    category_dir = notes_dir / "数据库"
    category_dir.mkdir()
    note_file = category_dir / "a.md"
    note_file.write_text("## 概念A\n\n内容\n\n---\n", encoding="utf-8")

    index_path = tmp_path / "data" / "concepts_index.json"
    index_path.parent.mkdir(parents=True)
    index_path.write_text(
        '{"version":1,"count":1,"concepts":[{"title":"概念A","category":"数据库","file_path":"%s","start_line":1,"end_line":5,"triggers":["触发器"],"question_type":["comparison"]}]}' % note_file,
        encoding="utf-8",
    )

    agent = InterviewerAgent(llm=MockLLM(), notes_dir=str(notes_dir), index_path=str(index_path))
    monkeypatch.setattr("builtins.input", lambda _: "测试回答")
    outcome = agent.run_one(no_followup=True)
    out = capsys.readouterr().out
    assert outcome is not None
    assert "no-followup mode, skipping follow-up" in out
    assert "Follow-up:" not in out
