"""Zero-call reanalysis of cached artifacts for the ARR review response.

Reads only the cached analyses in ``research/data/cached-analysis`` and the
completed replication summary; makes no provider call. Writes
``research/data/review-response-reanalysis-231.json``. Run from this
directory: ``python reanalyze_review_items.py``.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
import random

from direct_sampling_analysis import clopper_pearson

ROOT = Path(__file__).resolve().parents[1]
CACHED = ROOT / "research" / "data" / "cached-analysis"
OUT = ROOT / "research" / "data" / "review-response-reanalysis-231.json"

# Table 3 cohorts: (cached cohort key, original/control arm).
COHORTS = {
    "DeepSeek X1 evolve": ("deepseek_x1", "evolve"),
    "DeepSeek non-degenerate evolve": ("deepseek_nondegenerate", "original_evolve_canary"),
    "DeepSeek text-retention control": ("deepseek_execution_confirmatory", "text_heuristic_retention"),
    "Qwen released score": ("qwen_length", "original_score"),
}


def load(name: str) -> dict:
    return json.loads((CACHED / name).read_text(encoding="utf-8"))


def rounded(interval: list[float | None], digits: int = 3) -> list[float | None]:
    return [None if x is None else round(x, digits) for x in interval]


def headroom() -> dict:
    rows = load("iclr2027-cached-headroom-meta-analysis-081.json")["rows"]
    per_cohort = {}
    totals = {k: 0 for k in ("eligible", "final", "round_only", "inclusive", "final_only", "all", "ref_final", "ref_pool", "agree", "slots", "parseable")}
    for name, (cohort, arm) in COHORTS.items():
        runs = [r for r in rows[cohort] if r["arm"] == arm]
        eligible = [r for r in runs if r["semantic_eligible"]]
        stats = {
            "eligible": len(eligible),
            "final": sum(bool(r["final_execution_valid"]) for r in eligible),
            "round_only": sum(bool(r["round_oracle_execution_valid"]) for r in eligible),
            "inclusive": sum(bool(r["candidate_pool_oracle_execution_valid"]) for r in eligible),
            "final_only": sum(bool(r["final_execution_valid"]) and not r["round_oracle_execution_valid"] for r in eligible),
            "all": len(runs),
            "ref_final": sum(bool(r["final_reference_exact"]) for r in runs),
            "ref_pool": sum(bool(r["candidate_pool_oracle_reference_exact"]) for r in runs),
            "agree": sum(bool(r["final_execution_valid"]) == bool(r["final_reference_exact"]) for r in eligible),
            "slots": sum(r["candidate_slots"] for r in runs),
            "parseable": sum(r["parseable_slots"] for r in runs),
        }
        for key, value in stats.items():
            totals[key] += value
        per_cohort[name] = {
            **stats,
            "failed": stats["eligible"] - stats["final"],
            "selection_failures": stats["inclusive"] - stats["final"],
            "generation_failures": stats["eligible"] - stats["inclusive"],
            "parse_acceptance": round(stats["parseable"] / stats["slots"], 3),
        }
    failed = totals["eligible"] - totals["final"]
    selection = totals["inclusive"] - totals["final"]
    generation = totals["eligible"] - totals["inclusive"]
    return {
        "per_cohort": per_cohort,
        "pooled": {
            "eligible_runs": totals["eligible"],
            "failed_runs": failed,
            "selection_failures": selection,
            "generation_failures": generation,
            "generation_failures_of_failed": f"{generation}/{failed}",
            "generation_failures_of_failed_exact_95": rounded(clopper_pearson(generation, failed)),
            "selection_failures_of_failed": f"{selection}/{failed}",
            "selection_failures_of_failed_exact_95": rounded(clopper_pearson(selection, failed)),
            "recoverable_of_eligible": f"{selection}/{totals['eligible']}",
            "recoverable_of_eligible_exact_95": rounded(clopper_pearson(selection, totals["eligible"])),
            "round_only_oracle": totals["round_only"],
            "final_inclusive_oracle": totals["inclusive"],
            "valid_final_without_valid_round_candidate": totals["final_only"],
            "estimands_identical": totals["round_only"] == totals["inclusive"],
            "reference_exact_all_runs_including_impossible": {
                "runs": totals["all"],
                "final": totals["ref_final"],
                "pool_oracle": totals["ref_pool"],
                "recoverable": totals["ref_pool"] - totals["ref_final"],
                "recoverable_exact_95": rounded(clopper_pearson(totals["ref_pool"] - totals["ref_final"], totals["all"])),
            },
            "final_executable_vs_reference_exact_agreement": f"{totals['agree']}/{totals['eligible']}",
            "parser_acceptance": f"{totals['parseable']}/{totals['slots']}",
            "parser_acceptance_rate": round(totals["parseable"] / totals["slots"], 3),
        },
    }


def nested_pool(seed: int = 231, draws: int = 20_000) -> dict:
    data = load("iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json")
    rows = data["task_rows"]
    keys = ["C1", "C2", "C3", "C4", "C5"]
    values = {k: [int(bool(r["observed_nested_oracle_curve"][k])) for r in rows] for k in keys}
    rng = random.Random(seed)
    n = len(rows)
    samples = [[rng.randrange(n) for _ in range(n)] for _ in range(draws)]
    oracle = {}
    for k in keys:
        means = sorted(sum(values[k][i] for i in s) / n for s in samples)
        oracle[k] = {"mean": sum(values[k]) / n, "task_bootstrap_95": [means[int(0.025 * (draws - 1))], means[int(0.975 * (draws - 1))]]}
    patterns: dict[str, int] = {}
    for r in rows:
        key = "".join("1" if r["observed_nested_oracle_curve"][k] else "0" for k in keys)
        patterns[key] = patterns.get(key, 0) + 1
    support_deltas = data["inference_correction"]["support_C5_minus_C1"]["task_values"]
    delta_counts: dict[str, int] = {}
    for value in support_deltas:
        delta_counts[str(int(value))] = delta_counts.get(str(int(value)), 0) + 1
    plug_in = data["trajectory_dose_response"]["anchor_inclusive_plugin_curve"]
    return {
        "tasks": n,
        "oracle_points": oracle,
        "per_task_patterns_C1_to_C5": patterns,
        "support_C5_minus_C1_task_distribution": delta_counts,
        "plug_in_curve": {k: {"mean": v["mean"], "task_cluster_bootstrap_95": v["task_cluster_bootstrap_95_interval"]} for k, v in plug_in.items()},
    }


def score_sources() -> dict:
    data = load("iclr2027-x1-score-validity-037.json")
    counts = data["score_reason_counts"]
    total = sum(counts.values())
    heuristic = counts["heuristic_only_non_slow_round"]
    rows = data["rows"]
    success_obs = sum(r["agent_round_score_count"] for r in rows if r["deterministic_exact"])
    high = data["agent_round_high_score_audit"]
    high_success = high["high_score_observations"] - high["high_score_observations_on_deterministically_failed_runs"]
    return {
        "runs": len(rows),
        "contribution_score_observations": total,
        "fast_heuristic_observations": heuristic,
        "slow_judge_observations": total - heuristic,
        "observations_from_successful_runs": f"{success_obs}/{total}",
        "high_score_observations_from_successful_runs": f"{high_success}/{high['high_score_observations']}",
        "observation_level_lift": round((high_success / high["high_score_observations"]) / (success_obs / total), 3),
        "run_level_auc_max_contribution_score": round(data["run_level_auc"]["max_agent_contribution_score"], 3),
        "unit_note": "observations are agent-round scores, 15 per run; lift is descriptive and not a likelihood ratio",
    }


def degenerate_bootstrap_bound() -> dict:
    # DeepSeek initial length intervention: 10 pairs, 0 discordant pairs.
    upper = clopper_pearson(0, 10)[1]
    return {
        "pairs": 10,
        "discordant_pairs": 0,
        "bootstrap_interval": [0.0, 0.0],
        "exact_two_sided_95_bound_on_discordance": round(upper, 3),
        "implied_risk_difference_bound": [round(-upper, 3), round(upper, 3)],
        "note": "|RD| cannot exceed the discordant-pair rate, so the exact Clopper-Pearson bound on 0/10 discordances bounds the paired risk difference.",
    }


def repair_sensitivity() -> dict:
    # TEST0030 repair branch: 69 raw ["IMPOSSIBLE"], 9 plain IMPOSSIBLE, 2 empty
    # answers from the two calls made before thinking was explicitly disabled.
    return {
        "TEST0030_all_80_calls": {"raw_modal": "69/80", "semantic_modal": "78/80"},
        "TEST0030_excluding_2_empty_pre_fix_calls": {"raw_modal": f"69/78 = {69 / 78:.4f}", "semantic_modal": "78/78 = 1.0000"},
    }


def main() -> None:
    replication = json.loads((ROOT / "research" / "data" / "pre-submission-persistence-replication-result-223.json").read_text(encoding="utf-8"))
    result = {
        "artifact": "review-response-reanalysis-231",
        "mode": "zero-call reanalysis of cached artifacts 037, 081, 088 and replication result 223",
        "provider_calls": 0,
        "headroom": headroom(),
        "nested_pool": nested_pool(),
        "score_sources_x1": score_sources(),
        "degenerate_bootstrap_initial_length_ablation": degenerate_bootstrap_bound(),
        "repair_sensitivity": repair_sensitivity(),
        "canary_replication_denominators": {
            "runs_per_arm": replication["arms"],
            "total_runs": replication["complete_cells"],
            "no_canary_false_positive_one_sided_95_upper": round(1 - 0.05 ** (1 / 120), 4),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "generation_failures": result["headroom"]["pooled"]["generation_failures_of_failed"],
        "estimands_identical": result["headroom"]["pooled"]["estimands_identical"],
        "parser_acceptance": result["headroom"]["pooled"]["parser_acceptance"],
        "C1": result["nested_pool"]["oracle_points"]["C1"],
        "C5": result["nested_pool"]["oracle_points"]["C5"],
    }))
    assert math.isclose(result["score_sources_x1"]["observation_level_lift"], 1.745, abs_tol=0.01)


if __name__ == "__main__":
    main()
