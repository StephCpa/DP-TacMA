"""Zero-call preview of protocol 234 from the cached analyses (artifact 237).

Computes the parts of the candidate-support audit that cached per-run and
per-task rows already allow: dual endpoints for the two cached score-ablation
cells, random-selector baselines on the nested Qwen pools, and the census size
and run-level sensitivity that motivate auditing every rejected text. It reads
no candidate text and makes no provider call. Run from this directory:
``python candidate_support_cached_preview.py``.
"""

from __future__ import annotations

import json
from pathlib import Path

from candidate_support_audit import bootstrap_mean_ci, dual_endpoints, exact_interval

ROOT = Path(__file__).resolve().parents[1]
CACHED = ROOT / "research" / "data" / "cached-analysis"
OUT = ROOT / "research" / "data" / "candidate-support-cached-preview-237.json"
SEED = 234
TABLE3 = {
    "deepseek_x1": "evolve",
    "deepseek_nondegenerate": "original_evolve_canary",
    "deepseek_execution_confirmatory": "text_heuristic_retention",
    "qwen_length": "original_score",
}
SCORE_CELLS = {
    "deepseek_nondegenerate_length_removal": ("deepseek_nondegenerate", "original_evolve_canary", "length_zero_evolve_canary"),
    "qwen_length_removal": ("qwen_length", "original_score", "length_zero"),
}


def load(name: str) -> dict:
    return json.loads((CACHED / name).read_text(encoding="utf-8"))


def r3(values):
    return [None if v is None else round(v, 3) for v in values]


def endpoint_cells(rows: dict) -> dict:
    out = {}
    for cell, (cohort, control, treated) in SCORE_CELLS.items():
        runs = [{"arm": r["arm"], "task_id": r["instance_id"], "semantic_eligible": r["semantic_eligible"],
                 "exec_valid": bool(r["final_execution_valid"]), "ref_exact": bool(r["final_reference_exact"])}
                for r in rows[cohort] if r["arm"] in (control, treated)]
        result = dual_endpoints(runs, control, treated, seed=SEED)
        for v in result.values():
            v["difference"] = round(v["difference"], 3)
            v["bootstrap_95"] = r3(v["bootstrap_95"])
        diffs = {k: (v["difference"], tuple(v["discordant"])) for k, v in result.items()}
        out[cell] = {"control_arm": control, "treated_arm": treated, **result,
                     "endpoints_agree": len(set(diffs.values())) == 1}
    out["initial_deepseek_length_cohort"] = (
        "Not in the cached rows. Its 10 pairs had 0 discordant pairs under reference exactness "
        "(artifact 231); the executable-validity contrast needs the workspace run records.")
    return out


def selector_baselines() -> dict:
    rows = load("iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json")["task_rows"]
    out = {"tasks": len(rows), "definitions": {
        "oracle": "offline executable oracle over the round candidates of the anchor and first j stochastic trajectories (C_j)",
        "random_final": "uniform choice among the j+1 trajectory final answers in C_j; exact expectation",
        "random_stochastic_slot": "uniform choice among the 16j recorded slots of the first j stochastic trajectories; "
                                  "the anchor's per-slot validity is not cached, so it is excluded",
        "anchor_final": "the temperature-zero trajectory's own final answer",
    }}
    for j in range(1, 6):
        oracle = [float(r["observed_nested_oracle_curve"][f"C{j}"]) for r in rows]
        finals = [(float(r["anchor_final_valid"]) + sum(float(s["final_valid"]) for s in r["stochastic"][:j])) / (j + 1)
                  for r in rows]
        slots = [sum(s["valid_slots"] for s in r["stochastic"][:j]) / sum(s["slots"] for s in r["stochastic"][:j])
                 for r in rows]
        gap = [o - f for o, f in zip(oracle, finals)]
        out[f"C{j}"] = {
            "oracle": round(sum(oracle) / len(rows), 3),
            "random_final": round(sum(finals) / len(rows), 3),
            "random_final_task_bootstrap_95": r3(bootstrap_mean_ci(finals, seed=SEED)),
            "random_stochastic_slot": round(sum(slots) / len(rows), 3),
            "oracle_minus_random_final": round(sum(gap) / len(rows), 3),
            "oracle_minus_random_final_task_bootstrap_95": r3(bootstrap_mean_ci(gap, seed=SEED)),
        }
    out["anchor_final"] = round(sum(float(r["anchor_final_valid"]) for r in rows) / len(rows), 3)
    out["not_computable_from_cache"] = ("recorded-score, length-only, success-only, composite and judge selectors: the "
                                        "cached rows hold per-trajectory counts, not per-candidate scores or lengths")
    return out


