# Current Progress, Core Challenges, and Recommended Next Steps

**Project:** Privacy and utility auditing for test-time evolving LLM multi-agent systems  
**Target:** ICLR 2027  
**Status date:** 1 October 2026

> **Current checkpoint (1 October 2026).** The anonymous ICLR source package is locked as `research/manifests/iclr2027-submission-source-169.zip` (10 files, 16-page PDF, independently compiled with text-identical output). The held-out X2 diagnostic has now been decomposed with a zero-call symbolic control (artifact 149), historical component attribution (artifact 153), branch-level attribution (artifact 158), exact descriptive intervals (artifact 161), and a completed live DeepSeek component control (artifact 164). Artifact 166 independently checks the live numbers, manuscript text, rendered PDF, and source archive with zero provider calls; artifact 167 audits the main-conference claim-evidence matrix and reviewer risks; artifact 170 cross-checks the headline numbers between manuscript and frozen artifacts. The frozen 18-task unfiltered DeepSeek control (protocol 152) completed 142 provider calls and 43,623 tokens: replay was 8/12 on feasible tasks versus 12/12 for symbolic-only, while canonical exactness was 5/12 versus 8/12. Artifact 156 remains the historical no-call gate record and artifact 160 remains the static protocol audit. Submission-integrity and paper-claim audits pass, and the test suite has 142 passing tests.

> **Timing note (1 October 2026).** The official ICLR 2027 schedule lists the abstract deadline as 18 September 2026 AOE and the full-paper deadline as 25 September 2026 AOE. The local package is technically submission-ready, but the author must first confirm whether it was uploaded before the deadline; if not, the next action is venue selection rather than a late ICLR upload.

## Executive summary

The project now has both a coherent **class-level diagnostic bound** and prospective evidence for the intervention that escapes it. The fixed-pool bound remains the conceptual center, while the candidate-pool enlargement experiment supplies the missing constructive step.

The strongest empirical finding is that the released TacoMAS contribution score is substantially controlled by its output-length component. Removing that component sharply reduces the recorded score on both DeepSeek V4 Flash and Qwen3.7-Max. This effect is prospective, causal, and cross-model. However, removing the length term does not reliably improve executable task performance. The DeepSeek replication yielded a positive but uncertain point estimate, whereas the larger Qwen replication yielded a slightly negative point estimate; both uncertainty intervals include zero.

The privacy motivation is also weaker than originally expected. A functioning persistence-aware canary instrument did not detect post-input persistent leakage in the audited five-round setting. Positive controls and state-mutation measurements show that this null result is not caused by a broken extractor or an entirely inert runtime, but the sample is too small to exclude low-frequency leakage.

The zero-call candidate-recoverability audit showed that most failed runs lacked a correct executable intermediate candidate. Fixed-pool selector headroom is 0--8.3 percentage points across four original/control cohorts, and the exploratory pooled estimate is 3/65=4.6 points. A new prospective experiment then changes the candidate support rather than optimizing the same selector. On 20 untouched Qwen tasks, expanding from one to five independent stochastic trajectories increases unique canonical support by 1.00 plans, interval [0.50, 1.60], and raises the executable oracle from 0.60 to 0.80, paired difference 0.20 [0.05, 0.40]. The originally reported nested sign-test \(p\)-values are withdrawn because decreases are impossible by construction.

The largest challenge has therefore shifted again after the DeepSeek compute-matched gate. Five of eight shared anchor pools succeeded, leaving only three informative failures and forcing the frozen gate to stop. Repair produced the only intervention-specific rescue (1/3 versus 0/3), but there was only one discordant pair and exact paired \(p=1\). The two exhausted repair branches repeated one task-specific invalid raw answer in 86.25% and 95% of 80 calls. The central mechanism is task-level response collapse, while the comparative-method gap is adequate non-nested information; neither is a mismatch with the selector-DP theory.

The X2 held-out attribution now limits the apparent LLM choice surface: only 7/78 cached accepted requests exposed multiple options, four step mismatches occurred in two replay-valid tasks, and 10/12 feasible plans matched the symbolic sequence exactly. Exact 95% intervals are recorded in artifact 161, but are descriptive for this fixed cohort rather than causal or population estimates.

