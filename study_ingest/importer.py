from __future__ import annotations

import json
import shutil
import sqlite3
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree as ET

from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract

from study_ingest.markdowner import build_note_markdown, ensure_parent, guess_title_from_text, slugify
from study_ingest.schema import init_db
from study_ingest.splitter import refine_topics, split_topics

SUPPORTED_TEXT_EXTS = {".md", ".txt", ".html", ".htm"}
SUPPORTED_DOCX_EXTS = {".docx"}
SUPPORTED_PDF_EXTS = {".pdf"}
SUPPORTED_EXTS = SUPPORTED_TEXT_EXTS | SUPPORTED_DOCX_EXTS | SUPPORTED_PDF_EXTS


def setup_workspace(base_dir: str = "study") -> dict[str, str]:
    base = Path(base_dir)
    paths = {
        "base": str(base),
        "uploads": str(base / "uploads"),
        "parsed": str(base / "parsed"),
        "notes": str(base / "notes"),
        "sources": str(base / "sources"),
        "db": str(base / "data" / "index.db"),
    }
    for key, path in paths.items():
        if key != "db":
            Path(path).mkdir(parents=True, exist_ok=True)
    init_db(paths["db"])
    return paths


def _read_docx_text(path: Path) -> str:
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for para in root.findall(".//w:p", ns):
        texts = [node.text for node in para.findall(".//w:t", ns) if node.text]
        merged = "".join(texts).strip()
        if merged:
            paragraphs.append(merged)
    return "\n".join(paragraphs)


def _ocr_pdf_text(path: Path) -> str:
    try:
        pages = convert_from_path(str(path))
    except Exception as exc:
        raise ValueError(f"Failed to rasterize PDF for OCR: {exc}") from exc
    texts = []
    for image in pages:
        try:
            text = pytesseract.image_to_string(image, lang="chi_sim+eng")
        except Exception as exc:
            raise ValueError(f"Failed to OCR PDF page: {exc}") from exc
        if text.strip():
            texts.append(text.strip())
    return "\n\n".join(texts)


def _read_pdf_text(path: Path) -> str:
    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text.strip())
    extracted = "\n\n".join(pages).strip()
    if extracted:
        return extracted
    return _ocr_pdf_text(path)


def _read_source_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in SUPPORTED_TEXT_EXTS:
        return path.read_text(encoding="utf-8", errors="ignore")
    if suffix in SUPPORTED_DOCX_EXTS:
        return _read_docx_text(path)
    if suffix in SUPPORTED_PDF_EXTS:
        return _read_pdf_text(path)
    raise ValueError(f"Unsupported source type for MVP: {path.suffix}")


def import_file(file_path: str, *, category: str = "未分类", base_dir: str = "study") -> dict:
    paths = setup_workspace(base_dir)
    src = Path(file_path)
    if not src.exists():
        raise FileNotFoundError(f"Source file not found: {file_path}")
    if src.suffix.lower() not in SUPPORTED_EXTS:
        raise ValueError(f"Unsupported source type: {src.suffix}. Supported: {', '.join(sorted(SUPPORTED_EXTS))}")

    source_name = src.name
    upload_target = Path(paths["uploads"]) / source_name
    if src.resolve() != upload_target.resolve():
        shutil.copy2(src, upload_target)
    else:
        upload_target = src

    raw_text = _read_source_text(upload_target)
    title = guess_title_from_text(raw_text, fallback=src.stem)
    slug = slugify(title)
    parsed_path = Path(paths["parsed"]) / f"{slug}.txt"
    parsed_path.write_text(raw_text, encoding="utf-8")

    topic_chunks = refine_topics(split_topics(raw_text, fallback_title=title), use_ai=False)
    generated_notes = []
    first_note_path = None
    for chunk in topic_chunks:
        note_slug = slugify(chunk.title)
        note_path = Path(paths["notes"]) / category / f"{note_slug}.md"
        ensure_parent(str(note_path))
        note_path.write_text(
            build_note_markdown(title=chunk.title, category=category, source_name=source_name, body=chunk.text),
            encoding="utf-8",
        )
        generated_notes.append({
            "title": chunk.title,
            "note_path": str(note_path),
            "start_line": chunk.start_line,
            "end_line": chunk.end_line,
        })
        if first_note_path is None:
            first_note_path = str(note_path)

    source_map = {
        "source_name": source_name,
        "original_file": str(upload_target),
        "parsed_file": str(parsed_path),
        "generated_notes": generated_notes,
        "title": title,
        "category": category,
    }
    source_json_path = Path(paths["sources"]) / f"{slug}.json"
    source_json_path.write_text(json.dumps(source_map, ensure_ascii=False, indent=2), encoding="utf-8")

    now = datetime.now(timezone.utc).isoformat()
    conn = sqlite3.connect(paths["db"])
    try:
        conn.execute(
            """
            INSERT INTO documents (source_name, source_path, parsed_path, note_path, generated_notes_json, title, category, source_type, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(source_path) DO UPDATE SET
              parsed_path=excluded.parsed_path,
              note_path=excluded.note_path,
              generated_notes_json=excluded.generated_notes_json,
              title=excluded.title,
              category=excluded.category,
              source_type=excluded.source_type,
              updated_at=excluded.updated_at
            """,
            (source_name, str(upload_target), str(parsed_path), first_note_path, json.dumps(generated_notes, ensure_ascii=False), title, category, upload_target.suffix.lower(), now, now),
        )
        doc_id = conn.execute("SELECT id FROM documents WHERE source_path = ?", (str(upload_target),)).fetchone()[0]
        conn.execute("DELETE FROM note_chunks WHERE document_id = ?", (doc_id,))
        for idx, chunk in enumerate(topic_chunks, start=1):
            conn.execute(
                "INSERT INTO note_chunks (document_id, chunk_order, heading, content) VALUES (?, ?, ?, ?)",
                (doc_id, idx, chunk.title, chunk.text),
            )
        conn.commit()
    finally:
        conn.close()

    return {
        "title": title,
        "category": category,
        "source": str(upload_target),
        "parsed": str(parsed_path),
        "note": first_note_path,
        "notes": generated_notes,
        "source_map": str(source_json_path),
        "db": paths["db"],
    }


def import_dir(dir_path: str, *, category: str = "未分类", base_dir: str = "study", recursive: bool = True) -> dict:
    src_dir = Path(dir_path)
    if not src_dir.exists() or not src_dir.is_dir():
        raise FileNotFoundError(f"Source directory not found: {dir_path}")

    files = sorted(src_dir.rglob("*") if recursive else src_dir.glob("*"))
    candidates = [p for p in files if p.is_file() and p.suffix.lower() in SUPPORTED_EXTS]

    imported = []
    failed = []
    for path in candidates:
        try:
            imported.append(import_file(str(path), category=category, base_dir=base_dir))
        except Exception as exc:
            failed.append({"file": str(path), "error": str(exc)})

    return {
        "source_dir": str(src_dir),
        "category": category,
        "recursive": recursive,
        "total_found": len(candidates),
        "imported_count": len(imported),
        "failed_count": len(failed),
        "imported": imported,
        "failed": failed,
    }


def _split_chunks(text: str, max_chars: int = 1200) -> list[str]:
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start + max_chars])
        start += max_chars
    return chunks
