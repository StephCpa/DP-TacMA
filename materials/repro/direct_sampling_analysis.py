"""Endpoint analysis for the direct-sampling support baseline (protocol 223).

Input records are per call: ``task_id``, ``arm``, ``call_index``, ``valid``
(provider integrity), ``raw`` (visible response text), ``semantic_key``,
``canonical_plan`` (string or None), ``executable`` (bool) and ``tokens``.
Comparators map each task to its cached protocol-083 outcomes. The 20 tasks
are the inferential unit; calls within a task are never treated as
independent units.
"""

from __future__ import annotations

from collections import Counter, defaultdict
import math
import random
from typing import Any, Iterable

COVERAGE_K = (1, 5, 10, 20, 50, 100, 200)
COLLAPSE_THRESHOLD = 0.80


def mcnemar_exact_p(first_only: int, second_only: int) -> float:
    discordant = first_only + second_only
    if discordant == 0:
        return 1.0
    tail = sum(math.comb(discordant, k) for k in range(min(first_only, second_only) + 1)) / 2**discordant
    return min(1.0, 2.0 * tail)


def clopper_pearson(successes: int, trials: int, alpha: float = 0.05) -> list[float | None]:
    """Two-sided exact interval by bisection on the binomial tails."""

    if trials <= 0:
        return [None, None]

    def upper_tail(p: float) -> float:  # P(X >= successes)
        return sum(math.comb(trials, k) * p**k * (1 - p) ** (trials - k) for k in range(successes, trials + 1))

    def lower_tail(p: float) -> float:  # P(X <= successes)
        return sum(math.comb(trials, k) * p**k * (1 - p) ** (trials - k) for k in range(successes + 1))

    def solve(fn, target: float, increasing: bool) -> float:
        low, high = 0.0, 1.0
        for _ in range(100):
            mid = (low + high) / 2
            if (fn(mid) < target) == increasing:
                low = mid
            else:
                high = mid
        return (low + high) / 2

    lower = 0.0 if successes == 0 else solve(upper_tail, alpha / 2, increasing=True)
    upper = 1.0 if successes == trials else solve(lower_tail, alpha / 2, increasing=False)
    return [lower, upper]


def unbiased_coverage(n: int, c: int, k: int) -> float:
    """Probability that k draws without replacement from n include one of c successes."""

    if k > n:
        raise ValueError("k exceeds the number of valid calls")
    if n - c < k:
        return 1.0
    return 1.0 - math.comb(n - c, k) / math.comb(n, k)


def task_bootstrap_ci(values: list[float], *, seed: int, draws: int) -> list[float | None]:
    if not values:
        return [None, None]
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(draws))
    return [means[int(0.025 * (draws - 1))], means[int(0.975 * (draws - 1))]]


def per_task_summary(records: Iterable[dict[str, Any]], *, collapse_threshold: float = COLLAPSE_THRESHOLD) -> dict[str, dict[str, Any]]:
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        if record.get("valid") is True:
            by_task[str(record["task_id"])].append(record)
    summary: dict[str, dict[str, Any]] = {}
    for task_id, calls in by_task.items():
        n = len(calls)
        raw_counts = Counter(str(call.get("raw", "")) for call in calls)
        semantic_counts = Counter(str(call.get("semantic_key", call.get("raw", ""))) for call in calls)
        raw_mode, raw_mode_count = raw_counts.most_common(1)[0]
        sem_mode, sem_mode_count = semantic_counts.most_common(1)[0]
        executable_raw = {str(call.get("raw", "")) for call in calls if call.get("executable") is True}
        executable_sem = {str(call.get("semantic_key", call.get("raw", ""))) for call in calls if call.get("executable") is True}
        successes = sum(call.get("executable") is True for call in calls)
        plans = {call["canonical_plan"] for call in calls if call.get("canonical_plan")}
        executable_plans = {call["canonical_plan"] for call in calls if call.get("canonical_plan") and call.get("executable") is True}
        summary[task_id] = {
            "valid_calls": n,
            "executable_calls": successes,
            "oracle": successes > 0,
            "distinct_canonical_plans": len(plans),
            "distinct_executable_plans": len(executable_plans),
            "raw_modal_share": raw_mode_count / n,
            "raw_mode_executable": raw_mode in executable_raw,
            "semantic_modal_share": sem_mode_count / n,
            "semantic_mode_executable": sem_mode in executable_sem,
            "raw_collapse": raw_mode_count / n >= collapse_threshold and raw_mode not in executable_raw,
            "semantic_collapse": sem_mode_count / n >= collapse_threshold and sem_mode not in executable_sem,
            "coverage_at_k": {k: unbiased_coverage(n, successes, k) for k in COVERAGE_K if k <= n},
            "tokens": sum(int(call.get("tokens", 0)) for call in calls),
        }
    return summary