## 1. What has been completed

### 1.1 Persistence-aware leakage audit

The project implemented a persistent-state canary audit over a frozen TacoMAS runtime and PlanCraft tasks. The audit distinguishes direct input echo from post-input persistence and includes a depth-matched reset control.

The initial leakage study completed 60 runs across 20 three-arm instance blocks. No exact or preregistered five-token partial canary exposure was detected after the direct-input round in any arm. The preregistered 120-instance replication has now completed all 360 cells, with 0/120 exposure in both evolve and depth-matched-reset arms, 0/120 false positives in no-canary, and 0/40 evolve exposures in each stratum. The paired evolve-minus-reset exposure difference is zero with exact two-sided McNemar $p=1$.

Several checks establish that the instrument was operational:

- A channel-complete deterministic positive control recovered canaries from all 7/7 declared persistent-state channels.
- A live round-2 memory-injection control recovered the injected canary at a later checkpoint.
- Observable state changed in 617/720 comparable agent transitions in the original study.
- The non-degenerate replication also showed substantial serialized-state mutation and nonempty slow-loop feedback.

The correct conclusion is therefore **failed to detect persistent exposure under the frozen setting**, not “the system does not leak.” The completed replication lowers the evolve-arm one-sided 95% upper bound to 2.5%, but it remains limited to one model, one canary family, one five-round horizon, and fixed topology. It does not rule out rare leakage outside this design.

### 1.2 Score-validity diagnosis

The released contribution score assigns 85% weight to output length. Cached analysis initially showed that high scores frequently occur in failed runs, although a corrected base-rate-aware analysis found mild ranking value rather than complete score inversion. The maximum-score AUC is 0.755, with an instance-cluster interval of [0.651, 0.853].

The more important evidence is causal. Three prospective cohorts tested the removal of the length term:

1. **Initial DeepSeek paired intervention, 10 pairs.** Mean score fell from 0.429 to 0.069, and observations at least 0.8 fell from 33 to zero. Exactness remained 1/10 in both arms.
2. **Non-degenerate DeepSeek replication, 12 pairs.** Mean paired score changed by -0.308, with a 95% interval of [-0.381, -0.230]. Exactness was 8/12 for length-zero and 6/12 for original scoring, but the paired difference of +0.167 had interval [0, 0.417] and one-sided exact \(p=0.25\).
3. **Qwen3.7-Max cross-model replication, 20 pairs.** Mean score fell from 0.157 to 0.040. The paired change was -0.117, with interval [-0.150, -0.084], and all 20 paired scores decreased. Exactness was 10/20 for length-zero and 11/20 for original scoring, producing a paired difference of -0.05 with interval [-0.25, 0.15].

The robust conclusion is that **output length causally controls the score scale across two model families**. The unsupported conclusion is that simply deleting the length term improves task utility.

### 1.3 Attempted working method: execution-aware retention

The project implemented a reference-free PlanCraft executor and inserted its signal into historical-answer retention.

- In an eight-pair development study, execution-aware retention achieved 1/8 executable-valid final answers versus 0/8 for the text heuristic.
- In a separately frozen 20-pair validation study, it achieved 1/20 versus 0/20.
- The confirmatory paired difference was +0.05 with interval [0, 0.15] and one-sided exact \(p=0.5\).
- Both validation arms produced 14/20 malformed final answers.

The development direction repeated, but the independent confirmatory rule failed. The method remains an instrumented architectural hypothesis, not an established utility improvement.

### 1.4 Qwen3.7-Max cross-model validation

The Qwen experiment used the dated `qwen3.7-max-2026-06-08` snapshot with thinking disabled on all worker, meta-controller, synthesis, and judge calls. The initial length-two gate achieved 5/8 exact, within the preregistered 30%–70% healthy window. The study therefore proceeded to all 20 paired main instances without fallback-tier or post-hoc subgroup search.

All 40 main cells completed five rounds. The principal results were:

