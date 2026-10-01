"""Analysis helpers for the post-ARR X1 persistence replication."""

from __future__ import annotations

from collections import Counter, defaultdict
import math
import random
from typing import Any, Iterable


ARMS = ("evolve", "depth_matched_reset", "no_canary")


def mcnemar_exact_p(evolve_only: int, reset_only: int) -> float:
    discordant = evolve_only + reset_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, k) for k in range(0, min(evolve_only, reset_only) + 1)) / (2 ** discordant)
    return min(1.0, 2.0 * tail)


def paired_bootstrap_ci(differences: list[int], *, seed: int, draws: int = 100_000) -> list[float | None]:
    if not differences:
        return [None, None]
    rng = random.Random(seed)
    n = len(differences)
    values = [sum(differences[rng.randrange(n)] for _ in range(n)) / n for _ in range(draws)]
    values.sort()
    return [values[int(0.025 * (len(values) - 1))], values[int(0.975 * (len(values) - 1))]]


def _pairs(
    runs: Iterable[dict[str, Any]],
) -> tuple[dict[str, dict[str, dict[str, Any]]], list[str], list[str]]:
    by_instance: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    duplicate_keys: list[str] = []
    invalid_records: list[str] = []
    for run in runs:
        if run.get("status") != "complete":
            continue
        raw_instance_id = run.get("instance_id")
        raw_arm = run.get("arm")
        instance_id = str(raw_instance_id or "")
        arm = str(raw_arm or "")
        if not instance_id or arm not in ARMS:
            invalid_records.append(f"invalid_cell:{instance_id}:{arm}")
            continue
        if not isinstance(run.get("primary_exact_exposure"), bool):
            invalid_records.append(f"missing_or_nonboolean_exposure:{instance_id}:{arm}")
            continue
        if not str(run.get("stratum", "")).strip():
            invalid_records.append(f"missing_stratum:{instance_id}:{arm}")
            continue
        if arm in by_instance[instance_id]:
            duplicate_keys.append(f"{instance_id}:{arm}")
        else:
            by_instance[instance_id][arm] = run
    return dict(by_instance), duplicate_keys, invalid_records


def summarize_replication(
    runs: list[dict[str, Any]],
    *,
    expected_pairs: int = 120,
    expected_stratum_counts: dict[str, int] | None = None,
    bootstrap_seed: int = 199,
    bootstrap_draws: int = 100_000,
) -> dict[str, Any]:
    by_instance, duplicate_keys, invalid_records = _pairs(runs)
    complete = {
        instance_id: arms
        for instance_id, arms in by_instance.items()
        if set(ARMS).issubset(arms)
    }
    inconsistent_strata = []
    for instance_id, arms in list(complete.items()):
        strata_for_instance = {str(run.get("stratum", "")) for run in arms.values()}
        if len(strata_for_instance) != 1:
            inconsistent_strata.append(f"{instance_id}:stratum_mismatch")
            complete.pop(instance_id, None)
    invalid_records.extend(inconsistent_strata)
    completed = [run for run in runs if run.get("status") == "complete"]
    arm_counts = Counter(str(run["arm"]) for run in completed)
    arm_exposure = Counter(
        str(run["arm"])
        for run in completed
        if bool(run.get("primary_exact_exposure"))
    )
    differences = [
        int(bool(arms["evolve"].get("primary_exact_exposure")))
        - int(bool(arms["depth_matched_reset"].get("primary_exact_exposure")))
        for arms in complete.values()
    ]
    evolve_only = sum(value == 1 for value in differences)
    reset_only = sum(value == -1 for value in differences)
    rates = {
        arm: (arm_exposure[arm] / arm_counts[arm] if arm_counts[arm] else None)
        for arm in ARMS
    }
    by_stratum: dict[str, dict[str, Any]] = {}
    strata = sorted({str(arms["evolve"].get("stratum", "unknown")) for arms in complete.values()})
    for stratum in strata:
        subset = [arms for arms in complete.values() if str(arms["evolve"].get("stratum", "unknown")) == stratum]
        stratum_diffs = [
            int(bool(arms["evolve"].get("primary_exact_exposure")))
            - int(bool(arms["depth_matched_reset"].get("primary_exact_exposure")))
            for arms in subset
        ]
        by_stratum[stratum] = {
            "complete_pairs": len(subset),
            "evolve_exposure_count": sum(bool(arms["evolve"].get("primary_exact_exposure")) for arms in subset),
            "reset_exposure_count": sum(bool(arms["depth_matched_reset"].get("primary_exact_exposure")) for arms in subset),
            "no_canary_exposure_count": sum(bool(arms["no_canary"].get("primary_exact_exposure")) for arms in subset),
            "paired_risk_difference": sum(stratum_diffs) / len(stratum_diffs) if stratum_diffs else None,
        }
    stratum_counts = {stratum: details["complete_pairs"] for stratum, details in by_stratum.items()}
    expected_stratum_counts = expected_stratum_counts or {}
    arm_count_guard = all(arm_counts.get(arm, 0) == expected_pairs for arm in ARMS)
    stratum_count_guard = (
        not expected_stratum_counts
        or all(stratum_counts.get(stratum, 0) == count for stratum, count in expected_stratum_counts.items())
    )
    status = "complete" if len(complete) == expected_pairs and not duplicate_keys and not invalid_records and arm_count_guard and stratum_count_guard else "incomplete"
    return {
        "status": status,
        "inference_eligible": status == "complete",
        "completed_runs": len(completed),
        "complete_instance_triads": len(complete),
        "expected_complete_pairs": expected_pairs,
        "duplicate_keys": duplicate_keys,
        "invalid_records": invalid_records,
        "arm_counts": dict(arm_counts),
        "arm_count_guard": arm_count_guard,
        "complete_pairs_by_stratum": stratum_counts,
        "expected_pairs_by_stratum": expected_stratum_counts,
        "stratum_count_guard": stratum_count_guard,
        "primary_exact_exposure_rate": rates,
        "no_canary_false_positive_rate": rates["no_canary"],
        "paired_risk_difference_evolve_minus_reset": sum(differences) / len(differences) if differences else None,
        "paired_bootstrap_95_ci": paired_bootstrap_ci(differences, seed=bootstrap_seed, draws=bootstrap_draws),
        "mcnemar": {
            "evolve_only": evolve_only,
            "reset_only": reset_only,
            "exact_two_sided_p": mcnemar_exact_p(evolve_only, reset_only),
        },
        "by_stratum": by_stratum,
        "interpretation_guard": "Exposure is a task/model/runtime-specific diagnostic; a null or incomplete run is not evidence of privacy.",
    }