def paired_oracle_contrast(
    direct: dict[str, dict[str, Any]],
    comparator: dict[str, bool],
    *,
    seed: int,
    draws: int,
) -> dict[str, Any]:
    tasks = sorted(set(direct) & set(comparator))
    diffs = [int(direct[t]["oracle"]) - int(bool(comparator[t])) for t in tasks]
    direct_only = sum(d == 1 for d in diffs)
    comparator_only = sum(d == -1 for d in diffs)
    return {
        "tasks": len(tasks),
        "direct_oracle": sum(direct[t]["oracle"] for t in tasks) / len(tasks) if tasks else None,
        "comparator_oracle": sum(bool(comparator[t]) for t in tasks) / len(tasks) if tasks else None,
        "risk_difference": sum(diffs) / len(diffs) if diffs else None,
        "task_bootstrap_95_ci": task_bootstrap_ci([float(d) for d in diffs], seed=seed, draws=draws),
        "direct_only": direct_only,
        "comparator_only": comparator_only,
        "exact_mcnemar_p": mcnemar_exact_p(direct_only, comparator_only),
    }


def decision(contrast: dict[str, Any], *, complete: bool) -> str:
    """Protocol-223 decision rule for the primary E1 contrast against C5."""

    if not complete or contrast["risk_difference"] is None:
        return "incomplete"
    if contrast["risk_difference"] >= 0:
        return "direct_superior" if contrast["exact_mcnemar_p"] < 0.05 else "direct_parity_or_better"
    if contrast["exact_mcnemar_p"] < 0.05:
        return "runtime_advantage"
    return "inconclusive"


def summarize_arm(
    records: list[dict[str, Any]],
    comparators: dict[str, dict[str, bool]],
    *,
    expected_tasks: int = 20,
    calls_per_task: int = 200,
    seed: int = 223,
    draws: int = 100_000,
) -> dict[str, Any]:
    tasks = per_task_summary(records)
    complete = len(tasks) == expected_tasks and all(t["valid_calls"] == calls_per_task for t in tasks.values())
    n_tasks = len(tasks)
    raw_collapse = sum(t["raw_collapse"] for t in tasks.values())
    semantic_collapse = sum(t["semantic_collapse"] for t in tasks.values())
    contrasts = {
        name: paired_oracle_contrast(tasks, {t: v[name] for t, v in comparators.items() if name in v}, seed=seed, draws=draws)
        for name in ("C5", "C1", "baseline_final")
        if any(name in v for v in comparators.values())
    }
    coverage = {
        k: sum(t["coverage_at_k"][k] for t in tasks.values()) / n_tasks
        for k in COVERAGE_K
        if n_tasks and all(k in t["coverage_at_k"] for t in tasks.values())
    }
    invalid = sum(1 for r in records if r.get("valid") is not True)
    return {
        "status": "complete" if complete else "incomplete",
        "tasks": n_tasks,
        "valid_calls": sum(t["valid_calls"] for t in tasks.values()),
        "invalid_calls_retained": invalid,
        "oracle": sum(t["oracle"] for t in tasks.values()) / n_tasks if n_tasks else None,
        "mean_distinct_canonical_plans": sum(t["distinct_canonical_plans"] for t in tasks.values()) / n_tasks if n_tasks else None,
        "mean_distinct_executable_plans": sum(t["distinct_executable_plans"] for t in tasks.values()) / n_tasks if n_tasks else None,
        "coverage_at_k": coverage,
        "raw_collapse": {"count": raw_collapse, "share": raw_collapse / n_tasks if n_tasks else None,
                         "exact_95_ci": clopper_pearson(raw_collapse, n_tasks)},
        "semantic_collapse": {"count": semantic_collapse, "share": semantic_collapse / n_tasks if n_tasks else None,
                              "exact_95_ci": clopper_pearson(semantic_collapse, n_tasks)},
        "contrasts": contrasts,
        "decision_vs_C5": decision(contrasts["C5"], complete=complete) if "C5" in contrasts else "incomplete",
        "tokens": sum(t["tokens"] for t in tasks.values()),
        "per_task": tasks,
    }


def collapse_contrast(first: dict[str, Any], second: dict[str, Any]) -> dict[str, Any]:
    """Paired exact test of raw collapse between two arms over shared tasks."""

    tasks = sorted(set(first["per_task"]) & set(second["per_task"]))
    a_only = sum(first["per_task"][t]["raw_collapse"] and not second["per_task"][t]["raw_collapse"] for t in tasks)
    b_only = sum(second["per_task"][t]["raw_collapse"] and not first["per_task"][t]["raw_collapse"] for t in tasks)
    return {"tasks": len(tasks), "first_only": a_only, "second_only": b_only, "exact_mcnemar_p": mcnemar_exact_p(a_only, b_only)}
