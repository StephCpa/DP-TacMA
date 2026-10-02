# Latest Research Progress and Main Challenge

**Project:** Privacy and utility auditing for test-time evolving LLM multi-agent systems  
**Target:** ICLR 2027  
**Status date:** 1 October 2026

**Update after the X2 attribution audit:** The 18-task held-out planner result is now explicitly decomposed into symbolic and LLM components. A zero-call symbolic control (artifact 149) reproduces 12/12 feasible replay outcomes, 8/12 canonical exact plans, 6/6 bounded stops, and 14/18 evaluator-exact labels; all 12 feasible pairs are both-valid. A strict sequence comparison finds 10/12 feasible cached plans identical to the symbolic plans; the remaining two are alternative action orderings. Only 7/78 cached requests exposed multiple options, with four step-index mismatches in two replay-valid tasks (artifact 158). The historical nine-task comparison likewise gives 4/9 replay-valid for unfiltered state-verified LLM selection versus 7/9 for symbolic-only and bounded hybrid (artifact 153). These are post-hoc attribution diagnostics, not causal architecture results, and the manuscript no longer attributes the held-out execution success to LLM or multi-agent planning.

Protocol 152 has now been run prospectively with the frozen unfiltered DeepSeek control. The live arm completed all 18 tasks using 142 provider calls and 43,623 tokens. On the 12 feasible tasks, 8/12 plans were executable in concrete replay and 5/12 were canonical exact; all six impossible-reference tasks terminated without reaching a target. The paired analysis (artifact 164) finds replay 8/12 live versus 12/12 symbolic-only, with 8 both-valid, 4 symbolic-only, and 0 live-only pairs (two-sided exact paired (p=0.125)). Canonical exactness is 5/12 versus 8/12, with one live-only exact pair (two-sided (p=0.375)). This is evidence that bounded symbolic constraints account for much of the held-out executable coverage, while preserving a possible but small role for LLM choice.

The first live attempt was stopped by an inherited proxy timeout before a provider response; the retry used only a process-local `NO_PROXY=api.deepseek.com` setting and did not change the frozen scientific protocol. The provider audit found 142 trace entries for 142 accounted calls, 142 parseable JSON responses, no empty responses, and no provider-error markers. Two out-of-option selections were recorded as rejected by the local verifier. Artifact 156 remains the historical no-call gate record; artifact 160 remains the static protocol audit. Artifact 164 is a descriptive fixed-cohort component ablation, not a population estimate, architecture-superiority claim, or end-to-end DP result. Artifact 166 independently verifies the live numbers, manuscript text, PDF, and archive identity with zero provider calls. Artifact 167 adds the claim-evidence and reviewer-risk audit for main-conference submission.
The first live attempt was stopped by an inherited proxy timeout before a provider response; the retry used only a process-local `NO_PROXY=api.deepseek.com` setting and did not change the frozen scientific protocol. The provider audit found 142 trace entries for 142 accounted calls, 142 parseable JSON responses, no empty responses, and no provider-error markers. Two out-of-option selections were recorded as rejected by the local verifier. Artifact 156 remains the historical no-call gate record; artifact 160 remains the static protocol audit. Artifact 164 is a descriptive fixed-cohort component ablation, not a population estimate, architecture-superiority claim, or end-to-end DP result. Artifact 166 independently verifies the live numbers, manuscript text, PDF, and archive identity with zero provider calls. Artifact 167 adds the claim-evidence and reviewer-risk audit for main-conference submission, and artifact 170 cross-checks the headline numbers against their frozen source artifacts.

The cached branch audit now has a separate uncertainty record (artifact 161). On the fixed feasible cohort, 7/78 accepted requests exposed multiple options (95% exact interval [0.037, 0.176]), 4/78 step positions differed from the symbolic sequence ([0.014, 0.126]), 2/12 tasks contained any mismatch ([0.021, 0.484]), and 10/12 plans matched symbolically step-for-step ([0.516, 0.979]). These are decision-level descriptive intervals that do not account for task sampling, provider variation, dependence, or semantic equivalence, and are not causal estimates.

The intervals are now integrated into the Appendix and provenance pointer. After the final same-runtime wording clarification, the rebuilt anonymous source package is archive 169; independent extraction and compilation reproduce the 16-page workspace PDF with identical layout-extracted text.

**Update 1 October 2026:** A zero-call slot-level replay of all 48 non-degenerate main-phase final answers through the public PlanCraft environment reached the target in 26/48 rows, exactly matching the 26 reference-exact outputs. The result has been added to the appendix and the manuscript compiles and passes the submission-integrity audit and the current 142-test suite. This strengthens the execution interpretation of the existing exact-match results without changing the main estimands.

