# ICLR 2027 submission bundle manifest

Checked: 2026-10-01

## Review-facing source package

Include the following files when a source upload is required:

- `manuscript/main.tex`
- `manuscript/appendix.tex`
- `manuscript/math_commands.tex`
- `manuscript/iclr2027_conference.sty`
- `manuscript/iclr2027_conference.bst`
- `manuscript/fancyhdr.sty`
- `manuscript/natbib.sty`
- `manuscript/references.bib`
- `manuscript/figures/evolution-audit-main-results.pdf`
- `manuscript/figures/qwen-candidate-pool-enlargement.png`

The rendered review artifact is `manuscript/main.pdf` (17 pages: 8 main-text, 2 references, 7 appendix).

## Keep out of the review upload

Do not include API-connectivity logs, provider transcripts, raw console logs, environment/configuration files containing credential hooks, development drafts, temporary PDF renders, or any raw canary/trajectory material. The research directory is an audit workspace, not part of the anonymous paper upload.

The scientific provenance pointers retained in the appendix refer to artifacts 142--144, 149, 153, 158, and 161. Those artifacts remain local audit records and do not need to be uploaded with the anonymous submission unless the venue requests supplementary material.

## Pre-upload checks

From the project root:

```powershell
.venv\Scripts\python.exe research/experiments/verify_iclr_submission.py
.venv\Scripts\python.exe research/experiments/verify_iclr_paper_claims.py
.venv\Scripts\python.exe -m pytest research/tests -q
```

For a source-package smoke test, compile the copied bundle with `pdflatex`, `bibtex`, and two further `pdflatex` runs. The corrected 159 archive compiles independently to the same 16-page PDF with no undefined citations or references. The current checks pass, and a boundary-aware scan finds no `sk-...` or `rc-...` credential prefix in `research/` or `manuscript/`.

The isolated PDF and the workspace PDF have identical layout-extracted text and both contain 17 pages. Their binary hashes may differ because the PDFs are generated in different directories and runs.

The current archive was extracted into a fresh QA directory: all four compile commands returned zero, the PDF had 17 pages, the final log had no undefined citations or references, and its layout-extracted text matched the workspace PDF exactly.

The current review-facing source package is `research/manifests/iclr2027-submission-source-169.zip`. It contains exactly the 10 files listed above (235,713 bytes), preserving the required `figures/` directory structure; it excludes the rendered PDF, local audit artifacts, logs, provider traces, and configuration files. Earlier archives 146, 148, 151, 154, 155, 157, 159, 162, and 165 are superseded.

The listed anonymous source files contain no TODO/FIXME/TBD placeholders, stale `final-final` markers, API-key text, or reviewer-facing process notes. The only `Under review` string is the venue-template header.
