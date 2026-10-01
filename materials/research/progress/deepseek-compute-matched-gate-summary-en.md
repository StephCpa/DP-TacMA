# DeepSeek Conditional-Collapse Study: Final Summary

**Status date:** 14 August 2026  
**Decision:** Stopped at the frozen gate; no main-cohort task was run  
**Primary model:** DeepSeek V4 Flash  
**Qwen calls:** 0

## Research question

The Qwen candidate-pool experiment showed that independent trajectories can raise executable-oracle accuracy from 0.60 to 0.80, but at approximately three times the generation tokens. The DeepSeek follow-up asked whether a more directed use of the same added budget could be more efficient.

On each task, both methods shared a new temperature-0 five-round three-agent anchor trajectory. If the anchor pool already contained an executable plan, both methods received success and stopped without additional calls. On anchor failure, the comparison was non-nested:

- **Independent restart:** one new temperature-0.7 five-round three-agent trajectory.
- **Executor-guided repair:** sequential direct temperature-0.7 calls using the public task, the current candidate, and reference-free execution diagnostics. The restart's realized token cost defined the repair cap.

The frozen gate required at least four complete anchor-failure comparisons, at least one repair rescue, repair rescues no fewer than restart rescues, provider integrity, and complete exhaustion of every unsuccessful repair branch.

## Gate outcome

All eight gate tasks completed, but five anchor pools already contained an executable plan. Only three tasks were informative, below the frozen minimum of four. This was the sole failed gate condition, so the experiment stopped and all 12 reserved main tasks remained unrun.

| Intervention-specific endpoint | 3 anchor failures |
|---|---:|
| Independent-restart success | 0/3 |
| Executor-guided-repair success | 1/3 |
| Repair minus restart | +0.333 |
| Task-bootstrap 95% interval | [0, 1] |
| Exact paired two-sided test | \(p=1.0\) |

There was one repair-only win, no restart-only win, and two common failures. This direction is encouraging but not statistically informative: the exact test is determined by a single discordant task. The five shared-anchor successes are not included in an intervention effect because neither arm caused them.

## Efficiency and failure modes

On TEST0181, repair found `["dark_oak_planks", "pink_bed"]` in its first 1,008-token call, while the independent matched-budget restart used 157,910 tokens and failed. This is a one-task existence proof for an inexpensive directed rescue. It is not a 157-fold efficiency estimate because it compares an early success with a fully spent failed trajectory.

The other two branches reveal the main difficulty:

| Task | Restart tokens | Repair tokens | Repair calls | Modal invalid response |
|---|---:|---:|---:|---|
| TEST0030 | 138,559 | 51,330 | 80 | `["IMPOSSIBLE"]`, 69/80 |
| TEST0535 | 162,193 | 50,313 | 80 | `["redstone_torch"]`, 76/80 |

TEST0030 repeatedly asserted impossibility even though the task had a valid two-step plan. The identical raw string `["IMPOSSIBLE"]` accounts for 86.25% of calls; after normalizing nine plain-text variants, 97.5% express the same invalid semantic intent. TEST0535 repeatedly omitted the required intermediate product `redstone`, with one wrong raw and semantic answer accounting for 95% of calls. Across these two exhausted tasks, 145/160 calls (90.625%) equal their task-specific raw mode and 154/160 (96.25%) equal their semantic mode.

We call this **task-level response collapse**: nominally stochastic sampling concentrates on a single invalid response on a selected hard task instead of enlarging executable support. The control shows that the concentration persists without repair conditioning, so the label is not a causal claim about conditioning. It is based on two failed tasks, the 0.80 threshold is post hoc, and repeated calls do not create 160 independent task units. The successful branch stopped after one call, so concentration on successful repairs cannot be estimated. Earlier disjoint DeepSeek cohorts did not collect comparable repeated repairs, so cross-cohort modal stability is also not identifiable at zero additional API cost.

## Operational correction

The first two direct repair calls on TEST0030 consumed the output allowance in hidden reasoning and exposed empty visible answers. The direct path had omitted the explicit non-thinking switch already used by the full TacoMAS compatibility path. Both calls, their 3,768 tokens, and their malformed outcomes remain in the official intention-to-repair record. Subsequent direct calls explicitly set `thinking.type=disabled`. This restored visible outputs but did not solve the semantic-collapse problem.

LiteLLM response caching was disabled. DeepSeek's automatic provider-side prefix-cache accounting is distinct from that client flag and may still appear in provider usage metadata.

## Cost

| Surface | Recorded tokens |
|---|---:|
| Shared anchors | 1,081,254 |
| Independent restarts | 458,662 |
| Direct repairs | 102,651 |
| **Total** | **1,642,567** |

The run made 736 recorded DeepSeek calls. Every completed provider record passed the integrity audit. No credential is stored in any research artifact.

## Scientific interpretation

The experiment validates a narrow possibility: executor-guided repair can find an inexpensive first-attempt rescue on an individual task. It does not validate a general efficiency advantage. The gate had too few informative tasks and only one discordance.

Its stronger contribution is mechanistic. Earlier results showed small realized candidate support, better matched-slot coverage across independent trajectories than within one trajectory (0.626 versus 0.570), and polarized per-task resampling success. The repair failures now show the concentration directly: changing the stochastic token draw while retaining the diagnostic context repeatedly produces the same wrong plan. Together these measurements support the interpretation that useful diversity often comes from resampling context, not merely from raising decoding temperature. The present design does not causally isolate conditioning, so that last statement remains a triangulated interpretation rather than a controlled effect.

The largest observed problem is therefore not disagreement with the selector-DP theory. Binary executor utility still has maximal local separation, \(g_U=\Delta_c=1\), when a mixed candidate pool exists. The problem occurs earlier: the conditional generator often fails to produce a diverse or diagnostically responsive candidate pool.

## Recommended next action

Do not run the frozen main cohort and do not redesign the repair method before the submission deadline. Paper completion should take priority. The Qwen pool-enlargement result remains the constructive intervention; this DeepSeek study should be reported as the failed obvious efficiency remedy that directly exposes task-level response collapse.

## Artifacts

- Frozen protocol: `research/configs/deepseek-compute-matched-generation-protocol-090.json`
- Complete source artifact: `research/artifacts/iclr2027-deepseek-compute-matched-generation-091.json`
- Zero-call final analysis: `research/artifacts/iclr2027-deepseek-compute-matched-generation-gate-analysis-092.json`
- Conditional-collapse analysis: `research/artifacts/iclr2027-deepseek-conditional-collapse-analysis-094.json`
- Runner: `research/experiments/run_deepseek_compute_matched_generation.py`
- Finalizer: `research/experiments/analyze_deepseek_compute_matched_gate.py`
- Collapse analyzer: `research/experiments/analyze_deepseek_conditional_collapse.py`
