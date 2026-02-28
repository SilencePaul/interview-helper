"""Tests for note_chunker module."""
import pytest
from app.note_chunker import (
    Chunk, chunk_note, build_outline, select_chunks,
    estimate_tokens, chunks_for_prompt, format_chunks,
)


# ── estimate_tokens ────────────────────────────────────────────────────────────

def test_estimate_tokens_empty():
    assert estimate_tokens("") == 0


def test_estimate_tokens_basic():
    # "hello world" = 2 words * 1.3 = 2 (int truncation)
    assert estimate_tokens("hello world") == 2


def test_estimate_tokens_scales():
    text = "word " * 100  # 100 words → int(100 * 1.3) = 130
    assert estimate_tokens(text) == 130


# ── chunk_note ─────────────────────────────────────────────────────────────────

def test_chunk_note_no_headings_returns_single_chunk():
    content = "plain text\nno headings here"
    chunks = chunk_note(content)
    assert len(chunks) == 1
    assert chunks[0].heading == "(全文)"
    assert chunks[0].level == 2
    assert chunks[0].index == 0
    assert "plain text" in chunks[0].body


def test_chunk_note_h2_headings():
    content = "## Section A\nbody A\n## Section B\nbody B"
    chunks = chunk_note(content)
    assert len(chunks) == 2
    assert chunks[0].heading == "## Section A"
    assert chunks[0].level == 2
    assert "body A" in chunks[0].body
    assert chunks[1].heading == "## Section B"
    assert "body B" in chunks[1].body


def test_chunk_note_h3_headings():
    content = "### Sub A\nbody\n### Sub B\nbody2"
    chunks = chunk_note(content)
    assert len(chunks) == 2
    assert chunks[0].level == 3


def test_chunk_note_mixed_headings():
    content = "## Main\nbody\n### Sub\nsub body\n## Another\nfoo"
    chunks = chunk_note(content)
    assert len(chunks) == 3
    assert chunks[0].level == 2
    assert chunks[1].level == 3
    assert chunks[2].level == 2


def test_chunk_note_empty_body_between_headings():
    content = "## A\n## B\nbody"
    chunks = chunk_note(content)
    assert len(chunks) == 2
    assert chunks[0].body == ""
    assert chunks[1].body == "body"


def test_chunk_note_index_sequential():
    content = "## A\n## B\n## C"
    chunks = chunk_note(content)
    assert [c.index for c in chunks] == [0, 1, 2]


def test_chunk_note_heading_not_matched_at_h1_or_h4():
    # # H1 and #### H4 should NOT create chunks
    content = "# H1\nshould be body\n#### H4\nalso body"
    chunks = chunk_note(content)
    assert len(chunks) == 1  # falls through to single-chunk fallback
    assert chunks[0].heading == "(全文)"


# ── build_outline ──────────────────────────────────────────────────────────────

def test_build_outline_numbering_and_indent():
    chunks = [
        Chunk(heading="## A", level=2, body="", index=0),
        Chunk(heading="### B", level=3, body="", index=1),
        Chunk(heading="## C", level=2, body="", index=2),
    ]
    outline = build_outline(chunks)
    lines = outline.splitlines()
    assert lines[0] == "1. ## A"
    assert lines[1] == "  2. ### B"   # level-3 gets indent
    assert lines[2] == "3. ## C"


def test_build_outline_single_chunk():
    chunks = [Chunk(heading="(全文)", level=2, body="content", index=0)]
    outline = build_outline(chunks)
    assert "1. (全文)" in outline


def test_build_outline_no_body_in_output():
    chunks = [Chunk(heading="## Title", level=2, body="some body text", index=0)]
    outline = build_outline(chunks)
    assert "some body text" not in outline


# ── select_chunks ──────────────────────────────────────────────────────────────

