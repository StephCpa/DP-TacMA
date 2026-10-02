# Venue routing after the ICLR 2027 deadline check

Checked: 2 October 2026 against the official ARR and NAACL 2027 pages

## Current recommendation

If the paper was not uploaded to ICLR 2027 before its 25 September AOE deadline, the next live primary route is the **ACL Rolling Review October 2026 cycle**, with **NAACL 2027 as primary** and **COLING 2027 as secondary**. The paper is already written as an empirical audit of LLM-agent behavior, evaluation, reproducibility, and privacy premises, which is within the broad ARR/NAACL/COLING scope. This is a routing recommendation, not a claim that the current ICLR-format PDF can be submitted unchanged.

## Official dates to verify in the submission form

The official pages confirm the October 12 submission deadline and expose a calendar discrepancy that must not be silently merged: ARR lists reviewer registration on October 14, meta-reviews on December 17, and a December 20 venue commitment; the NAACL 2027 CFP lists all-author reviewer registration on October 12, meta-reviews on December 18, and a December 23 NAACL commitment. Use the NAACL dates as the conservative author/action deadlines and verify the live OpenReview form. Full evidence is in `research/artifacts/acl-arr-schedule-crosscheck-186.json`.

- ARR October 2026 submission: **12 October 2026**.
- ARR reviewer registration: **14 October 2026** on the ARR dates page; the NAACL CFP says **12 October 2026** for all authors.
- ARR reviews due: **16 November 2026**.
- ARR author response: **24--30 November 2026**.
- ARR meta-review release: **17 December 2026** on the ARR dates page; the NAACL CFP says **18 December 2026**.
- ARR venue commitment: **20 December 2026** on the ARR dates page; NAACL commitment: **23 December 2026** on the NAACL CFP.
- NAACL 2027 main notification: **10 February 2027**.

Dates and venue participation must be rechecked in OpenReview at upload time because ARR policies are being updated for the October 2026 cycle.

