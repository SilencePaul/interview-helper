from __future__ import annotations

from study_ingest.splitter import split_topics


def test_split_topics_by_markdown_headings():
    text = "# 事务\n事务是一组操作。\n\n# MVCC\nMVCC 用于提升并发。"
    chunks = split_topics(text, fallback_title="数据库")
    assert len(chunks) == 2
    assert chunks[0].title == "事务"
    assert "事务是一组操作" in chunks[0].text
    assert chunks[1].title == "MVCC"


def test_split_topics_by_numbered_headings():
    text = "1. 锁\n锁用于控制并发。\n\n2. 隔离级别\n隔离级别用于平衡一致性和性能。"
    chunks = split_topics(text, fallback_title="数据库")
    assert len(chunks) == 2
    assert chunks[0].title == "锁"
    assert chunks[1].title == "隔离级别"