**Update 1 October 2026 (X2 screening):** After removing an inherited dead proxy, the credentialed DeepSeek V4 Flash G0 smoke passed with a deterministic PlanCraft match and positive token accounting. Two additional frozen PlanCraft blocks (TEST0069 and TEST0097) then completed all eight arms each. The screening artifact now has 56 canonical complete cells, 3,086 provider calls, and 9,971,526 tokens. These interim cells are retained as a screening audit, not yet a headline result: the dominant operational failure is exact output-shape mismatch, with agents often returning explanations or tool-like labels instead of the canonical action list or `IMPOSSIBLE` required by the evaluator. BrowseComp remains gated by an unresolved dependency failure.

The next frozen block, TEST0115, completed all eight arms. It is a feasible `polished_granite` task: A0 direct failed exact matching, whereas A1--A7 all returned the canonical action sequence. The updated screening artifact contains 64 canonical complete PlanCraft cells, 3,472 provider calls, and 10,957,660 tokens. This is still an interim screening audit rather than a paper headline result.

TEST0122 then completed all eight arms on a longer `polished_diorite_slab` dependency chain. Every arm failed exact matching; the traces repeatedly stopped at intermediate recipe searches or emitted explanatory text instead of the canonical action list. The artifact now contains 72 canonical complete PlanCraft cells, 4,159 provider calls, and 12,590,832 tokens. This strengthens the diagnosis of dependency-chain and output-contract failure, but remains an interim screening observation rather than a claim about the architecture.

### Zero-call X2 failure taxonomy

Artifact 108 classifies the 72 latest complete PlanCraft cells without additional provider calls. Twelve cells are exact (16.7%). Twenty-six (36.1%) have no parsed final answer, 14 (19.4%) are explanatory/search outputs rather than canonical output when the two narrative categories are combined, 11 (15.3%) are token-like but incorrect action sequences, and 9 (12.5%) return an action list for an `IMPOSSIBLE` reference. The taxonomy is deliberately evaluator-facing: it separates output-contract and finalization failures from action-sequence mismatches, but it does not establish semantic correctness beyond the deterministic endpoint.

At the paired task level, A6 full evolution beats A0 direct on 2/9 tasks with no losses (7 ties), while A7 full zero-length beats A6 on 1/9 with no losses (8 ties). These sparse contrasts are screening diagnostics only; they are not confirmatory multi-agent evidence.

The task-by-arm matrix, cost accounting, and interpretation are preserved in `research/x2-interim-screening-report.md`. It recommends freezing unchanged X2 expansion until the output contract and finalization treatment are prospectively addressed; otherwise additional cells mainly replicate the same evaluator-facing failure surface.

An outcome-aware, zero-call raw-trace audit (artifact 109) finds a mixed mechanism: 30 of 60 non-exact cells contain the reference sequence or `IMPOSSIBLE` signal somewhere in saved agent/round traces, but only 2 retain it in the raw final answer; 28 contain no reference signal at all. This is evidence for a finalization/serialization bottleneck in part of the loss, not evidence that all failures are formatting failures.

The amended reference-free finalizer gate provides a causal diagnostic for that hypothesis without regenerating candidates. One uniform serializer call per saved cell raises exact matching from 12/72 to 26/72, with 14 gains and no losses. All gains occur on the two `IMPOSSIBLE` tasks; the 56 action-list tasks remain at 10/56. The gate therefore fixes a narrow impossible-output normalization problem but does not recover feasible multi-step plans. It is a post-processing mechanism result, not an end-to-end architecture or multi-agent superiority claim.

A separately frozen dependency-aware prompt (protocol 113) asked the same finalizer to reconstruct recipe chains and verify inventory rather than trust candidate explanations. It yields the same 26/72 exact rate as protocol 111, with the same 14 impossible-task gains and no action-list gains (70/72 outputs are identical). The simple prompt-only dependency repair is therefore not sufficient.

An attempted tool-enabled finalizer gate (protocols 115--116) was stopped at a tool-surface audit. The public PlanCraft `gold_search_recipe` interface returns a representative cartography-table recipe and does not enumerate the `warped_planks` alternative used by TEST0011's executable reference; its `warped_planks` lookup also exposes a different intermediate name. Artifact 117 records this zero-call mismatch. Until the search interface is complete and frozen, tool-enabled finalizer results would confound model reasoning with incomplete evidence retrieval.

## Executive summary

The project has moved from a largely negative feasibility study to a clearer **bound-and-escape** result.

The earlier experiments established that three assumptions behind private selection in evolving-agent systems cannot be taken for granted:

