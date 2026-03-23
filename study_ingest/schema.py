from __future__ import annotations

import sqlite3
from pathlib import Path


def init_db(db_path: str) -> None:
    path = Path(db_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_name TEXT NOT NULL,
                source_path TEXT NOT NULL UNIQUE,
                parsed_path TEXT,
                note_path TEXT,
                generated_notes_json TEXT DEFAULT '[]',
                title TEXT,
                category TEXT,
                tags_json TEXT DEFAULT '[]',
                source_type TEXT,
                status TEXT NOT NULL DEFAULT 'imported',
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS note_chunks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER NOT NULL,
                chunk_order INTEGER NOT NULL,
                heading TEXT,
                content TEXT NOT NULL,
                FOREIGN KEY(document_id) REFERENCES documents(id)
            );

            CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
            CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
            CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON note_chunks(document_id);
            """
        )
        cols = {row[1] for row in conn.execute("PRAGMA table_info(documents)")}
        if "generated_notes_json" not in cols:
            conn.execute("ALTER TABLE documents ADD COLUMN generated_notes_json TEXT DEFAULT '[]'")
        conn.commit()
    finally:
        conn.close()