def census_planning() -> dict:
    rows = load("iclr2027-cached-headroom-meta-analysis-081.json")["rows"]
    failed = [r for cohort, arm in TABLE3.items() for r in rows[cohort]
              if r["arm"] == arm and r["semantic_eligible"] and not r["final_execution_valid"]]
    generation = [r for r in failed if not r["candidate_pool_oracle_execution_valid"]]
    rejected = [r["candidate_slots"] - r["parseable_slots"] for r in generation]
    unique = [min(r["unique_exact_texts"], r["candidate_slots"] - r["parseable_slots"]) for r in generation]
    sensitivity = {}
    for q in (0.005, 0.01, 0.02, 0.05):
        sensitivity[str(q)] = {
            "independent_rejected_slots": round(sum(1 - (1 - q) ** n for n in rejected), 1),
            "independent_unique_texts_upper": round(sum(1 - (1 - q) ** n for n in unique), 1),
        }
    return {
        "p0_failed_runs": len(failed),
        "rejected_slots_in_failed_runs": sum(r["candidate_slots"] - r["parseable_slots"] for r in failed),
        "unique_texts_in_failed_runs_upper_bound": sum(r["unique_exact_texts"] for r in failed),
        "generation_failure_runs": len(generation),
        "rejected_slots_in_generation_failures": sum(rejected),
        "mean_rejected_slots_per_generation_failure": round(sum(rejected) / len(generation), 2),
        "generation_failures_exact_95": r3(exact_interval(len(generation), len(failed))),
        "expected_runs_reclassified_if_each_rejected_text_is_a_false_negative_with_rate_q": sensitivity,
        "reading": ("A small slot-level false-negative rate can still move many runs because each generation failure "
                    "has many rejected slots, so protocol 234 audits every unique rejected text in the failed runs "
                    "and decides on run reclassifications, not on a slot-level rate alone. Independence is a "
                    "worst-case planning assumption; duplicated texts make false negatives cluster within runs."),
    }


def main() -> None:
    rows = load("iclr2027-cached-headroom-meta-analysis-081.json")["rows"]
    result = {
        "artifact": "candidate-support-cached-preview-237",
        "protocol": "candidate-support-audit-protocol-234 (draft); this preview is not the frozen analysis 235",
        "mode": "zero-call reanalysis of cached artifacts 081 and 088",
        "provider_calls": 0,
        "candidate_texts_read": 0,
        "endpoint_ablation": endpoint_cells(rows),
        "selector_baselines_qwen_nested_pool": selector_baselines(),
        "census_planning": census_planning(),
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sel = result["selector_baselines_qwen_nested_pool"]
    print(json.dumps({
        "endpoints_agree": {k: v["endpoints_agree"] for k, v in result["endpoint_ablation"].items() if isinstance(v, dict)},
        "random_final": [sel[f"C{j}"]["random_final"] for j in range(1, 6)],
        "oracle": [sel[f"C{j}"]["oracle"] for j in range(1, 6)],
        "gap": [sel[f"C{j}"]["oracle_minus_random_final"] for j in range(1, 6)],
        "census": {k: result["census_planning"][k] for k in ("p0_failed_runs", "rejected_slots_in_failed_runs",
                                                            "unique_texts_in_failed_runs_upper_bound")},
    }, indent=1))


if __name__ == "__main__":
    main()