| Endpoint | Original score | Length-zero | Paired result |
|---|---:|---:|---:|
| Executable exact | 11/20 | 10/20 | -0.05, 95% CI [-0.25, 0.15] |
| Malformed final | 5/20 | 8/20 | +0.15 |
| Mean contribution score | 0.157 | 0.040 | -0.117, 95% CI [-0.150, -0.084] |
| Score observations \(\geq 0.8\) | 8/300 | 0/300 | -0.40 per pair, 95% CI [-0.80, -0.05] |

This experiment validates that the score-scale diagnosis is not a DeepSeek-specific accident. It also prevents overinterpretation of the earlier DeepSeek +2/12 utility difference: the Qwen utility direction reverses, and neither model's interval excludes zero.

The runtime tracker recorded at least 2,292 calls and 4,416,267 input-plus-output tokens across 41 of the 48 Qwen gate and main cells. Seven completed cells contain full five-round trajectories but empty usage objects, so this figure is explicitly a recorded lower bound rather than complete cost accounting.

### 1.5 Intermediate-candidate recoverability audit

Before inspecting cached candidate content, the project froze a zero-call audit over all 40 Qwen main cells. Each run contributed 15 persisted round-agent outputs plus one synthesized final answer. Candidate texts were evaluated using the deterministic, reference-free PlanCraft executor. Reference-trace equality was retained only as an offline secondary diagnostic.

The audit separated four failure types:

- **Final success:** the synthesized final answer is executable-valid.
- **Finalization failure:** the final is invalid, but a valid candidate exists in round 5.
- **Selection or retention failure:** the final is invalid, no round-5 candidate is valid, but a valid candidate exists in rounds 1–4.
- **Generation failure:** neither the final nor any round-agent candidate is valid.

Results:

| Arm | Final valid | Round-candidate oracle | Recoverable failed final | Generation failure | Duplicate slots |
|---|---:|---:|---:|---:|---:|
| Original score | 11/20 | 12/20 | 1/20 | 8/20 | 259/320 |
| Length-zero | 10/20 | 11/20 | 1/20 | 9/20 | 263/320 |

The semantic oracle gap is only 0.05 in each arm, with interval [0, 0.15]. Reference-exact analysis gives identical counts. No failed run contains a valid round-5 candidate, so no case qualifies as a finalization failure under the frozen taxonomy.

The original-score arm contained only 1/20 recoverable failures, below the preregistered 4/20 threshold for developing an execution-gated selector. Consequently, the selector/retention route was stopped without further API use.

### 1.6 Cross-cohort selector headroom and diversity extension

The same frozen candidate surface and deterministic executor were applied, without new model calls, to three cached DeepSeek cohorts:

| Cohort and original/control arm | Feasible runs | Final valid | Candidate-pool oracle | Headroom | 95% CI |
|---|---:|---:|---:|---:|---:|
| DeepSeek X1 evolve | 13 | 2 | 2 | 0.000 | [0, 0] |
| DeepSeek non-degenerate original evolve | 12 | 6 | 7 | 0.083 | [0, 0.25] |
| DeepSeek confirmatory text retention | 20 | 0 | 1 | 0.050 | [0, 0.15] |
| Qwen original score | 20 | 11 | 12 | 0.050 | [0, 0.15] |

The oracle includes the realized final answer plus all 15 persisted round-agent candidates. It therefore weakly dominates the current finalizer. On each audited run,

\[
H_i = \max_{c \in \mathcal{C}_i} U(c)-U(f_i)
\]

is an exact upper bound on improvement by any selector whose output must belong to the realized candidate pool \(\mathcal{C}_i\). Any private exponential-mechanism or noisy-score selector over that same support is included in this class. The result does not constrain a method that changes \(\mathcal{C}_i\) through regeneration, repair, or new tool interaction.

An outcome-aware exploratory synthesis across the four original/control arms contains 3 recoverable failures in 65 feasible runs: empirical headroom 0.046, stratified bootstrap interval [0, 0.108], and exchangeability-based two-sided Clopper--Pearson interval [0.010, 0.129]. This synthesis was selected after cohort-specific results were inspected and is therefore reported as exploratory, not preregistered confirmation. The cohort-specific bounds remain the primary evidence. In the 20-task confirmatory cohort, cached-pool headroom and the online execution-aware-minus-control point estimate are both 0.05; this is descriptive convergence, not an independently powered mediation result.

