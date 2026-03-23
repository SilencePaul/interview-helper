from __future__ import annotations

from interviewer.interviewer import _parse_evaluation


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
