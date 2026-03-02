from __future__ import annotations

import re
import warnings
from dataclasses import dataclass
from pathlib import Path

MAX_CONCEPT_CHARS = 6000


@dataclass
class Concept:
    title: str
    category: str
    content: str              # single ## block only, max MAX_CONCEPT_CHARS
    triggers: list[str]       # 🎯 Interview Triggers
    question_type: list[str]  # 🧠 Question Type
    follow_up_paths: list[str]  # 🔥 Follow-up Paths
    engineering_hooks: list[str]  # 🛠 Engineering Hooks
    file_path: str
    start_line: int  # 1-indexed, line of ## heading (inclusive)
    end_line: int    # exclusive upper bound for slicing: lines[start_line-1:end_line]


def parse_concept_blocks(file_path: str, category: str) -> list[Concept]:
    """Split one markdown file into individual ## concept blocks.

    Splitting rules:
    - Block starts at a line beginning with "## "
    - Block ends just before the next "## " line, a bare "---" line, or EOF
    - Content > MAX_CONCEPT_CHARS is warned and truncated
    """
    lines = Path(file_path).read_text(encoding="utf-8").splitlines(keepends=True)
    n = len(lines)
    concepts: list[Concept] = []

    i = 0
    while i < n:
        if not lines[i].startswith("## "):
            i += 1
            continue

        title = lines[i][3:].strip()
        start_line = i + 1  # 1-indexed

        # Advance j to the first line NOT belonging to this block
        j = i + 1
        while j < n:
            if lines[j].startswith("## ") or lines[j].rstrip("\n").strip() == "---":
                break
            j += 1

        # end_line is the exclusive upper bound (1-indexed):
        # load_block uses lines[start_line-1 : end_line] == lines[i:j]
        end_line = j

        raw = "".join(lines[i:j])

        if len(raw) > MAX_CONCEPT_CHARS:
            warnings.warn(
                f"Concept '{title}' in {file_path}: {len(raw)} chars "
                f"> {MAX_CONCEPT_CHARS}, truncating.",
                stacklevel=2,
            )
            raw = raw[:MAX_CONCEPT_CHARS]

        concepts.append(Concept(
            title=title,
            category=category,
            content=raw,
            triggers=parse_bullet_list(raw, "🎯"),
            question_type=parse_question_type(raw),
            follow_up_paths=parse_bullet_list(raw, "🔥"),
            engineering_hooks=parse_bullet_list(raw, "🛠"),
            file_path=str(Path(file_path)),
            start_line=start_line,
            end_line=end_line,
        ))

        i = j

    return concepts


def load_block(file_path: str, start_line: int, end_line: int) -> str:
    """Load lines [start_line, end_line) from file (1-indexed start, exclusive end).

    Matches the slice lines[start_line-1 : end_line] which equals
    lines[i:j] used during parse_concept_blocks.
    """
    lines = Path(file_path).read_text(encoding="utf-8").splitlines(keepends=True)
    return "".join(lines[start_line - 1:end_line])


def parse_bullet_list(content: str, emoji: str) -> list[str]:
    """Extract bullet items following a line that contains the given emoji marker.

    Stops collecting at the first non-bullet, non-blank line after the marker.
    Blank lines between bullets are skipped (not treated as list terminator).
    """
    lines = content.splitlines()
    n = len(lines)
    i = 0

    # Find the marker line
    while i < n and emoji not in lines[i]:
        i += 1

    if i >= n:
        return []

    i += 1  # skip the marker line itself

    result: list[str] = []
    while i < n:
        stripped = lines[i].strip()
        if stripped.startswith("- "):
            result.append(stripped[2:].strip())
        elif stripped == "":
            i += 1
            continue  # skip blank lines, keep collecting
        else:
            break  # non-bullet, non-blank → end of list
        i += 1

    return result


def parse_question_type(content: str) -> list[str]:
    """Extract question type tags from the 🧠 Question Type line.

    Uses the last ':' in the line to skip past bold markers (e.g. `**Type:**`).
    Splits on middle-dot (·) or comma separators.
    Returns empty list if the marker is absent.
    """
    for line in content.splitlines():
        if "🧠" not in line:
            continue
        idx = line.rfind(":")
        if idx == -1:
            return []
        # Strip trailing bold markers '**' that precede the actual tag values
        raw = line[idx + 1:].strip().lstrip("*").strip()
        return [t.strip() for t in re.split(r"\s*[·,]\s*", raw) if t.strip()]
    return []
