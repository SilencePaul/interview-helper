from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from knowledge.loader import parse_concept_blocks


@dataclass
class ConceptEntry:
    """Lightweight concept reference stored in concepts_index.json.

    Does NOT include full content — that is loaded on demand via load_block().
    """
    title: str
    category: str
    file_path: str
    start_line: int
    end_line: int
    triggers: list[str]
    question_type: list[str]


def build_index(notes_dir: str, output_path: str) -> int:
    """Scan notes_dir, parse all ## concept blocks, write index JSON.

    Guarantees:
    - Files processed in sorted path order (deterministic).
    - Concept order within each file is preserved.
    - Entries deduplicated by (file_path, start_line, title).

    Returns the total number of indexed concepts.
    """
    notes_path = Path(notes_dir)
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    all_entries: list[ConceptEntry] = []
    seen: set[tuple[str, int, str]] = set()

    for md_file in sorted(notes_path.rglob("*.md")):
        category = md_file.parent.name
        concepts = parse_concept_blocks(str(md_file), category)
        for concept in concepts:
            key = (concept.file_path, concept.start_line, concept.title)
            if key in seen:
                continue
            seen.add(key)
            all_entries.append(ConceptEntry(
                title=concept.title,
                category=concept.category,
                file_path=concept.file_path,
                start_line=concept.start_line,
                end_line=concept.end_line,
                triggers=concept.triggers,
                question_type=concept.question_type,
            ))

    index = {
        "version": 1,
        "notes_dir": str(notes_dir),
        "built_at": datetime.now(timezone.utc).isoformat(),
        "count": len(all_entries),
        "concepts": [asdict(e) for e in all_entries],
    }

    output.write_text(json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(all_entries)


def load_index(index_path: str) -> list[ConceptEntry]:
    """Deserialize concepts_index.json into a list of ConceptEntry objects.

    Raises FileNotFoundError with a helpful message if the index is missing.
    """
    path = Path(index_path)
    if not path.exists():
        raise FileNotFoundError(
            f"Index not found at '{index_path}'. "
            "Run `python -m app build-index` first."
        )
    data = json.loads(path.read_text(encoding="utf-8"))
    return [ConceptEntry(**entry) for entry in data["concepts"]]
