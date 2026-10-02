# DP-TacMA research handoff

Updated: 2026-10-02 (Asia/Shanghai)

## Verified state

- The completed persistence replication contains 360/360 cells: 120 evolve, 120 depth-matched reset, and 120 no-canary controls. Exposure is 0/120 in the two canary arms and false positives are 0/120 in the no-canary arm. The evolve-arm one-sided 95% upper bound is 2.5%.
- The Qwen independent-trajectory study is complete on 20 untouched tasks and has a zero-call corrected reanalysis. The matched 16-slot cross-trajectory oracle is 0.626 versus 0.570 within one stochastic trajectory; this is a coverage allocation result, not a multi-agent causal estimate.
- ICLR and ARR manuscripts, anonymous source archive, metadata, reviewer-response sheet, and bundle manifest are synchronized. The ICLR PDF is 17 pages (8-page main body, 2 reference pages, 7 appendix pages).
- The reproducibility test suite passes 157/157 tests with third-party plugin autoload disabled.

## Frozen evidence boundaries

- No end-to-end DP claim: only the narrow selector-level release is analyzed.
- No general leakage-prevalence claim: the canary result is bounded to the audited model, injection route, horizon, topology, and canary family.
- No causal multi-agent-superiority claim: the Qwen result compares independent trajectory allocation within the same three-agent runtime.
- No prevalence claim for response collapse: the control covers two selected hard failures.

## Author actions remaining

1. Confirm whether an ICLR 2027 upload was made before the official deadline; do not attempt a late upload.
2. Fill author names, OpenReview profiles, affiliations, and conflicts in the venue form, not in the anonymous source archive.
3. Choose the active venue route (ICLR review-period preparation if already submitted; otherwise ARR/NAACL/COLING routing).
4. Decide whether to send the prepared TacoMAS score-formula correspondence as a human author.

## Do not repeat without a new question

The persistence replication, Qwen candidate-pool experiment, score intervention, response-collapse control, and current audit suite are frozen. Further provider calls should require a new preregistered question, not an attempt to improve a settled headline number.

## Latest package commit

The synchronized materials repository is `StephCpa/DP-TacMA`; the latest recorded package commit is `a96443e`.
