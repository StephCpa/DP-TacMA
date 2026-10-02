"""Aggregate existing no-call audits into one author handoff gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/artifacts/final-handoff-gate-226.json"


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def main() -> None:
    tests = load("research/artifacts/full-test-suite-225.json")
    iclr = load("research/artifacts/iclr2027-submission-integrity-audit-101.json")
    readiness = load("research/artifacts/iclr2027-main-conference-readiness-audit-167.json")
    reviewer = load("research/artifacts/iclr2027-reviewer-response-prep-audit-168.json")
    evidence = load("research/artifacts/iclr2027-active-evidence-path-audit-172.json")
    arr_numeric = load("research/artifacts/acl-arr-numeric-consistency-audit-189.json")
    arr_claims = load("research/artifacts/acl-arr-claim-evidence-audit-191.json")
    arr_ready = load("research/artifacts/acl-arr-draft-readiness-audit-174.json")
    cross = load("research/artifacts/cross-version-headline-consistency-audit-224.json")
    live_control = load("research/artifacts/iclr2027-live-control-integrity-audit-166.json")
    checks = {
        "tests_157_passed": tests["status"] == "passed" and tests["tests_passed"] == 157,
        "iclr_submission_integrity": iclr["status"] == "passed" and not iclr["failed_checks"],
        "iclr_main_readiness": readiness["status"] == "passed" and not readiness["failed_checks"],
        "reviewer_response": reviewer["status"] == "passed" and not reviewer["failed_checks"],
        "active_evidence_paths": evidence["status"] == "passed" and not evidence["failed_checks"],
        "arr_numeric_consistency": arr_numeric["status"] == "passed" and not arr_numeric["failed_checks"],
        "arr_claim_evidence": arr_claims["status"] == "passed" and not arr_claims["failed_checks"],
        "arr_draft_readiness": arr_ready["status"] == "passed" and not arr_ready["failed_checks"],
        "cross_version_consistency": cross["status"] == "passed" and not cross["failed_checks"],
        "live_control_consistency": live_control["status"] == "passed" and not live_control["failed_checks"],
    }
    result = {
        "artifact_id": "FINAL-HANDOFF-GATE-226",
        "date_local": "2026-10-02",
        "status": "passed" if all(checks.values()) else "failed",
        "provider_calls": 0,
        "checks": checks,
        "human_gates_open": [
            "confirm whether an ICLR upload exists before the deadline",
            "complete author profiles, ORCID, affiliations, and conflicts",
            "verify live ARR/NAACL OpenReview dates and service-contributor requirements",
            "obtain license or redistribution permission before adding the code supplement",
        ],
        "scope_guard": "This gate verifies packaging and evidence consistency; it is not a scientific acceptance prediction and does not authorize new provider calls.",
        "failed_checks": [name for name, passed in checks.items() if not passed],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact_id"], "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))
    if result["failed_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
