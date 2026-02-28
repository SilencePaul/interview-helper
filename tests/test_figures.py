"""Tests for figures module (no API calls)."""
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

import app.figures as fig_module
from app.figures import (
    _matches_placeholder, context_window, preview_diff,
    apply_patch, scan_all_notes,
)


# ── _matches_placeholder ───────────────────────────────────────────────────────

class TestMatchesPlaceholder:
    def test_bare_image_word(self):
        assert _matches_placeholder("image\n")
        assert _matches_placeholder("image")
        assert _matches_placeholder("  image  \n")

    def test_image_png_filename(self):
        assert _matches_placeholder("image.png\n")
        assert _matches_placeholder("  image.png  ")
        assert _matches_placeholder("image.png")

    def test_13_digit_timestamp_png(self):
        assert _matches_placeholder("1733845949539.png")
        assert _matches_placeholder("some context 1733845949539.png")
        assert _matches_placeholder("里面既有 1733845949539.png")

    def test_markdown_image_with_missing_keyword(self):
        assert _matches_placeholder("![alt](missing_image.png)")
        assert _matches_placeholder("![fig](placeholder.png)")
        assert _matches_placeholder("![](TODO.png)")
        assert _matches_placeholder("![x](image_here.png)")

    def test_empty_src_markdown_image(self):
        assert _matches_placeholder("![alt]()")
        assert _matches_placeholder("![ ](  )")

    def test_valid_https_image_not_matched(self):
        assert not _matches_placeholder("![logo](https://example.com/img.png)")
        assert not _matches_placeholder("![fig](https://docs.example.com/arch.png)")

    def test_normal_text_not_matched(self):
        assert not _matches_placeholder("Normal text here")
        assert not _matches_placeholder("## Heading")
        assert not _matches_placeholder("B+树是一种平衡多叉树索引结构")

    def test_image_case_insensitive(self):
        assert _matches_placeholder("IMAGE")
        assert _matches_placeholder("Image.PNG")
        assert _matches_placeholder("IMAGE.PNG")

    def test_12_digit_png_not_matched(self):
        # Must be exactly 13 digits
        assert not _matches_placeholder("123456789012.png")  # 12 digits


# ── context_window ─────────────────────────────────────────────────────────────

class TestContextWindow:
    def test_middle_of_file(self):
        lines = [f"line {i}\n" for i in range(30)]
        result = context_window(lines, line_idx=15, radius=5)
        assert "line 10" in result
        assert "line 20" in result
        assert "line 5\n" not in result  # outside radius

    def test_start_of_file_no_index_error(self):
        lines = [f"line {i}\n" for i in range(10)]
        result = context_window(lines, line_idx=0, radius=5)
        assert "line 0" in result
        assert "line 5" in result

    def test_end_of_file_no_index_error(self):
        lines = [f"line {i}\n" for i in range(10)]
        result = context_window(lines, line_idx=9, radius=5)
        assert "line 9" in result
        assert "line 4" in result

    def test_radius_0_returns_target_line_only(self):
        lines = ["a\n", "b\n", "c\n"]
        result = context_window(lines, line_idx=1, radius=0)
        assert result == "b\n"

    def test_radius_larger_than_file(self):
        lines = ["a\n", "b\n"]
        result = context_window(lines, line_idx=0, radius=100)
        assert "a" in result
        assert "b" in result


# ── preview_diff ───────────────────────────────────────────────────────────────

class TestPreviewDiff:
    def test_contains_file_path(self):
        diff = preview_diff(Path("/notes/test.md"), 42, "old", "new")
        assert "/notes/test.md" in diff

    def test_contains_line_number(self):
        diff = preview_diff(Path("f.md"), 42, "old", "new")
        assert "42" in diff

    def test_contains_old_and_new_content(self):
        diff = preview_diff(Path("f.md"), 1, "image", "```mermaid\ngraph TD\n```")
        assert "image" in diff
        assert "```mermaid" in diff

    def test_contains_diff_markers(self):
        diff = preview_diff(Path("f.md"), 1, "old", "new")
        assert "---" in diff
        assert "+++" in diff

    def test_returns_string(self):
        result = preview_diff(Path("f.md"), 1, "x", "y")
        assert isinstance(result, str)


