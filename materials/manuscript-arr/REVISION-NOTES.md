# Revision notes for the complete persistence replication

This update incorporates the completed 120-instance, three-arm persistence
replication into the ARR manuscript.

- `main.tex` updates the abstract, experimental sequence, Results, conclusion,
  limitations, reproducibility paragraph, and primary audit table.
- `appendix.tex` updates endpoint status, null sensitivity, and the artifact
  index.
- The replication result is 0/120 exact-or-five-token partial exposure in both
  evolve and depth-matched-reset arms, 0/120 no-canary false positives, and a
  2.4655% one-sided 95% upper bound for the evolve arm.
- The wording remains “failed to detect” and does not claim a privacy guarantee.
- Local checks passed: numeric consistency, claim-evidence, draft readiness,
  Pubcheck preflight, metadata synchronization, and 15-page LaTeX compilation.

The direct-sampling baseline proposed in the research plan has not been run and
is not represented as evidence in this package.
