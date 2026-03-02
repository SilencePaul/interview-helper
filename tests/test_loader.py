"""Tests for knowledge/loader.py."""
from __future__ import annotations

import textwrap

import pytest

from knowledge.loader import (
    MAX_CONCEPT_CHARS,
    load_block,
    parse_bullet_list,
    parse_concept_blocks,
    parse_question_type,
)

# ---------------------------------------------------------------------------
# Fixture: a minimal two-concept markdown file
# ---------------------------------------------------------------------------

_SAMPLE_MD = textwrap.dedent("""\
    # Test File

    ---

    ## 概念A

    > 核心概念A的解释

    **关键点：**
    - 普通列表项一
    - 普通列表项二

    🎯 **Interview Triggers:**
    - 问题一（MECHANISM）
    - 问题二（COMPARISON）

    🧠 **Question Type:** mechanism · comparison

    🔥 **Follow-up Paths:**
    - 路径一
    - 路径二

    🛠 **Engineering Hooks:**
    - 工程建议一

    ---

    ## 概念B

    > 核心概念B的解释

    🎯 **Interview Triggers:**
    - 问题三（DESIGN）

    🧠 **Question Type:** design

    ---
""")


@pytest.fixture()
def sample_md(tmp_path):
    f = tmp_path / "sample.md"
    f.write_text(_SAMPLE_MD, encoding="utf-8")
    return str(f)


# ---------------------------------------------------------------------------
# Splitting
# ---------------------------------------------------------------------------

def test_parse_concept_blocks_count(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert len(blocks) == 2


def test_parse_concept_blocks_titles(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert blocks[0].title == "概念A"
    assert blocks[1].title == "概念B"


def test_parse_concept_blocks_category(sample_md):
    blocks = parse_concept_blocks(sample_md, "数据库")
    assert all(b.category == "数据库" for b in blocks)


def test_parse_concept_blocks_no_cross_contamination(sample_md):
    """Block content must not bleed into adjacent blocks."""
    blocks = parse_concept_blocks(sample_md, "测试")
    assert "概念B" not in blocks[0].content
    assert "概念A" not in blocks[1].content


def test_parse_concept_blocks_content_starts_with_heading(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert blocks[0].content.startswith("## 概念A")
    assert blocks[1].content.startswith("## 概念B")


# ---------------------------------------------------------------------------
# Annotation parsing
# ---------------------------------------------------------------------------

def test_parse_triggers(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert len(blocks[0].triggers) == 2
    assert "问题一（MECHANISM）" in blocks[0].triggers
    assert "问题二（COMPARISON）" in blocks[0].triggers


def test_parse_triggers_second_block(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert blocks[1].triggers == ["问题三（DESIGN）"]


def test_parse_question_type(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert "mechanism" in blocks[0].question_type
    assert "comparison" in blocks[0].question_type


def test_parse_follow_up_paths(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert "路径一" in blocks[0].follow_up_paths
    assert "路径二" in blocks[0].follow_up_paths


def test_parse_engineering_hooks(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    assert "工程建议一" in blocks[0].engineering_hooks


def test_missing_annotation_returns_empty(sample_md):
    """Block without 🛠 should return empty engineering_hooks."""
    blocks = parse_concept_blocks(sample_md, "测试")
    # 概念B has no 🛠 section
    assert blocks[1].engineering_hooks == []


# ---------------------------------------------------------------------------
# load_block correctness
# ---------------------------------------------------------------------------

def test_load_block_matches_parsed_content(sample_md):
    """load_block with stored start/end_line must reproduce parsed content."""
    blocks = parse_concept_blocks(sample_md, "测试")
    for b in blocks:
        loaded = load_block(b.file_path, b.start_line, b.end_line)
        assert loaded == b.content


def test_load_block_first_concept(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    b = blocks[0]
    loaded = load_block(b.file_path, b.start_line, b.end_line)
    assert "概念A" in loaded
    assert "概念B" not in loaded


def test_load_block_second_concept(sample_md):
    blocks = parse_concept_blocks(sample_md, "测试")
    b = blocks[1]
    loaded = load_block(b.file_path, b.start_line, b.end_line)
    assert "概念B" in loaded
    assert "概念A" not in loaded


# ---------------------------------------------------------------------------
# Truncation
# ---------------------------------------------------------------------------

def test_truncation_warns_and_trims(tmp_path):
    long_content = "x" * 7000
    big_md = tmp_path / "big.md"
    big_md.write_text(f"## 大概念\n\n{long_content}\n\n---\n", encoding="utf-8")

    with pytest.warns(UserWarning, match="truncating"):
        blocks = parse_concept_blocks(str(big_md), "测试")

    assert len(blocks[0].content) == MAX_CONCEPT_CHARS


# ---------------------------------------------------------------------------
# parse_bullet_list (unit)
# ---------------------------------------------------------------------------

def test_parse_bullet_list_basic():
    content = "🎯 **Triggers:**\n- 问题一\n- 问题二\n"
    result = parse_bullet_list(content, "🎯")
    assert result == ["问题一", "问题二"]


def test_parse_bullet_list_stops_at_next_emoji():
    content = "🎯 **Triggers:**\n- 问题一\n🧠 **Type:** x\n- 其他\n"
    result = parse_bullet_list(content, "🎯")
    assert result == ["问题一"]


def test_parse_bullet_list_missing_marker():
    content = "Some text\n- item\n"
    result = parse_bullet_list(content, "🎯")
    assert result == []


# ---------------------------------------------------------------------------
# parse_question_type (unit)
# ---------------------------------------------------------------------------

def test_parse_question_type_basic():
    content = "🧠 **Question Type:** mechanism · comparison\n"
    result = parse_question_type(content)
    assert result == ["mechanism", "comparison"]


def test_parse_question_type_comma_separator():
    content = "🧠 **Question Type:** design, tradeoff\n"
    result = parse_question_type(content)
    assert result == ["design", "tradeoff"]


def test_parse_question_type_missing():
    content = "Some content without the marker.\n"
    result = parse_question_type(content)
    assert result == []
