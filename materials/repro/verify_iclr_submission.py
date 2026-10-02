"""Audit the compressed ICLR LaTeX submission against frozen experiment artifacts."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MAIN = ROOT / "manuscript/main.tex"
APPENDIX = ROOT / "manuscript/appendix.tex"
BIB = ROOT / "manuscript/references.bib"
PDF = ROOT / "manuscript/main.pdf"
OUTPUT = ROOT / "research/artifacts/iclr2027-submission-integrity-audit-101.json"


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    main_tex = MAIN.read_text(encoding="utf-8")
    appendix_tex = APPENDIX.read_text(encoding="utf-8")
    bib_text = BIB.read_text(encoding="utf-8")

    headroom = load_json("research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json")
    pool = load_json("research/artifacts/iclr2027-qwen-candidate-pool-enlargement-decision-085.json")
    trajectories = load_json("research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json")
    gate = load_json("research/artifacts/iclr2027-deepseek-compute-matched-generation-gate-analysis-092.json")
    collapse = load_json("research/artifacts/iclr2027-deepseek-conditional-collapse-analysis-094.json")
    unconditioned = load_json("research/artifacts/iclr2027-deepseek-unconditioned-collapse-analysis-098.json")
    notation = load_json("research/artifacts/iclr2027-signal-selector-notation-correction-100.json")
    x2_heldout = load_json("research/artifacts/iclr2027-x2-heldout-replication-analysis-142.json")
    x2_browsecomp_gate = load_json("research/artifacts/iclr2027-browsecomp-dependency-gate-143.json")
    x2_closure = load_json("research/artifacts/iclr2027-x2-screening-closure-144.json")
    x2_symbolic_control = load_json("research/artifacts/iclr2027-x2-heldout-symbolic-control-149.json")
    x2_attribution = load_json("research/artifacts/iclr2027-x2-component-attribution-153.json")
    x2_branch_attribution = load_json("research/artifacts/iclr2027-x2-heldout-branch-attribution-158.json")
    x2_branch_uncertainty = load_json("research/artifacts/iclr2027-x2-heldout-branch-uncertainty-161.json")
    terminology = load_json("research/artifacts/iclr2027-active-terminology-audit-163.json")
    live_integrity = load_json("research/artifacts/iclr2027-live-control-integrity-audit-166.json")
    readiness_audit = load_json("research/artifacts/iclr2027-main-conference-readiness-audit-167.json")
    reviewer_prep_audit = load_json("research/artifacts/iclr2027-reviewer-response-prep-audit-168.json")
    numeric_consistency_audit = load_json("research/artifacts/iclr2027-manuscript-numeric-consistency-audit-170.json")
    evidence_path_audit = load_json("research/artifacts/iclr2027-active-evidence-path-audit-172.json")
    readiness = load_json("research/artifacts/iclr2027-submission-readiness-145.json")
    live_control = load_json("research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json")
    with zipfile.ZipFile(ROOT / readiness["source_zip"]) as archive:
        bundle_identity = len(archive.namelist()) == 10 and all(
            archive.read(name) == (ROOT / "manuscript" / name).read_bytes()
            for name in archive.namelist()
        )

    citation_keys = {
        key.strip()
        for group in re.findall(r"\\cite[pt]?\{([^}]+)\}", main_tex)
        for key in group.split(",")
    }
    bib_keys = re.findall(r"@[A-Za-z]+\{([^,]+),", bib_text)
    duplicate_bib_keys = sorted({key for key in bib_keys if bib_keys.count(key) > 1})
    missing_citations = sorted(citation_keys - set(bib_keys))
    selected_arms = {
        "deepseek_x1": "evolve",
        "deepseek_nondegenerate": "original_evolve_canary",
        "deepseek_execution_confirmatory": "text_heuristic_retention",
        "qwen_length": "original_score",
    }
    selected_headroom_rows = [
        row
        for cohort, arm in selected_arms.items()
        for row in headroom["rows"][cohort]
        if row["arm"] == arm and row["semantic_eligible"]
    ]
    synthesized_only_valid = sum(
        row["final_execution_valid"] is True and row["round_oracle_execution_valid"] is False
        for row in selected_headroom_rows
    )

    pdfinfo = subprocess.run(
        ["pdfinfo", str(PDF)], check=True, capture_output=True
    ).stdout.decode("ascii", errors="ignore")
    total_pages = int(re.search(r"(?m)^Pages:\s+(\d+)", pdfinfo).group(1))

    checks = {
        "official_style_loaded": "\\usepackage{iclr2027_conference,times}" in main_tex,
        "double_blind_author": "\\author{Anonymous Authors}" in main_tex,
        "ai_use_statement_present": "\\section*{AI Use Statement}" in main_tex,
        "appendix_separate_and_loaded": "\\input{appendix.tex}" in main_tex and "\\appendix" in appendix_tex,
        "citations_resolve": not missing_citations and not duplicate_bib_keys,
        "literature_breadth_at_least_20": len(citation_keys) >= 20 and len(bib_keys) >= 20,
        "length_synthesis_matches_artifact": (
            headroom["pooled_length_utility"]["pairs"] == 42
            and round(headroom["pooled_length_utility"]["stratified_paired_risk_difference"], 3) == 0.024
            and [round(value, 3) for value in headroom["pooled_length_utility"]["stratified_bootstrap_95_ci"]]
            == [-0.095, 0.143]
            and "42 paired runs" in main_tex
            and "$[-0.095,0.143]$" in main_tex
        ),
        "fixed_pool_bound_matches_artifact": (
            max(
                headroom["deepseek_recoverability_and_diversity"]["deepseek_x1"]["evolve"]["semantic_headroom"],
                headroom["deepseek_recoverability_and_diversity"]["deepseek_nondegenerate"]["original_evolve_canary"]["semantic_headroom"],
                headroom["deepseek_recoverability_and_diversity"]["deepseek_execution_confirmatory"]["text_heuristic_retention"]["semantic_headroom"],
                headroom["deepseek_recoverability_and_diversity"]["qwen_length"]["original_score"]["semantic_headroom"],
            )
            == 1 / 12
            and "0--8.3 percentage points" in main_tex
            and "$[0.010,0.129]$" in main_tex
            and len(selected_headroom_rows) == 65
            and synthesized_only_valid == 0
            and "0/65" in appendix_tex
        ),
        "pool_enlargement_matches_artifact": (
            pool["main"]["tasks"] == 20
            and trajectories["inference_correction"]["support_C5_minus_C1"]["mean"] == 1.0
            and trajectories["inference_correction"]["oracle_C5_minus_C1"]["mean"] == 0.2
            and "1.00 unique canonical plan" in main_tex
            and "0.60 to 0.80" in main_tex
        ),
        "matched_slot_result_matches_artifact": (
            round(
                trajectories["final_only_and_matched_slot_decomposition"]
                ["matched_16_slot_cross_trajectory_expected_oracle"],
                3,
            )
            == 0.626
            and round(
                trajectories["final_only_and_matched_slot_decomposition"]
                ["matched_16_slot_single_trajectory_mean_oracle"],
                3,
            )
            == 0.570
            and "0.626" in main_tex
            and "0.570" in main_tex
        ),
        "repair_gate_matches_artifact": (
            gate["gate"]["complete_tasks"] == 8
            and gate["gate"]["informative_anchor_failures"] == 3
            and gate["gate"]["main_tasks_run"] == 0
            and gate["paired_outcomes"]["anchor_failures_only"]["repair_successes"] == 1
            and gate["paired_outcomes"]["anchor_failures_only"]["restart_successes"] == 0
            and "restart succeeds on 0/3 and repair on 1/3" in main_tex
        ),
        "collapse_matches_artifact": (
            collapse["failure_branch_summary"]["tasks"] == 2
            and collapse["failure_branch_summary"]["calls"] == 160
            and collapse["failure_branch_summary"]["raw_modal_rate_range"] == [0.8625, 0.95]
            and "86.25\\% and 95\\%" in main_tex
        ),
        "unconditioned_control_matches_artifact": (
            unconditioned["frozen_decision"] == "near_determinism"
            and unconditioned["source_provider_calls"] == 160
            and unconditioned["source_recorded_tokens"] == 37298
            and [row["public_task_only_raw_modal_rate"] for row in unconditioned["tasks"]]
            == [0.9875, 0.95]
            and all(row["public_task_only_executable_rate"] == 0 for row in unconditioned["tasks"])
            and "98.75\\%" in main_tex
            and "None of the 160 public-task-only responses was executable" in main_tex
        ),
        "collapse_guards_present": (
            "not 160 task units" in main_tex
            and "does not estimate a population prevalence" in main_tex
            and "task-level response collapse" in main_tex
            and "conditional response collapse" not in main_tex.lower()
            and "157-fold" not in main_tex
        ),
        "notation_correction_present": (
            notation["arm_level_utility_consequence"]["symbol"] == "delta_U^abl"
            and notation["candidate_level_selector_ratio"]["symbol"] == "rho_U^sel"
            and "\\widehat\\delta_U^{\\mathrm{abl}}" in main_tex
            and "\\rho_U^{\\mathrm{sel}}" in main_tex
            and "artifact 071 conflated these estimands" in appendix_tex
        ),
        "private_selection_citations_present": (
            {"liu2019private", "hsu2014private", "dwork2014foundations"}.issubset(citation_keys)
        ),
        "money_figure_precedes_secondary_audit": (
            main_tex.index("figures/qwen-candidate-pool-enlargement.png")
            < main_tex.index("figures/evolution-audit-main-results.pdf")
        ),
        "selector_scope_guard_present": (
            "not end-to-end privacy" in main_tex
            and "candidate-score replacement adjacency" in main_tex
            and "Candidate texts" in main_tex
        ),
        "x2_screening_closure_matches_artifacts": (
            x2_closure["original_screening"]["cells"] == 72
            and x2_closure["original_screening"]["raw_exact"] == 12
            and x2_closure["original_screening"]["action_list_exact"] == 10
            and x2_heldout["combined_18_tasks"]["feasible_replay_valid"] == 12
            and x2_heldout["combined_18_tasks"]["feasible_canonical_exact"] == 8
            and x2_heldout["combined_18_tasks"]["impossible_bounded_stops"] == 6
            and x2_heldout["combined_18_tasks"]["all_exact"] == 14
            and "12/12 feasible tasks" in main_tex
            and "8/12 canonical exact" in main_tex
            and "all six impossible-reference tasks trigger bounded stops" in main_tex
            and "artifacts 142--144, 149, 153, 158, 161, and 164" in appendix_tex
        ),
        "x2_symbolic_control_matches_artifact": (
            x2_symbolic_control["summary"]["tasks"] == 18
            and x2_symbolic_control["summary"]["symbolic_feasible_replay_valid"] == 12
            and x2_symbolic_control["summary"]["symbolic_feasible_exact"] == 8
            and x2_symbolic_control["summary"]["symbolic_bounded_stops_on_impossible"] == 6
            and x2_symbolic_control["summary"]["symbolic_all_exact"] == 14
            and x2_symbolic_control["summary"]["paired_feasible_replay"] == {
                "both_valid": 12, "symbolic_only": 0, "llm_only": 0, "neither_valid": 0
            }
            and x2_symbolic_control["summary"]["new_provider_calls"] == 0
            and ("zero-call control returned" in appendix_tex or "zero-call control reproduces" in appendix_tex)
            and "Symbolic search alone reproduces the held-out totals without model calls" in main_tex
        ),
        "x2_component_attribution_matches_artifact": (
            x2_attribution["historical_nine_task_comparison"]["n"] == 9
            and x2_attribution["historical_nine_task_comparison"]["unfiltered_llm_replay_valid"] == 4
            and x2_attribution["historical_nine_task_comparison"]["symbolic_replay_valid"] == 7
            and x2_attribution["historical_nine_task_comparison"]["hybrid_replay_valid"] == 7
            and x2_attribution["heldout_eighteen_task_control"]["paired_feasible_replay"] == {
                "both_valid": 12, "symbolic_only": 0, "llm_only": 0, "neither_valid": 0
            }
            and x2_attribution["heldout_eighteen_task_control"]["cached_hybrid_feasible_plan_equals_symbolic"] == 10
            and "unfiltered state-verified variant replayed 4/9" in appendix_tex
            and "symbolic-only search and the bounded hybrid" in appendix_tex
        ),
        "x2_branch_attribution_matches_artifact": (
            x2_branch_attribution["summary"]["feasible_tasks"] == 12
            and x2_branch_attribution["summary"]["historical_llm_requests"] == 78
            and x2_branch_attribution["summary"]["multi_option_requests"] == 7
            and x2_branch_attribution["summary"]["step_index_mismatches"] == 4
            and x2_branch_attribution["summary"]["mismatch_tasks"] == ["TEST0179", "TEST0588"]
            and x2_branch_attribution["summary"]["all_mismatch_tasks_replay_valid"] is True
            and ("7/78 requests exposed multiple options" in appendix_tex or "Seven of 78 requests expose multiple options" in appendix_tex)
        ),
        "x2_branch_uncertainty_matches_artifact": (
            x2_branch_uncertainty["metrics"]["multi_option_request_rate"]["successes"] == 7
            and x2_branch_uncertainty["metrics"]["multi_option_request_rate"]["trials"] == 78
            and x2_branch_uncertainty["metrics"]["step_index_mismatch_rate"]["successes"] == 4
            and x2_branch_uncertainty["metrics"]["task_with_mismatch_rate"]["successes"] == 2
            and x2_branch_uncertainty["metrics"]["strict_sequence_match_rate"]["successes"] == 10
            and [round(value, 3) for value in x2_branch_uncertainty["metrics"]["multi_option_request_rate"]["clopper_pearson_95_ci"]]
            == [0.037, 0.176]
            and "Exact 95\\% intervals" in appendix_tex
        ),
        "active_terminology_audit_passes": (
            terminology["status"] == "passed"
            and all(row["old_term_count"] == 0 and row["new_term_count"] > 0 for row in terminology["files"])
            and "conditional response collapse" not in main_tex.lower()
        ),
        "browsecomp_gate_is_explicitly_closed": (
            x2_browsecomp_gate["status"] == "blocked_for_screening"
            and x2_browsecomp_gate["runtime_checks"]["transformers"] is False
            and x2_browsecomp_gate["runtime_checks"]["torch"] is False
            and x2_browsecomp_gate["runtime_checks"]["faiss"] is False
            and "BrowseComp" in appendix_tex
        ),
        "pdf_compiles": PDF.exists() and total_pages > 0,
        "readiness_record_is_valid": (
            readiness["verification"]["unit_tests"] == "157 passed"
            and readiness["source_zip"] == "research/manifests/iclr2027-submission-source-169.zip"
            and bundle_identity
            and readiness["verification"]["source_zip_byte_identity"].startswith("passed:")
            and readiness["evidence_scope"]["x2_unfiltered_protocol_audit"].startswith("artifact 160")
        ),
        "live_unfiltered_control_matches_artifact": (
            live_control["status"] == "complete"
            and live_control["paired_feasible"]["replay"]["live_true"] == 8
            and live_control["paired_feasible"]["replay"]["symbolic_true"] == 12
            and live_control["paired_feasible"]["replay"]["two_sided_exact_p"] == 0.125
            and live_control["paired_feasible"]["exact"]["live_true"] == 5
            and live_control["paired_feasible"]["exact"]["two_sided_exact_p"] == 0.375
            and live_control["live_run"]["provider_integrity"]["usage_calls"] == 142
            and live_control["live_run"]["provider_integrity"]["usage_totals"]["total_tokens"] == 43623
            and "142 calls and 43,623 tokens" in appendix_tex
            and "$p=0.125$" in appendix_tex and "$p=0.375$" in appendix_tex
        ),
        "live_control_integrity_audit_passes": (
            live_integrity["status"] == "passed"
            and live_integrity["failed_checks"] == []
            and live_integrity["live_provider_calls"] == 142
            and live_integrity["live_total_tokens"] == 43623
        ),
        "main_conference_readiness_audit_passes": (
            readiness_audit["status"] == "passed"
            and readiness_audit["failed_checks"] == []
            and readiness_audit["checks"]["main_body_page_budget"] is True
            and readiness_audit["checks"]["scope_language_present"] is True
            and readiness_audit["verdict"]["largest_risk"]
        ),
        "reviewer_response_prep_audit_passes": (
            reviewer_prep_audit["status"] == "passed"
            and reviewer_prep_audit["failed_checks"] == []
            and reviewer_prep_audit["checks"]["all_evidence_paths_exist"] is True
            and reviewer_prep_audit["checks"]["no_credential_prefix"] is True
        ),
        "manuscript_numeric_consistency_audit_passes": (
            numeric_consistency_audit["status"] == "passed"
            and numeric_consistency_audit["failed_checks"] == []
        ),
        "active_evidence_path_audit_passes": (
            evidence_path_audit["status"] == "passed"
            and evidence_path_audit["failed_checks"] == []
            and evidence_path_audit["missing_paths"] == []
            and evidence_path_audit["stale_hits"] == []
        ),
    }

    failed = [name for name, passed in checks.items() if not passed]
    result = {
        "schema_version": 1,
        "artifact_id": "ICLR2027-SUBMISSION-INTEGRITY-AUDIT-101",
        "status": "passed" if not failed else "failed",
        "artifacts": {
            "main_tex": {"path": str(MAIN.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(MAIN)},
            "appendix_tex": {"path": str(APPENDIX.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(APPENDIX)},
            "bibliography": {"path": str(BIB.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(BIB)},
            "pdf": {"path": str(PDF.relative_to(ROOT)).replace("\\", "/"), "sha256": sha256(PDF), "pages": total_pages},
        },
        "citation_summary": {
            "cited_keys": len(citation_keys),
            "bibliography_entries": len(bib_keys),
            "missing_citations": missing_citations,
            "duplicate_bib_keys": duplicate_bib_keys,
        },
        "checks": checks,
        "failed_checks": failed,
        "no_invention_status": "All numerical checks are derived from frozen local artifacts.",
    }
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(OUTPUT)
    if failed:
        raise SystemExit(f"failed checks: {failed}")


if __name__ == "__main__":
    main()
