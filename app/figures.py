"""Placeholder scanner, Mermaid/table/ASCII generator, diff preview + confirm patch."""
from __future__ import annotations
import re
from dataclasses import dataclass
from pathlib import Path

from app.config import MODEL_FIGURES, NOTES_DIR
from app.llm.base import LLMBase

# Patterns that indicate a missing/placeholder figure
_PLACEHOLDER_PATTERNS = [
    re.compile(r'^\s*image\s*$', re.IGNORECASE | re.MULTILINE),
    re.compile(r'^\s*image\.png\s*$', re.IGNORECASE | re.MULTILINE),
    re.compile(r'\d{13}\.png'),
    re.compile(r'!\[.*?\]\((?!https?://)[^)]*(?:missing|TODO|placeholder|image)[^)]*\)', re.IGNORECASE),
    re.compile(r'!\[.*?\]\(\s*\)'),  # empty src
]


@dataclass
class Placeholder:
    file: Path
    line_num: int      # 1-based
    raw_text: str
    context_window: str


def _matches_placeholder(line: str) -> bool:
    for pat in _PLACEHOLDER_PATTERNS:
        if pat.search(line):
            return True
    return False


def context_window(lines: list[str], line_idx: int, radius: int = 10) -> str:
    """Extract ±radius lines around line_idx (0-based), return as string."""
    start = max(0, line_idx - radius)
    end = min(len(lines), line_idx + radius + 1)
    return "".join(lines[start:end])


def scan_all_notes() -> list[Placeholder]:
    """Walk NOTES_DIR and return all Placeholder instances."""
    placeholders: list[Placeholder] = []
    if not NOTES_DIR.exists():
        return placeholders
    for md_file in NOTES_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lines = content.splitlines(keepends=True)
        for idx, line in enumerate(lines):
            if _matches_placeholder(line):
                placeholders.append(Placeholder(
                    file=md_file,
                    line_num=idx + 1,
                    raw_text=line.rstrip('\n'),
                    context_window=context_window(lines, idx),
                ))
    return placeholders


def generate_replacement(context: str, placeholder: str, llm: LLMBase) -> str:
    """
    Call MODEL_FIGURES to generate a Mermaid/table/ASCII substitute
    derived only from surrounding context.
    """
    system = (
        "你是一个技术文档图表生成助手。"
        "根据用户提供的上下文文字，生成一个简洁的图表替代原来缺失的图片。"
        "只能使用以下三种格式之一：Mermaid代码块、Markdown表格、或ASCII示意图。"
        "不得引用任何外部事实，只能根据上下文推断。"
        "只输出图表内容，不要加任何解释文字。"
    )
    user = (
        f"缺失的图片占位符：{placeholder}\n\n"
        f"周围上下文：\n{context}\n\n"
        "请生成一个合适的图表来替代这个缺失的图片。"
    )
    r = llm.chat(
        MODEL_FIGURES,
        system,
        [{"role": "user", "content": user}],
        max_tokens=512,
        tag="figures.generate",
    )
    return r.text.strip()


def preview_diff(path: Path, line_num: int, old: str, new: str) -> str:
    """Return a human-readable diff string."""
    lines = [
        f"文件: {path}",
        f"行号: {line_num}",
        "",
        "--- 原内容 ---",
        old,
        "",
        "+++ 替换内容 +++",
        new,
    ]
    return "\n".join(lines)


def apply_patch(path: Path, line_num: int, old_text: str, new_text: str) -> None:
    """Replace line at line_num (1-based) with new_text in-place."""
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    idx = line_num - 1
    if 0 <= idx < len(lines):
        # Preserve trailing newline
        ending = '\n' if lines[idx].endswith('\n') else ''
        lines[idx] = new_text.rstrip('\n') + ending
    path.write_text("".join(lines), encoding="utf-8")
