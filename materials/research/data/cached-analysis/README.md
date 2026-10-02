## Cached analysis snapshot (2026-10-02)

This package now includes zero-new-call reanalyses of frozen traces:

- `cached-analysis/iclr2027-cached-headroom-meta-analysis-081.json`: cross-cohort candidate-pool headroom, diversity, and length-mechanism analysis.
- `cached-analysis/iclr2027-x1-score-validity-037.json`: deterministic validity audit of local contribution signals.
- `cached-analysis/iclr2027-x2-failure-modes-108.json`: operational endpoint-failure decomposition for the canonical X2 screening records.
- `cached-analysis/cached-headroom-meta-analysis-protocol-080.json`: frozen analysis protocol and amendment record.

These files contain no provider credentials or raw canary strings. They are cached analyses only. The direct-sampling baseline is complete; its zero-call corrected trajectory reanalysis is recorded below, and further provider experiments remain frozen unless a new preregistered question is approved.

Additional direct-sampling reanalysis:

- `qwen-candidate-pool-trajectory-reanalysis-protocol-087.json` freezes the zero-call correction.
- `iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json` withdraws nested sign tests and reports task-cluster uncertainty. The matched 16-slot cross-trajectory oracle is 0.626 versus 0.570 for a single stochastic trajectory, difference 0.056 (95% task-bootstrap interval [0.016, 0.105]). This is a coverage decomposition within the same three-agent runtime, not a single-agent/multi-agent causal comparison.
