"""Validate the internal reviewer-response sheet against local evidence paths."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "research" / "iclr2027-main-conference-reviewer-response-prep.md"
OUT = ROOT / "research" / "artifacts" / "iclr2027-reviewer-response-prep-audit-168.json"


def main() -> None:
    text = DOC.read_text(encoding="utf-8")
    evidence_paths = []
    for token in re.findall(r"`([^`]+)`", text):
        if token.startswith(("research/", "manuscript/")):
            evidence_paths.append(token.split(":", 1)[0])
    unique_paths = sorted(set(evidence_paths))
    missing = [path for path in unique_paths if not (ROOT / path).exists()]
    checks = {
        "document_exists": DOC.exists(),
        "all_evidence_paths_exist": not missing,
        "all_required_questions_present": all(
            heading in text
            for heading in [
                "Why is this an ICLR paper",
                "Does zero observed canary exposure prove that",
                "What exactly is causal about",
                "Does the Qwen result show that",
                "task-level response collapse",
                "Does the live X2 ablation show that",
                "Why not build an end-to-end private",
                "What is the strongest reproducibility evidence",
            ]
        ),
        "red_lines_present": all(
            phrase in text
            for phrase in [
                "system does not leak",
                "Response collapse is a general LLM phenomenon",
                "Multi-agent evolution improves utility",
                "LLM contributes nothing to X2",
                "paper provides private TacoMAS",
            ]
        ),
        "no_credential_prefix": not re.search(r"(?:sk|rc)-[A-Za-z0-9._-]{12,}", text),
        "upstream_integrity_audits_passed": (
            json.loads((ROOT / "research/artifacts/iclr2027-live-control-integrity-audit-166.json").read_text(encoding="utf-8"))["status"] == "passed"
            and json.loads((ROOT / "research/artifacts/iclr2027-main-conference-readiness-audit-167.json").read_text(encoding="utf-8"))["status"] == "passed"
        ),
    }
    failed = [name for name, value in checks.items() if not value]
    result = {
        "artifact": "iclr2027-reviewer-response-prep-audit-168",
        "status": "passed" if not failed else "failed",
        "mode": "internal evidence-link and scope audit; no provider calls",
        "document": str(DOC.relative_to(ROOT)).replace("\\", "/"),
        "evidence_paths": unique_paths,
        "missing_paths": missing,
        "checks": checks,
        "failed_checks": failed,
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "failed_checks": failed}, ensure_ascii=False))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