1. No post-input persistent canary exposure was detected in the completed 120-instance, five-round replication. The evolve arm has a one-sided 95\% upper bound of 2.5\%; this is a failed-to-detect result for the audited model, topology, horizon, and canary family, not a privacy guarantee.
2. The released TacoMAS contribution score is causally dominated by its output-length component across both DeepSeek V4 Flash and Qwen3.7-Max.
3. Removing the length term changes the score strongly but does not produce a stable improvement in executable task utility.

The fixed-pool candidate audit then showed why downstream selection had little room to help. Across four frozen original/control cohorts, observed selector headroom was only 0–8.3 percentage points. An exploratory cross-cohort synthesis found only 3 recoverable failed finals among 65 feasible runs, or 4.6 percentage points. For every realized candidate pool, this oracle is a deterministic upper bound on any private or non-private selector restricted to that pool.

The latest prospective Qwen experiment tests the constructive implication of this bound: if the existing pool is the bottleneck, enlarge the pool before applying private selection. The result is positive but expensive. Accumulating five independent stochastic trajectories instead of one increases canonical candidate support by 1.00 plan on average and raises executable-oracle accuracy from 0.60 to 0.80. Selector-level DP then approaches the enlarged non-private oracle at moderate privacy budgets. However, the executable gain comes from only four tasks and requires approximately three times the generation tokens.

The follow-up DeepSeek compute-matched gate now answers part of that question mechanistically. Five of eight shared anchor pools already succeed, leaving only three informative failures and triggering the frozen stop rule. Repair produces the only intervention-specific rescue (1/3 versus 0/3 for restart), but the comparison has one discordant pair and exact paired \(p=1\). On both exhausted tasks, one invalid raw response occupies 86.25%--95% of 80 temperature-0.7 calls. The largest challenge is therefore task-level response collapse and adequate non-nested information, not executor calibration or the DP formula.

An important statistical correction is now part of the official record: the originally reported nested-pool sign-test values are invalid because \(C_1\subset C_5\) makes decreases impossible. They have been withdrawn without changing any observed endpoint. The corrected analysis uses task-bootstrap estimation and a zero-call trajectory decomposition.

## 1. Findings established before the latest experiment

### 1.1 Persistent leakage was not detected

The initial persistence-aware canary audit completed 60 runs over 20 three-arm instance blocks. No exact or preregistered partial canary appeared in post-input persistent state. The preregistered follow-up then completed 360 cells over 120 balanced instance blocks: evolve, depth-matched reset, and no-canary each have 120 complete runs, with zero exact or five-token partial exposures and zero no-canary false positives. Exposure is zero in each 40-instance stratum. The paired evolve-minus-reset risk difference is zero with exact two-sided McNemar $p=1$, and the evolve-arm one-sided 95\% upper bound is 2.5\%.

The null is operationally credible because:

- the extractor recovered all declared channels in deterministic positive controls;
- a live round-2 memory injection was recovered at a later checkpoint;
- observable agent state changed substantially during the runs.

The correct interpretation is “failed to detect persistent exposure under this setting,” not “the system does not leak.” The larger replication narrows the compatible evolve-arm rate to below 2.5\% at one-sided 95\% confidence, while rare leakage and other canary families remain outside the design.

### 1.2 The released score is causally length-dominated

Three prospective length-term interventions were completed:

| Cohort | Pairs | Score effect of removing length | Executable-utility effect |
|---|---:|---:|---:|
| Initial DeepSeek | 10 | Mean score 0.429 → 0.069 | 1/10 vs. 1/10 |
| Non-degenerate DeepSeek | 12 | Paired mean −0.308, CI [−0.381, −0.230] | +0.167, CI [0, 0.417] |
| Qwen3.7-Max | 20 | Paired mean −0.117, CI [−0.150, −0.084] | −0.05, CI [−0.25, 0.15] |

Across all 42 pairs, the stratified executable effect is +0.024 with interval [−0.095, 0.143]. Thus the causal measurement diagnosis transfers across model families, while the claim that deleting length improves utility does not.

### 1.3 Execution-aware retention did not pass confirmation

A reference-free executor was inserted into historical-answer retention:

- development: 1/8 executable successes versus 0/8 for the text heuristic;
- independent validation: 1/20 versus 0/20;
- confirmatory difference: +0.05, interval [0, 0.15], one-sided exact \(p=0.5\).

The development direction repeated, but the frozen confirmation rule failed.

### 1.4 Fixed candidate pools provide little selector headroom

The candidate audit executes the synthesized final and all 15 persisted round-agent outputs without using the reference answer. In the selected original/control arms:

