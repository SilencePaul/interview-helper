from __future__ import annotations

from interviewer.interviewer import _normalize_evaluation, _parse_evaluation


def test_parse_evaluation_with_dimensions():
    raw = '''
    {
      "score": 8,
      "dimensions": {
        "accuracy": 4,
        "completeness": 2,
        "practicality": 1,
        "clarity": 1
      },
      "strengths": ["准确"],
      "missing_points": ["少例子"],
      "ideal_answer": "理想答案"
    }
    '''
    result = _parse_evaluation(raw)
    assert result is not None
    assert result.score == 8
    assert result.dimensions["accuracy"] == 4
    assert result.dimensions["clarity"] == 1


def test_parse_evaluation_recomputes_score_from_dimensions():
    raw = '''
    {
      "score": 99,
      "dimensions": {
        "accuracy": 2,
        "completeness": 2,
        "practicality": 1,
        "clarity": 1
      },
      "strengths": ["ok"],
      "missing_points": ["x"],
      "ideal_answer": "理想答案"
    }
    '''
    result = _parse_evaluation(raw)
    assert result is not None
    assert result.score == 6


def test_normalize_evaluation_blocks_full_score_when_missing_points_exist():
    dimensions, score = _normalize_evaluation(
        {"accuracy": 4, "completeness": 3, "practicality": 2, "clarity": 1},
        ["缺少边界条件说明"],
    )
    assert score == 9
    assert dimensions == {"accuracy": 4, "completeness": 2, "practicality": 2, "clarity": 1}


def test_parse_evaluation_downgrades_perfect_score_if_missing_points_exist():
    raw = '''
    {
      "score": 10,
      "dimensions": {
        "accuracy": 4,
        "completeness": 3,
        "practicality": 2,
        "clarity": 1
      },
      "strengths": ["回答完整"],
      "missing_points": ["没有说明适用边界"],
      "ideal_answer": "理想答案"
    }
    '''
    result = _parse_evaluation(raw)
    assert result is not None
    assert result.score == 9
    assert result.dimensions == {"accuracy": 4, "completeness": 2, "practicality": 2, "clarity": 1}
    assert result.missing_points == ["没有说明适用边界"]
