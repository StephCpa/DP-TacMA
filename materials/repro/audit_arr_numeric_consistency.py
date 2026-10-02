"""No-provider numeric and scope consistency audit for the separate ARR draft."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "research" / "artifacts"
OUT = ART / "acl-arr-numeric-consistency-audit-189.json"


def load(name: str) -> dict:
    return json.loads((ART / name).read_text(encoding="utf-8"))


def main() -> None:
    main = (ROOT / "manuscript-arr" / "main.tex").read_text(encoding="utf-8")
    appendix = (ROOT / "manuscript-arr" / "appendix.tex").read_text(encoding="utf-8")
    qwen = load("iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json")
    length = load("iclr2027-qwen-cross-model-length-decision-075.json")
    live = load("iclr2027-x2-unfiltered-llm-control-analysis-164.json")
    direct = load("iclr2027-deepseek-unconditioned-collapse-analysis-098.json")
    selector = load("iclr2027-signal-selector-notation-correction-100.json")
    replication = load("pre-submission-persistence-replication-result-223.json")
    checks: dict[str, bool] = {}

    checks["persistence_replication"] = (
        replication["status"] == "complete"
        and replication["complete_cells"] == 360
        and replication["arms"] == {"evolve": 120, "depth_matched_reset": 120, "no_canary": 120}
        and replication["exposure"]["evolve_exact_or_partial"] == "0/120"
        and replication["exposure"]["depth_matched_reset_exact_or_partial"] == "0/120"
        and replication["exposure"]["no_canary_false_positive"] == "0/120"
        and abs(replication["exposure"]["evolve_one_sided_95_percent_upper_bound"] - 0.0246554011) < 1e-10
        and "0/120" in main
        and "2.5\\%" in main
        and "0/120" in appendix
        and "2.5\\%" in appendix
    )

    support = qwen["inference_correction"]["support_C5_minus_C1"]
    oracle = qwen["inference_correction"]["oracle_C5_minus_C1"]
    matched = qwen["final_only_and_matched_slot_decomposition"]
    checks["qwen_support_and_oracle"] = (
        support["mean"] == 1.0
        and support["two_sided_percentile_95_interval"] == [0.5, 1.6]
        and oracle["mean"] == 0.2
        and oracle["two_sided_percentile_95_interval"] == [0.05, 0.4]
        and "0.60 to 0.80" in main
        and "[0.50, 1.60]" in appendix
        and "[0.05, 0.40]" in appendix
        and "+1.00" in appendix
        and "+0.20" in appendix
    )
    checks["qwen_matched_slots"] = (
        round(matched["matched_16_slot_cross_trajectory_expected_oracle"], 3) == 0.626
        and round(matched["matched_16_slot_single_trajectory_mean_oracle"], 3) == 0.570
        and "0.626" in appendix
        and "0.570" in appendix
        and "0.056" in appendix
    )
    curve = selector["candidate_level_selector_ratio"]["binary_executor_example"]["mean_valid_selection_probability"]
    checks["selector_curve"] = (
        [round(curve[str(epsilon)], 4) for epsilon in (0.5, 1, 2, 4, 8)]
        == [0.5119, 0.5748, 0.6822, 0.7793, 0.7996]
        and "0.512, 0.575, 0.682, 0.779, and 0.800" in main
        and "0.5119, 0.5748, 0.6822, 0.7793, and 0.7996" in appendix
    )
    checks["length_intervention"] = (
        length["complete_pairs"] == 20
        and length["paired_analysis"]["length_zero_minus_original_exact_difference"] == -0.05
        and "42 pairs" in main
        and "+0.024" in main
        and "[-0.095,0.143]" in main
        and "0.0238" in appendix
        and "[-0.0952, 0.1429]" in appendix
    )
    replay = live["paired_feasible"]["replay"]
    exact = live["paired_feasible"]["exact"]
    checks["live_x2_control"] = (
        replay["live_true"] == 8
        and replay["symbolic_true"] == 12
        and replay["two_sided_exact_p"] == 0.125
        and exact["live_true"] == 5
        and exact["symbolic_true"] == 8
        and exact["two_sided_exact_p"] == 0.375
        and "8/12 feasible targets" in appendix
        and "5/12 canonical exact" in appendix
        and "0.125" in appendix
        and "0.375" in appendix
        and "43,623" in appendix
    )
    checks["collapse_control"] = (
        direct["source_provider_calls"] == 160
        and [row["public_task_only_raw_modal_rate"] for row in direct["tasks"]] == [0.9875, 0.95]
        and r"98.75\%" in main
        and "None of the 160 public-task-only responses was executable." in main
        and "task-level response collapse" in (main + appendix)
        and "conditional response collapse" not in (main + appendix).lower()
    )
    checks["scope_guards"] = (
        "not a causal multi-agent advantage" in main
        and "does not provide end-to-end DP" in main
        and "not an empirical end-to-end DP experiment" in appendix
    )
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "artifact": "acl-arr-numeric-consistency-audit-189",
        "status": "passed" if not failed else "failed",
        "mode": "ARR draft cross-file numeric and scope consistency; no provider calls",
        "checks": checks,
        "failed_checks": failed,
        "sources": [
            "manuscript-arr/main.tex",
            "manuscript-arr/appendix.tex",
            "research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json",
            "research/artifacts/iclr2027-qwen-cross-model-length-decision-075.json",
            "research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json",
            "research/artifacts/iclr2027-deepseek-unconditioned-collapse-analysis-098.json",
            "research/artifacts/iclr2027-signal-selector-notation-correction-100.json",
            "research/artifacts/pre-submission-persistence-replication-result-223.json",
        ],
        "no_invention_status": "All checks compare ARR manuscript strings against frozen local artifacts.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "failed_checks": failed}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
