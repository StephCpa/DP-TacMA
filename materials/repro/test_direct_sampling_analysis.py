"""Synthetic-fixture tests for the protocol-227 analysis (no provider calls).

Run from this directory: ``python test_direct_sampling_analysis.py``.
"""

from __future__ import annotations

import math

from direct_sampling_analysis import (
    clopper_pearson,
    collapse_contrast,
    decision,
    summarize_arm,
    unbiased_coverage,
)


def _calls(task_id: str, responses: list[tuple[str, bool]], arm: str = "qwen_direct") -> list[dict]:
    return [
        {
            "task_id": task_id,
            "arm": arm,
            "call_index": i,
            "valid": True,
            "raw": raw,
            "semantic_key": raw.strip().lower(),
            "canonical_plan": None if raw == "IMPOSSIBLE" else raw,
            "executable": executable,
            "tokens": 250,
        }
        for i, (raw, executable) in enumerate(responses)
    ]


def _cohort(n_tasks: int, solved: set[int], collapsed: set[int], calls: int = 200) -> list[dict]:
    records = []
    for t in range(n_tasks):
        if t in collapsed:
            responses = [("IMPOSSIBLE", False)] * calls
        elif t in solved:
            responses = [("plan_ok", True)] * 3 + [(f"wrong_{i % 7}", False) for i in range(calls - 3)]
        else:
            responses = [(f"wrong_{i % 7}", False) for i in range(calls)]
        records += _calls(f"T{t:02d}", responses)
    return records


def test_unbiased_coverage_matches_closed_form() -> None:
    assert unbiased_coverage(200, 0, 50) == 0.0
    assert unbiased_coverage(200, 200, 1) == 1.0
    assert math.isclose(unbiased_coverage(200, 3, 1), 3 / 200)
    assert math.isclose(unbiased_coverage(10, 1, 5), 0.5)


def test_clopper_pearson_known_values() -> None:
    low, high = clopper_pearson(0, 20)
    assert low == 0.0 and math.isclose(high, 1 - 0.025 ** (1 / 20), rel_tol=1e-6)
    low, high = clopper_pearson(3, 65)
    assert math.isclose(low, 0.0096, abs_tol=5e-4) and math.isclose(high, 0.1290, abs_tol=5e-4)


def test_parity_and_collapse_counts() -> None:
    records = _cohort(20, solved=set(range(16)), collapsed={18, 19})
    comparators = {f"T{t:02d}": {"C5": t < 16, "C1": t < 12, "baseline_final": t < 10} for t in range(20)}
    arm = summarize_arm(records, comparators, draws=500)
    assert arm["status"] == "complete"
    assert arm["oracle"] == 0.8
    assert arm["contrasts"]["C5"]["risk_difference"] == 0.0
    assert arm["decision_vs_C5"] == "direct_parity_or_better"
    assert arm["raw_collapse"]["count"] == 2
    assert math.isclose(arm["coverage_at_k"][200], 0.8)


def test_runtime_advantage_requires_significance() -> None:
    contrast = {"risk_difference": -0.4, "exact_mcnemar_p": 0.0078}
    assert decision(contrast, complete=True) == "runtime_advantage"
    contrast = {"risk_difference": -0.1, "exact_mcnemar_p": 0.5}
    assert decision(contrast, complete=True) == "inconclusive"
    assert decision(contrast, complete=False) == "incomplete"


def test_invalid_calls_are_excluded_and_make_the_arm_incomplete() -> None:
    records = _cohort(20, solved={0}, collapsed=set())
    records[0]["valid"] = False
    arm = summarize_arm(records, {}, draws=200)
    assert arm["invalid_calls_retained"] == 1
    assert arm["status"] == "incomplete"
    assert arm["decision_vs_C5"] == "incomplete"


def test_collapse_contrast_between_arms() -> None:
    first = summarize_arm(_cohort(20, solved=set(), collapsed={0, 1, 2}), {}, draws=200)
    second = summarize_arm(_cohort(20, solved=set(), collapsed={0}), {}, draws=200)
    result = collapse_contrast(first, second)
    assert result["first_only"] == 2 and result["second_only"] == 0
    assert result["exact_mcnemar_p"] == 0.5


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_") and callable(test):
            test()
    print("all tests passed")