| Cohort | Feasible runs | Final valid | Pool oracle valid | Headroom |
|---|---:|---:|---:|---:|
| DeepSeek X1 evolve | 13 | 2 | 2 | 0.000 |
| DeepSeek non-degenerate original | 12 | 6 | 7 | 0.083 |
| DeepSeek confirmatory text retention | 20 | 0 | 1 | 0.050 |
| Qwen original score | 20 | 11 | 12 | 0.050 |

The exploratory pooled result is 3/65 recoverable failures, or 0.046, with stratified-bootstrap interval [0, 0.108] and exchangeability-based Clopper–Pearson interval [0.010, 0.129].

The cross-model mechanism is a small task-relevant support, not necessarily literal text copying. Among 72 selected original/control runs, 38 contain no parseable canonical plan, 22 contain one, 8 contain two, and only 4 contain at least three.

## 2. Latest experiment: prospective candidate-pool enlargement

### 2.1 Design

Protocol 083 selected 28 untouched PlanCraft tasks with reference-plan length two:

- eight tasks for a frozen advancement gate;
- 20 tasks for the main experiment;
- one complete uncached temperature-0 trajectory per task;
- five independent complete uncached temperature-0.7 trajectories per task;
- five rounds and 16 candidate slots per trajectory;
- thinking disabled on every Qwen call path;
- canonical deduplication followed by reference-free executable validation.

The nested pool \(C_j\) contains the temperature-0 trajectory and stochastic trajectories 1 through \(j\). The primary comparison is \(C_5-C_1\), so it measures the effect of four additional independent trajectories on the same tasks.

### 2.2 Gate result

The gate passed:

- 48/48 valid trajectories completed all five rounds;
- all 48 recorded positive usage;
- mean support gain \(S_5-S_1=0.875\);
- 6/8 tasks had at least two canonical candidates in \(C_5\).

A provider payment interruption created nine persisted error traces. The integrity audit excluded all nine, including two with positive partial usage. After seven valid gate tasks, only the recorded-token cap was amended from 6.5M to 7.5M. At that point, the substantive gate result was mathematically irreversible; no task, condition, endpoint, threshold, or main-cohort definition changed.

### 2.3 Main result

All 20 main tasks and 120 trajectories completed successfully.

| Endpoint | \(C_1\) | \(C_5\) | Paired change | One-sided 95% lower bound |
|---|---:|---:|---:|---:|
| Mean unique canonical support | 1.85 | 2.85 | +1.00, CI [0.50, 1.60] | 0.60 |
| Executable oracle | 0.60 | 0.80 | +0.20, CI [0.05, 0.40] | 0.05 |
| Headroom over temperature-0 final | 0.10 | 0.30 | +0.20, CI [0.05, 0.40] | 0.05 |

Support increased on 12 tasks, and executable oracle improved on four. Decreases are impossible because the pools are nested. The previously reported sign-test \(p=0.000488\) and \(p=0.125\) values are therefore invalid and withdrawn: their equal-direction null contradicts the design. The bootstrap intervals remain useful for task-level estimation.

The support curve is monotone:

| Pool | Mean support | Executable oracle | Headroom |
|---|---:|---:|---:|
| \(C_1\) | 1.85 | 0.60 | 0.10 |
| \(C_2\) | 2.15 | 0.70 | 0.20 |
| \(C_3\) | 2.35 | 0.70 | 0.20 |
| \(C_4\) | 2.60 | 0.80 | 0.30 |
| \(C_5\) | 2.85 | 0.80 | 0.30 |

A standalone temperature-0.7 trajectory does not contain more canonical candidates than the temperature-0 trajectory: mean difference −0.05, interval [−0.35, 0.25], \(p=1\). The result is therefore driven by accumulating independent trajectories, not by raising temperature alone.

### 2.4 Zero-call trajectory decomposition

The 100 stochastic trajectories contain 57 trajectory-level successes, but they remain repeated observations nested within 20 tasks. They improve within-task characterization; they do not create 100 independent task samples.

The empirical \(\widehat p_i\) distribution is polarized: 5/20 tasks are at 0, 4/20 at 0.2, 2/20 at 0.8, and 9/20 at 1. Using these estimates, the anchor-inclusive plug-in oracle curve is 0.660, 0.700, 0.722, 0.738, and 0.751 for \(n=1\) through \(5\). Model-based extrapolations are 0.784 at \(n=10\) and 0.798 at \(n=20\).

The 0.80 asymptote is a finite-sample MLE plug-in result, not an identified hard ceiling. Zero successes in five stochastic trajectories has a one-sided 95% binomial upper bound of 0.451, so tasks with \(\widehat p_i=0\) may still have meaningful nonzero success probabilities. The observed flattening argues against spending the next budget on unchanged resampling, but it does not prove that 20% of tasks are structurally unreachable.

