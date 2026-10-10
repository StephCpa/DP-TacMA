"""Build and verify the anonymous reproducibility supplement for the ARR paper.

The supplement holds our own scripts, frozen protocols, cached analyses, and the
replication summary; the upstream runtime and raw traces are excluded. Internal
file-name and identifier prefixes are stripped for anonymity without changing
any number. A fresh extraction must regenerate the review reanalysis (artifact
231) byte-for-byte and pass the bundled tests. No provider calls.

Run from this directory: ``python build_anonymous_supplement.py``.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # materials/
SUPPLEMENT_ID = 233
ARCHIVE = ROOT / "research" / "data" / f"acl-arr-anonymous-supplement-{SUPPLEMENT_ID}.zip"
AUDIT = ROOT / "research" / "data" / f"anonymous-supplement-audit-{SUPPLEMENT_ID}.json"
REFERENCE_REANALYSIS = ROOT / "research" / "data" / "review-response-reanalysis-231.json"
FIXED_TIME = (2026, 10, 1, 0, 0, 0)
PREFIXES = ("iclr2027-", "ICLR2027-")
CACHED = "research/data/cached-analysis/"
FILES = {
    "repro/reanalyze_review_items.py": "repro/reanalyze_review_items.py",
    "repro/direct_sampling_analysis.py": "repro/direct_sampling_analysis.py",
    "repro/post_arr_persistence_analysis.py": "repro/post_arr_persistence_analysis.py",
    "repro/test_post_arr_persistence_analysis.py": "repro/test_post_arr_persistence_analysis.py",
    "manuscript-arr/figures/make_main_figures.py": "figures/make_main_figures.py",
    CACHED + "iclr2027-x1-score-validity-037.json": CACHED + "x1-score-validity-037.json",
    CACHED + "cached-headroom-meta-analysis-protocol-080.json": CACHED + "cached-headroom-meta-analysis-protocol-080.json",
    CACHED + "iclr2027-cached-headroom-meta-analysis-081.json": CACHED + "cached-headroom-meta-analysis-081.json",
    CACHED + "qwen-candidate-pool-trajectory-reanalysis-protocol-087.json": CACHED + "qwen-candidate-pool-trajectory-reanalysis-protocol-087.json",
    CACHED + "iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json": CACHED + "qwen-candidate-pool-trajectory-reanalysis-088.json",
    "research/data/pre-submission-persistence-replication-result-223.json": "research/data/pre-submission-persistence-replication-result-223.json",
    "research/data/pre-submission-persistence-analysis-222.json": "research/data/pre-submission-persistence-analysis-222.json",
    "research/protocols/post-arr-persistence-replication-protocol-199.json": "research/protocols/post-arr-persistence-replication-protocol-199.json",
    "research/protocols/post-arr-persistence-runner-cohort-203.json": "research/protocols/post-arr-persistence-runner-cohort-203.json",
}
IDENTITY_PATTERN = re.compile(
    r"(?i)iclr|stephcpa|petlover|github\.com/[a-z]|[a-z0-9._-]+@[a-z0-9-]+\.[a-z]{2,}|\b[A-Z]:\\[A-Za-z]|/home/|/Users/|博士|dp-es"
)
README = """# Anonymous reproducibility supplement

Zero-call materials for "Before Candidate Selection in Test-Time LLM Agents".
Nothing here contacts a model provider.

## Regenerate the reported numbers

    cd repro
    python reanalyze_review_items.py          # writes research/data/review-response-reanalysis-231.json
    python test_post_arr_persistence_analysis.py

`reanalyze_review_items.py` reproduces, from the cached per-run and per-task rows:

- the Table 3 counts, the pooled row, and generation/selection failures with exact intervals;
- the round-candidate-only versus final-inclusive oracle check and the IMPOSSIBLE-reference sensitivity;
- parser acceptance rates and final-answer metric agreement;
- the per-task C1-C5 patterns and oracle intervals plotted in Figure 2;
- the score-source and score-observation counts of Figure 1c;
- the exact bound for the degenerate initial-ablation bootstrap and the canary denominators.

`figures/make_main_figures.py` redraws Figures 1-2 and the appendix figures (matplotlib).

## Contents

- `research/data/cached-analysis/`: cached zero-call analyses 037, 081, 088 and their protocols 080, 087.
- `research/data/`: the completed persistence replication summary (223) and analysis (222).
- `research/protocols/`: replication protocol 199 and its answer-free runner cohort 203.
- `repro/`: analysis, reanalysis, and test scripts.

## Not included

The upstream agent runtime (its license could not be confirmed), raw provider traces,
raw canary strings, and credentials. Live runs need a separate runtime checkout and
the frozen protocols. Internal project prefixes were removed from file names and
identifiers for anonymity; no number was changed.
"""


def sanitize(text: str) -> str:
    for prefix in PREFIXES:
        text = text.replace(prefix, "")
    return text


def build() -> dict[str, str]:
    payloads: dict[str, bytes] = {"README.md": README.encode("utf-8")}
    for source, target in FILES.items():
        payloads[target] = sanitize((ROOT / source).read_text(encoding="utf-8")).encode("utf-8")
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(payloads):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, payloads[name])
    return {name: hashlib.sha256(data).hexdigest() for name, data in payloads.items()}


def verify() -> dict:
    with tempfile.TemporaryDirectory(prefix="anon-supplement-") as temp:
        root = Path(temp)
        with zipfile.ZipFile(ARCHIVE) as bundle:
            names = sorted(bundle.namelist())
            identity_hits = sorted(
                name for name in names if IDENTITY_PATTERN.search(bundle.read(name).decode("utf-8", errors="ignore") + name)
            )
            bundle.extractall(root)
        reanalysis = subprocess.run([sys.executable, "reanalyze_review_items.py"], cwd=root / "repro", capture_output=True, text=True)
        tests = subprocess.run([sys.executable, "test_post_arr_persistence_analysis.py"], cwd=root / "repro", capture_output=True, text=True)
        produced = root / "research" / "data" / "review-response-reanalysis-231.json"
        regenerated = produced.exists() and json.loads(produced.read_text(encoding="utf-8")) == json.loads(
            sanitize(REFERENCE_REANALYSIS.read_text(encoding="utf-8"))
        )
    return {
        "entries": names,
        "identity_hits": identity_hits,
        "reanalysis_exit_code": reanalysis.returncode,
        "reanalysis_regenerates_artifact_231": regenerated,
        "tests_exit_code": tests.returncode,
    }


def main() -> None:
    hashes = build()
    result = verify()
    checks = {
        "no_identity_or_path_strings": not result["identity_hits"],
        "reanalysis_runs": result["reanalysis_exit_code"] == 0,
        "reanalysis_regenerates_artifact_231": result["reanalysis_regenerates_artifact_231"],
        "bundled_tests_pass": result["tests_exit_code"] == 0,
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    audit = {
        "artifact": f"anonymous-supplement-audit-{SUPPLEMENT_ID}",
        "status": "passed" if not failed else "failed",
        "mode": "deterministic anonymous supplement with fresh-extraction regeneration; no provider calls",
        "archive": ARCHIVE.name,
        "archive_sha256": hashlib.sha256(ARCHIVE.read_bytes()).hexdigest(),
        "entry_sha256": hashes,
        "checks": checks,
        "failed_checks": failed,
        **{k: v for k, v in result.items() if k != "entries"},
    }
    AUDIT.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": audit["artifact"], "status": audit["status"], "failed_checks": failed}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