# ── apply_patch ────────────────────────────────────────────────────────────────

class TestApplyPatch:
    def test_replaces_target_line(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("line1\nimage\nline3\n", encoding="utf-8")
        apply_patch(f, line_num=2, old_text="image", new_text="replacement")
        lines = f.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "line1"
        assert lines[1] == "replacement"
        assert lines[2] == "line3"

    def test_multiline_replacement_inserts_correctly(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("line1\nimage\nline3\n", encoding="utf-8")
        apply_patch(f, 2, "image", "```mermaid\ngraph TD\n  A-->B\n```")
        content = f.read_text(encoding="utf-8")
        assert "```mermaid" in content
        assert "graph TD" in content
        assert "line3" in content

    def test_preserves_trailing_newline_on_replaced_line(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("line1\nimage\nline3\n", encoding="utf-8")
        apply_patch(f, 2, "image", "replacement")
        raw = f.read_text(encoding="utf-8")
        lines = raw.splitlines(keepends=True)
        assert lines[1].endswith("\n")

    def test_out_of_bounds_line_does_not_crash(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("only one line", encoding="utf-8")
        apply_patch(f, 999, "old", "new")  # Should not raise
        assert f.read_text(encoding="utf-8") == "only one line"

    def test_first_line_replacement(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("image\nline2\n", encoding="utf-8")
        apply_patch(f, 1, "image", "replaced")
        lines = f.read_text(encoding="utf-8").splitlines()
        assert lines[0] == "replaced"
        assert lines[1] == "line2"

    def test_last_line_without_newline(self, tmp_path):
        f = tmp_path / "note.md"
        f.write_text("line1\nimage", encoding="utf-8")  # no trailing newline
        apply_patch(f, 2, "image", "replaced")
        content = f.read_text(encoding="utf-8")
        assert "replaced" in content


# ── scan_all_notes ─────────────────────────────────────────────────────────────

class TestScanAllNotes:
    def test_finds_known_placeholders_in_real_notes(self):
        placeholders = scan_all_notes()
        assert len(placeholders) >= 9

    def test_placeholder_file_exists(self):
        for ph in scan_all_notes():
            assert ph.file.exists(), f"File missing: {ph.file}"

    def test_placeholder_line_num_is_positive(self):
        for ph in scan_all_notes():
            assert ph.line_num >= 1

    def test_placeholder_context_contains_raw_text(self):
        for ph in scan_all_notes():
            assert ph.raw_text.strip() in ph.context_window

    def test_known_files_flagged(self):
        phs = scan_all_notes()
        files = {ph.file.name for ph in phs}
        assert "索引.md" in files
        assert "网络基础.md" in files

    def test_nonexistent_dir_returns_empty(self, monkeypatch, tmp_path):
        monkeypatch.setattr(fig_module, "NOTES_DIR", tmp_path / "nonexistent")
        assert scan_all_notes() == []

    def test_synthetic_bare_image_detected(self, monkeypatch, tmp_path):
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()
        (notes_dir / "test.md").write_text(
            "## Section\nimage\nsome text\n", encoding="utf-8"
        )
        monkeypatch.setattr(fig_module, "NOTES_DIR", notes_dir)
        result = scan_all_notes()
        assert len(result) == 1
        assert result[0].line_num == 2
        assert result[0].raw_text == "image"

    def test_synthetic_13digit_detected(self, monkeypatch, tmp_path):
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()
        (notes_dir / "net.md").write_text(
            "TCP三次握手 1733845949539.png\n", encoding="utf-8"
        )
        monkeypatch.setattr(fig_module, "NOTES_DIR", notes_dir)
        result = scan_all_notes()
        assert len(result) == 1
        assert "1733845949539" in result[0].raw_text

    def test_valid_https_image_not_flagged(self, monkeypatch, tmp_path):
        notes_dir = tmp_path / "notes"
        notes_dir.mkdir()
        (notes_dir / "ok.md").write_text(
            "![arch](https://example.com/diagram.png)\n", encoding="utf-8"
        )
        monkeypatch.setattr(fig_module, "NOTES_DIR", notes_dir)
        result = scan_all_notes()
        assert result == []
