"""Split notes by ## / ### headings into token-bounded chunks."""
from __future__ import annotations
import re
from dataclasses import dataclass, field


@dataclass
class Chunk:
    heading: str         # e.g. "## B-Tree 索引"
    level: int           # 2 for ##, 3 for ###
    body: str
    index: int           # position in the note


def estimate_tokens(text: str) -> int:
    """Rough token estimate: words * 1.3."""
    return int(len(text.split()) * 1.3)


def chunk_note(content: str) -> list[Chunk]:
    """Split note content on ## / ### headings into Chunk objects."""
    heading_pattern = re.compile(r'^(#{2,3})\s+(.+)$', re.MULTILINE)
    matches = list(heading_pattern.finditer(content))

    if not matches:
        # No headings — return whole note as single chunk
        return [Chunk(heading="(全文)", level=2, body=content.strip(), index=0)]

    chunks: list[Chunk] = []
    for i, match in enumerate(matches):
        level = len(match.group(1))
        heading = match.group(0).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        chunks.append(Chunk(heading=heading, level=level, body=body, index=i))

    return chunks


def build_outline(chunks: list[Chunk]) -> str:
    """Return numbered list of headings only (no body text)."""
    lines = []
    for i, chunk in enumerate(chunks, 1):
        indent = "  " if chunk.level == 3 else ""
        lines.append(f"{indent}{i}. {chunk.heading}")
    return "\n".join(lines)


def select_chunks(chunks: list[Chunk], subtopic_hint: str = "") -> list[Chunk]:
    """
    Select chunks matching subtopic_hint by keyword.
    Returns matching chunks; if no hint or no match, returns all chunks.
    """
    if not subtopic_hint:
        return chunks

    hint_lower = subtopic_hint.lower()
    matched = [c for c in chunks if hint_lower in c.heading.lower() or hint_lower in c.body.lower()]
    return matched if matched else chunks


def chunks_for_prompt(chunks: list[Chunk], max_tokens: int = 2000) -> list[Chunk]:
    """
    Trim chunk list so total tokens stay under max_tokens.
    Prioritises earlier chunks.
    """
    selected: list[Chunk] = []
    total = 0
    for chunk in chunks:
        t = estimate_tokens(chunk.heading + "\n" + chunk.body)
        if total + t > max_tokens and selected:
            break
        selected.append(chunk)
        total += t
    return selected


def format_chunks(chunks: list[Chunk]) -> str:
    """Render chunks as markdown string."""
    parts = []
    for chunk in chunks:
        parts.append(chunk.heading)
        if chunk.body:
            parts.append(chunk.body)
        parts.append("")
    return "\n".join(parts).strip()