def test_select_chunks_empty_hint_returns_all():
    chunks = [
        Chunk(heading="## A", level=2, body="alpha", index=0),
        Chunk(heading="## B", level=2, body="beta", index=1),
    ]
    result = select_chunks(chunks, "")
    assert result is chunks  # exact same object


def test_select_chunks_heading_match():
    chunks = [
        Chunk(heading="## B+树索引", level=2, body="body1", index=0),
        Chunk(heading="## 哈希索引", level=2, body="body2", index=1),
    ]
    result = select_chunks(chunks, "哈希")
    assert len(result) == 1
    assert result[0].heading == "## 哈希索引"


def test_select_chunks_body_match():
    chunks = [
        Chunk(heading="## Section", level=2, body="contains sliding window pattern", index=0),
        Chunk(heading="## Other", level=2, body="nothing relevant", index=1),
    ]
    result = select_chunks(chunks, "sliding")
    assert len(result) == 1
    assert result[0].heading == "## Section"


def test_select_chunks_no_match_returns_all():
    chunks = [
        Chunk(heading="## A", level=2, body="foo", index=0),
        Chunk(heading="## B", level=2, body="bar", index=1),
    ]
    result = select_chunks(chunks, "xyz_not_found")
    assert result == chunks


def test_select_chunks_case_insensitive():
    chunks = [Chunk(heading="## Redis", level=2, body="info", index=0)]
    result = select_chunks(chunks, "redis")
    assert len(result) == 1


def test_select_chunks_multiple_matches():
    chunks = [
        Chunk(heading="## B+树", level=2, body="索引结构", index=0),
        Chunk(heading="## 哈希", level=2, body="索引对比", index=1),
        Chunk(heading="## 锁", level=2, body="并发控制", index=2),
    ]
    result = select_chunks(chunks, "索引")
    assert len(result) == 2


# ── chunks_for_prompt ──────────────────────────────────────────────────────────

def test_chunks_for_prompt_limits_by_tokens():
    big_body = "word " * 300  # 300 words → 390 tokens per chunk
    chunks = [
        Chunk(heading="## A", level=2, body=big_body, index=0),
        Chunk(heading="## B", level=2, body=big_body, index=1),
        Chunk(heading="## C", level=2, body=big_body, index=2),
    ]
    result = chunks_for_prompt(chunks, max_tokens=500)
    assert 1 <= len(result) < 3


def test_chunks_for_prompt_always_includes_first_chunk():
    # First chunk alone exceeds limit — should still be returned
    big_body = "word " * 5000
    chunks = [Chunk(heading="## A", level=2, body=big_body, index=0)]
    result = chunks_for_prompt(chunks, max_tokens=100)
    assert len(result) == 1


def test_chunks_for_prompt_all_fit_under_limit():
    chunks = [
        Chunk(heading="## A", level=2, body="short", index=0),
        Chunk(heading="## B", level=2, body="short", index=1),
    ]
    result = chunks_for_prompt(chunks, max_tokens=2000)
    assert len(result) == 2


def test_chunks_for_prompt_empty_input():
    assert chunks_for_prompt([], max_tokens=2000) == []


# ── format_chunks ──────────────────────────────────────────────────────────────

def test_format_chunks_includes_heading_and_body():
    chunks = [Chunk(heading="## Title", level=2, body="Some content here", index=0)]
    result = format_chunks(chunks)
    assert "## Title" in result
    assert "Some content here" in result


def test_format_chunks_multiple_chunks_ordered():
    chunks = [
        Chunk(heading="## A", level=2, body="body_a", index=0),
        Chunk(heading="## B", level=2, body="body_b", index=1),
    ]
    result = format_chunks(chunks)
    assert result.index("## A") < result.index("## B")


def test_format_chunks_empty_body_no_body_line():
    chunks = [Chunk(heading="## A", level=2, body="", index=0)]
    result = format_chunks(chunks)
    assert "## A" in result
    # No body text should leak in
    assert result.strip() == "## A"


def test_format_chunks_empty_list():
    assert format_chunks([]) == ""
