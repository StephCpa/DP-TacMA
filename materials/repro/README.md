# Reproduction notes

The copied Python files are the analysis and controlled-run entry points used
in the source workspace. A full rerun additionally requires the upstream
TacoMAS checkout, the frozen PlanCraft cohort, and a locally configured
provider key. Those dependencies are deliberately not included here.

The current pre-submission run is explicitly separated from ARR submission
claims. Do not overwrite the frozen manuscript with its incomplete output.

## Changes in this copy (2026-10-02)

- `post_arr_persistence_analysis.py` now reports the protocol-199 G1 decision
  (`g1_decision`), the paired five-token partial detector, one-sided exact
  (Clopper--Pearson) upper bounds per arm, and per-arm mean calls/tokens for
  the call-comparability stop rule. A completed run record missing its `arm`
  key now marks the summary `incomplete` instead of raising `KeyError`.
  Existing output fields keep their previous meaning.
- `analyze_post_arr_persistence_replication.py` adds `--pre-submission`, which
  reads artifact 220 and writes the complete analysis 222 (221 is the
  historical one-cell staged check). It also falls back to the sibling
  module, so this copy runs without the workspace package layout.
- `test_post_arr_persistence_analysis.py` holds synthetic-fixture tests. Run
  `python test_post_arr_persistence_analysis.py` or `python -m pytest -q` here.

Port these changes to the source workspace and rerun its full test suite
before using them on artifact 220.

## Direct-sampling baseline (protocol 227, draft)

- `run_direct_sampling_baseline.py`: the dry run is the default. Live calls
  need a frozen protocol, `--execute`, and `DIRECT_SAMPLING_227_AUTHORIZED=1`.
  `--analyze` makes no calls.
- `direct_sampling_analysis.py`: E1 (oracle versus C5/C1/baseline, exact
  McNemar), E2 (collapse prevalence, Clopper--Pearson), unbiased coverage at k,
  and the decision rule.
- `direct_sampling_adapter.py`: wire every hook to the protocol-083/096 code
  before use; each raises `NotImplementedError` until then.
- Tests: `python test_direct_sampling_analysis.py` and
  `python test_run_direct_sampling_baseline.py`.


## Candidate-support audit (protocol 234, draft) and cached preview (237)

- `candidate_support_cached_preview.py`: zero-call, reads only cached 081/088
  and writes `research/data/candidate-support-cached-preview-237.json`. It
  computes:
  - executable validity versus reference exactness for the two cached
    length-removal cohorts;
  - random-final and random-slot selector baselines on the Qwen nested pools;
  - the run-level parser-sensitivity calculation behind the census design.
- `candidate_parsers.py`: P1, a format-only normalizer applied before the
  unchanged P0, and P2, an independent parser that accepts `IMPOSSIBLE` or
  exactly one JSON array of item ids.
- `candidate_support_audit.py`: the analysis library. It covers:
  - re-parsing and slot states;
  - run classes and reclassification;
  - funnels;
  - blinded packet construction;
  - label merging with kappa;
  - q_FN with exact and run-clustered bounds;
  - selector replay B0–B6 under both endpoints;
  - dual endpoints;
  - the frozen decision tiers.
- `candidate_support_adapter.py`: wire every hook to the 081/088 code paths.
  Each hook raises `NotImplementedError` until then.
- `run_candidate_support_audit.py`: stages `--check`, `--reparse`, `--packet`,
  `--second-pass`, and `--analyze`. Every stage except `--check` needs the
  frozen protocol and refuses outputs made under another protocol hash. The
  packet directory holds candidate texts and the de-blinding key, gets a
  `.gitignore`, and must never be published.
- `make_candidate_support_figures.py`: draws the funnel, the reclassification
  matrix, selector versus support, and the cost table from analysis 235.
- Tests: `python test_candidate_support_audit.py` (15 synthetic-fixture
  tests with a fake adapter).

The human-readable protocol, annotation guide, and pre-written tier A/B/C
reporting text are in
`research/progress/candidate-support-audit-protocol-234.md`. The optional
live canary reachability control is draft protocol 236.