Rescue robustness is heterogeneous:

| Rescued task | Successful stochastic trajectories |
|---|---:|
| TEST0102 | 1/5 |
| TEST0105 | 1/5 |
| TEST0526 | 4/5 |
| TEST0361 | 1/5 |

Thus three rescues are fragile one-of-five discoveries, while one is a stable signal missed by \(C_1\).

Five stochastic final answers alone achieve oracle coverage 0.65. The temperature-0 full 16-slot trajectory achieves 0.55, the mean stochastic full trajectory achieves 0.57, and the 32-slot \(C_1\) pool achieves 0.60. In an equal-16-slot cached comparison, distributing slots across five trajectories gives expected oracle 0.626 versus 0.570 within one trajectory, difference 0.056, interval [0.016, 0.105]. Within this runtime, cross-restart coverage is therefore more valuable than additional within-trajectory slots on the cached surface. Every restart still uses the same three-agent runtime, and the unmatched comparisons consume different compute, so this is neither a single-agent comparison nor a compute-matched architecture result.

### 2.5 Compute cost

The positive result is expensive:

| Generation surface | Recorded tokens |
|---|---:|
| \(C_1\) | 4,807,489 |
| \(C_5\) | 14,430,644 |
| Increment from \(C_1\) to \(C_5\) | 9,623,155 |

\(C_5\) uses 3.0017 times the recorded tokens of \(C_1\). The current result therefore demonstrates that additional independent generation can expand executable support, but not that it does so efficiently.

### 2.6 Selector-level DP result

The enlarged candidates were cached, so the DP grid required no additional model calls. Using binary executable utility and the monotone exponential mechanism gives:

| \(\varepsilon\) | Expected executable validity |
|---:|---:|
| 0.5 | 0.512 |
| 1 | 0.575 |
| 2 | 0.682 |
| 4 | 0.779 |
| 8 | 0.800 |

The non-private \(C_5\) oracle is 0.80. At \(\varepsilon=4\), the selector retains approximately 97.4% of this oracle. This curve should be read through the project's signal theory: binary valid-versus-invalid executor utility has \(g_U=\Delta_c=1\), hence the maximum local \(\rho_U=1\), conditional on a mixed candidate pool. The curve is the expected closed-form consequence of that favourable signal, not a separately discovered privacy frontier.

Under candidate-score replacement adjacency, one candidate's clipped validity bit may change; candidate texts and all other utilities are trusted, and only the selected index/output is released. The beneficiary is an observer of the release, such as a downstream consumer or transcript reader, whose inference about an individual candidate's validity is bounded. The trusted selecting party already sees the candidates and utilities. The mechanism does not protect prompts, candidate text, memories, natural-language messages, or control flow.

## 3. What the Qwen enlargement experiment validates

It validates four claims:

1. The small fixed-pool headroom was not a universal task impossibility; changing generation can escape the realized-pool bound.
2. Independent trajectories causally enlarge task-relevant candidate support.
3. The enlarged support can produce additional executable solutions.
4. Once useful alternatives exist, private selection has a non-vacuous privacy–utility curve.

It does not validate:

1. a specifically multi-agent architectural advantage;
2. a compute-efficient generation method;
3. a non-nested hypothesis test for the executable gain;
4. end-to-end DP for the evolving system;
5. generalization beyond Qwen, PlanCraft, five rounds, and the fixed topology.

## 4. DeepSeek compute-matched restart-versus-repair gate

Protocol 090 prospectively compares two non-nested uses of added test-time compute on DeepSeek V4 Flash. Every task shares one temperature-0 full trajectory. If its candidate pool is already executable, both interventions succeed and stop. Otherwise, an independent temperature-0.7 full restart defines realized token budget \(B_i\), and direct executor-guided repair may generate candidates under the same cap.

All eight gate tasks completed, but five anchors already succeeded. Only three tasks were informative, below the frozen minimum of four, so the gate stopped and none of the 12 reserved main tasks ran. The other gate checks passed.

| Intervention-specific surface | Three anchor failures |
|---|---:|
| Independent restart success | 0/3 |
| Executor-guided repair success | 1/3 |
| Repair minus restart | +0.333, CI [0, 1] |
| Exact paired test | \(p=1\) |

