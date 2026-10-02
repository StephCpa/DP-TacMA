"""No-provider reviewer-style claim/evidence audit for the ICLR manuscript."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "research" / "artifacts"
OUT = ART / "iclr2027-main-conference-readiness-audit-167.json"


def load(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def first_line(text: str, needle: str) -> int | None:
    for number, line in enumerate(text.splitlines(), 1):
        if needle in line:
            return number
    return None


def main() -> None:
    main_tex = (ROOT / "manuscript" / "main.tex").read_text(encoding="utf-8")
    appendix_tex = (ROOT / "manuscript" / "appendix.tex").read_text(encoding="utf-8")
    live = load("research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json")
    live_integrity = load("research/artifacts/iclr2027-live-control-integrity-audit-166.json")
    readiness = load("research/artifacts/iclr2027-submission-readiness-145.json")
    pdfinfo = subprocess.run(["pdfinfo", str(ROOT / "manuscript" / "main.pdf")], check=True, capture_output=True).stdout.decode("ascii", errors="ignore")
    total_pages = int(re.search(r"(?m)^Pages:\s+(\d+)", pdfinfo).group(1))

    claims = [
        {
            "claim": "Persistent canary exposure was not detected under the preregistered five-round setting.",
            "evidence": ["research/artifacts/iclr2027-x1-operational-events-034.json", "research/artifacts/pre-submission-persistence-replication-result-223.json", "manuscript/main.tex:22,101"],
            "status": "supported_bounded",
            "risk": "medium",
            "risk_reason": "120 evolve instances in the completed replication, one model/runtime, fixed topology; the manuscript explicitly avoids a non-leakage claim.",
        },
        {
            "claim": "The released score scale is causally dominated by output length, but length removal is not a validated utility improvement.",
            "evidence": ["research/artifacts/iclr2027-qwen-cross-model-length-decision-075.json", "manuscript/main.tex:124"],
            "status": "supported",
            "risk": "low",
            "risk_reason": "Prospective interventions span DeepSeek and Qwen; utility directions are reported without being promoted.",
        },
        {
            "claim": "Recorded candidate pools impose a small selector headroom bound.",
            "evidence": ["research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json", "manuscript/main.tex:131-151"],
            "status": "supported_bounded",
            "risk": "medium",
            "risk_reason": "The bound applies only to persisted candidates and binary executable utility.",
        },
        {
            "claim": "Independent trajectories enlarge task-relevant support and raise the executable oracle from 0.60 to 0.80 at roughly 3x token cost.",
            "evidence": ["research/artifacts/iclr2027-qwen-candidate-pool-enlargement-decision-085.json", "research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json", "manuscript/main.tex:154-170"],
            "status": "supported_bounded",
            "risk": "medium",
            "risk_reason": "20 tasks and one benchmark; the nested design is not a sign-symmetric treatment test and does not identify a multi-agent architectural effect.",
        },
        {
            "claim": "Direct stochastic generation can collapse onto one invalid endpoint with or without repair conditioning on two selected hard failures.",
            "evidence": ["research/artifacts/iclr2027-deepseek-compute-matched-generation-gate-analysis-092.json", "research/artifacts/iclr2027-deepseek-unconditioned-collapse-analysis-098.json", "manuscript/main.tex:176-188"],
            "status": "supported_bounded",
            "risk": "high",
            "risk_reason": "Two selected tasks are mechanism evidence, not a prevalence estimate; the manuscript states this scope.",
        },
        {
            "claim": "Selector-level DP becomes non-vacuous after support expansion, but the work does not provide end-to-end DP.",
            "evidence": ["research/artifacts/iclr2027-signal-selector-notation-correction-100.json", "manuscript/main.tex:190-197,227"],
            "status": "supported_narrow",
            "risk": "high",
            "risk_reason": "Only selected-index/output release is protected under a narrow adjacency; memories, messages, prompts, topology, and stopping remain trusted.",
        },
        {
            "claim": "Removing bounded symbolic pre-checks and distance filtering reduces held-out executable coverage in a live DeepSeek component ablation.",
            "evidence": ["research/artifacts/iclr2027-x2-heldout-unfiltered-llm-control-152.json", "research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json", "research/artifacts/iclr2027-live-control-integrity-audit-166.json", "manuscript/main.tex:221", "manuscript/appendix.tex:229"],
            "status": "supported_bounded",
            "risk": "medium",
            "risk_reason": "Fixed 18-task cohort, one model and one benchmark; the protocol retains local state verification and is explicitly not an architecture-level causal estimate.",
        },
    ]

    reviewer_risks = [
        {
            "priority": "P1",
            "risk": "The paper may be judged as an audit of premises rather than a new DP method.",
            "evidence": "main.tex:29-39,190-197,227",
            "mitigation_already_present": "The paper makes the premise-audit question explicit and labels the DP result selector-level.",
            "remaining_action": "Do not claim end-to-end privacy or a new private architecture; emphasize the phenomenon-to-remedy-to-escape arc.",
            "api_needed": False,
        },
        {
            "priority": "P1",
            "risk": "The two-task response-collapse mechanism could be overgeneralized.",
            "evidence": "main.tex:182-188,225; appendix.tex:208",
            "mitigation_already_present": "The term is scoped to selected hard failures and the public-only control reverses the initial explanation.",
            "remaining_action": "Keep the scope word in abstract, contributions, Results, and limitations; no additional calls are required for the current claim.",
            "api_needed": False,
        },
        {
            "priority": "P2",
            "risk": "X2 can distract from the privacy audit because it is one benchmark and exploratory.",
            "evidence": "main.tex:221,223; appendix.tex:212-229",
            "mitigation_already_present": "X2 is framed as a planning diagnostic and the live component result is bounded.",
            "remaining_action": "Keep X2 in the current compact paragraph and appendix; do not promote it to a headline architecture result.",
            "api_needed": False,
        },
        {
            "priority": "P2",
            "risk": "Reviewers may ask why no end-to-end private agent was built.",
            "evidence": "main.tex:197,213,227; appendix.tex:231",
            "mitigation_already_present": "The manuscript explains that the audited premises fail or are weak before end-to-end calibration is meaningful.",
            "remaining_action": "Treat end-to-end DP as a scope boundary and future architecture, not as a missing baseline to be silently implied.",
            "api_needed": False,
        },
    ]

    checks = {
        "main_body_page_budget": total_pages == 17 and readiness["manuscript"]["main_text_pages"] == 8,
        "all_claims_have_evidence": all(item["evidence"] for item in claims),
        "live_control_integrity_passed": live_integrity["status"] == "passed" and not live_integrity["failed_checks"],
        "live_control_numbers": live["paired_feasible"]["replay"]["live_true"] == 8 and live["paired_feasible"]["exact"]["live_true"] == 5,
        "scope_language_present": all(phrase in main_tex for phrase in ["not a causal multi-agent advantage", "does not provide end-to-end DP", "not confirmatory comparisons"]),
        "abstract_contains_bounded_collapse": "two selected hard failures" in main_tex.split("\\begin{document}", 1)[1].split("\\section", 1)[0],
    }
    failed = [name for name, value in checks.items() if not value]
    result = {
        "artifact": "iclr2027-main-conference-readiness-audit-167",
        "status": "passed" if not failed else "failed",
        "mode": "reviewer-style claim/evidence/scope audit; no provider calls",
        "venue_assumption": "ICLR 2027 main conference, 8-page main body with references and appendix outside the main-body count",
        "checks": checks,
        "failed_checks": failed,
        "claim_evidence_matrix": claims,
        "reviewer_risks": reviewer_risks,
        "verdict": {
            "scientific_position": "Defensible as a bounded empirical audit of privacy-utility premises with a phenomenon-remedy-escape arc.",
            "largest_risk": "Reviewers may require an end-to-end private evolving-agent system or may treat the two-task collapse result as overgeneralized.",
            "recommended_action": "Freeze the empirical claim set and perform final venue/reviewer response preparation; no additional provider calls are required for the current claims.",
        },
        "line_anchors": {
            "abstract": first_line(main_tex, "A stopped DeepSeek repair gate"),
            "main_x2": first_line(main_tex, "An exploratory X2 diagnostic"),
            "appendix_live_x2": first_line(appendix_tex, "The unfiltered DeepSeek control"),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "failed_checks": failed}, ensure_ascii=False))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
