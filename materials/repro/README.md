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

