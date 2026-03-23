from __future__ import annotations

import re
from pathlib import Path


def slugify(text: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in text.strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    return cleaned or "untitled"


def build_note_markdown(*, title: str, category: str, source_name: str, body: str) -> str:
    sections = build_review_sections(title=title, body=body)
    bullets = lambda items: "\n".join(f"- {item}" for item in items) if items else "- （待补充）"
    return f"""# {title}

## 来源
- 原文件：{source_name}
- 分类：{category}

## 核心概念
{sections['summary']}

## 重点内容
{bullets(sections['key_points'])}

## 高频考点
{bullets(sections['high_frequency'])}

## 易错点
{bullets(sections['pitfalls'])}

## 面试题 / 自测题
{bullets(sections['questions'])}

## 延伸阅读
{bullets(sections['further_reading'])}
"""


def build_review_sections(*, title: str, body: str) -> dict[str, list[str] | str]:
    paragraphs = _extract_paragraphs(body)
    summary = _build_summary(paragraphs)
    key_points = _pick_key_points(paragraphs)
    high_frequency = _build_high_frequency(title, paragraphs)
    pitfalls = _build_pitfalls(paragraphs)
    questions = _build_questions(title, paragraphs)
    further_reading = _build_further_reading(paragraphs)
    return {
        "summary": summary,
        "key_points": key_points,
        "high_frequency": high_frequency,
        "pitfalls": pitfalls,
        "questions": questions,
        "further_reading": further_reading,
    }


def _extract_paragraphs(text: str) -> list[str]:
    parts = []
    for raw in text.splitlines():
        line = raw.strip().lstrip("#").strip()
        if not line:
            continue
        if len(line) < 2:
            continue
        parts.append(re.sub(r"\s+", " ", line))
    return parts


def _build_summary(paragraphs: list[str]) -> str:
    if not paragraphs:
        return "（待补充）"
    picked = []
    for item in paragraphs:
        if len(item) >= 8:
            picked.append(item[:140])
        if len(picked) >= 3:
            break
    return "\n\n".join(picked) if picked else "（待补充）"


def _pick_key_points(paragraphs: list[str]) -> list[str]:
    points = []
    for item in paragraphs[:8]:
        text = item[:80]
        if text not in points:
            points.append(text)
    return points[:5]


def _build_high_frequency(title: str, paragraphs: list[str]) -> list[str]:
    keywords = _extract_keywords(paragraphs)
    items = [f"{title} 的定义、核心作用和适用场景"]
    if keywords:
        items.append(f"重点关注：{'、'.join(keywords[:4])}")
    if len(paragraphs) >= 2:
        items.append("梳理它与相近概念的区别，以及工程上的取舍")
    return items[:4]


def _build_pitfalls(paragraphs: list[str]) -> list[str]:
    items = []
    joined = "\n".join(paragraphs)
    if any(word in joined for word in ["优缺点", "区别", "对比"]):
        items.append("容易只背定义，但忽略与相近概念的区别和边界")
    if any(word in joined for word in ["场景", "实践", "工程"]):
        items.append("容易停留在概念层，答题时漏掉工程场景和取舍")
    items.append("复习时不要只记结论，最好能补上原因和适用条件")
    return items[:3]


def _build_questions(title: str, paragraphs: list[str]) -> list[str]:
    questions = [
        f"什么是{title}？它解决的核心问题是什么？",
        f"{title} 在实际工程里通常用在什么场景？",
    ]
    keywords = _extract_keywords(paragraphs)
    if keywords:
        questions.append(f"围绕 {'、'.join(keywords[:3])}，最容易被追问的点是什么？")
    questions.append(f"如果让你在面试里用 30 秒解释 {title}，你会怎么说？")
    return questions[:4]


def _build_further_reading(paragraphs: list[str]) -> list[str]:
    keywords = _extract_keywords(paragraphs)
    if not keywords:
        return ["回看原资料，补充更具体的实现细节和案例"]
    return [
        f"围绕 {'、'.join(keywords[:3])} 回看原资料中的实现细节",
        "补充一个真实工程案例，理解它为什么这样设计",
    ]


def _extract_keywords(paragraphs: list[str]) -> list[str]:
    stop = {"什么", "这个", "那个", "以及", "一个", "一些", "可以", "我们", "你们", "它们", "用于", "进行", "需要", "如果", "通过", "相关"}
    found: list[str] = []
    for text in paragraphs[:10]:
        for token in re.findall(r"[A-Za-z][A-Za-z0-9_\-]+|[\u4e00-\u9fff]{2,8}", text):
            if token in stop:
                continue
            if token not in found:
                found.append(token)
            if len(found) >= 8:
                return found
    return found


def guess_title_from_text(text: str, fallback: str) -> str:
    lines = [line.strip().lstrip('#').strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return fallback
    first = lines[0]
    if len(first) <= 80:
        return first
    for line in lines[1:]:
        if 1 <= len(line) <= 80:
            return line
    return fallback


def ensure_parent(path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
