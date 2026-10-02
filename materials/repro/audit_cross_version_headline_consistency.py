"""Zero-call consistency audit across the ICLR and ARR submission snapshots."""

from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research/artifacts/cross-version-headline-consistency-audit-224.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    iclr = (ROOT / "manuscript/main.tex").read_text(encoding="utf-8")
    iclr_appendix = (ROOT / "manuscript/appendix.tex").read_text(encoding="utf-8")
    arr = (ROOT / "manuscript-arr/main.tex").read_text(encoding="utf-8")
    arr_appendix = (ROOT / "manuscript-arr/appendix.tex").read_text(encoding="utf-8")
    reviewer = (ROOT / "research/iclr2027-main-conference-reviewer-response-prep.md").read_text(encoding="utf-8")
    metadata = (ROOT / "research/manifests/iclr2027-submission-metadata-147.md").read_text(encoding="utf-8")
    required_current = {
        "iclr_main_replication": "0/120",
        "iclr_main_bound": "2.5\\%",
        "arr_main_replication": "0/120",
        "arr_main_bound": "2.5\\%",
        "reviewer_replication": "120 evolve instances",
        "metadata_replication": "0/120",
    }
    forbidden_headline = {
        "iclr_abstract_old_bound": "upper bound of 13.9\\%",
        "arr_abstract_old_bound": "upper bound of 13.9\\%",
        "reviewer_old_current_claim": "With zero events in 20 evolve instances, the one-sided 95% upper bound remains 13.9%.",
        "metadata_old_current_claim": "Persistent canary exposure: 0/20 in the preregistered three-arm study",
    }
    checks = {
        key: value in {
            "iclr_main_replication": iclr,
            "iclr_main_bound": iclr,
            "arr_main_replication": arr,
            "arr_main_bound": arr,
            "reviewer_replication": reviewer,
            "metadata_replication": metadata,
        }[key]
        for key, value in required_current.items()
    }
    checks.update({key: value not in {"iclr_abstract_old_bound": iclr, "arr_abstract_old_bound": arr, "reviewer_old_current_claim": reviewer, "metadata_old_current_claim": metadata}[key] for key, value in forbidden_headline.items()})
    archive = ROOT / "research/manifests/iclr2027-submission-source-169.zip"
    with zipfile.ZipFile(archive) as z:
        names = set(z.namelist())
        archive_bytes_match = all(
            z.read(name) == (ROOT / "manuscript" / name).read_bytes()
            for name in names
            if not name.endswith("/")
        )
    checks["archive_has_exactly_10_entries"] = len(names) == 10
    checks["archive_entry_bytes_match_current_sources"] = archive_bytes_match
    checks["iclr_pdf_exists"] = (ROOT / "manuscript/main.pdf").exists()
    checks["arr_pdf_exists"] = (ROOT / "manuscript-arr/main.pdf").exists()
    result = {
        "artifact_id": "CROSS-VERSION-HEADLINE-CONSISTENCY-224",
        "status": "passed" if all(checks.values()) else "failed",
        "model_calls": 0,
        "checks": checks,
        "iclr_main_sha256": sha256(ROOT / "manuscript/main.tex"),
        "arr_main_sha256": sha256(ROOT / "manuscript-arr/main.tex"),
        "source_archive_sha256": sha256(archive),
        "source_archive_entries": sorted(names),
        "interpretation": "Cross-version text and anonymous-source consistency only; this audit does not establish new scientific evidence.",
        "failed_checks": [key for key, passed in checks.items() if not passed],
    }
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact_id"], "status": result["status"], "failed_checks": result["failed_checks"]}, ensure_ascii=False))
    if result["failed_checks"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