The one rescue succeeds on its first 1,008-token repair call while its 157,910-token matched-budget restart fails. This is a one-task existence proof for an inexpensive directed rescue, not a multiplicative efficiency estimate. TEST0030 and TEST0535 both exhaust 80 repairs without success. Their task-specific raw modal invalid outputs occur in 69/80 (86.25%) and 76/80 (95%) calls. Semantic normalization raises TEST0030's concentration to 78/80 (97.5%); the call-weighted raw and semantic modal shares over both exhausted tasks are 90.625% and 96.25%. Total use is 736 calls and 1,642,567 tokens: 1,081,254 anchor, 458,662 restart, and 102,651 repair tokens.

An operational correction is retained transparently. The first two direct repair calls produced empty visible answers because the direct path did not explicitly disable hidden thinking. Both calls and 3,768 tokens remain included. Subsequent direct calls use the same explicit non-thinking setting as the full runtime. This correction restored visible answers but did not prevent semantic collapse.

## 5. The largest current difficulty

The largest scientific difficulty is now **task-level response collapse: stochastic decoding on selected hard tasks often fails to create useful candidate support**.

The nested support and executable contrasts admit estimation but not sign tests: negative changes are excluded by construction. The corrected evidence is therefore the estimated +1.00 support gain [0.50, 1.60], the +0.20 oracle gain [0.05, 0.40], and the rescue decomposition showing that three of four rescues occur in only 1/5 stochastic trajectories.

The Qwen result shows that independent trajectories enlarge support, but \(C_5\) triples the token budget. The DeepSeek follow-up does not establish a more efficient method: it stopped with only three informative failures. It does, however, directly observe the concentration mechanism on both exhausted tasks. The 86.25%--95% range is descriptive over two task units, not a population estimate; TEST0181 stops after one draw, and earlier disjoint DeepSeek cohorts lack comparable repeated-repair samples. The current data support the statements:

> Independent generation expands candidate support and can make private selection consequential.

> On two observed failures, direct generation exhibits task-level response collapse; on a third task, executor-guided repair succeeds on the first draw.

They do not support the stronger statement:

> The proposed architecture is a compute-efficient or specifically multi-agent solution.

This is now the central issue that should be foregrounded rather than hidden. It is an empirical model-behaviour bottleneck, not a mismatch between the observed results and the selector-DP theory: when a mixed candidate pool exists, the binary executor signal still has \(\rho_U=1\).

## 6. Recommended next step

Do not run the frozen 12-task main cohort, scale the unchanged repair prompt, or begin a repair redesign before the submission deadline. The highest-value action is now paper completion. The stopped DeepSeek gate belongs in the main mechanism section, not merely the limitations: it is the failed obvious efficiency remedy that exposes task-level response collapse. The Qwen support-enlargement result remains the constructive escape. Any tool-augmented or duplicate-aware repair redesign should be deferred to future work because it would constitute a new method requiring its own frozen development and validation cycle.

A further 30-task \(C_5-C_1\) replication is no longer the first recommendation. It would repeat a nested contrast for which the proposed sign test is invalid, while the zero-call dose-response already suggests saturation near 0.80. Independent replication remains useful for external validity, but it does not resolve the compute attribution problem.

No further unchanged length-zero ablation or fixed-pool selector experiment is recommended. Those questions are already empirically resolved.

## 7. Current paper position

The paper now has a defensible ICLR arc:

1. audit the persistent privacy channel;
2. show that the obvious score privatization target is causally length-dominated;
3. measure the tight realized-pool bound that explains failed selection methods;
4. prospectively expand the support;
5. show that private selection becomes meaningful only after that expansion;
6. show task-level response collapse as the mechanism that makes stochasticity on selected hard tasks ineffective; and
7. quantify the compute price and remaining uncertainty.

This is stronger than the previous purely negative audit framing. The principal weaknesses are the simplicity of the intervention, its 3× token cost, the fragile one-of-five basis of three rescues, a stopped rather than successful compute-matched method gate, and the absence of end-to-end privacy. The new gate nevertheless improves credibility because it reports the failure of the obvious efficiency remedy instead of silently omitting it.

## Artifact pointers

- Candidate-pool protocol: research/configs/qwen-candidate-pool-enlargement-protocol-083.json
- Complete source artifact: research/artifacts/iclr2027-qwen-candidate-pool-enlargement-084.json
- Final decision artifact: research/artifacts/iclr2027-qwen-candidate-pool-enlargement-decision-085.json
- Corrected inference protocol: research/configs/qwen-candidate-pool-trajectory-reanalysis-protocol-087.json
- Corrected trajectory reanalysis: research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json
- Reanalysis closure manifest: research/manifests/iclr2027-qwen-candidate-pool-reanalysis-closure-089.json
- DeepSeek compute-matched protocol: research/configs/deepseek-compute-matched-generation-protocol-090.json
- DeepSeek stopped gate source: research/artifacts/iclr2027-deepseek-compute-matched-generation-091.json
- DeepSeek zero-call gate analysis: research/artifacts/iclr2027-deepseek-compute-matched-generation-gate-analysis-092.json
- DeepSeek conditional-collapse analysis: research/artifacts/iclr2027-deepseek-conditional-collapse-analysis-094.json
- Closure manifest: research/manifests/iclr2027-qwen-candidate-pool-enlargement-closure-086.json
- Main paper draft: iclr2027-paper-draft.md
- Experimental appendix: iclr2027-paper-appendix.md
- Candidate-pool figure: research/figures/qwen-candidate-pool-enlargement.png