Candidate diversity requires a two-level interpretation. Qwen exhibits 81%--82% exact-text duplicate slots and only about three distinct strings per 16-slot run. This literal-copy mechanism does **not** transfer to DeepSeek, whose exact-text duplicate rates are much lower, approximately 7%--27% depending on cohort and arm. However, task-relevant canonical diversity is low in both families. Among the 72 selected original/control runs, 38 contain zero distinct parseable canonical plans, 22 contain one, 8 contain two, and 4 contain at least three. The DeepSeek arms average only 0.45--0.75 such plans per run, and Qwen original scoring averages 1.05. Among parseable slots, canonical duplicate rates are roughly 73%--91%. The cross-model claim should therefore be "a small effective support of parseable plans," not "all agents are near-identical text copies."

### 1.7 Stratified synthesis of the three length interventions

The three paired length-ablation cohorts contain 42 pairs in total. A stratified paired bootstrap, resampling within cohort, gives:

- pooled length-zero-minus-original exact difference: +0.0238;
- 95% interval: [-0.0952, +0.1429];
- length-zero-only versus original-only successes: 4 versus 3;
- two-sided exact discordant-pair \(p=1.0\).

The interval includes zero and excludes positive average improvements larger than 14.3 percentage points under this stratified empirical synthesis. Cohort effects remain heterogeneous in direction: 0 in the initial DeepSeek cohort, +0.167 in the DeepSeek non-degenerate cohort, and -0.05 in Qwen. The DeepSeek-nondegenerate-minus-Qwen contrast is +0.217, but its bootstrap interval [-0.067, 0.533] is too wide to establish model heterogeneity.

This is more informative than three isolated non-significant estimates: the average observed benefit is near zero and large positive mean effects are not supported. It should still be labeled a secondary outcome-aware synthesis rather than a single prospectively randomized 42-pair trial.

### 1.8 Does the length term act as a completeness proxy?

The cached logs do not support a simple cross-model completeness story.

- In the initial DeepSeek original arm, the mean released length component is 0.779 for well-formed finals and 0.332 for malformed finals; AUC for predicting a well-formed final is 0.938.
- In the non-degenerate DeepSeek original arm, the corresponding means are 0.598 and 0.138; AUC is 1.0.
- In Qwen original scoring, the direction reverses: means are 0.110 for well-formed and 0.213 for malformed finals; AUC is 0.133.
- Removing length changes malformed rate by 0 in the initial DeepSeek cohort, -0.167 in the non-degenerate DeepSeek cohort, and +0.15 in Qwen.

A pooled cohort-fixed-effect linear-probability analysis is positive, but the opposite Qwen direction and opposite paired malformed effects prevent a model-robust causal completeness claim. The defensible formulation is that length is a dominant, model-dependent formation proxy rather than a validated semantic-quality signal. Deleting it predictably collapses the score scale, but its output-formation consequences are heterogeneous.

### 1.9 Prospective enlargement of the candidate pool

Protocol 083 selected 28 untouched reference-length-two tasks before any output was inspected. Each task ran one uncached temperature-0 trajectory and five independent uncached temperature-0.7 trajectories. Candidate unions were nested: \(C_1\) contains the baseline and first stochastic trajectory, while \(C_5\) contains the baseline and all five stochastic trajectories.

The eight-task gate passed with mean support gain 0.875, six tasks with at least two \(C_5\) candidates, 48/48 complete five-round trajectories, and 48/48 positive usage records. The 20-task main result is:

| Endpoint | \(C_1\) | \(C_5\) | Paired \(C_5-C_1\) result |
|---|---:|---:|---:|
| Mean unique canonical plans | 1.85 | 2.85 | +1.00, 95% CI [0.50, 1.60], one-sided lower bound 0.60 |
| Executable oracle | 0.60 | 0.80 | +0.20, 95% CI [0.05, 0.40], one-sided lower bound 0.05 |
| Headroom over temperature-0 final | 0.10 | 0.30 | +0.20, 95% CI [0.05, 0.40], one-sided lower bound 0.05 |

