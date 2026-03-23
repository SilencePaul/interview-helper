from __future__ import annotations

from interviewer.interviewer import _pick_followup_dimension


def test_pick_followup_dimension_prefers_lowest_ratio():
    dims = {
        "accuracy": 2,
        "completeness": 1,
        "practicality": 0,
        "clarity": 1,
    }
    assert _pick_followup_dimension(dims) == "practicality"


def test_pick_followup_dimension_can_pick_clarity():
    dims = {
        "accuracy": 4,
        "completeness": 3,
        "practicality": 2,
        "clarity": 0,
    }
    assert _pick_followup_dimension(dims) == "clarity"