## 8. October 1 X2 screening update

The nine-task PlanCraft X2 screening slice is now complete at 72 canonical cells (9 tasks × 8 arms), but it remains a screening diagnostic rather than a confirmatory architecture result. The dominant failure surface is output-contract and dependency-chain execution: only 12/72 raw cells are exact, and a uniform reference-free finalizer raises this to 26/72 only by normalizing impossible-task outputs; action-list tasks remain 10/56.

Two controls were then run to separate finalization failure from tool coverage. A complete deterministic recipe-search wrapper was implemented and unit-tested (136/136 tests), exposing all recipe alternatives and output counts. A task-only DeepSeek finalizer that excluded all saved candidate evidence still failed the TEST0011 smoke by omitting the intermediate `warped_planks` action. A minimal output-semantics amendment requiring one array element per recipe execution and prerequisite ordering produced the same failure. Thus the remaining bottleneck is multi-step dependency/action-sequence planning under the current model, not historical evidence contamination or incomplete recipe coverage. The 72-cell complete-tool gate was stopped before expansion; artifacts 120--121 are retained.

This update does not strengthen the multi-agent claim. It strengthens the audit: the current X2 trace does not support interpreting small arm differences as architectural gains until a prospective, end-to-end action-sequence treatment is separately designed and validated. DeepSeek remains the primary model; no Qwen calls were used in this screening continuation.

## 9. Structured planner control

Protocol 122 tested a one-cell structured action-sequence planner on TEST0011/A1. The model was required to produce a dependency ledger with one object per recipe execution, including inputs and output counts, after consulting the complete recipe tool. It used three provider calls and 2,563 tokens, but returned prose plus an embedded JSON fragment rather than parseable JSON. More importantly, it declared the task impossible by counting only the birch and jungle planks and failed to use the valid `warped_hyphae -> warped_planks x4` route.

This rules out treating the residual problem as serialization alone. The immediate bottleneck is composition of equivalent-material dependencies and state transitions. A larger prompt-only structured-planner cohort is therefore not justified; any next method experiment needs explicit state verification or symbolic planning and a new frozen protocol.

## 10. Reference-free symbolic baseline

Protocol 123 ran a zero-call bounded breadth-first search over the public PlanCraft recipe transitions on the nine completed X2 instances. It found plans for 7/9 tasks and they pass the repository's reference-free sequence validator, but discovery and that validator share the same transition implementation, so this is not independent execution evidence. Five exactly matched the benchmark's canonical action list; two more (TEST0014 and TEST0139) used valid alternative plank choices and were subsequently checked by environment replay.

The solver resolves TEST0011 as `[paper, warped_planks, cartography_table]`, including the `warped_hyphae -> warped_planks x4` dependency that the DeepSeek finalizers missed. A separate concrete environment replay reaches the target for all seven solver-found plans. The two impossible-reference tasks exhausted the bounded search, which is not a formal impossibility proof. This baseline therefore separates task/tool executability from model planning failure, with the shared recipe-registry limitation made explicit.

The broader replay audit of all 72 original X2 cells finds 10 target-reaching outputs, exactly the 10 executable action-list exact matches; no non-exact output becomes a replay witness. The finalizer also has 10 witnesses, so its additional exact matches are impossible-task normalization only.
## 11. State-verified step planner (exploratory)

Protocols 125--126 changed the treatment from free-form plan generation to stepwise action selection. At each step, a local verifier exposed only currently applicable recipe outputs, applied accepted transitions to the inventory state, and rejected premature termination. After a verifier-feedback retry, TEST0011 reached the target in five DeepSeek calls with paper -> stick -> warped_planks -> cartography_table; the redundant stick made it non-canonical, but concrete environment replay confirmed execution.

The exploratory extension to the other eight A1 tasks used 62 calls and 16,386 tokens. Across all nine tasks, 4/9 trajectories reached and replayed to the target, while the original A1 arm had 1/9 exact cells; 3/9 treatment plans were canonical exact. The remaining failures were mostly irrelevant action cycles. Since TEST0011 was chosen for the smoke and the other tasks were added after its positive result, this is not confirmatory evidence or a multi-agent architecture claim. It does, however, identify state-verified step selection as a plausible next method rather than another prompt-only finalizer.