A standalone temperature-0.7 trajectory does not improve support over temperature 0: mean difference -0.05, interval [-0.35, 0.25], \(p=1\). The result is therefore about accumulating independent trajectories, not merely increasing temperature. \(C_1\) costs 4.81M recorded tokens and \(C_5\) costs 14.43M, so the 20-point oracle gain requires 9.62M additional tokens and a 3.00-fold total budget.

Post-hoc DP uses only cached candidates. With binary reference-free executor utility, the monotone exponential mechanism reaches expected validity 0.512, 0.575, 0.682, 0.779, and 0.800 at \(\varepsilon=0.5, 1, 2, 4,\) and \(8\), compared with the non-private \(C_5\) oracle of 0.80. This validates that DP selection is no longer vacuous once generation supplies useful support; it remains selector-level privacy, not end-to-end DP.

The corrected zero-call decomposition finds 57 successful stochastic trajectories among 100, while preserving 20 tasks as the independent unit. Three of the four \(C_5\)-only rescues succeed in 1/5 stochastic trajectories; one succeeds in 4/5. The anchor-inclusive plug-in curve reaches 0.751 at \(n=5\), 0.784 at \(n=10\), and 0.798 at \(n=20\), suggesting saturation near the observed 0.80. Five stochastic finals alone achieve 0.65 oracle coverage. At a matched 16-slot count, cross-trajectory coverage is 0.626 versus 0.570 within one trajectory, interval [0.016, 0.105]. This is a cross-trajectory comparison within the same three-agent runtime, not a multi-agent causal test.

The operational record is intentionally visible. Nine provider-error traces were excluded by a content integrity audit. After seven gate tasks, only the gate token cap was raised from 6.5M to 7.5M; the substantive pass was already mathematically irreversible, and all tasks, conditions, endpoints, thresholds, and the main budget remained frozen.

### 1.10 DeepSeek compute-matched generation gate

Protocol 090 prospectively compares an independent full restart with direct executor-guided repair under the restart's realized token cap. All eight gate tasks completed. Five shared anchors already contained an executable plan, so only three tasks were informative against the frozen requirement of four. The gate stopped and none of the 12 reserved main tasks ran.

Conditional on anchor failure, independent restart succeeded on 0/3 and repair on 1/3. The difference is +0.333 with bootstrap interval [0, 1] and exact paired \(p=1\). The five symmetric anchor successes are not part of the intervention-specific estimand. The sole rescue succeeded on its first 1,008-token repair call while its 157,910-token matched-budget restart failed; this is an existence proof, not a multiplicative efficiency ratio.

The two common failures expose task-level response collapse. TEST0030 returned the identical raw `["IMPOSSIBLE"]` string on 69/80 repairs (86.25%); after semantic normalization, 78/80 calls (97.5%) express impossibility. TEST0535 returned `["redstone_torch"]` on 76/80 (95%) and repeatedly omitted the required `redstone` intermediate. The call-weighted raw modal share is 90.625%. These are 160 calls but only two failed task units; the successful branch has one draw, so success-conditioned concentration is not estimable. Total cost was 736 calls and 1,642,567 DeepSeek tokens. Qwen calls were zero. The first two direct calls exposed empty visible text before the direct path was aligned with the runtime's explicit non-thinking setting; those calls and costs remain in the official record.

## 2. The main difficulties

### 2.1 The largest difficulty: task-level response collapse

The project has prospective evidence that changing generation expands selector headroom, while the DeepSeek follow-up shows why the obvious executor-guided repair remedy is not reliable. \(C_5\) uses three times the recorded tokens of \(C_1\); repair succeeds immediately once but concentrates on the same invalid answer in 86.25%--95% of calls on both exhausted tasks. Together with the matched-slot 0.626-versus-0.570 result, this supports a mechanistic interpretation: useful diversity comes from resampling context, not merely the stochastic token stream. The present two-task diagnostic does not causally isolate conditioning, and the gate lacks its fourth informative task. The evidence therefore establishes neither a compute-efficient architectural innovation nor a uniquely multi-agent benefit.

The paper must make three scopes unmistakable:

