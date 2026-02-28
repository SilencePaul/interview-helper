"""Tests for notes module (uses real notes directory)."""
import pytest
from pathlib import Path

import app.notes as notes_module
from app.notes import list_topics, find_notes, load_note, _score_match


# ── _score_match ───────────────────────────────────────────────────────────────

class TestScoreMatch:
    def test_exact_match_returns_100(self):
        assert _score_match("索引", "索引") == 100

    def test_substring_match_returns_80(self):
        assert _score_match("索引", "数据库索引结构") == 80

    def test_case_insensitive_substring(self):
        assert _score_match("redis", "Redis") == 100  # exact after lower

    def test_token_overlap_counts(self):
        # "hello world" vs "hello python" → 1 token overlap × 10 = 10
        score = _score_match("hello world", "hello python")
        assert score == 10

    def test_no_match_returns_zero(self):
        assert _score_match("xyz", "abc") == 0

    def test_empty_query_with_empty_text(self):
        # Both empty → exact match
        assert _score_match("", "") == 100


# ── list_topics ────────────────────────────────────────────────────────────────

class TestListTopics:
    def test_returns_dict_of_categories(self):
        topics = list_topics()
        assert isinstance(topics, dict)
        assert len(topics) > 0

    def test_known_categories_present(self):
        topics = list_topics()
        assert "数据库" in topics
        assert "计算机网络" in topics
        assert "操作系统" in topics

    def test_each_category_has_nonempty_list(self):
        topics = list_topics()
        for cat, topic_list in topics.items():
            assert isinstance(topic_list, list)
            assert len(topic_list) > 0

    def test_topic_names_are_bare_stems(self):
        topics = list_topics()
        for cat, topic_list in topics.items():
            for t in topic_list:
                assert "/" not in t
                assert ".md" not in t

    def test_known_topics_present(self):
        topics = list_topics()
        assert "索引" in topics.get("数据库", [])
        assert "Redis" in topics.get("数据库", [])

    def test_nonexistent_notes_dir_returns_empty(self, monkeypatch, tmp_path):
        monkeypatch.setattr(notes_module, "NOTES_DIR", tmp_path / "nonexistent")
        assert list_topics() == {}

    def test_empty_notes_dir_returns_empty(self, monkeypatch, tmp_path):
        empty_notes = tmp_path / "notes"
        empty_notes.mkdir()
        monkeypatch.setattr(notes_module, "NOTES_DIR", empty_notes)
        assert list_topics() == {}


# ── find_notes ─────────────────────────────────────────────────────────────────

class TestFindNotes:
    def test_finds_exact_topic_name(self):
        results = find_notes("索引")
        assert len(results) > 0

    def test_top_result_is_best_match(self):
        results = find_notes("索引")
        # The top result display name should contain 索引
        assert "索引" in results[0][1]

    def test_result_is_list_of_path_display_tuples(self):
        results = find_notes("Redis")
        assert len(results) > 0
        path, display = results[0]
        assert isinstance(path, Path)
        assert path.exists()
        assert isinstance(display, str)
        assert "/" in display  # "category/stem" format

    def test_finds_by_category_name(self):
        # Searching the category name should find notes inside it
        results = find_notes("数据库")
        assert len(results) > 0

    def test_fuzzy_partial_match(self):
        # "事务" is a topic in 数据库
        results = find_notes("事务")
        assert len(results) > 0
        assert any("事务" in d for _, d in results)

    def test_no_match_returns_empty_list(self):
        results = find_notes("zzz_impossible_xyz_topic_99999")
        assert results == []

    def test_nonexistent_notes_dir_returns_empty(self, monkeypatch, tmp_path):
        monkeypatch.setattr(notes_module, "NOTES_DIR", tmp_path / "nonexistent")
        assert find_notes("索引") == []

    def test_results_sorted_by_score_desc(self):
        # All results should have score > 0 (they matched)
        results = find_notes("索引")
        # An exact-name match should be first, not buried
        assert len(results) >= 1
        assert "索引" in results[0][1]

    def test_custom_dir_finds_custom_note(self, monkeypatch, tmp_path):
        notes_dir = tmp_path / "notes"
        cat = notes_dir / "mycat"
        cat.mkdir(parents=True)
        (cat / "my_topic.md").write_text("content", encoding="utf-8")
        monkeypatch.setattr(notes_module, "NOTES_DIR", notes_dir)
        results = find_notes("my_topic")
        assert len(results) == 1
        assert "mycat/my_topic" in results[0][1]


# ── load_note ──────────────────────────────────────────────────────────────────

class TestLoadNote:
    def test_loads_real_note_as_string(self):
        results = find_notes("索引")
        path, _ = results[0]
        content = load_note(path)
        assert isinstance(content, str)
        assert len(content) > 0

    def test_loads_known_content(self, tmp_path):
        test_file = tmp_path / "test.md"
        test_file.write_text("## Hello\nbody content", encoding="utf-8")
        assert load_note(test_file) == "## Hello\nbody content"

    def test_loads_utf8_chinese_content(self, tmp_path):
        test_file = tmp_path / "chinese.md"
        test_file.write_text("## 索引\nB+树是一种平衡多叉树", encoding="utf-8")
        content = load_note(test_file)
        assert "索引" in content
        assert "B+树" in content
