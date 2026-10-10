# Parser-independent candidate-support audit (protocol 234, draft)

Machine-readable protocol:
`research/protocols/candidate-support-audit-protocol-234.json`.
Status: **draft, not frozen**. No candidate text has been read and no provider
call has been made.

## Why this audit

The paper's most exposed claim is that 43 of 46 failed runs contain no
parser-accepted executable candidate. The parser accepts only 365 of 1,152
slots, so a reviewer can argue that the parser, not the generator, is the
bottleneck. The audit separates four explanations:

- generation absence;
- parser rejection;
- executor failure;
- selector non-selection.

It asks three questions:

1. Was a candidate generated?
2. Did the parser wrongly reject it?
3. Can a real selector use it?

## What the cached data already settle (artifact 237, zero calls)

`repro/candidate_support_cached_preview.py` computes what the cached rows
allow. These results are already in the paper:

- **Endpoint ablation.** In both cached non-degenerate length-removal cohorts,
  executable validity, reference exactness, and their conjunction give the same
  paired contrasts:

  | Cohort | Contrast | 95% interval | Discordant pairs | Exact McNemar p |
  |---|---|---|---|---|
  | DeepSeek | +0.167 | [0, 0.417] | 2/0 | 0.5 |
  | Qwen | −0.050 | [−0.25, 0.15] | 2/3 | 1 |

  The initial 10-pair cohort needs the workspace run records.
- **Selector baseline.** On the Qwen nested pools, a uniformly random final
  answer scores 0.50, 0.52, 0.53, 0.55, and 0.54 for C1–C5, while the offline
  oracle scores 0.60–0.80. The gap therefore grows from 0.10 [0, 0.23] to 0.26
  [0.10, 0.43]. A random stochastic slot scores about 0.41. Score-based
  selectors need per-candidate scores, which are not cached.
- **Why a census.** The 43 generation failures average 13.6 rejected slots
  each. Under independence, a 1% per-slot false-negative rate would move about
  5.4 runs, and a 5% rate about 21. Bounding q_FN at 5% therefore cannot
  protect the run count. The primary unit is a census of every unique rejected
  text in the 46 failed runs: at most 495 texts from 604 slots.

## Design in one page

| Layer | What | Where |
|---|---|---|
| Re-parse | P0 (unchanged), P1 (format-only normalizer + P0), P2 (independent parser) over all U1 (1,152) and U2 (Qwen pool) slots; execute every accepted plan | `--reparse` |
| Blind audit | Census of unique P0-rejected texts in the 46 failed runs; secondary sample from non-failed runs (≤60 per cohort); 60 accepted controls | `--packet` |
| Annotation | A labels everything; B labels a seeded 30% of the census plus all secondary and control items; every A2/A3 is double-labelled; disagreements are adjudicated | `--second-pass` |
| Analysis | q_FN (exact and design-weighted, run-clustered bootstrap); run reclassification under P0/P1/P2/census; selector replay B0–B6 on round-only, final-inclusive and 16-slot-matched pools under both endpoints; dual endpoints for every score-ablation cell; frozen decision tier | `--analyze` |
| Figures | Funnel, reclassification matrix, selector versus support, cost table | `make_candidate_support_figures.py` |

**Blinding.** Annotators see only the following:

- an opaque audit id;
- the candidate text;
- the public answer schema;
- the P0/P1/P2 parse outputs and their reasons.

They never see:

- the cohort, model, run or task;
- the run outcome or the 43/46 classification;
- any reference.

The id-to-slot key (`private-key.json`) stays with a non-annotating author. The
packet directory gets a `.gitignore` and must never be published.

**Statistics.**

- Runs and tasks are the inferential units.
- Selector contrasts use paired task-level bootstraps (10,000 draws, seed 234).
- Binary run outcomes use exact McNemar tests.
- Slot-level intervals are descriptive only.

## Running it (workspace)

```bash
cd research/experiments            # or repro/ in this repository
python run_candidate_support_audit.py --check        # before freezing: reports unwired hooks, reads no text
# freeze protocol 234 (pre-freeze checklist in the JSON), record its SHA-256, commit
python run_candidate_support_audit.py --reparse
python run_candidate_support_audit.py --packet
#   annotator A fills labels-annotator-a.csv; annotator B fills labels-annotator-b.csv
python run_candidate_support_audit.py --second-pass  # extra items B must label (A's A2/A3 outside B's set)
#   B fills labels-annotator-b-second-pass.csv; adjudicator writes adjudication.csv for disagreements
python run_candidate_support_audit.py --analyze      # writes candidate-support-audit-analysis-235.json
python make_candidate_support_figures.py research/artifacts/candidate-support-audit-analysis-235.json <out-dir>
```

Every stage after `--check` refuses an unfrozen protocol and refuses outputs
made under a different protocol hash. `--analyze` stops if any required B
label or adjudication is missing.

## Annotation guide

Each row of a packet gives one candidate text. Fill `intent`,
`format_failure`, `human_plan` and optionally `notes`. Judge only what the
text says. Do not add steps, guess missing items, or use knowledge of the
task.

**intent**

| Label | Meaning |
|---|---|
| A0 | No recognizable executable intent: empty, off-topic, a question, or reasoning with no plan. |
| A1 | An action intent with critical information missing, e.g. "craft the planks first, then the rest". |
| A2 | A complete action intent that maps to canonical items, but is not written in the answer format, e.g. a numbered prose plan naming every item. |
| A3 | An explicit plan that violates only the parser's format, e.g. a code fence, capitalized ids, or a namespace. |

**format_failure**