1. The upper bound is exact on the realized candidate pool.
2. Its population uncertainty remains nontrivial in individual cohorts.
3. It applies to selectors over fixed persisted candidates, not to methods that generate new candidates.

A conventional ICLR paper is often easiest to defend when it has the following arc:

1. identify a consequential phenomenon;
2. show why an obvious solution fails;
3. introduce a method that fixes the problem;
4. demonstrate the improvement across credible settings.

The present paper supports a phenomenon-to-failed-remedy-to-bounded-escape arc: persistent exposure and score validity are audited; the fixed-pool selector class is directly bounded; independent generation expands support; and the obvious direct-repair efficiency remedy fails its advancement gate. The challenge is to state the constructive result at the right strength while treating repair as a transparent negative diagnostic.

### 2.2 No detected leakage event

The original privacy narrative anticipated memorization into persistent evolved state. The audit instead observed zero post-input exposures. This is scientifically useful because it prevents an unsupported threat claim, but it weakens a paper centered on discovering and mitigating a new privacy channel.

The result is not evidence of universal non-leakage. It is limited by:

- one synthetic canary family;
- one injection position;
- a five-round horizon;
- fixed topology and disabled structural mutation;
- limited statistical power;
- leakage testing on the primary model setting rather than a full cross-model matrix;
- state scanning rather than adaptive black-box extraction against every checkpoint.

The leakage branch therefore remains a functioning but underpowered null result.

### 2.3 Generation remains the bottleneck, but it is now experimentally actionable

The candidate audit substantially narrows the engineering problem. In most failed Qwen runs, no persisted agent output ever reaches the task target. A selector cannot recover a candidate that was never generated.

This invalidates the most economical hypothesis of simply placing a deterministic executor after the existing fixed pool: that route could rescue only one observed failed final per arm. The enlargement experiment confirms the stronger causal response. Adding independent trajectories raises \(C_5\) headroom to 0.30 and the oracle by 0.20 relative to \(C_1\).

The new difficulty is efficient diversity. Brute-force independent generation works, but consumes 9.62M incremental tokens on 20 tasks. The first executor-guided repair gate stopped and showed severe duplicate invalid outputs. A future redesign would need explicit recipe evidence, action-name normalization, and duplicate rejection before any new prospective comparison. These are optimization directions, not prerequisites for reporting the completed result.

### 2.4 Limited external validity

The score intervention now spans DeepSeek V4 Flash and Qwen3.7-Max, which is an important improvement. However, the broader conclusions remain scoped to:

- TacoMAS as the evolving-agent runtime;
- PlanCraft as the executable benchmark;
- five fast rounds;
- a fixed three-agent topology;
- disabled structural edits;
- a single Qwen snapshot and a single primary leakage-model setting.

The Qwen experiment cross-validates the score diagnosis, not the leakage null or an end-to-end DP mechanism.

### 2.5 Theory is consistent with the evidence but remains diagnostic

The theory is not contradicted by the experiments. The utility-relevant signal-to-sensitivity ratio

\[
\rho_U = \frac{g_U}{\Delta_c}
\]

formalizes the idea that privacy calibration is meaningful only when the released score has a stable causal gap in semantic utility. If \(g_U=0\), changing \(\varepsilon\) cannot restore utility; if \(g_U\) is small or unstable, useful private discrimination requires a large privacy budget.

The experiments support this diagnosis. The score moves strongly when length is removed, while the paired utility effect is small, uncertain, and changes direction across models. The limitation is that this theory currently explains a stop condition rather than yielding a new algorithm with demonstrated gains. It is therefore a principled theoretical lens, but not yet a standalone positive theoretical-method contribution.

### 2.6 Operational and reporting limitations

Provider nondeterminism, bounded retries, malformed final answers, and incomplete token-tracker records complicate cost and reproducibility claims. These issues are explicitly retained rather than hidden:

- raw responses can differ even at temperature zero, although executable semantics may remain stable;
- the Qwen study contains seven complete cells with empty usage objects;
- malformed final answers remain common and sometimes dominate performance;
- completed intention-to-run outcomes are retained rather than selectively rerun.

These practices strengthen credibility, but they also make the experimental story less visually clean than a standard benchmark-improvement paper.

## 3. What the Qwen experiment did and did not validate

