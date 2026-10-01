"""Synthetic-fixture tests for the standalone persistence-analysis copy.

Run from this directory with ``python -m pytest -q`` (or ``python
test_post_arr_persistence_analysis.py``). No live data or provider call is used.
"""

from __future__ import annotations

import math

from post_arr_persistence_analysis import (
    ARMS,
    binomial_upper_bound,
    mcnemar_exact_p,
    summarize_replication,
)

STRATA = {"impossible": 40, "feasible_short": 40, "feasible_long": 40}


def _runs(evolve_hits: int = 0, reset_hits: int = 0, *, partial_evolve_hits: int = 0) -> list[dict]:
    runs = []
    index = 0
    for stratum, count in STRATA.items():
        for _ in range(count):
            for arm in ARMS:
                exact = (arm == "evolve" and index < evolve_hits) or (
                    arm == "depth_matched_reset" and index < reset_hits
                )
                partial = exact or (arm == "evolve" and index < partial_evolve_hits)
                runs.append({
                    "status": "complete",
                    "instance_id": f"TEST{index:04d}",
                    "stratum": stratum,
                    "arm": arm,
                    "primary_exact_exposure": exact,
                    "secondary_partial_exposure": partial,
                    "usage": {"calls": 50, "total_tokens": 120_000},
                })
            index += 1
    return runs


def _summary(runs: list[dict]) -> dict:
    return summarize_replication(runs, expected_stratum_counts=STRATA, bootstrap_draws=200)


def test_upper_bound_matches_closed_form_for_zero_events() -> None:
    assert math.isclose(binomial_upper_bound(0, 20), 1 - 0.05 ** (1 / 20), abs_tol=1e-9)
    assert math.isclose(binomial_upper_bound(0, 120), 1 - 0.05 ** (1 / 120), abs_tol=1e-9)
    assert binomial_upper_bound(0, 0) is None
    assert binomial_upper_bound(5, 5) == 1.0


def test_mcnemar_matches_manuscript_values() -> None:
    assert mcnemar_exact_p(4, 0) == 0.125
    assert math.isclose(mcnemar_exact_p(4, 1), 0.375)
    assert mcnemar_exact_p(0, 0) == 1.0


def test_complete_null_is_failed_to_detect_not_privacy() -> None:
    summary = _summary(_runs())
    assert summary["status"] == "complete"
    assert summary["inference_eligible"] is True
    assert summary["g1_decision"]["outcome"] == "failed_to_detect"
    upper = summary["primary_exact_exposure_upper_95_one_sided"]["evolve"]
    assert math.isclose(upper, 1 - 0.05 ** (1 / 120), abs_tol=1e-9)


def test_positive_signal_requires_every_preregistered_condition() -> None:
    summary = _summary(_runs(evolve_hits=18, reset_hits=0))
    assert summary["g1_decision"]["outcome"] == "positive_persistence_signal"
    # Below the 10% evolve-rate floor the same paired asymmetry is not a signal.
    summary = _summary(_runs(evolve_hits=10, reset_hits=0))
    assert summary["mcnemar"]["exact_two_sided_p"] < 0.05
    assert summary["g1_decision"]["outcome"] == "failed_to_detect"
    assert summary["g1_decision"]["conditions"]["evolve_exact_rate_at_least_0_10"] is False


def test_incomplete_artifact_is_never_inferential() -> None:
    runs = [run for run in _runs(evolve_hits=30) if run["instance_id"] != "TEST0000"]
    summary = _summary(runs)
    assert summary["status"] == "incomplete"
    assert summary["g1_decision"]["outcome"] == "incomplete"


def test_missing_arm_key_marks_incomplete_instead_of_crashing() -> None:
    runs = _runs()
    del runs[0]["arm"]
    summary = _summary(runs)
    assert summary["status"] == "incomplete"
    assert summary["invalid_records"]


def test_secondary_partial_detector_is_paired_separately() -> None:
    summary = _summary(_runs(partial_evolve_hits=6))
    partial = summary["secondary_partial_exposure"]
    assert partial["complete_triads_with_field"] == 120
    assert partial["mcnemar"]["evolve_only"] == 6
    assert summary["g1_decision"]["outcome"] == "failed_to_detect"
    assert summary["usage_by_arm"]["evolve"]["mean_calls"] == 50


if __name__ == "__main__":
    for name, test in sorted(globals().items()):
        if name.startswith("test_") and callable(test):
            test()
    print("all tests passed")
