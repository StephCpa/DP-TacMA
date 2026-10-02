"""No-provider readiness audit for the separate ACL ARR manuscript draft."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARR = ROOT / "manuscript-arr"
OUT = ROOT / "research" / "artifacts" / "acl-arr-draft-readiness-audit-174.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    main_tex = (ARR / "main.tex").read_text(encoding="utf-8")
    appendix_tex = (ARR / "appendix.tex").read_text(encoding="utf-8")
    checklist = (ARR / "submission" / "arr-october-readiness.md").read_text(encoding="utf-8")
    responsible = (ARR / "submission" / "responsible-nlp-checklist-draft.md").read_text(encoding="utf-8")
    log = (ARR / "main.log").read_text(encoding="utf-8", errors="ignore")
    live = json.loads((ROOT / "research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json").read_text(encoding="utf-8"))
    supplement_boundary = json.loads(
        (ROOT / "research/artifacts/acl-arr-supplement-boundary-audit-175.json").read_text(encoding="utf-8")
    )
    code_supplement = json.loads(
        (ROOT / "research/artifacts/acl-arr-code-supplement-audit-176.json").read_text(encoding="utf-8")
    )
    code_smoke = json.loads(
        (ROOT / "research/artifacts/acl-arr-code-supplement-smoke-177.json").read_text(encoding="utf-8")
    )
    license_audit = json.loads(
        (ROOT / "research/artifacts/acl-arr-license-audit-178.json").read_text(encoding="utf-8")
    )
    manuscript_archive = json.loads(
        (ROOT / "research/artifacts/acl-arr-manuscript-archive-audit-179.json").read_text(encoding="utf-8")
    )
    pubcheck_preflight = json.loads(
        (ROOT / "research/artifacts/acl-arr-pubcheck-preflight-180.json").read_text(encoding="utf-8")
    )
    official_pubcheck = json.loads(
        (ROOT / "research/artifacts/acl-arr-official-pubcheck-194.json").read_text(encoding="utf-8")
    )
    historical_official_pubcheck = json.loads(
        (ROOT / "research/artifacts/acl-arr-official-pubcheck-181.json").read_text(encoding="utf-8")
    )
    legacy_pubcheck = json.loads(
        (ROOT / "research/artifacts/acl-arr-legacy-pubcheck-183.json").read_text(encoding="utf-8")
    )
    upload_candidate = json.loads(
        (ROOT / "research/artifacts/acl-arr-upload-candidate-185.json").read_text(encoding="utf-8")
    )
    openreview_access = json.loads(
        (ROOT / "research/artifacts/acl-arr-openreview-access-187.json").read_text(encoding="utf-8")
    )
    numeric_consistency = json.loads(
        (ROOT / "research/artifacts/acl-arr-numeric-consistency-audit-189.json").read_text(encoding="utf-8")
    )
    claim_evidence = json.loads(
        (ROOT / "research/artifacts/acl-arr-claim-evidence-audit-191.json").read_text(encoding="utf-8")
    )
    citation_audit = json.loads(
        (ROOT / "research/artifacts/acl-arr-citation-audit-192.json").read_text(encoding="utf-8")
    )
    metadata_audit = json.loads(
        (ROOT / "research/artifacts/acl-arr-metadata-audit-193.json").read_text(encoding="utf-8")
    )
    pdfinfo = subprocess.run(["pdfinfo", str(ARR / "main.pdf")], check=True, capture_output=True).stdout.decode("ascii", errors="ignore")
    pages = int(re.search(r"(?m)^Pages:\s+(\d+)", pdfinfo).group(1))
    combined = main_tex + appendix_tex + checklist + responsible
    credential_hits = re.findall(r"(?i)(?:sk|rc)-[A-Za-z0-9_-]{12,}", combined)
    checks = {
        "acl_review_style_and_anonymity": "\\usepackage[review]{acl}" in main_tex and "\\author{Anonymous ACL Submission}" in main_tex,
        "required_limitations_and_ethics": "\\section{Limitations}" in main_tex and "\\section{Ethical Considerations}" in main_tex,
        "terminology_current": "task-level response collapse" in combined.lower() and "conditional response collapse" not in combined.lower() and "response-concentration" not in combined.lower(),
        "live_x2_control_present": (
            "8/12 feasible targets with 5/12 canonical exact plans" in appendix_tex
            and "two-sided exact $p=0.125$" in appendix_tex
            and "$p=0.375$" in appendix_tex
            and "held-out planning component control" in main_tex.lower()
        ),
        "live_x2_numbers_match_artifact": (
            live["paired_feasible"]["replay"]["live_true"] == 8
            and live["paired_feasible"]["exact"]["live_true"] == 5
            and live["live_run"]["provider_integrity"]["usage_totals"]["total_tokens"] == 43623
        ),
        "pdf_compiles_to_expected_length": pages == 15,
        "no_undefined_citations_or_references": not any(
            token in log.lower()
            for token in ("there were undefined references", "citation `", "undefined citations")
        ),
        "responsible_nlp_disclosure_present": "Generative-AI assistance disclosure" in responsible and "No AI system is listed as an author" in responsible,
        "no_credential_prefix": not credential_hits,
        "safe_supplement_candidate_is_clean": (
            supplement_boundary["checks"]["safe_candidate_files_exist"]
            and supplement_boundary["checks"]["safe_candidate_has_no_secret_patterns"]
            and supplement_boundary["checks"]["raw_research_material_excluded"]
        ),
        "code_supplement_boundary_is_explicit": (
            supplement_boundary["checks"]["upstream_code_requires_scrub"]
            and "upstream/TacoMAS-MultiAgent/scripts/run_evolution.py until hardcoded credential defaults are removed"
            in supplement_boundary["excluded_by_policy"]
        ),
        "scrubbed_code_supplement_audit_passed": (
            code_supplement["status"] == "passed"
            and code_supplement["checks"]["no_secret_patterns"]
            and code_supplement["checks"]["no_forbidden_components"]
            and code_supplement["checks"]["no_machine_specific_paths"]
            and code_supplement["checks"]["no_experiment_identifiers"]
            and code_supplement["checks"]["python_sources_compile"]
        ),
        "scrubbed_code_supplement_smoke_passed": (
            code_smoke["status"] == "passed"
            and code_smoke["checks"]["help_exit_code_zero"]
            and code_smoke["checks"]["help_output_present"]
            and code_smoke["checks"]["no_credential_prefix_in_output"]
        ),
        "license_gate_is_explicit": (
            license_audit["status"] == "manual_confirmation_required"
            and not license_audit["checks"]["redistribution_clearance"]
            and "upstream maintainers" in " ".join(license_audit["source_notes"])
        ),
        "license_git_history_check_recorded": (
            "local_git_history_check" in license_audit
            and "no LICENSE or COPYING path" in license_audit["local_git_history_check"]["license_path_history"]
        ),
        "manuscript_source_archive_verified": (
            manuscript_archive["status"] == "passed"
            and manuscript_archive["entry_count"] == 10
            and manuscript_archive["independent_compile"]["command_exit_codes"] == [0, 0, 0, 0]
            and manuscript_archive["independent_compile"]["pages"] == 15
            and manuscript_archive["independent_compile"]["normalized_text_equal"]
            and manuscript_archive["independent_compile"]["text_outputs_distinct"]
        ),
        "local_pubcheck_preflight_passed": (
            pubcheck_preflight["status"] == "passed"
            and pubcheck_preflight["checks"]["non_line_numbered_source"]
            and pubcheck_preflight["checks"]["no_overfull_boxes"]
            and pubcheck_preflight["checks"]["no_undefined_references"]
            and pubcheck_preflight["official_pubcheck"] == "not_available_in_environment"
        ),
        "official_pubcheck_state_is_explicit": (
            official_pubcheck["status"] == "passed"
            and official_pubcheck["exit_code"] == 0
            and official_pubcheck["result"] == "All Clear!"
            and historical_official_pubcheck["status"] == "environment_unavailable"
            and "Git fetch failed" in historical_official_pubcheck["result"]
        ),
        "legacy_pubcheck_is_scoped_as_supplementary": (
            legacy_pubcheck["status"] == "passed_supplementary"
            and legacy_pubcheck["exit_code"] == 0
            and "does not replace" in legacy_pubcheck["scope_note"]
        ),
        "upload_candidate_manifest_ready": (
            upload_candidate["status"] == "manuscript_only_candidate_ready"
            and upload_candidate["checks"]["archive_hash_matches_audit"]
            and upload_candidate["checks"]["archive_has_ten_entries"]
            and upload_candidate["checks"]["archive_entry_set_exact"]
            and upload_candidate["checks"]["archive_entry_hashes_match_current_sources"]
            and upload_candidate["checks"]["archive_paths_safe"]
            and upload_candidate["checks"]["readiness_audit_passed"]
            and upload_candidate["code_supplement_policy"] == "not included in the default upload candidate"
        ),
        "openreview_policy_check_recorded": (
            openreview_access["status"] == "public_group_reachable_form_details_source_verified"
            and "ORCID" in " ".join(openreview_access["observations"])
            and "48 hours" in " ".join(openreview_access["observations"])
        ),
        "numeric_consistency_audit_passed": (
            numeric_consistency["status"] == "passed"
            and not numeric_consistency["failed_checks"]
        ),
        "claim_evidence_audit_passed": (
            claim_evidence["status"] == "passed"
            and not claim_evidence["failed_checks"]
        ),
        "citation_audit_passed": (
            citation_audit["status"] == "passed"
            and not citation_audit["failed_checks"]
        ),
        "metadata_form_audit_passed": (
            metadata_audit["status"] == "passed"
            and not metadata_audit["failed_checks"]
        ),
        "readiness_checklist_tracks_remaining_human_gates": all(
            marker in checklist for marker in ("ACL Pubcheck", "licenses and citation requirements", "clean-environment help-only smoke test")
        ),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "artifact": "acl-arr-draft-readiness-audit-174",
        "status": "passed" if not failed else "failed",
        "mode": "ARR manuscript structure, scope, live-result sync, and build audit; no provider calls",
        "checks": checks,
        "failed_checks": failed,
        "pages": pages,
        "files": {
            "main_tex_sha256": sha256(ARR / "main.tex"),
            "appendix_tex_sha256": sha256(ARR / "appendix.tex"),
            "pdf_sha256": sha256(ARR / "main.pdf"),
        },
        "supplement_boundary": {
            "artifact": supplement_boundary["artifact"],
            "status": supplement_boundary["status"],
            "upstream_files_with_secret_patterns": len(supplement_boundary["upstream_code_secret_pattern_hits"]),
            "safe_candidate_secret_hits": supplement_boundary["safe_candidate_secret_hits"],
            "code_supplement_artifact": code_supplement["artifact"],
            "code_supplement_status": code_supplement["status"],
            "code_supplement_file_count": code_supplement["file_count"],
            "code_smoke_artifact": code_smoke["artifact"],
            "code_smoke_status": code_smoke["status"],
            "license_audit_artifact": license_audit["artifact"],
            "license_audit_status": license_audit["status"],
            "license_git_history_checked": "local_git_history_check" in license_audit,
            "manuscript_archive_artifact": manuscript_archive["artifact"],
            "manuscript_archive_status": manuscript_archive["status"],
            "manuscript_archive_sha256": manuscript_archive.get("archive_sha256"),
            "pubcheck_preflight_artifact": pubcheck_preflight["artifact"],
            "pubcheck_preflight_status": pubcheck_preflight["status"],
            "official_pubcheck_artifact": official_pubcheck["artifact"],
            "official_pubcheck_status": official_pubcheck["status"],
            "historical_official_pubcheck_artifact": historical_official_pubcheck["artifact"],
            "historical_official_pubcheck_status": historical_official_pubcheck["status"],
            "legacy_pubcheck_artifact": legacy_pubcheck["artifact"],
            "legacy_pubcheck_status": legacy_pubcheck["status"],
            "upload_candidate_artifact": upload_candidate["artifact"],
            "upload_candidate_status": upload_candidate["status"],
            "openreview_access_artifact": openreview_access["artifact"],
            "openreview_access_status": openreview_access["status"],
            "numeric_consistency_artifact": numeric_consistency["artifact"],
            "numeric_consistency_status": numeric_consistency["status"],
            "claim_evidence_artifact": claim_evidence["artifact"],
            "claim_evidence_status": claim_evidence["status"],
            "citation_audit_artifact": citation_audit["artifact"],
            "citation_audit_status": citation_audit["status"],
            "metadata_audit_artifact": metadata_audit["artifact"],
            "metadata_audit_status": metadata_audit["status"],
        },
        "known_remaining_human_gates": [
            "rerun official ACL Pubcheck only if the submitted PDF changes",
            "code-supplement license and redistribution permission",
            "author profiles, ORCID, conflicts, and service-contributor qualification",
        ],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "pages": pages, "failed_checks": failed}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
