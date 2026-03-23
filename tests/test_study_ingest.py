from __future__ import annotations

import sqlite3
from pathlib import Path
import zipfile

from study_ingest.importer import import_dir, import_file, setup_workspace
import study_ingest.importer as importer


def test_setup_workspace_creates_expected_layout(tmp_path):
    paths = setup_workspace(str(tmp_path / "study"))
    assert Path(paths["uploads"]).exists()
    assert Path(paths["parsed"]).exists()
    assert Path(paths["notes"]).exists()
    assert Path(paths["sources"]).exists()
    assert Path(paths["db"]).exists()


def test_import_file_generates_markdown_and_db(tmp_path):
    source = tmp_path / "sample.txt"
    source.write_text("# 事务\n事务是一组操作，要么全成要么全失败。\n\n# MVCC\nMVCC 是多版本并发控制。", encoding="utf-8")

    result = import_file(str(source), category="数据库", base_dir=str(tmp_path / "study"))
    note_path = Path(result["note"])
    parsed_path = Path(result["parsed"])
    source_map = Path(result["source_map"])

    assert note_path.exists()
    assert parsed_path.exists()
    assert source_map.exists()
    note_text = note_path.read_text(encoding="utf-8")
    assert "## 核心概念" in note_text
    assert "## 高频考点" in note_text
    assert "什么是事务？它解决的核心问题是什么？" in note_text
    assert len(result["notes"]) == 2

    conn = sqlite3.connect(result["db"])
    try:
        row = conn.execute("SELECT title, category FROM documents").fetchone()
        assert row == ("事务", "数据库")
        chunk_count = conn.execute("SELECT COUNT(*) FROM note_chunks").fetchone()[0]
        assert chunk_count == 2
    finally:
        conn.close()


def test_import_docx_generates_markdown(tmp_path):
    source = tmp_path / "sample.docx"
    xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
      <w:body>
        <w:p><w:r><w:t>MVCC</w:t></w:r></w:p>
        <w:p><w:r><w:t>多版本并发控制用于提升读写并发。</w:t></w:r></w:p>
      </w:body>
    </w:document>'''
    with zipfile.ZipFile(source, 'w') as zf:
        zf.writestr('word/document.xml', xml)

    result = import_file(str(source), category="数据库", base_dir=str(tmp_path / "study"))
    assert Path(result["note"]).exists()
    assert "MVCC" in Path(result["note"]).read_text(encoding="utf-8")


def test_import_pdf_generates_markdown(tmp_path, monkeypatch):
    source = tmp_path / "sample.pdf"
    source.write_bytes(b"%PDF-test")

    class FakePage:
        def extract_text(self):
            return "B树索引\nB树适合范围查询。"

    class FakeReader:
        def __init__(self, path):
            self.pages = [FakePage()]

    monkeypatch.setattr(importer, "PdfReader", FakeReader)
    result = import_file(str(source), category="数据库", base_dir=str(tmp_path / "study"))
    assert Path(result["note"]).exists()
    assert "B树索引" in Path(result["note"]).read_text(encoding="utf-8")


def test_import_pdf_falls_back_to_ocr(tmp_path, monkeypatch):
    source = tmp_path / "scan.pdf"
    source.write_bytes(b"%PDF-test")

    class EmptyPage:
        def extract_text(self):
            return ""

    class EmptyReader:
        def __init__(self, path):
            self.pages = [EmptyPage()]

    monkeypatch.setattr(importer, "PdfReader", EmptyReader)
    monkeypatch.setattr(importer, "_ocr_pdf_text", lambda path: "OCR标题\n这是扫描版 PDF 的 OCR 结果。")

    result = import_file(str(source), category="数据库", base_dir=str(tmp_path / "study"))
    assert "OCR标题" in Path(result["note"]).read_text(encoding="utf-8")


def test_import_dir_imports_supported_files(tmp_path, monkeypatch):
    source_dir = tmp_path / "materials"
    source_dir.mkdir()
    (source_dir / "a.txt").write_text("索引\n索引用于加速查询。", encoding="utf-8")
    (source_dir / "b.md").write_text("# 事务\n事务用于保证一致性。", encoding="utf-8")
    (source_dir / "ignore.bin").write_bytes(b"x")

    result = import_dir(str(source_dir), category="数据库", base_dir=str(tmp_path / "study"))
    assert result["total_found"] == 2
    assert result["imported_count"] == 2
    assert result["failed_count"] == 0
    assert len(result["imported"]) == 2
