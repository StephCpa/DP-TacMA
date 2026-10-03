"""Build and independently verify the anonymous ARR manuscript source archive.

Workspace layout (as for the other ARR audits): ``manuscript-arr/`` holds the
sources and ``research/manifests``/``research/artifacts`` receive the archive
and its audit. The archive is deterministic (sorted entries, fixed timestamps),
is compiled from a fresh extraction with pdflatex/bibtex/pdflatex/pdflatex, and
its normalized text is compared with the workspace PDF. No provider calls.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARR = ROOT / "manuscript-arr"
ARCHIVE_ID = 230
ARCHIVE = ROOT / "research" / "manifests" / f"acl-arr-october-manuscript-source-{ARCHIVE_ID}.zip"
OUT = ROOT / "research" / "artifacts" / f"acl-arr-manuscript-archive-audit-{ARCHIVE_ID}.json"
EXPECTED_PAGES = 17
MAIN_BODY_PAGE_LIMIT = 8
ENTRIES = [
    "main.tex",
    "appendix.tex",
    "math_commands.tex",
    "references.bib",
    "acl.sty",
    "acl_natbib.bst",
    "figures/evolution-audit-main-results.pdf",
    "figures/qwen-candidate-pool-enlargement.pdf",
    "figures/failure-decomposition.pdf",
    "figures/make_main_figures.py",
]
FIXED_TIME = (2026, 10, 1, 0, 0, 0)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command: list[str], cwd: Path) -> int:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False).returncode


def pdf_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext", str(pdf), "-"], capture_output=True, text=True, check=True).stdout


def normalize(text: str) -> str:
    """Drop review line numbers and whitespace so layout-neutral text compares.

    Review-mode line numbers can land inline in extracted text, so every
    standalone 3-4 digit token is removed from both sides of the comparison.
    """

    return " ".join(token for token in text.split() if not re.fullmatch(r"\d{3,4}", token))


def page_count(pdf: Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"(?m)^Pages:\s+(\d+)", info).group(1))


def limitations_page(pdf: Path, pages: int) -> int | None:
    """First page whose text has a standalone Limitations heading."""

    for page in range(1, pages + 1):
        text = subprocess.run(
            ["pdftotext", "-f", str(page), "-l", str(page), str(pdf), "-"],
            capture_output=True, text=True, check=True,
        ).stdout
        if re.search(r"(?m)^(?:\d+\s+)?Limitations\s*$", text):
            return page
    return None


def build_archive() -> None:
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for name in sorted(ENTRIES):
            info = zipfile.ZipInfo(name, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, (ARR / name).read_bytes())


def main() -> None:
    missing = [name for name in ENTRIES if not (ARR / name).exists()]
    if missing:
        raise SystemExit(f"missing archive sources: {missing}")
    build_archive()
    with zipfile.ZipFile(ARCHIVE) as bundle:
        names = sorted(bundle.namelist())
        sources = "\n".join(
            bundle.read(name).decode("utf-8", errors="ignore") for name in names if name.endswith((".tex", ".bib", ".py"))
        )
    with tempfile.TemporaryDirectory(prefix="arr-archive-audit-") as temp:
        qa = Path(temp)
        with zipfile.ZipFile(ARCHIVE) as bundle:
            bundle.extractall(qa)
        codes = [
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], qa),
            run(["bibtex", "main"], qa),
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], qa),
            run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], qa),
        ]
        log_path = qa / "main.log"

        def read_log() -> str:
            return log_path.read_text(encoding="latin-1", errors="ignore") if log_path.exists() else ""

        # Review-mode line numbers (lineno) can need extra passes to settle; an
        # unsettled pass leaves numbers overlapping text at page bottoms.
        extra_passes = 0
        while extra_passes < 4 and re.search(r"(?i)re-?run to get|Rerun to get", read_log()):
            codes.append(run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"], qa))
            extra_passes += 1
        log = read_log()
        pdf = qa / "main.pdf"
        pages = page_count(pdf) if pdf.exists() else None
        limits_page = limitations_page(pdf, pages) if pages else None
        archive_text = normalize(pdf_text(pdf)) if pdf.exists() else ""
        workspace_pdf = ARR / "main.pdf"
        workspace_text = normalize(pdf_text(workspace_pdf))
        workspace_pages = page_count(workspace_pdf)
        outputs_distinct = pdf.resolve() != workspace_pdf.resolve()
    checks = {
        "entry_list_matches_manifest": names == sorted(ENTRIES),
        "compile_passes": all(code == 0 for code in codes) and len(codes) >= 4,
        "line_numbers_settled": not re.search(r"(?i)re-?run to get|Rerun to get", log),
        "expected_pages": pages == EXPECTED_PAGES and workspace_pages == EXPECTED_PAGES,
        "main_body_within_page_limit": limits_page is not None and limits_page <= MAIN_BODY_PAGE_LIMIT,
        "normalized_text_equal_to_workspace_pdf": archive_text == workspace_text and bool(archive_text),
        "no_undefined_references": "undefined references" not in log.lower() and "undefined citations" not in log.lower(),
        "no_overfull_boxes": "Overfull \\hbox" not in log and "Overfull \\vbox" not in log,
        "anonymous_author": "\\author{Anonymous ACL Submission}" in sources,
        "no_credential_prefixes": not re.search(r"(?i)(?:sk|rc)-[A-Za-z0-9_-]{12,}|AIza[0-9A-Za-z_-]{20,}|tvly-[A-Za-z0-9_-]{12,}", sources),
        "no_machine_paths": not re.search(r"\b[A-Z]:\\[A-Za-z]|/home/|/Users/", sources),
    }
    failed = sorted(name for name, passed in checks.items() if not passed)
    result = {
        "artifact": f"acl-arr-manuscript-archive-audit-{ARCHIVE_ID}",
        "status": "passed" if not failed else "failed",
        "mode": "deterministic ARR manuscript-only source archive with independent compile; no provider calls",
        "archive": str(ARCHIVE.relative_to(ROOT)).replace("\\", "/"),
        "archive_sha256": sha256(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "entry_count": len(names),
        "entries": names,
        "independent_compile": {
            "command_exit_codes": codes,
            "extra_pdflatex_passes": extra_passes,
            "pages": pages,
            "limitations_heading_page": limits_page,
            "normalized_text_equal": archive_text == workspace_text and bool(archive_text),
            "text_outputs_distinct": outputs_distinct,
        },
        "workspace_pdf_sha256": sha256(workspace_pdf),
        "workspace_pdf_pages": workspace_pages,
        "checks": checks,
        "failed_checks": failed,
        "supersedes": "acl-arr-october-manuscript-source-179.zip (15-page version)",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"artifact": result["artifact"], "status": result["status"], "pages": pages, "failed_checks": failed}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
