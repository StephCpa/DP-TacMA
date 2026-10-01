# Pre-written reporting text for the 120-triad replication (amendment 222)

Fill the placeholders from the `--pre-submission` analysis summary
(`summary.g1_decision`, rates, upper bounds, McNemar, partial detector,
no-canary rate). Use the block that matches `g1_decision.outcome` exactly.
These blocks are written **before** the result is known. Replace numbers
only; changing the wording after seeing the result defeats the purpose of
amendment 222.

Placeholders:

- `{E}`, `{R}`, `{N}`: evolve hits, reset hits, and complete triads (120)
- `{UE}`: one-sided 95% upper bound for evolve
- `{RD}` `[{L},{U}]`: paired risk difference and bootstrap interval
- `{P}`: exact McNemar p
- `{PE}`, `{PR}`: partial-detector hits
- `{FP}`: no-canary false-positive count

## Outcome `failed_to_detect`

**Abstract** (replace the canary sentence):
> A three-arm study detects no post-input canary exposure in 20 instances, and a preregistered 120-instance replication across three task strata again fails to detect exposure ({E}/120 evolve versus {R}/120 reset; one-sided 95% upper bound {UE}).

**§3.1** (append after the first paragraph):
> A preregistered replication then ran 120 new instances, 40 in each of three strata (impossible, short feasible, long feasible), with the same three arms, extractor, and positive-control gate. Its decision rule, fixed before execution, required evolve exposure of at least 10%, a positive paired difference, and exact McNemar $p<0.05$. Evolve and reset arms recorded {E}/120 and {R}/120 exact post-input exposures (paired difference {RD} [{L},{U}], $p={P}$), the five-token partial detector {PE}/120 and {PR}/120, and the no-canary control {FP}/120 false positives. The one-sided 95% upper bound on evolve exposure is {UE}. This is a powered failed-to-detect result for this model, runtime, canary, and five-round window, not a privacy guarantee.

**Table 2 row:**
`Canary replication: evolve & 120 & exact/partial ${E}/120$ & upper bound {UE} \\`

**Limitations** (replace "With 0/20 observations it cannot exclude rates below 13.9%"):
> The preregistered replication bounds evolve exposure below {UE} at one-sided 95% confidence for this setting but does not test adaptive extraction, task-relevant secrets, or structural evolution.

## Outcome `positive_persistence_signal`

**Abstract** (replace the canary sentence):
> A 20-instance pilot detected no post-input canary exposure, but a preregistered 120-instance replication does: evolve state retains the canary in {E}/120 instances versus {R}/120 under a depth-matched reset (exact McNemar $p={P}$).

**§3.1** (replace the "defensible result" sentence and append):
> The pilot was therefore underpowered. A preregistered replication ran 120 new instances in three strata with the same arms, extractor, and positive-control gate. All four preregistered conditions for a persistence signal hold: evolve exposure {E}/120 is at least 10%, the paired difference is {RD} [{L},{U}], and exact McNemar $p={P}$. The partial detector records {PE}/120 and {PR}/120, and the no-canary control {FP}/120. Report exposure by stratum and by channel from `by_stratum` and the checkpoint paths.

**Required follow-on edits:**

- Change the Table 1 roadmap verdict for exposure to "Detected".
- In the Introduction, replace "we did not detect the motivating post-input canary channel" with the detected rate.
- In the Conclusion, change the first finding.

The privacy motivation becomes empirically grounded. Do not extend the claim
to structural evolution, other models, or adaptive attacks.

## Outcome `incomplete` (artifact not complete by the cutoff)

**Limitations** (one sentence; no numbers):
> A preregistered 120-instance replication of the canary study across three task strata is in progress and will be reported separately; no interim result is used here.

Do not report interim counts anywhere in the manuscript.
