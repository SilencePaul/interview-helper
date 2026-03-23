from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class TopicChunk:
    title: str
    text: str
    start_line: int
    end_line: int


HEADING_PATTERNS = [
    re.compile(r"^#{1,6}\s*(.+)$"),
    re.compile(r"^(第[一二三四五六七八九十百千万0-9]+[章节部分篇讲]).*$"),
    re.compile(r"^([一二三四五六七八九十]+[、.].+)$"),
    re.compile(r"^(\d+(?:\.\d+)*[、.\s].+)$"),
    re.compile(r"^(（[一二三四五六七八九十]+）.+)$"),
]


def split_topics(text: str, fallback_title: str) -> list[TopicChunk]:
    lines = text.splitlines()
    chunks: list[TopicChunk] = []
    current_title = fallback_title
    current_lines: list[str] = []
    start_line = 1

    def flush(end_line: int) -> None:
        nonlocal current_lines, start_line, current_title
        body = "\n".join(current_lines).strip()
        if body:
            chunks.append(TopicChunk(title=_clean_heading(current_title) or fallback_title, text=body, start_line=start_line, end_line=end_line))
        current_lines = []

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        heading = _match_heading(line)
        if heading and current_lines:
            flush(idx - 1)
            current_title = heading
            start_line = idx
            current_lines = [raw]
        elif heading and not current_lines:
            current_title = heading
            start_line = idx
            current_lines = [raw]
        else:
            if not current_lines:
                start_line = idx
            current_lines.append(raw)

    if current_lines:
        flush(len(lines))

    normalized = _post_merge_small_chunks(chunks, fallback_title=fallback_title)
    return normalized or [TopicChunk(title=fallback_title, text=text.strip(), start_line=1, end_line=len(lines))]


def refine_topics(chunks: list[TopicChunk], use_ai: bool = False) -> list[TopicChunk]:
    """Hook for future AI-assisted refinement.

    Current MVP keeps rule-based chunks unchanged.
    Later this can merge/split/rename chunks with model assistance.
    """
    return chunks


def _match_heading(line: str) -> str | None:
    if not line:
        return None
    for pattern in HEADING_PATTERNS:
        match = pattern.match(line)
        if match:
            return _clean_heading(match.group(1) if match.groups() else line)
    return None


def _clean_heading(text: str) -> str:
    text = text.strip().lstrip('#').strip()
    text = re.sub(r"^[一二三四五六七八九十]+[、.]\s*", "", text)
    text = re.sub(r"^\d+(?:\.\d+)*[、.\s]+", "", text)
    return text.strip()


def _post_merge_small_chunks(chunks: list[TopicChunk], fallback_title: str) -> list[TopicChunk]:
    if not chunks:
        return []
    merged: list[TopicChunk] = []
    for chunk in chunks:
        should_merge = (
            merged
            and len(chunk.text) < 120
            and chunk.title == fallback_title
            and merged[-1].title == fallback_title
        )
        if should_merge:
            prev = merged[-1]
            merged[-1] = TopicChunk(
                title=prev.title or fallback_title,
                text=f"{prev.text}\n\n{chunk.text}".strip(),
                start_line=prev.start_line,
                end_line=chunk.end_line,
            )
        else:
            merged.append(chunk)
    return merged
