# DP-TacMA research materials

This repository contains the paper-writing materials and a public, scrubbed
research record for the DP-TacoMAS study.

## Package layout

- `materials/manuscript-arr/`: current ACL ARR manuscript source, bibliography,
  style files, figures, and the compiled PDF.
- `materials/research/progress/`: English progress summaries, the frozen X1
  persistence protocol, launch runbook, and append-only progress log.
- `materials/research/protocols/`: machine-readable protocols and the explicit
  pre-submission authorization amendment.
- `materials/research/data/`: audit artifacts and cached analyses that contain
  no API credentials or raw canary strings.
- `materials/repro/`: the analysis and live-run entry points. The upstream
  TacoMAS checkout and provider credentials are intentionally not bundled.

## Current live experiment status (2026-10-02, Asia/Shanghai)

The user-authorized pre-submission persistence replication completed separately
from the ARR manuscript: 360/360 cells, balanced at 120 per arm and 40 per
stratum, with 17,048 provider calls and 39,637,371 recorded tokens. Evolve and
depth-matched-reset exposure are both 0/120, no-canary false positives are
0/120, and the evolve-arm one-sided 95% upper bound is 2.5%. The machine-
readable result is explicitly scoped as a failed-to-detect result for the
audited design, not a privacy guarantee.

The ARR manuscript in this package now reports this complete replication. No API key,
provider token, raw canary, local credential, or machine-specific secret is
part of this package.

## Reproduction and credential policy

Run experiments only from a separately configured local checkout. Set provider
credentials through environment variables; never commit them. The live
replication is resumable by `(instance_id, arm)` and must not be interpreted
until the protocol's completeness and balance gates pass.