Official pages checked: [ARR dates](https://aclrollingreview.org/dates), [NAACL 2027 main-conference CFP](https://2027.naacl.org/calls/main_conference_papers/), and [ARR sustainable-reviewing policy](https://aclrollingreview.org/sustainable-reviewing-2026).

## Policy gates before upload

1. Confirm every author has an accurate OpenReview profile, ORCID, affiliation history, and required bibliographic links.
2. Identify the qualified service contributor/reviewer required by the October 2026 sustainable-reviewing policy, or obtain the applicable manual qualification decision.
3. Confirm the author list and conflicts before submission; do not rely on the ICLR metadata draft.
4. Convert the manuscript from the ICLR template to the current ACL ARR template and obey its page/format rules.
5. Retain the dedicated `Limitations` section. The canonical manuscript already contains `\section{Limitations}` before the conclusion and references.
6. Preserve the existing AI-use statement and add any ACL-required ethics/reproducibility wording without exposing identities.
7. Check dual-submission status. A paper already submitted to ICLR cannot be simultaneously submitted elsewhere while under review; if it was not submitted, make the ARR upload the single active submission.

## Scientific adaptation, not new experiments

The ARR version should keep the current evidence boundary:

- bounded failed-to-detect persistence result, not non-leakage;
- score-length intervention changes the score scale but does not establish utility improvement;
- fixed-pool headroom bound and Qwen support expansion;
- task-level response collapse on two selected failures;
- X2 as a bounded planning/component diagnostic, not a causal multi-agent claim;
- selector-level post-processing only, not end-to-end DP.

No additional provider calls are required before this venue decision. The verified anonymous source candidate remains `research/manifests/iclr2027-submission-source-169.zip`; a venue conversion should be made in a separate working copy only after the author chooses the route.

## Evidence

- Anonymous source and PDF readiness: `research/manifests/iclr2027-submission-source-169.zip` and `research/manifests/iclr2027-author-submission-checklist-171.md`.
- Numeric consistency: `research/artifacts/iclr2027-manuscript-numeric-consistency-audit-170.json`.
- Active evidence paths: `research/artifacts/iclr2027-active-evidence-path-audit-172.json`.
- Separate ARR draft readiness: `research/artifacts/acl-arr-draft-readiness-audit-174.json` (15-page PDF, live X2 result synchronized, no-provider checks passed).
- Anonymous supplement boundary: `manuscript-arr/submission/anonymous-supplement-boundary-175.md`, `research/artifacts/acl-arr-supplement-boundary-audit-175.json`, `research/artifacts/acl-arr-code-supplement-audit-176.json`, and `research/artifacts/acl-arr-code-supplement-smoke-177.json` (upstream checkout excluded; separate code candidate is scrubbed, syntax-audited, and smoke-tested; license review remains).
- License provenance: `manuscript-arr/submission/license-review-178.md` and `research/artifacts/acl-arr-license-audit-178.json` (no authoritative LICENSE text found; maintainer confirmation remains required).
- Manuscript-only source package: `research/manifests/acl-arr-october-manuscript-bundle-179.md`, `research/manifests/acl-arr-october-manuscript-source-179.zip`, and `research/artifacts/acl-arr-manuscript-archive-audit-179.json` (10 entries, independent 15-page compile verified).
- Local ACL preflight: `research/artifacts/acl-arr-pubcheck-preflight-180.json` (non-line-numbered proof passes local checks).
- Official ACL Pubcheck: `research/artifacts/acl-arr-official-pubcheck-194.json` (`All Clear!` on the non-line-numbered proof; source commit recorded). Historical network attempt: `research/artifacts/acl-arr-official-pubcheck-181.json`.
- Legacy supplementary check: `research/artifacts/acl-arr-legacy-pubcheck-183.json` (retained as historical supplementary evidence only).
- License confirmation draft: `manuscript-arr/submission/license-confirmation-request-182.md` (prepared for manual author/maintainer contact; not sent automatically).
- Upload handoff: `manuscript-arr/submission/arr-upload-handoff-184.md` (manuscript-only archive is the default candidate; code supplement remains opt-in after license clearance).
- Upload-candidate verification: `research/artifacts/acl-arr-upload-candidate-185.json` (archive hash, entry count, PDF presence, readiness state, and remaining human gates recorded).
- OpenReview access/policy check: `research/artifacts/acl-arr-openreview-access-187.json` (public group reachable; form availability, ORCID profile requirement, and 48-hour service-contributor rule recorded).
- ARR author-response preparation: `manuscript-arr/submission/arr-author-response-prep-188.md` (scope-safe responses for canary power, score intervention, Qwen support expansion, task-level collapse, X2 attribution, and non-end-to-end DP).
- ARR metadata draft: `manuscript-arr/submission/arr-metadata-draft-190.md` (title, synchronized abstract, keywords, routing preference, and author-only form fields; no identity-bearing values).
- Claim-evidence integrity audit: `research/artifacts/acl-arr-claim-evidence-audit-191.json` (claim matrix, artifact paths, citation-key equality, figure/table references, scope guards, and metadata synchronization).
- Citation audit: `research/artifacts/acl-arr-citation-audit-192.json` (27-entry BibTeX metadata completeness, key equality, context spot checks, and credential scan; existing citations only).
- Metadata form audit: `research/artifacts/acl-arr-metadata-audit-193.json` (title/abstract synchronization, five-keyword check, routing fields, placeholder-only author fields, and credential/path scan).
- Sequential submission-freeze runner: `research/artifacts/acl-arr-submission-freeze-196.json` (all no-provider audits and pytest executed in dependency order to avoid transient readiness/upload races).
- ARR numeric consistency: `research/artifacts/acl-arr-numeric-consistency-audit-189.json` (ARR main/appendix headline values checked against frozen artifacts).
- Canonical manuscript Limitations section: `manuscript/main.tex`.