## 12. Goal-filtered state verification

Protocol 130 added a backward dependency-closure filter to the step planner, so the model saw only currently applicable outputs that can contribute to the target's recipe closure. Across all nine A1 tasks, it used 48 calls and 11,052 tokens, reached and replayed 5/9 tasks, and produced 5/9 canonical exact plans. This compares with 1/9 original A1 exact and 3/9 exact for the unfiltered step treatment. TEST0014 and TEST0139 still cycle between redstone and redstone_block, while TEST0057 cycles over wool/carpet and TEST0069 has no goal-relevant action. The result is exploratory method evidence, not a causal multi-agent claim; next improvement would require a shortest-path/state-distance constraint.

## 13. Bounded state-distance filtering

Protocol 132 added finite-depth reachability lookahead. Across the nine A1 tasks, it used 48 calls and 10,943 tokens, reached and replayed 7/9 tasks, and produced 4/9 canonical exact plans. The extra replay-valid cases are TEST0014, TEST0139, and TEST0122, whose plans contain redundant or alternative valid actions. TEST0057 still cycles over wool/carpet and TEST0069 has no reachable action under the bound. Artifact 133 compares all variants; this is still post-hoc method-development evidence rather than a causal multi-agent result.
## 14. Minimum-distance action filtering

Protocol 134 retained only actions with the minimum finite post-action distance to the target. It used 43 calls and 9,344 tokens, reached and replayed 7/9 tasks, and produced 6/9 canonical exact plans—the strongest exploratory treatment so far. TEST0011, TEST0014, TEST0095, TEST0097, TEST0115, and TEST0122 are exact; TEST0139 is executable but non-canonical; TEST0057 and TEST0069 remain failures. Artifact 135 records the comparison against all earlier variants. This remains post-hoc method-development evidence, not a causal multi-agent result.

## 15. Bounded no-plan termination

Protocol 136 added a bounded symbolic pre-check: only exhaustive search within depth 12 and 50,000 states can trigger IMPOSSIBLE; otherwise the minimum-distance planner runs unchanged. The nine-task run used 35 calls and 7,779 tokens. All 7 feasible-reference tasks reached the target in concrete replay, with 5/7 canonical exact and 2/7 executable alternatives. Both impossible-reference tasks triggered the bounded stop, so evaluator exact is 7/9. Artifact 137 keeps the distinction explicit: bounded no-plan is not a global impossibility proof. This is the strongest exploratory treatment so far, still not a causal multi-agent result.

## 16. Held-out validation

The pre-frozen cohort contained unused tasks in all three PlanCraft strata. Protocol 138 selected three remaining impossible, three multi-step, and three long tasks before inspecting outputs and applied the same planner with an eight-step cap. It reached 3/6 feasible tasks because the long tasks were truncated. Protocol 139 amended only the cap to 12 and reran the same nine tasks: all 6/6 feasible tasks reached the target in concrete replay, 4/6 were canonical exact, and 2/6 were executable alternatives; all 3/3 impossible tasks triggered bounded stops. Overall evaluator exact was 7/9 at 41 calls and 9,087 tokens. This is the first held-out validation of the post-hoc planner, with bounded impossibility and single-benchmark scope retained as limitations.
 
## 17. Held-out replication batch

Protocol 141 repeated the unchanged 12-step treatment on a second nine-task batch, frozen before output inspection. It again reached 6/6 feasible tasks in concrete replay, produced 4/6 canonical exact plans and 2/6 executable alternatives, and triggered bounded stops on all 3/3 impossible tasks (7/9 evaluator exact; 37 calls; 8,514 tokens). Pooling the two held-out batches gives 12/12 feasible replay-valid tasks, 8/12 feasible canonical exact plans, 6/6 bounded impossible stops, and 14/18 overall evaluator exact across 18 tasks (78 calls; 17,601 tokens). Artifact 142 records the pooled analysis. This strengthens within-benchmark method validation, but remains a single-model diagnostic rather than a causal multi-agent result.

## 18. BrowseComp dependency gate

A final no-call check confirmed that the BrowseComp-Plus dataset and environment sources are present, but the project environment cannot import `transformers`, `torch`, `faiss`, `faiss_cpu`, or `sentence_transformers`, and no frozen Qwen embedding/FAISS index is present. Artifact 143 closes this gate as unavailable for the current X2 screening. BrowseComp is therefore not silently replaced with another retrieval stack; the completed X2 evidence remains PlanCraft-only and is explicitly scoped as such.