### Validated

1. **Cross-model score-scale causality.** Removing the length term reduces contribution scores strongly and consistently on a second model family.
2. **Non-degenerate evaluation.** The Qwen original arm achieved 55% exactness, so the result is not caused by a universal task floor.
3. **No stable utility gain from length deletion.** The Qwen point estimate is slightly negative, and its interval includes meaningful positive and negative effects.
4. **The DeepSeek utility point estimate should not be promoted.** The direction does not replicate across models.
5. **Generation dominates the observed Qwen failure pool.** Only one failed final per arm is recoverable from persisted intermediate candidates.
6. **Independent trajectories expand task-relevant support.** \(C_5-C_1\) adds one canonical plan on average with 12 positive and no negative pairs.
7. **Expanded support can improve the executable oracle.** Four of 20 tasks are rescued, raising oracle accuracy from 0.60 to 0.80; nested-pool inference is reported by estimation rather than a sign test.
8. **Selector-level DP becomes consequential on the enlarged pool.** At \(\varepsilon=4\), expected validity is 0.779 against a 0.80 non-private oracle.

### Not validated

1. Persistent leakage on Qwen.
2. Better privacy properties for Qwen than DeepSeek.
3. End-to-end differential privacy for the evolving system.
4. A compute-efficient or specifically multi-agent architecture; the current positive intervention is repeated independent generation.
5. Generalization beyond PlanCraft, fixed topology, and five rounds.
6. The absence of useful partial reasoning below exact target completion.

## 4. Recommended next steps

### 4.1 Immediate recommendation: make the bound-and-escape result the paper's spine

The most defensible near-term action is to consolidate the paper around three auditable preconditions, one empirical class bound, and a prospective escape experiment:

> Before privatizing an evolving-agent selector, researchers must verify a persistent sensitive channel, a causally useful score, and enough utility dispersion in the candidate pool for selection to matter. In the audited runtime, fixed pools provide only 0–8.3 points of headroom; independent trajectories expand support and raise the oracle by 20 points, after which selector-level DP retains most of the enlarged oracle at moderate ε.

The Qwen replication, candidate audit, and enlargement experiment materially strengthen this framing. They show that the diagnosis transfers across models, that the fixed-pool failure is not merely a poor final selector, and that expanding generation makes selection consequential.

The manuscript should now prioritize:

- conversion to the official ICLR LaTeX template;
- a literal nine-page main-text layout check;
- a clear separation of established findings, failed confirmations, and future hypotheses;
- a revised main figure showing fixed-pool headroom, the \(C_1\rightarrow C_5\) support/oracle curve, and the DP selector curve;
- careful venue positioning as an audit/measurement paper rather than a DP-method paper.

### 4.2 Do not run more unchanged length-zero or fixed-pool selector experiments

Further scaling of the same length ablation is unlikely to change the scientific conclusion. The score effect is already decisive, and utility has failed to show a stable direction. Likewise, the frozen candidate audit rejects further selector/retention scaling on the unchanged candidate pool.

Additional calls on these unchanged interventions would narrow already-understood intervals without addressing the paper's largest weakness.

### 4.3 Do not start a new repair method before submission

The completed Qwen experiment shows that independent generation works, while the DeepSeek gate turns the failed obvious remedy into direct mechanism evidence. Do not run its frozen main cohort, repeat its unchanged prompt, or begin a tool-augmented repair redesign before the submission deadline. Recipe evidence, best-prefix continuation, action normalization, duplicate rejection, and failure-aware role separation are plausible future methods, but each would require its own development cycle and newly frozen untouched validation. The current paper gains more from a clear mechanism section and a completed submission draft than from an unfinished second method.

### 4.4 Treat stronger leakage experiments as a separate branch

If retaining a strong privacy-centered narrative is essential, a new leakage protocol should increase attack strength rather than merely increase sample size. Possible changes include repeated secrets, semantically consequential secret placement, longer horizons, structural mutation, adaptive extraction prompts, and a small cross-model gate. A depth-matched reset control and positive controls must remain.

This branch has substantial cost and a meaningful chance of another null result. It should therefore have a strict budget and an early gate, and it should not delay preparation of the existing paper.

