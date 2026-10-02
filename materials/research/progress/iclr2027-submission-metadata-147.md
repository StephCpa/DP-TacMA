# ICLR 2027 submission metadata draft

Status: author review required

## Title

Before Privatizing Evolution: Is There Enough Utility to Select?

## Author fields

- Authors: `TBD by author`
- OpenReview profiles: `TBD by author`
- Corresponding author: `TBD by author`
- Conflict-of-interest entries: `TBD by author`

## Keywords

Differential privacy; LLM agents; multi-agent systems; test-time compute; candidate selection; privacy auditing; PlanCraft.

## Scope statement for the form

This work audits when private selection in test-time evolving LLM systems can be consequential. It measures persistent-state exposure, score validity, realized candidate-pool headroom, independent-trajectory support expansion, and direct response concentration. The paper does not claim end-to-end differential privacy or general multi-agent superiority.

## Evidence anchors

- Persistent canary exposure: 0/120 in the completed three-arm replication (with the earlier 0/20 study retained as historical context), reported as a bounded failed-to-detect result.
- Length intervention: score scale changes strongly, but executable exactness does not improve reliably across the frozen cohorts.
- Fixed-pool headroom: 0--8.3 percentage points across the audited cohorts.
- Independent support expansion: Qwen (C_5-C_1) adds 1.00 canonical plan per task on average and raises executable-oracle accuracy from 0.60 to 0.80 at approximately three times the token cost.
- Direct repair diagnostic: task-level response collapse is observed on two selected hard failures, with the same-task public-only control reversing the initial conditioning explanation.

## Upload checks

- Use the anonymous source bundle in `research/manifests/iclr2027-submission-bundle-146.md`.
- Keep author names, affiliations, and OpenReview identities out of the anonymous source until the venue workflow requests them.
- Re-run `verify_iclr_submission.py`, `verify_iclr_paper_claims.py`, and the test suite after any author-side source edit.
