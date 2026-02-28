"""Note discovery, fuzzy matching, and loading."""
from __future__ import annotations
import re
from pathlib import Path

from app.config import NOTES_DIR


def list_topics() -> dict[str, list[str]]:
    """Return {category: [topic_names]} by walking NOTES_DIR."""
    result: dict[str, list[str]] = {}
    if not NOTES_DIR.exists():
        return result
    for category_dir in sorted(NOTES_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        topics = sorted(p.stem for p in category_dir.glob("*.md"))
        if topics:
            result[category_dir.name] = topics
    return result


def _score_match(query: str, text: str) -> int:
    """Simple scoring: count how many query tokens appear in text."""
    query_lower = query.lower()
    text_lower = text.lower()
    if query_lower == text_lower:
        return 100
    if query_lower in text_lower:
        return 80
    # token overlap
    q_tokens = set(re.split(r'\W+', query_lower))
    t_tokens = set(re.split(r'\W+', text_lower))
    return len(q_tokens & t_tokens) * 10


def find_notes(topic: str) -> list[tuple[Path, str]]:
    """
    Fuzzy-match topic against note filenames and directory names.
    Returns list of (path, display_name) sorted by match score desc.
    """
    if not NOTES_DIR.exists():
        return []

    candidates: list[tuple[int, Path, str]] = []
    for md_file in NOTES_DIR.rglob("*.md"):
        # Score against stem and parent dir name
        stem_score = _score_match(topic, md_file.stem)
        dir_score = _score_match(topic, md_file.parent.name)
        score = max(stem_score, dir_score)
        if score > 0:
            display = f"{md_file.parent.name}/{md_file.stem}"
            candidates.append((score, md_file, display))

    candidates.sort(key=lambda x: x[0], reverse=True)
    return [(path, display) for _, path, display in candidates]


def load_note(path: Path) -> str:
    """Read and return note content."""
    return path.read_text(encoding="utf-8")