| Label | Meaning |
|---|---|
| F0 | No content |
| F1 | Truncation |
| F2 | JSON or schema error |
| F3 | Missing fields |
| F4 | Field type error |
| F5 | Complete natural-language plan |
| F6 | Multi-step form the parser cannot process |
| F7 | Other |

**human_plan.** Fill this only for A2/A3. Write the plan exactly as the text
gives it, as `IMPOSSIBLE` or a JSON array of lower-case item ids, e.g.
`["oak_planks", "chest"]`. Use the item names the text uses, and the order the
text gives. Leave it empty if the text names no complete plan; in that case
the label should be A1.

The executor then derives:

- **E0:** no canonical plan;
- **E1:** a plan that is executor-invalid;
- **E2:** a plan that is executor-valid;
- **E3:** a plan that is also reference-exact.

Annotators never assign E labels.

**Calibration.**

1. Before the census, both annotators label the same 20 synthetic items.
   These are written by the adjudicator, are not from the study, and cover
   every label.
2. They discuss disagreements on the synthetic items only.
3. They may not discuss census items until both have finished.

## Frozen decision rules

| Tier | Condition | Paper consequence |
|---|---|---|
| A, robust | The census, P1 and P2 each reclassify ≤2 of the 43 runs, and the decision upper bound of q_FN is ≤0.05 | Keep the generation-support wording; report the audited count. |
| B, qualified | 3–9 runs reclassified under any rule | Most failures are generation failures; name the formats responsible. |
| C, weakened | ≥10 runs reclassified | Rename the bottleneck "parser- and protocol-mediated candidate support" in the title, abstract and conclusion. |
| Provider flag | One cohort's q_FN upper bound exceeds twice the pooled one | Report it as provider-specific and stratify the claim. |
| Selector claim | A paired task-level 95% interval excludes zero on the round-only pool | Claim nothing else about selector improvement. |

The 2-run, 10-run and 5% cut-offs are internal reporting thresholds fixed
before inspection.

## Pre-written reporting text (fill in after analysis 235)

The placeholders are:

- `{N}`: unique texts audited;
- `{k}`: human executor-valid texts;
- `{u}`: q_FN decision upper bound;
- `{r}`: runs reclassified by the census;
- `{r1}`, `{r2}`: runs reclassified by P1 and P2;
- `{kappa}`: intent agreement;
- `{formats}`: the F labels responsible.

### Tier A

**§3.2.** Replace "and we have not hand-audited the rejected slots, so a
parser false negative would be counted as a generation failure" with:

> A blinded census of all {N} unique parser-rejected texts in the 46 failed
> runs, double-annotated with adjudication (intent κ = {kappa}), found {k}
> texts with an executor-valid plan (one-sided 95% upper bound {u}). Together
> with a format-robust and an independent parser (reclassifying {r1} and {r2}
> runs), it reclassifies {r} of the 43 runs, leaving {43−r}/46 generation
> failures.

**Limitations.** Replace "but rejected slots were not hand-audited, so
generation failures may include parser false negatives" with:

> and a blinded census of rejected texts reclassified {r} runs, so the
> generation-failure count is robust to the parser at the audited level.

**Abstract.** It may then say "{43−r} of 46 failed runs contain no executable
candidate under strict, independent, or human parsing".

### Tier B

**§3.2.**

> Most failures remain generation failures, but parsing matters for some
> runs: the census reclassifies {r} of the 43 runs ({formats}), and the
> format-robust and independent parsers reclassify {r1} and {r2}. We therefore
> report {43−r}/46 generation failures and {3+r}/46 runs with a recoverable
> candidate.

**Abstract.** Replace "43 of 46" with "{43−r} of 46 failed runs contain no
executable candidate even under human reading of rejected outputs".

**Limitations.** Name the output-format issue.

### Tier C

**Title.** "… Exposure, Score Interventions, and Parser- and
Protocol-Mediated Candidate Support".

**Abstract.**

> In four frozen cohorts, {r} of the 43 apparent generation failures held a
> valid candidate that the strict parser rejected ({formats}), so the binding
> constraint is parser- and protocol-mediated candidate support rather than
> generation alone.

**§3.2.** Report the four-rule reclassification table and the funnel in the
main text.

**Conclusion.** Replace "generation support" with "parser- and
protocol-mediated candidate support".

### Selector results (any tier)

> On the round-only pools, the released 0.85/0.15 composite reaches {B4_C5} at
> C5 versus {B1_C5} for random selection (difference {d} [{lo}, {hi}]) and
> {B6_C5} for the offline oracle.

Add only if the interval excludes zero:

> Neither length-only nor success-only selection closes the oracle gap.

Name the score-based selectors that could not be replayed because the traces
lack their scores.

## Optional canary reachability control (protocol 236, live)

`research/protocols/canary-reachability-control-protocol-236.json` defines
four conditions on 20 instances each (80 runs, about 5k calls):

| Condition | Round-one input | Write mechanism | Purpose |
|---|---|---|---|
| R1 | Explicit canary | Direct memory write by the harness | Observer validity on live state |
| R2 | Explicit canary plus an instruction to store it | Agent-mediated | Input-to-state reachability |
| R3 | Canary inside ordinary task text | Agent-mediated, uninstructed | The natural route |
| R4 | No canary | — | False positives |

The control checks state after rounds 1, 2, 3 and 5 and in the final state. It
separates input reachability from persistence and changes no reported canary
number. It needs authorization, a frozen protocol, and a cost cap from the
workspace model.

## Cost

Protocol 234 makes zero provider calls. The human effort is:

- annotator A: about 735 items, at most 495 of them in the census;
- annotator B: about 300–400 items;
- the adjudicator: disagreements only.

The minimum viable version is listed in the JSON. It never drops the census or
the frozen decision rules.