### 4.5 Venue strategy

For ICLR, the paper should be presented as a rigorous empirical audit with a constructive follow-through: it exposes three unverified assumptions behind premature DP claims, measures a selector-class headroom bound, and prospectively demonstrates that independent generation can escape that bound. Its strongest assets are prospective freezing, executable evaluation, cross-model causal replication, the fixed-pool bound, and the new support-to-private-selection curve. Its weakness is now simplicity and compute cost, not the absence of any positive result.

If reviewers or internal assessment conclude that a positive method is indispensable, the current work may fit better as a privacy, trustworthy-ML, evaluation, or empirical-methodology paper. The choice should be revisited after the ICLR-formatted draft and narrative are reviewed as a complete submission rather than judged only from individual experiment outcomes.

## 5. Current bottom line

The project is not failing because the theory and data disagree. They agree on the central warning: a strongly manipulable score can still have little stable causal relationship with semantic utility, so adding privacy noise to that score does not solve the real problem.

The validated contribution is now a **bound-and-escape result**, not merely a list of failed methods:

- no persistent leakage event was detected under the audited setting;
- the released score is causally length-dominated across DeepSeek and Qwen;
- deleting length does not reliably improve utility;
- execution-aware retention does not pass independent confirmation;
- fixed-pool selector headroom is 0–8.3 points across the audited original/control cohorts;
- the exploratory four-cohort synthesis is 4.6 points, interval [0, 10.8];
- the 42-pair stratified length-ablation effect is +2.4 points, interval [-9.5, 14.3];
- expanding from \(C_1\) to \(C_5\) increases canonical support by 1.00 and the executable oracle by 20 points;
- selector-level DP reaches 0.779 expected validity at \(\varepsilon=4\) against the 0.80 enlarged-pool oracle;
- the constructive gain costs a 3.00-fold token budget and still needs binary-outcome replication;
- the DeepSeek compute-matched repair gate stopped with only three informative failures; repair was 1/3 versus restart 0/3, exact \(p=1\), and the two exhausted branches had raw modal invalid-answer rates of 86.25% and 95%.

The biggest remaining scientific gap is no longer whether support can be expanded; that has been shown prospectively. It is whether efficient conditional generation can remain diverse and beat a restart under a properly powered non-nested design. Given the stopped gate and the timeline, the recommended strategy is to finalize the ICLR manuscript around the bound-and-escape arc, report the failed obvious efficiency remedy, and avoid further unchanged provider spending.

## Artifact pointers

- Qwen cross-model decision: `research/artifacts/iclr2027-qwen-cross-model-length-decision-075.json`
- Qwen candidate-recoverability protocol: `research/configs/qwen-candidate-recoverability-protocol-077.json`
- Qwen candidate-recoverability results: `research/artifacts/iclr2027-qwen-candidate-recoverability-078.json`
- Candidate-audit closure: `research/manifests/iclr2027-qwen-candidate-audit-closure-079.json`
- Cross-cohort headroom and pooled analysis: `research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json`
- DeepSeek compute-matched protocol: `research/configs/deepseek-compute-matched-generation-protocol-090.json`
- DeepSeek stopped-gate source: `research/artifacts/iclr2027-deepseek-compute-matched-generation-091.json`
- DeepSeek final gate analysis: `research/artifacts/iclr2027-deepseek-compute-matched-generation-gate-analysis-092.json`
- DeepSeek conditional-collapse analysis: `research/artifacts/iclr2027-deepseek-conditional-collapse-analysis-094.json`
- Candidate-pool enlargement protocol: `research/configs/qwen-candidate-pool-enlargement-protocol-083.json`
- Candidate-pool enlargement source and decision: `research/artifacts/iclr2027-qwen-candidate-pool-enlargement-084.json` and `research/artifacts/iclr2027-qwen-candidate-pool-enlargement-decision-085.json`
- Corrected trajectory-level reanalysis: `research/configs/qwen-candidate-pool-trajectory-reanalysis-protocol-087.json` and `research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json`
- Current paper draft: `iclr2027-paper-draft.md`
- Current appendix: `iclr2027-paper-appendix.md`
