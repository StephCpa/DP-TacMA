# ICLR 2027 author-side submission checklist

Status: experiment and anonymous-source checks complete; ICLR 2027 submission status must be confirmed

## Official timing status

The official ICLR 2027 schedule lists the abstract deadline as 18 September 2026 AOE and the full-paper deadline as 25 September 2026 AOE. The author guidelines state that the deadlines are final and that late uploads or post-deadline paper edits are not accepted. As of the workspace date, 2 October 2026, this package is therefore a verified submission candidate, not evidence that a new ICLR 2027 main-conference upload is still possible.

- If this paper was submitted before the deadline: preserve the exact submitted PDF/source snapshot and use the package below for review-period preparation.
- If it was not submitted: do not attempt a late ICLR upload; select the next venue or a later ICLR cycle before making venue-specific changes.

The currently checked alternative route is recorded in `research/manifests/acl-arr-october-2026-routing-173.md`: ARR October 2026, NAACL 2027 primary, COLING 2027 secondary.

## Frozen upload candidate

- Source archive: `research/manifests/iclr2027-submission-source-169.zip`
- Source archive SHA-256: `4f7c7e7f12a616a0e85975573c6dd2cb226d9ac3615d61de1e20c88fa5974663`
- Rendered PDF: `manuscript/main.pdf`
- PDF SHA-256: `ac2561af3ba7eb29a6e6da99df50f8bea3bf824e352d34646f933b1ff02cf821`
- PDF length: 17 pages (8-page main body, 2 reference pages, 7 appendix pages)
- Source package: 10 anonymous files; no rendered PDF, provider logs, audit workspace, credentials, or author identities

## Author-only fields still to fill

Complete these in the venue form, not in the anonymous source archive:

- author names, order, affiliations, and corresponding author;
- OpenReview profile identifiers and conflict-of-interest entries;
- title-page metadata required by the submission form;
- any venue-specific ethics, data, code, or reproducibility declarations not already requested by the template.

The current metadata draft is `research/manifests/iclr2027-submission-metadata-147.md`; its `TBD by author` entries are intentional and are not manuscript placeholders.

## Claim and disclosure guardrails

- Describe the work as a bounded audit of privacy/utility premises in an evolving LLM runtime.
- Do not claim end-to-end differential privacy, a general leakage prevalence estimate, or causal multi-agent superiority.
- Keep the response-collapse result scoped to two selected hard failures.
- Keep the Qwen support result scoped to one benchmark and one model snapshot.
- Preserve the AI-use statement and anonymous author line in the uploaded source.

## Final local verification

From the project root, run:

```powershell
.venv\Scripts\python.exe research/experiments/verify_iclr_submission.py
.venv\Scripts\python.exe research/experiments/verify_iclr_paper_claims.py
.venv\Scripts\python.exe research/experiments/audit_manuscript_numeric_consistency.py
.venv\Scripts\python.exe -m pytest research/tests -q
```

The current local evidence is: submission-integrity audit passed, paper-claim audit passed, [numeric-consistency artifact 170](research/artifacts/iclr2027-manuscript-numeric-consistency-audit-170.json) passed, and the latest recorded full test run has 157 tests passed. No provider calls are needed for these checks.

## Review-period preparation if already submitted

The official schedule lists reviews and author-reviewer discussion for 5--18 November 2026, with final decisions on 16 December 2026. Keep the reviewer-response preparation file and evidence artifacts local until the venue's discussion interface requests a response.
