# Response to the 2026-10-10 pre-submission review

This maps each point of the ARR-style review to the revision on branch
`claude/inspiring-shannon-rhio9o`. No experiment was run and no provider call
was made. Every new number is regenerated from cached per-run or per-task
records by `repro/reanalyze_review_items.py` (artifact 231).

Status key: **Done** = changed in the paper; **Partly** = addressed with
existing evidence plus a stated limitation; **Not done** = needs a new
experiment, stated as a limitation.

## Headline changes

- **Title.** Now "Before Candidate Selection in Test-Time LLM Agents: A
  Scope-Limited Audit of Exposure, Score Interventions, and Realized Candidate
  Support". The abstract, introduction, and conclusion name the fixed-topology
  TacoMAS–PlanCraft configuration and say that structural edits are disabled
  in every study.
- **Abstract.** Gives per-arm canary denominators (120 per arm, 360 runs) and
  the canary, observer, and horizon scope. It calls the score result
  "heterogeneous and inconclusive", makes 43/46 parser-conditional, says
  "offline oracle" and "four additional restarts", and drops the repair
  collapse.
- **§3.4–3.6 moved.** The repair gate and the held-out planner are reduced to
  one exploratory subsection; details are in the appendix. The ε curve moved
  to an appendix figure with a privacy proof.
- **Appendix additions:** audit procedure with stop rules, metric definitions,
  score sources, DP proof, per-task pool patterns, repair sensitivity, planner
  batch-by-batch results, closest-work table, and reproducibility contents.

## Point by point

**II.1 Exponential-mechanism factor of two: Done.** This is not an error under
the paper's adjacency, but the paper did not show why. Candidate-score
replacement changes one candidate's score with the candidate set fixed, so the
changes are monotone and `exp(εu/Δu)` is ε-DP.
- Appendix "Fixed-pool selector calculation" now states the setting: a fixed,
  public candidate set and output domain, clipped scores, the adjacency, and
  trusted components. It gives a full proof.
- The main text and appendix figure report the general-calibration equivalents
  (ε = 1, 2, 4, 8, 16).
- The curve left the main figure; §3.5 is a short, explicitly illustrative
  paragraph.

**II.2 Score intervention: Done or Partly.**
- **Wording.** "Randomized" became "paired, prospective"; there is no record
  of randomized arm order. "Score validity" became "score consequences". The
  arm is now the "length-term removal arm" ("length-zero" only as the artifact
  name).
- **New text** says that removal changes retention, the history passed to the
  Meta-LLM, feedback, calls, and tokens. The estimand is therefore system-level,
  and a null does not show invalidity; the reviewer's list of alternative
  causes is in the text.
- **Score sources**, from cached artifact 037: 705 of 900 contribution scores
  are fast-heuristic and 195 come from slow-update judging.
- **Claim** is now exactly the reviewer's supported claim.
- **Not done:** rank-preserving rescaling, mean- or variance-matched pseudo
  terms, and score baselines. These need new runs.
- **Authors:** if call order was interleaved or counterbalanced, state it in
  the appendix; the repository records only the paired design.

**II.3 "Evolving" versus fixed topology: Done (option A).** The title is
narrowed, and the introduction and Limitations say that structural
birth/death and edge edits are disabled everywhere. Option B, a
topology-edit arm, was not run.

**II.4 Canary scope: Done.**
- The abstract and Table 2 give 120 per arm and 360 runs.
- The no-canary row now reports "upper bound 0.025", and the figure draws its
  whisker.
- §3.1 states that the positive controls cover the declared channels, not the
  round-one injection path.
- Limitations lists paraphrase, encoding, cross-channel, task-relevant,
  adaptive, and provider-log channels as untested.

**II.5 43/46 and the parser: Partly.**
- **Both estimands are identical.** The round-candidate-only oracle and the
  final-inclusive oracle are both 22/65, because no run had a valid final
  without a valid round candidate (0/65). The amendment changes no value.
- **Exact intervals:**
  - 43/46: [0.821, 0.986];
  - 3/46: [0.014, 0.179];
  - 3/65: [0.010, 0.129].

  Table 3 shows failed-run denominators per cohort and a pooled
  exploratory row.
- **IMPOSSIBLE sensitivity.** Under reference exactness over all 72 runs, the
  same 3 runs are recoverable.
- **Metric agreement.** Executable validity and reference exactness agree on
  65/65 eligible finals, and environment replay matches reference exactness on
  48/48 non-degenerate finals.
- **Parser acceptance** is 365/1,152 slots (32%) and is now disclosed.
  Generation failures are stated as parser-conditional.
