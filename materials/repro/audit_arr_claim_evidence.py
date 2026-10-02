"""No-provider claim/evidence and citation integrity audit for the ARR draft."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "research" / "artifacts"
OUT = ART / "acl-arr-claim-evidence-audit-191.json"


def load(name: str) -> dict:
    return json.loads((ART / name).read_text(encoding="utf-8"))


def main() -> None:
    main_tex = (ROOT / "manuscript-arr" / "main.tex").read_text(encoding="utf-8")
    appendix_tex = (ROOT / "manuscript-arr" / "appendix.tex").read_text(encoding="utf-8")
    metadata = (ROOT / "manuscript-arr" / "submission" / "arr-metadata-draft-190.md").read_text(encoding="utf-8")
    bib = (ROOT / "manuscript-arr" / "references.bib").read_text(encoding="utf-8")

    g1 = load("iclr2027-x1-g1-decision-036.json")
    replication = load("pre-submission-persistence-replication-result-223.json")
    extractor = load("iclr2027-x1-extractor-positive-control-064.json")
    mutation = load("iclr2027-x1-state-mutation-065.json")
    headroom = load("iclr2027-cached-headroom-meta-analysis-081.json")
    numeric = load("acl-arr-numeric-consistency-audit-189.json")
    collapse = load("iclr2027-deepseek-unconditioned-collapse-analysis-098.json")
    live_x2 = load("iclr2027-x2-unfiltered-llm-control-analysis-164.json")

    cited_groups = re.findall(r"\\citep?\{([^}]+)\}", main_tex + appendix_tex)
    cited = sorted({key.strip() for group in cited_groups for key in group.split(",")})
    bib_keys = sorted(re.findall(r"@\w+\{([^,]+),", bib))
    labels = set(re.findall(r"\\label\{([^}]+)\}", main_tex + appendix_tex))
    refs = set(re.findall(r"\\ref\{([^}]+)\}", main_tex + appendix_tex))

    abstract_main = re.search(r"(?s)\\begin\{abstract\}\s*(.*?)\s*\\end\{abstract\}", main_tex).group(1).strip()
    abstract_metadata = re.search(r"(?s)## Abstract\s*\r?\n\r?\n(.*?)\s*\r?\n\r?\n## Keywords", metadata).group(1).strip()

    claims = [
        {
            "claim": "The completed canary replication detects no post-input exposure in 120 instances.",
            "status": "supported",
            "scope": "failed-to-detect result for the audited model, benchmark, canary family, five-round horizon, and fixed topology; not a prevalence or privacy guarantee",
            "evidence": ["research/artifacts/pre-submission-persistence-replication-result-223.json", "research/artifacts/post-arr-raw-canary-hygiene-audit-216.json"],
        },
        {
            "claim": "The runtime is instrumented and observably mutates state despite the exposure null.",
            "status": "supported",
            "scope": "observable mutation proxies; not byte-level full-state edit distance",
            "evidence": ["research/artifacts/iclr2027-x1-state-mutation-065.json", "research/artifacts/iclr2027-x1-extractor-positive-control-064.json"],
        },
        {
            "claim": "Removing the length term changes the released score scale without a consistent exactness gain.",
            "status": "supported",
            "scope": "frozen DeepSeek and Qwen interventions; utility result is not a general scorer-validity theorem",
            "evidence": ["research/artifacts/iclr2027-qwen-cross-model-length-decision-075.json", "research/artifacts/acl-arr-numeric-consistency-audit-189.json"],
        },
        {
            "claim": "Selectors restricted to recorded candidates have at most 0--8.3 percentage points of observed headroom.",
            "status": "supported",
            "scope": "realized-pool upper bound across four frozen cohorts; not a population generalization bound",
            "evidence": ["research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json", "research/artifacts/acl-arr-numeric-consistency-audit-189.json"],
        },
        {
            "claim": "Five independent Qwen trajectories raise executable-oracle accuracy from 0.60 to 0.80 at higher token cost.",
            "status": "supported",
            "scope": "same three-agent runtime and one PlanCraft benchmark; not a causal multi-agent advantage",
            "evidence": ["research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json", "research/artifacts/acl-arr-numeric-consistency-audit-189.json"],
        },
        {
            "claim": "Two selected hard failures show task-level response collapse under both repair-conditioned and public-only prompts.",
            "status": "supported",
            "scope": "two selected hard failures; task-level diagnostic rather than a general decoding prevalence claim",
            "evidence": ["research/artifacts/iclr2027-deepseek-unconditioned-collapse-analysis-098.json", "research/artifacts/acl-arr-numeric-consistency-audit-189.json"],
        },
        {
            "claim": "The live X2 result is a component attribution and not an architecture-level causal multi-agent result.",
            "status": "supported",
            "scope": "fixed held-out PlanCraft cohort; symbolic control and live component comparison",
            "evidence": ["research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json", "research/artifacts/acl-arr-numeric-consistency-audit-189.json"],
        },
    ]

    evidence_paths = sorted({path for claim in claims for path in claim["evidence"]})
    checks = {
        "claim_evidence_paths_exist": all((ROOT / path).exists() for path in evidence_paths),
        "numeric_consistency_audit_passed": numeric["status"] == "passed" and not numeric["failed_checks"],
        "g1_counts_match_claim": (
            replication["complete_cells"] == 360
            and replication["complete_instance_triads"] == 120
            and replication["exposure"]["evolve_exact_or_partial"] == "0/120"
            and replication["exposure"]["depth_matched_reset_exact_or_partial"] == "0/120"
            and replication["exposure"]["no_canary_false_positive"] == "0/120"
            and "120 instances" in main_tex
            and r"2.5\%" in main_tex
        ),
        "instrumentation_claim_matches_controls": (
            extractor["recovered_path_count"] == 7
            and extractor["passed"] is True
            and mutation["overall"]["changed_agent_transitions"] == 617
            and mutation["overall"]["comparable_agent_transitions"] == 720
            and mutation["overall"]["nonempty_feedback_fields"] == 168
            and mutation["overall"]["retention_fire_rounds"] == 60
            and all(token in main_tex for token in ("7/7", "617/720", "168", "60/300"))
        ),
        "headroom_scope_matches_artifact": (
            headroom["exploratory_cross_cohort_selector_headroom"]["cohorts"]["deepseek_nondegenerate"]["headroom"] == 1 / 12
            and "0--8.3 percentage points" in main_tex
            and "not a confidence statement about all future tasks" in main_tex
        ),
        "collapse_scope_matches_artifact": (
            collapse["source_provider_calls"] == 160
            and "Use task-level response collapse" in collapse["nomenclature_decision"]
            and "two selected hard failures" in main_tex
        ),
        "x2_scope_matches_artifact": (
            live_x2["live_run"]["summary"]["feasible_replay_valid"] == 8
            and live_x2["live_run"]["summary"]["feasible_canonical_exact"] == 5
            and "not a causal multi-agent advantage" in main_tex
        ),
        "citations_equal_bibliography": cited == bib_keys,
        "all_figure_and_table_refs_resolve": refs <= labels,
        "metadata_abstract_synchronized": abstract_main == abstract_metadata,
        "scope_guards_present": (
            all(
                phrase in main_tex
                for phrase in (
                    "do not provide end-to-end privacy",
                    "does not provide end-to-end DP",
                    "not a causal multi-agent advantage",
                )
            )
            and ("not a general prevalence estimate" in main_tex or "or a general prevalence estimate" in main_tex)
        ),
        "retracted_terminology_absent": "conditional response collapse" not in (main_tex + appendix_tex).lower(),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "artifact": "acl-arr-claim-evidence-audit-191",
        "status": "passed" if not failed else "failed",
        "mode": "CCF integrity claim-evidence, numeric, citation, reference, and scope audit; no provider calls",
        "claims": claims,
        "checks": checks,
        "failed_checks": failed,
        "citation_counts": {"cited_keys": len(cited), "bib_keys": len(bib_keys)},
        "figure_table_counts": {"refs": len(refs), "labels": len(labels)},
        "no_invention_status": "Every claim is paired with an existing local artifact; unsupported generalization is marked in scope fields.",
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "failed_checks": failed}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
