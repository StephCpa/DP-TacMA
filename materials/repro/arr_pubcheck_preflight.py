"""Run a local ACL-style preflight on a non-line-numbered ARR proof."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
ARCHIVE = ROOT / "research" / "manifests" / "acl-arr-october-manuscript-source-179.zip"
OUT = ROOT / "research" / "artifacts" / "acl-arr-pubcheck-preflight-180.json"


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="arr-pubcheck-preflight-") as temp:
        qa = Path(temp)
        with zipfile.ZipFile(ARCHIVE) as bundle:
            bundle.extractall(qa)
        main_tex = qa / "main.tex"
        source = main_tex.read_text(encoding="utf-8")
        source = source.replace("\\usepackage[review]{acl}", "\\usepackage{acl}", 1)
        main_tex.write_text(source, encoding="utf-8")
        commands = [
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ["bibtex", "main"],
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ]
        results = [run(command, qa) for command in commands]
        codes = [result.returncode for result in results]
        log_path = qa / "main.log"
        log = log_path.read_text(encoding="latin-1", errors="ignore") if log_path.exists() else ""
        pdf = qa / "main.pdf"
        pdfinfo = run(["pdfinfo", os.fspath(pdf)], qa) if pdf.exists() else None
        pdfinfo_text = pdfinfo.stdout if pdfinfo else ""
        page_match = re.search(r"(?m)^Pages:\s+(\d+)", pdfinfo_text)
        pages = int(page_match.group(1)) if page_match else None
        fonts = run(["pdffonts", os.fspath(pdf)], qa).stdout if pdf.exists() else ""
        checks = {
            "non_line_numbered_source": "\\usepackage[review]{acl}" not in source and "\\usepackage{acl}" in source,
            "compile_passes": codes == [0, 0, 0, 0],
            "expected_pages": pages == 15,
            "no_overfull_boxes": "Overfull \\hbox" not in log and "Overfull \\vbox" not in log,
            "no_undefined_references": "undefined references" not in log.lower() and "undefined citations" not in log.lower(),
            "no_type3_fonts": "Type 3" not in fonts,
            "anonymous_author_text_present": "Anonymous ACL Submission" in source,
            "blank_pdf_author_metadata": re.search(r"(?m)^Author:\s*$", pdfinfo_text) is not None,
            "no_credential_prefixes": not any(re.search(pattern, source) for pattern in (r"(?i)(?:sk|rc)-[A-Za-z0-9_-]{12,}", r"(?i)AIza[0-9A-Za-z_-]{20,}", r"(?i)tvly-[A-Za-z0-9_-]{12,}")),
            "no_machine_paths": not re.search(r"(?i)[A-Z]:\\\\|/home/|/Users/", source),
        }
        failed = sorted(name for name, passed in checks.items() if not passed)
        proof_sha = hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None
        result = {
            "artifact": "acl-arr-pubcheck-preflight-180",
            "status": "passed" if not failed else "failed",
            "mode": "local non-line-numbered ACL preflight; not the official ACL Pubcheck tool; no provider calls",
            "source_archive": "research/manifests/acl-arr-october-manuscript-source-179.zip",
            "proof_pdf_sha256": proof_sha,
            "pages": pages,
            "command_exit_codes": codes,
            "checks": checks,
            "failed_checks": failed,
            "official_pubcheck": "not_available_in_environment",
            "next_action": "Run the official ACL Pubcheck tool when available, then complete venue-form and license gates.",
        }
        OUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"artifact": result["artifact"], "status": result["status"], "pages": pages, "failed_checks": failed}))
        if failed:
            raise SystemExit(1)


if __name__ == "__main__":
    main()