- **Not done:** a human audit of rejected slots. This needs raw traces from
  the workspace and is the most valuable remaining check for this claim.

**II.6 C1→C5: Done.**
- "Independent contexts expand support" became "Additional independent
  restarts expand recorded support". The text names everything that changes
  together and calls the slot-matched comparison retrospective and not
  token-matched.
- The five-finals claim left the main text.
- Figure 2 now has task-bootstrap intervals per point (C1 [0.40, 0.80],
  C5 [0.60, 0.95]) and an extrapolation band. "Empirical asymptote" became
  "finite-sample extrapolation".
- The per-task pattern is in the appendix: 12 tasks always succeed, 4 never
  do, and 4 are rescued.

**II.7 Post-hoc and stopped analyses: Done.**
- Table 1's score row says "primary exactness effects heterogeneous and
  inconclusive", and the 42-pair synthesis is labelled secondary everywhere.
- "Outcome-blind gate" became a gate "blind to the length contrast".
- "Preregistered" became "frozen as an internal record"; the paper states that
  these are not external registrations.
- Limitations lists every exploratory or amended analysis.

**II.8 Repair and planner: Done.**
- Both are in one exploratory subsection. The public-only control is
  described as removing several components at once.
- TEST0030 sensitivity without the two empty pre-fix calls: raw 69/78
  (88.5%), semantic 78/78.
- The planner is reported per batch: development 7/7; held-out batch 1 3/6 at
  cap 8 and 6/6 at cap 12; untouched batch 2 6/6 with 4/6 canonical. Only
  batch 2 is called a clean held-out evaluation.

**III.1 Metrics: Done.** An appendix metric table covers executable validity,
reference exactness, canonical exact, and replay validity. Tables and axes now
say "ref. exactness" or "executable".

**III.2 Degenerate bootstrap: Done.** Table 2 flags it (†), and Figure 1b
draws the exact bound |RD| ≤ 0.31 from 0/10 discordant pairs.

**III.3 The 1.75× lift: Done.** The label is removed. Figure 1c shows the raw
counts 24/165 and 75/900, names the unit (agent-round observations, 15 per
run), and reports the run-level AUC of 0.755.

**III.4 Task-level distributions: Done** for C1–C5 and 43/46, in the appendix
and artifact 231.

**IV Reproducibility: Partly.**
- New anonymous supplement `acl-arr-anonymous-supplement-233.zip`. A fresh
  extraction regenerates every new number above (artifact 231) and passes its
  tests; its identity scan is clean.
- The appendix lists models, temperatures, the thinking and caching settings,
  and the PlanCraft file hash.
- **Not included:** the upstream runtime (license gate) and raw traces.
  Provider SDK and LiteLLM versions, prompts, and tool schemas live in the
  workspace; add them to the supplement if the license gate clears.

**V Related work and novelty: Done.**
- Added MEXTRA (ACL 2025) and Scaling Test-time Compute for LLM Agents
  (arXiv 2506.12928), with a closest-work table in the appendix.
- The contributions now say the oracle gap, term ablation, and canary matching
  are standard tools, and that the contribution is the audit order.
- Appendix "Audit procedure" gives estimands, stop rules, minimum detectable
  effects, and escalation.

**VI Figures and tables: Done** as listed above. Figure 1b's axis already
extended to 0.45 and now to 0.47, so nothing is clipped.

**VII P1 (second runtime or benchmark, real selector baselines, stronger
canary): Not done.** All need new experiments. Each is stated in Limitations.
A random or released-score selector baseline cannot be computed from the
cached rows, which store only oracle indicators, not per-candidate scores.

## Verification (zero provider calls)

| Check | Result |
|---|---|
| Build | 18 pages; Limitations on page 8; no warnings; line numbers settled |
| Archive 232 (11 entries) | Deterministic; independent compile 18 pages; text matches the PDF |
| Local preflight | Passed |
| Official aclpubcheck (`237bee3`), non-line-numbered proof | **All Clear!** |
| Text conditions of 189/191/174/224 and emulated 192/193 | Pass (36 cited = 36 bibliography keys; title and abstract synced) |
| Anonymous supplement 233 | Passed |

Workspace-only: the full audit runs, freeze 196, and the 157-test suite.
Expectation changes to port: 18 pages, 11 archive entries, archive id 232.
The record is `research/data/arr-review-revision-local-verification-2026-10-10.json`.

## Still the authors' call

- **Dual submission.** Your venue brief already gates ARR upload on the ICLR
  submission state; that gate still applies.
- **Parser hand-audit.** A 50–100 slot hand audit of rejected slots, run in
  the workspace, would most strengthen the 43/46 claim.
