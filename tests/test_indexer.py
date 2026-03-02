"""Tests for knowledge/indexer.py."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

import pytest

from knowledge.indexer import ConceptEntry, build_index, load_index


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_notes_dir(tmp_path: Path) -> str:
    """Create a mini notes_clean_v2-like structure with 3 concepts total."""
    db_dir = tmp_path / "数据库"
    db_dir.mkdir()
    os_dir = tmp_path / "操作系统"
    os_dir.mkdir()

    (db_dir / "索引.md").write_text(textwrap.dedent("""\
        ## B+ 树

        > B+ 树是 InnoDB 默认索引结构。

        🎯 **Interview Triggers:**
        - B+ 树和 B 树的区别是什么？（COMPARISON）

        🧠 **Question Type:** comparison · mechanism

        ---

        ## 哈希索引

        > 哈希索引适合等值查询。

        🎯 **Interview Triggers:**
        - 哈希索引的优缺点？（TRADEOFF）

        🧠 **Question Type:** tradeoff

        ---
    """), encoding="utf-8")

    (os_dir / "进程.md").write_text(textwrap.dedent("""\
        ## 进程与线程

        > 进程是资源分配单位，线程是调度单位。

        🎯 **Interview Triggers:**
        - 进程和线程的区别？（COMPARISON）

        🧠 **Question Type:** comparison

        ---
    """), encoding="utf-8")

    return str(tmp_path)


# ---------------------------------------------------------------------------
# build_index
# ---------------------------------------------------------------------------

def test_build_index_count(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    count = build_index(notes_dir, output)
    assert count == 3


def test_build_index_creates_file(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "data" / "index.json")
    build_index(notes_dir, output)
    assert Path(output).exists()


def test_build_index_json_schema(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    data = json.loads(Path(output).read_text(encoding="utf-8"))
    assert data["version"] == 1
    assert data["count"] == 3
    assert len(data["concepts"]) == 3

    for entry in data["concepts"]:
        assert "title" in entry
        assert "category" in entry
        assert "file_path" in entry
        assert "start_line" in entry
        assert "end_line" in entry
        assert "triggers" in entry
        assert "question_type" in entry


def test_build_index_categories(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    categories = {e.category for e in entries}
    assert "数据库" in categories
    assert "操作系统" in categories


def test_build_index_sorted_by_path(tmp_path):
    """Files must be processed in sorted path order (deterministic builds)."""
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    paths = [e.file_path for e in entries]
    assert paths == sorted(paths)


def test_build_index_concept_order_within_file(tmp_path):
    """Concepts in a file must appear in their original order in the index."""
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    db_entries = [e for e in entries if e.category == "数据库"]
    assert db_entries[0].title == "B+ 树"
    assert db_entries[1].title == "哈希索引"


def test_build_index_deduplication(tmp_path):
    """Running build_index twice on the same dir must not duplicate entries."""
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)          # first run
    count = build_index(notes_dir, output)  # second run
    assert count == 3  # still 3, not 6


def test_build_index_triggers_stored(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    btree = next(e for e in entries if e.title == "B+ 树")
    assert len(btree.triggers) == 1
    assert "COMPARISON" in btree.triggers[0]


# ---------------------------------------------------------------------------
# load_index
# ---------------------------------------------------------------------------

def test_load_index_roundtrip(tmp_path):
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    assert len(entries) == 3
    assert all(isinstance(e, ConceptEntry) for e in entries)


def test_load_index_missing_raises(tmp_path):
    with pytest.raises(FileNotFoundError, match="build-index"):
        load_index(str(tmp_path / "nonexistent.json"))


def test_load_index_start_before_end(tmp_path):
    """start_line must always be less than end_line."""
    notes_dir = _make_notes_dir(tmp_path)
    output = str(tmp_path / "index.json")
    build_index(notes_dir, output)

    entries = load_index(output)
    for e in entries:
        assert e.start_line < e.end_line, (
            f"start_line >= end_line for '{e.title}': "
            f"{e.start_line} >= {e.end_line}"
        )
