# Research Progress Log

## 2026-08-12 — External empirical review corrections and program reset

- Verified that single-coordinate score replacement satisfies the same-sign/monotone condition, so exponential selection uses `exp(epsilon*u/Delta_u)` rather than the general factor-two denominator.
- Recomputed mechanism comparison and the 100-cell phase diagram. The former vector 100/100 sweep is withdrawn: exponential wins 19/25 binary cells, while vector usually wins at larger candidate counts, producing a crossover surface.
- Corrected the frozen binary projected exact rate for exponential selection at epsilon 4 from 66.06% to 73.65%.
- Withdrew the three-candidate live protocol before execution: instances 23, 27, and 29 were reused from scorer validation and were incorrectly described as unused. The runner now refuses provider calls for the withdrawn protocol.
- Added decision-level Wilson intervals to live routing: epsilon 1 is 11/20, 55%, 95% interval 34.2%–74.2%; intervals are descriptive because seeds reuse four instances and cached outputs.
- Froze a 20-call provider nondeterminism protocol and implemented a cache-bypassing runner.
- Audited the released runtime: it has no explicit fast-time replicator weight update; repeated rounds update outputs/memory/scores, while capability mutation occurs in slow-loop birth/death.
- Froze an implementation-level repeated-fast-round and zero-length-score ablation protocol with a hard stop-gate on further E3-style claims.
- Created `dp-tacomas-claims-report.md` as the claim-organized paper; retained the original report as the full technical notebook and audit trail.

Decision: prioritize evaluator/evolution validity and the fast-loop/length-term ablations. Treat current scalar work as generic DP handoff routing until the typed-edge architecture and slow-loop E4 experiment exist.

## 2026-08-12 — Three-candidate live protocol frozen and audited

> **Withdrawn before live execution.** This historical entry is retained for auditability. Instances 23, 27, and 29 came from scorer validation, and the corrected exponential calibration also changes the prediction.

- Preregistered two-action instances 23, 27, and 29 before any new live compiler outcomes; the later reuse audit invalidated their confirmatory status.
- Mechanically constructed complete, first-call-only partial, and plot-type-ablated candidates; reference-free score vectors are `[1, 2/3, 0]` for every instance.
- All seven pre-live integrity gates passed; post-freeze action recall is `[1, 0.5, 0]`, and exact labels are `[1, 0, 0]`.
- Froze vector Laplace versus exponential selection at epsilon 1/2/4 with 20 seeds, exact match primary and call recall secondary.
- Ran one million vector samples per epsilon plus exact exponential probabilities without model calls. At epsilon 4, complete/partial/ablated selection was 77.14%/21.56%/1.29% for vector Laplace and 60.65%/31.14%/8.21% for exponential selection.
- Implemented checkpointed live execution with unique-handoff caching and strict prompt visibility. The current environment had no API credential, and the runner exited before making any call.

Decision: keep protocol and runner frozen; execute the cached live controls and routed evaluation when a credential is injected, without changing cohort, candidates, gates, seeds, or endpoints.

## 2026-08-12 — DP routing robustness phase diagram

- Froze a 5 score-gap × 4 candidate-count × 5 epsilon grid under the existing S2/E replacement adjacency; no model calls or tokens were used.
- Evaluated one unique best candidate against tied alternatives using 100,000 vector-Laplace trials per cell and exact exponential-mechanism probabilities.
> **Original calibration withdrawn.** The claims in this historical entry used the general factor-two exponential calibration. Current corrected results are in the review-correction entry above and schema-v2 artifact.

- Historical result: vector Laplace exceeded exponential selection in all 100 point estimates under the now-withdrawn calibration.
- At unit gap and epsilon 1, vector/exponential best-selection probabilities fell from 72.09%/62.25% at two candidates to 25.86%/15.48% at ten candidates.
- At unit gap and epsilon 4, the corresponding two-to-ten decline was 97.25%/88.08% to 85.58%/45.09%.
- Kept noisy-gap release strictly binary: data-dependent top-two selection or multiple public gaps require a new disclosure and sensitivity analysis.
- Multi-candidate live rates in the artifact are explicitly counterfactual projections from frozen 75%/0% controls, not observed live outcomes.

Decision: condition mechanism choice on disclosure policy and candidate count; next construct a preregistered live cohort with at least three genuinely divergent handoffs.

## 2026-08-12 — Equal-epsilon DP routing mechanism comparison

> **Original calibration withdrawn.** The exponential values and ranking in this historical entry are superseded by the schema-v2 artifact.

- Reused the frozen divergent cohort and cached live-summary control outcomes; no new model calls or tokens.
- Compared pure-DP noisy score vector, public noisy score gap, and exponential selection under the same event adjacency and epsilon grid.
- At epsilon 4, expected exact rates were 72.94%, 74.31%, and 66.06%, respectively; fractions of the 75% live ceiling were 97.25%, 99.08%, and 88.08%.
- Noisy gap ranked first at every epsilon from 0.5 to 8; vector Laplace ranked second; exponential selection ranked third.
- 100,000 Monte Carlo trials per cell matched closed forms with maximum absolute probability error below 0.0018.
- Equal epsilon does not imply equal disclosure: vector releases two values, gap releases one numeric margin, exponential selection releases only identity.

Decision: adopt noisy-gap release as the binary E-level primary mechanism when public margins are allowed; retain exponential selection as the minimum-disclosure comparator and test both beyond two candidates/unit gaps.

## 2026-08-12 — Prospective divergent-information live routing

- Froze instances 15, 17, 20, and 21 before live execution; excluded all prior causal-routing and live-prompt development samples.
- Mechanically deleted every `plot_type` argument to create incomplete candidates; no reference answer or live outcome informed the ablation.
- Reference-free score vectors were `(1,0)` for all four candidate pairs.
- All preregistered gates passed: complete 75%, ablated 0%, all handoffs 75%, no handoff 0%.
- Retained instance 21's empty complete-handoff output as a real compiler failure.
- Five-seed empirical routing: epsilon 1 = 55%; epsilon 2 = 75%; epsilon 4 = 75%.
- Exact expected rates: 54.31%, 64.85%, and 72.94%; these retain 72.41%, 86.47%, and 97.25% of the 75% complete-control ceiling.
- Thirteen unique live-summary calls used 6,979 tokens.
- Protocol audit passed; only clipped scores are DP-protected, while raw handoffs remain in the TCB.

Decision: retain this cohort as an E-level causal benchmark and compare Laplace-vector routing against a billboard-compatible rule or exponential mechanism without changing handoffs or controls.

## 2026-08-12 — Live summary behind DP-selected routing

- Replaced the deterministic action compiler with DeepSeek V4 Flash as a live second-stage summary agent.
- Enforced a visibility contract: no task question, reference, unselected candidate, raw score, noise, or released magnitudes; only selected role, selected handoff, and public schema.
- Cached by instance/role/handoff/prompt hash, producing eight unique calls and 3,605 tokens across the complete epsilon/seed grid.
- Structural provenance audit passed for all eight handoffs. Two content collisions arose because selected verifier text quoted planner calls; no unselected object was separately passed.
- All eight possible handoffs compiled exactly, so every non-private and DP condition scored 100%.
- Verdict: cohort is degenerate for routing-utility identification. This is not evidence of zero DP loss.

Decision: freeze a prospective divergent-information protocol using predefined field ablation/corruption strata, with all-handoff and no-handoff controls, before the next live run.

## 2026-08-12 — Causal E-level DP routing pilot

- Froze new instances 11, 12, 13, and 14 before running the routing intervention.
- Generated fixed planner/verifier candidates through the three-agent TacoMAS path; total candidate-generation cost was 16,896 tokens.
- Implemented a pure helper for one noisy clipped score-vector release and a deterministic selected-handoff compiler.
- Closed the causal design against question re-solving: compiler reads only the selected handoff, never the question or reference; reference is posthoc evaluation only.
- Candidate quality: planner 4/4 recoverable exact; verifier 2/4 recoverable exact.
- Non-private route: 4/4. Three-seed empirical means: epsilon 1 = 75.0%, epsilon 2 = 91.7%, epsilon 4 = 100%.
- Added the exact two-Laplace selection probability. Analytic expected exact rates are 86.20%, 93.23%, and 98.63% at epsilon 1/2/4.
- Privacy scope remains E-level score replacement. Raw candidate handoffs remain in the TCB and are not DP-protected.
- Tests increased to 26 passing cases.

Decision: proceed to a live second-round summary agent with only the authorized handoff visible; retain the deterministic compiler as a causal lower-complexity control.

## 2026-08-12 — Reference-free contribution-score repair

- Confirmed the upstream non-slow-round formula: 85% output-length score plus a 15% environment-success indicator; action correctness is not evaluated.
- Implemented a reference-free WorkBench analytics contract scorer that derives slots from the question/public schema and recovers function-syntax or structured-JSON actions.
- Added three scorer tests; total local tests increased from 19 to 22.
- Froze held-out instances 23, 27, 28, and 29 before scorer evaluation. Derived contracts matched benchmark references in 4/4.
- Across 12 agent outputs: old-score AUC 0.111 and top-selector exactness 25%; contract-score AUC 1.000 and top-selector exactness 100%.
- Both multi-agent and direct final outputs were 4/4; tokens were 19,350 versus 2,514.
- Repeated the E-level DP grid on contract scores. Counterfactual selected-output accuracy at epsilon 0.5/1/2/4/8 was 83.2%/89.3%/95.7%/99.455%/100%.
- At epsilon 4, binary-tree SD was 0.3523 versus theory 0.3536.
- Above-mean threshold flips plateau near 12.5% at high epsilon because tied all-one scores lie exactly on the decision boundary.

Decision: use contract-aligned bounded scores for the next online pilot, avoid raw above-mean gates at zero margin, and wire the release into a real second-round decision before making end-to-end DP utility claims.

## 2026-08-12 — E5 real-trace score mechanism pilot

- Extracted real contribution-score vectors from held-out instances 22, 25, and 26.
- Froze an E-level replacement-adjacency grid at epsilon 0.5, 1, 2, 4, and 8; ran 10,000 Monte Carlo trials per level.
- Design A measured noisy top-score retention; Design B measured personal above-mean decision flips; Design B+ measured binary-tree final-prefix error.
- Empirical tree SD matched theory at every epsilon. At epsilon 4, top-score retention was 72.2%, billboard threshold flips were 7.71%, and tree SD was 0.331 versus theory 0.333.
- Critical validity finding: verifier was top-scored in 3/3 but exact in 0/3; summary was exact in 3/3. Clean top-score selection was therefore 0/3.
- Score/output-length Pearson correlation was 0.950 across nine outputs; all scores were marked `heuristic_only_non_slow_round`.
- DP was applied offline after inference, so observed direct-agent and multi-agent task answers were causally unchanged.

Decision: do not optimize privacy mechanisms for preservation of the current contribution ranking. First validate or replace the score, then wire a bounded release into an actual score-dependent multi-round decision.

## 2026-08-12 — Aggregation repair held-out validation

- Development evidence was restricted to failed instance 24.
- Before changing the prompt, held-out instances 22, 25, and 26 were frozen in `configs/workbench-aggregation-heldout.json`.
- The repair added a dataset-global scope invariant: distribution/histogram applies to every listed metric, and verifier agents must not redesign an explicit chart type.
- Repaired three-agent result: 3/3 exact, 9 calls, 14,821 tokens.
- Matched direct-agent result: 3/3 exact, 3 calls, 1,783 tokens.
- Interpretation: the repair generalized across this small held-out set, but the three-agent path still cost 8.31 times as many tokens without an accuracy gain.
- Decision: begin only a tightly scoped DP pilot with both controls retained; defer multi-agent benefit claims until a stateful tool environment supports genuinely coordination-demanding tasks.

## 2026-08-12 — WorkBench identifiability audit and stratified ablation

### Completed

- Audited all 690 converted WorkBench instances for reference identifier arguments unavailable in the natural-language question.
- Froze a six-instance prompt-identifiable analytics cohort before execution: indices 10, 15, 17, 20, 21, and 24.
- Ran the fixed three-agent fast path and rescored every trace with exact normalized function-and-argument matching.
- Ran a matched one-agent direct-output ablation with the same prompt contract, temperature, cohort, and evaluator.
- Preserved the failed multi-agent trace for instance 24; no success-only rerun replaced it.
- Re-ran 19 local tests, verified the frozen upstream tracked tree is clean, and found no persisted API-key pattern in research/report files.

### Results

| Path | Exact | Model calls | Total tokens | Mean tokens |
|---|---:|---:|---:|---:|
| Three-agent planner/verifier/summary | 5/6 (83.3%) | 18 | 28,280 | 4,713 |
| One-agent direct output | 6/6 (100%) | 6 | 3,354 | 559 |

The multi-agent path cost 8.43 times as many tokens and was 16.7 percentage points less accurate. On instance 24, the planner was correct, the verifier changed the second histogram to a line chart contrary to the global contract, and the summary propagated that error. Non-analytics converted instances are not yet a fair live-model target because many references require hidden event/customer/email/task IDs and the frozen runner exposes no corresponding workplace state tools.

### Decision

Do not attribute the next accuracy difference directly to DP. First retain both direct-agent and multi-agent controls, repair aggregation on a development case, evaluate the repair on a newly frozen held-out set, and restore a stateful WorkBench-compatible environment before expanding to hidden-ID families.

## 2026-08-11 — WP0/WP1 启动

### 完成

- 获取并冻结 TacoMAS 上游提交 `6f0d545f2493cf95d2eb6a325d1a6686acf658eb`；
- 验证四个数据集记录数和 SHA-256 前缀；
- 完成上游源码 `compileall`；
- 完成真实 fast/slow loop、Judge、跨 agent 通信和停止路径的静态审计；
- 识别 scalar replicator surrogate 与真实 prompt/memory 实现的关键差距；
- 编写 E/A/O privacy games v0.1；
- 编写公共转录 JSON Schema v0.1；
- 建立 E5 pilot 配置；
- 实现 Design A 解析诊断、E-level Fenwick counter 和 scalar baseline-invariance 测试；
- 11 个单元测试全部通过（标量机制、privacy edge、stats-only payload）；
- 完成 10,000 次 E5 标量 Monte Carlo pilot；
- 将 pilot 的精确校准和实现差距回写研究报告。
- 实现 `PrivacyEdgeType`、默认拒绝路由契约和 typed stats-only Meta payload；

### 结果

| 指标 | 理论 | 经验 |
|---|---:|---:|
| Design A 单轮 SD | 5.3033 | — |
| Design A 累计 SD | 20.5396 | 20.5710 |
| Design A effective SNR | 0.1461 | — |
| Design A sign-threshold FNR | — | 44.79% |
| Tree 最终 prefix SD | 0.4714 | 0.4737 |
| Tree cumulative SNR | 6.3640 | — |
| Tree sign-threshold FNR | — | 0/10,000 |
| Scalar-share 最大差异 | 0 | $2.22\times10^{-16}$ |

### 新发现

1. 上游 fast loop 不执行显式数值 replicator 更新；
2. Judge 输入包含任务、query、tools 和 agent output；
3. graph neighbors 的 raw outputs 会直接进入下游 query；
4. slow Meta-LLM 输入含 latest output、memory summary 和 score histories；
5. 当前 edge type 不是 privacy type；
6. 数据依赖停止必须纳入公共转录或在首个可证明原型中关闭。

### 阻塞与处理

- 默认 Python 3.10 低于上游要求；已用 bundled Python 3.12 创建 `.venv`；
- PyPI 下载多次超时，完整依赖尚未安装；不影响 stdlib 标量 pilot；
- 未发现任何 LLM/Search API 凭据，真实 TacoMAS baseline 暂不能调用；
- 用户提供的 DeepSeek V4 Flash 凭据已对官方端点做最小验证，返回 HTTP 401；未落盘。该凭据疑似属于第三方网关，需对应 Base URL；
- 第二个 DeepSeek 凭据已在官方 `deepseek-v4-flash` 端点通过认证与正文响应测试；凭据未落盘，并已生成仅从 `DEEPSEEK_API_KEY` 读取秘密的 smoke runner；
- 上游未检测到 LICENSE 文件，公开派生代码前需核实授权。

### 下一步

1. 完成可锁定的 Python 依赖环境；
2. 运行注册表 sanity check；
3. 在具备凭据后运行 finance-benchmark 单实例固定轮数 baseline；
4. 从真实 trace 提取 score-gap 分布，替换合成 $g=0.2$；
5. 开始 `PrivacyEdgeType` 和 stats-only payload builder 的接口设计。

## 2026-08-11 — DeepSeek 接入与运行时复现

### 已完成

- 第二个 DeepSeek 凭据已在官方 `deepseek-v4-flash` 对话端点通过认证和正文响应测试；凭据仅作为进程环境变量使用，未写入仓库。
- 已新增可复现检查脚本 `research/experiments/check_deepseek_api.py`，本轮运行结果为 `PASS`。
- 已完成 Python 3.12 虚拟环境依赖安装，并生成 `research/manifests/requirements-lock-py312.txt`。
- 已生成最小调用包装器 `research/experiments/run_deepseek_smoke.py`，固定为单样本、单 fast round、零实例重试。
- 11 项本地机制测试全部通过。

### 完整烟雾实验状态

完整 TacoMAS 调用在首次 LLM 请求之前被冻结上游提交中的配置问题阻断：

1. `plancraft` 可选包 0.4.8/0.4.9 均在导入配方时触发 `KeyError: acacia_logs`；
2. 上游运行器默认使用未注册的 `multi-agent-independent`；
3. 改用已注册的 `tacomas` 后，其必需提示词与运行器硬编码的 `base_agent`/`aggregator` 提示词集合不一致。

因此本轮没有产生 TacoMAS 多智能体模型调用费用。下一步需要先制作可审计的本地兼容补丁或切换到已知可运行的上游提交，再采集真实 trace。

## 2026-08-11 — 首个真实 TacoMAS trace

### 运行结果

- 使用仓库外兼容层补齐冻结运行器缺失的 `multi-agent-independent` 注册，未修改冻结上游源码。
- 13 项测试通过。
- DeepSeek V4 Flash 完成 WorkBench 样本 0 的一轮动态运行；退出码 0，实例失败数 0。
- 最终状态：4 个代理、5 条边、1 个 fast round、0 个 slow update、runner raw score 0.5、evolution quality 0.5。
- 完整产物位于 `upstream/TacoMAS-MultiAgent/outputs/evolution_trace_20260811_230440_workbench_0_1`；trace 未发现 API key 模式。

### 诊断结论

该结果仅证明模型接入与 trace 链路可达，不能作为非私有质量基线：

1. `INSTANCE_RETRIES=0` 会导致零次执行，实际最小值必须为 1；
2. 配置三代理却生成四代理；
3. WorkBench 被注入金融专用角色提示词；
4. 缺少数据的合理回答被 low-signal 规则额外重试；
5. 最终答案包含内部 thinking，而正确 rubric 期望 `analytics.create_plot.func(...)`；
6. 数据集指标给出 `success=0.0, score=0.5`，需要避免把 0.5 误读为任务成功。

下一阶段先修复非私有基线的提示词路由、种群规模和最终输出抽取，再进行多样本或 DP 对照实验。

## 2026-08-11 — 非私有基线三道门与评估器审计

### 已完成

- 固定 WorkBench 三代理、三边拓扑：planner、verifier、summary。
- 恢复 summary 合法角色和 `done` 工具路径。
- 增加 WorkBench 专用动作提示词、provider thinking 清洗和逐运行 token 计量。
- 增加确定性 WorkBench 函数调用解析与精确参数匹配；当前共 19 项测试通过。
- 增加 WorkBench 旧金融 storage-key 指南清除补丁及测试。

### 两个受控样本

| 样本 | LLM judge | 确定性 exact | input tokens | output tokens | total tokens |
|---:|---:|---:|---:|---:|---:|
| 0 | 0.0 | false | 5,052 | 9,769 | 14,821 |
| 20 | 1.0 | false | 5,176 | 18,944 | 24,120 |

样本 20 的输出把两个指标合并进一个 `line` 调用，并使用错误指标名；参考答案要求两个独立 `histogram` 调用。LLM judge 仍给满分，而确定性比较为 precision=0、recall=0。因此暂停扩展样本，先将确定性动作匹配接入主实验汇总并压缩分类、schema 和 judge 等辅助调用。

## 2026-08-12 — 确定性 WorkBench 快速路径

### 改动

- WorkBench task profile 和 schema 改为确定性元数据，不再调用 LLM。
- 最终综合直接选择 summary 的 `done` 输出，不再调用 LLM synthesizer。
- runtime 与 dataset evaluator 均改为确定性函数名和参数多集比较。
- 补回全局工具契约：2023 日历年、有效指标名、distribution→histogram、单调用单指标。
- 新增批量汇总脚本和 `research/artifacts/workbench-run-summary.json`。

### 同实例成本/质量对照

| 路径 | 确定性 exact | 调用数 | input | output | total |
|---|---:|---:|---:|---:|---:|
| 旧受控路径 | false | 6 | 5,176 | 18,944 | 24,120 |
| 确定性快速路径 | true | 3 | 3,284 | 1,072 | 4,356 |

记录 token 减少 81.9%；旧路径另有两次未计量的直接 grading，因此真实降幅更大。样本 20 已通过单实例非私有基线门，下一步执行小规模分层批量，而非立即启动 DP 对照。
## 2026-08-12 — ICLR 2027 execution-plan correction and protocol freeze

- Verified that the official abstract and paper deadlines are Sep 11 and Sep 16 AOE, reducing the working horizon from the assumed 44 days to 35 days.
- Reframed the empirical spine as persistent evolution leakage → naive score noising loses utility → architectural restriction and privatized release.
- Froze G1 and G2 ahead of model execution. G1 requires canary exposure in persistent evolved state plus a positive paired difference over a depth/call-matched reset control; final-answer echo alone does not pass.
- Implemented X1 canary generation, state scanning, reset control, structural masks, and equal-depth round driving.
- Replaced X2's ambiguous fast-loop ablation with eight arms covering direct, static MAS, repeated rounds, feedback, topology, birth/death, full evolution, and zeroed length term.
- Audited local benchmark readiness: PlanCraft and BrowseComp Plus are stateful; converted WorkBench is not a valid G2 main benchmark.
- Froze outcome-blind 30-instance cohorts for each X2 screening benchmark and generated a SHA-256 preregistration manifest.
- Prepared but did not execute a two-round credentialed PlanCraft G0 smoke runner with persisted token accounting. No accepted credential is present in the current process.
- Local verification: 48 tests passed under Python 3.12 before the generic usage-tracking extraction; final post-change verification follows.

## 2026-08-12 — G0 PlanCraft credentialed scientific smoke

### Result

- Ran the frozen three-agent PlanCraft cake instance for two fast rounds with DeepSeek V4 Flash.
- Completed 1 instance with 0 failures and 0 slow updates.
- Produced `["sugar", "sugar", "cake"]`; the deterministic PlanCraft evaluator returned exact match, runner score 1.0, and evolution quality 1.0.
- Both transport and scientific-harness gates passed: the PlanCraft prompt route, task schema, search tools, consensus extraction, and deterministic evaluator were active.

### Cost and integrity

| Calls | Input tokens | Output tokens | Total tokens |
|---:|---:|---:|---:|
| 18 | 37,316 | 3,291 | 40,607 |

- Persisted validation, usage, summary, per-instance trace, and SHA-256 hashes in `research/artifacts/iclr2027-g0-plancraft-smoke-029.json`.
- The credential was supplied only to the interactive child process and cleared afterward; secret-pattern scan found zero matching files in the run, manifests, and research artifacts.
- The frozen upstream tracked tree remained clean and all 56 local tests passed.

### Gate decision

G0 runnable science passes. The next experiment is the preregistered 20-pair X1 persistence-leakage pilot; G1 must be decided before X2 screening.

## 2026-08-12 — X1 persistent-canary pilot halfway checkpoint

### Formal progress

- Completed 30/60 cells: 10 frozen PlanCraft instances, each with `evolve`, `depth_matched_reset`, and `no_canary` arms.
- All 30 runs completed five fast rounds and five persistent-state checkpoints.
- Primary exact exposure: 0/10 in every arm. Secondary five-token partial exposure: 0/10 in every arm.
- Interim paired evolve-minus-reset risk difference is 0.0; this is descriptive only and is not an early G1 decision.
- Formal usage is 3,851,131 tokens (mean 128,371 per cell), projecting 7,702,262 tokens for 60 cells.

### Transport reliability and analysis integrity

- Two provider requests hung before a cell could be persisted. Their verified experiment process trees were terminated; neither partial cell entered the formal artifact, and execution resumed from the frozen order.
- Added a 45-second request timeout and one retry across agent, judge, and meta-controller clients. Local verification now passes 61 tests.
- In completed cell `TEST0249/depth_matched_reset`, the single slow meta call exhausted bounded retries and returned the existing default no-change decision; all fast rounds and checkpoints completed.
- Primary analysis retains the frozen intention-to-run schedule. A sensitivity analysis excluding the entire TEST0249 triad was frozen before running the remaining 30 cells. Completed cells will not be rerun and arms will not be selectively deleted.
- Credential scans remain clean and the child-process credential was cleared after every batch.

## 2026-08-12 — X1 75% checkpoint

- Formal progress reached 45/60 cells: 15 complete three-arm PlanCraft blocks.
- Exact persistent-state exposure remains 0/15 in every arm; five-token partial exposure also remains 0/15 in every arm.
- Deterministic task exact is 5/45 overall. The system is not uniformly nonfunctional, but task utility is low on this harder frozen cohort.
- Formal usage is 5,651,700 tokens, projecting 7,535,600 tokens for all 60 cells.
- Provider instability caused bounded round-3 meta-controller fallbacks in TEST0249, all three TEST0427 arms, and TEST0432/evolve. Primary analysis retains them; sensitivity analysis excludes each affected instance's whole triad.
- The next TEST0470 attempt was terminated before persistence, leaving a clean resumable boundary at cell 46. No completed cell was rerun.

## 2026-08-12 — X1 complete and G1 decision

- Completed all 60 formal cells: 20 frozen PlanCraft instances × three arms, with five rounds and five checkpoints in every run.
- Exact post-input persistent exposure was 0/20 in `evolve`, `depth_matched_reset`, and `no_canary`; the five-token partial endpoint was also 0/20 in every arm.
- Paired evolve-minus-reset risk difference was 0.0, paired bootstrap interval [0.0, 0.0], and exact McNemar p=1.0.
- The predeclared operational sensitivity analysis excluded whole triads TEST0249, TEST0427, and TEST0432 and obtained the same result on 17 pairs.
- G1 failed all three frozen criteria. The 40-pair and structural-evolution extensions are stopped.
- Formal usage: 3,317 provider calls and 7,479,153 tokens. Aborted provider-side request usage is unknown and excluded from the local ledger.

## 2026-08-12 — Zero-call fallback score-validity analysis

- Reused all 60 X1 trajectories without new model calls; deterministic task exact was 5/60.
- At max agent contribution score ≥0.8, run-level precision for final deterministic exact was 5/33 = 15.2%, with 28 false-positive runs.
- Of 165 agent-round score observations ≥0.8, 141 (85.5%) belonged to deterministically failed runs.
- Max contribution-score AUC against final exact was 0.755. Final runtime answer quality had AUC 1.0 only because the final compatibility evaluator is deterministic.
- `TEST0413/depth_matched_reset` reached deterministic quality 1.0 at round 3 but ended incorrect at round 5, showing that transient correctness and final executable delivery are distinct.
- The paper route switches to evaluation validity and persistence-aware scoring; X1 remains a scoped, fully instrumented null result.

## 2026-08-12 — Provider repeatability audit

- Repeated one frozen cache-bypassed DeepSeek V4 Flash compiler prompt 20 times at temperature zero.
- Byte-identical modal rate was 65%; pairwise raw-response disagreement was 47.9%, with two unique text hashes.
- Parsed canonical action calls were identical in 20/20 runs, and deterministic exact match was 20/20.
- Raw-text reproducibility and executable semantic reproducibility must be reported separately. The result is prompt-specific and not a model-wide determinism claim.
- The artifact contains no credential pattern and the child-process credential was cleared.

## 2026-08-12 — Prospective score-persistence fallback complete

- Froze a 10-pair PlanCraft test on the untouched remainder of the X2 screening cohort, comparing the current 85% text-length contribution term with a zero-length-term arm.
- A first paired calibration exposed a reference-withholding harness defect: constant-zero online quality prevented strict-improvement best-state capture. Amendment 041 was frozen before restarting; both calibration cells remain in the artifact as invalid and excluded.
- Completed 20 valid cells. Every cell ran five rounds, one slow feedback event, fixed topology, and structural masks; references were read only after each run.
- Final deterministic exact was 1/10 in both arms. Paired risk difference was 0.0, bootstrap interval [0.0, 0.0], exact McNemar p=1.0, and correctness-regression count was 0 versus 0.
- The frozen decision is negative: stop the length-term intervention.
- Manipulation check passed: mean contribution score fell from 0.429 to 0.069 and score>=0.8 observations fell from 33 to 0. Of the 33 control-arm high scores, 23 occurred in failed runs.
- Valid usage was 1,083 provider calls and 2,716,894 tokens. Including the retained invalid calibration, observed usage was 2,999,293 tokens.
- This supports a causal score-validity diagnosis but does not establish a utility-improving method or revive G1/G2.

## 2026-08-12 — English paper first draft and statistical closure

- Wrote the complete English ICLR first draft in `iclr2027-paper-draft.md`, framed around auditing persistent state and contribution scores rather than claiming an unsupported DP method win.
- Generated the artifact-derived three-panel main figure in PNG and PDF formats.
- Added exact uncertainty for the zero-exposure result: with 0/20 evolve-arm events, the one-sided 95% exact-binomial upper bound is 13.9%.
- Added paired inference for the length-term manipulation: all 10 score differences were negative, mean difference -0.360, paired bootstrap 95% interval [-0.500, -0.225], exact two-sided sign-test p=0.00195.
- Extended the automated paper claim audit to 12 headline claims and prepared a new SHA-256 closure manifest without changing any empirical outcome.

## 2026-08-12 — Reference-free executable-plan signal

- Implemented a PlanCraft candidate validator that uses only the question inventory, target, and public recipe graph; it does not read the expected action trace.
- On the 60 cached X1 final answers, 46 were malformed/empty, 9 parsed plans failed during recipe execution, and 5 reached the requested target. All 5 reference-exact candidates were accepted; there were no exact false rejections.
- As a calibration check only, all 39 feasible list references executed successfully. Impossible claims remain explicitly unverified because an executor alone cannot certify non-existence.
- The development gate passed. Froze a fresh 8-pair feasible-task pilot comparing the released text-heuristic historical retention with execution-aware retention. The cohort excludes all X1 and length-term-pilot instances and was selected before inspecting any output on those tasks.
- The credentialed runner, budget rule, reference-withholding rule, and resume behavior are implemented and dry-run verified. No new provider call has yet been made for this pilot.
- A follow-up zero-call candidate-pool audit found no coverage gain from adding the latest per-agent outputs: valid coverage remained 5/60 and reference-exact coverage remained 5/60. The frozen pilot therefore keeps the simpler synthesized-answer intervention; no post-freeze amendment was needed.

## 2026-08-12 — Execution-aware retention development pilot complete

- Completed all 16 frozen cells over eight fresh feasible PlanCraft pairs; every cell ran five rounds and references remained offline until persistence.
- Execution-aware retention produced 1/8 executable-valid and reference-exact final answers versus 0/8 for the text heuristic. The paired difference was +0.125, bootstrap 95% interval [0, 0.375], with one method-only discordance and two-sided exact McNemar p=1.0.
- Both arms had 7/8 malformed finals. Token use was 1,018,841 for execution-aware and 1,058,730 for control (895 calls and 2,077,571 tokens total), so the signal was not purchased with greater inference cost.
- TEST0080 demonstrates the intended mechanism: the execution score recognized and retained the correct eight-action ladder plan at round 3; the control ended with a plan whose first item, `bamboo`, is not an executable crafted output.
- The frozen development gate passes, but the effect comes from one pair and is not confirmatory. A 20-pair independent validation protocol was frozen on unused instances before any calls to those tasks.

## 2026-08-12 — Execution-aware retention independent validation complete

- Completed all 40 frozen cells over 20 previously unused feasible PlanCraft pairs; every cell ran five rounds and the reference firewall remained intact.
- Execution-aware retention produced 1/20 executable-valid and reference-exact finals versus 0/20 for the text heuristic. The paired risk difference was +0.05 with a 100,000-draw paired bootstrap 95% interval [0, 0.15].
- There was one method-only discordance and no control-only discordance; the frozen one-sided exact p-value was 0.5. Both arms had 14/20 malformed final answers.
- Method/control token use was 2,604,731/2,669,935 (ratio 0.976). Total validation usage was 2,206 provider calls and 5,274,666 tokens, within the 6M cap.
- The cost, completion, and malformed-rate checks passed, but neither confirmatory statistical condition passed. The frozen decision is `not_confirmed_development_signal_only`.
- Stop further scaling of this unchanged intervention. Preserve the executor and mechanism trace as an architectural hypothesis; the paper must report a failed independent confirmation rather than a utility-improving method.

## 2026-08-13 — Review correction, sensitivity controls, and non-degenerate replication

- Corrected the base-rate interpretation of the X1 score audit. High-score observations are mildly enriched in successful runs: max-score AUC 0.755, run-bootstrap interval [0.689, 0.821], instance-cluster interval [0.651, 0.853], and agent-round high-score success lift 1.75x. All runs have 15 observations, so unequal round length is not a confound here.
- Added a deterministic persisted-state extractor positive control: exact recovery from all 7/7 declared state-channel fixtures. A live round-2 direct-memory-injection control also passed end to end.
- Quantified cached observable state mutation: 617/720 comparable agent transitions changed (85.7%), 168/168 slow-feedback fields were nonempty, retention fired in 60/300 rounds, and 11/60 runs retained a final answer. The historical traces do not support a byte-complete retrospective state diff.
- Quantified null sensitivity. Zero events in 20 leave a one-sided 95% upper bound of 13.9%; a two-sided paired exact test needs six pure evolve-only discordances (RD 0.30). Under the explicit 5% versus 10% planning scenario, 20-pair one-sided power is 1.7%.
- Formalized the utility-relevant signal-to-sensitivity ratio \(\rho_U=g_U/\Delta_c\). Exact zero useful gap cannot be repaired by changing epsilon; small \(\rho_U\) requires epsilon on the order of \(1/\rho_U\).
- Froze an outcome-blind PlanCraft replication after excluding 59 previously seen task IDs. The first eight-cell length-2 gate scored 3/8 exact (37.5%), inside the preregistered 30--70% healthy window, so no fallback tier or post-hoc subgroup search was used.
- Completed the frozen 12-instance, four-arm main matrix. Original evolve reached 6/12 exact (50%), length-zero 8/12, reset 5/12, and no-canary 7/12. The floor-effect decision passed.
- Length-zero minus original changed exactness by +0.167 with paired bootstrap interval [0, 0.417] and one-sided exact p=0.25; this is a promising but unconfirmed utility signal. Mean score changed by -0.308 with interval [-0.381, -0.230], and high-score observations fell 26 to 0, confirming length domination at a healthy base rate.
- Exact and partial post-input exposure remained 0/12 for evolve and reset. In original evolve, all 48 measured state transitions were non-no-op, 1,200/3,558 comparable paths changed, retention fired in 37/60 rounds, and all 21 feedback fields were nonempty. Zero events in 12 still leave a 22.1% one-sided upper bound.
- The positive control, gate, and main replication used 3,044 calls and 7,181,203 tokens; the 48-cell main matrix used 5,966,364 tokens, within its 7.5M cap.
- Updated the English paper, claim report, author-contact draft, quantitative claim audit, and finalizer. All 98 tests pass.

## 2026-08-13 — Audit-method reframing and statistical presentation closure

- Reframed the paper as a validated audit method using four documented near-misses: direct-input echo, raw-base-rate reversal, the constant-zero reference-firewall persistence bug, and byte-versus-semantic repeatability.
- Promoted the length-dominated score diagnosis into the title and abstract: `Before Privatizing Evolution: What Do Test-Time Evolving Agents Actually Optimize?`
- Quantified the four-arm nuisance floor. The three original-score arms span two successes (5/12 to 7/12), exactly matching the +2 length-zero contrast; high-score counts 26, 36, and 39 map non-monotonically to 6, 5, and 7 successes.
- Reported degenerate instance-cluster bootstrap draws explicitly: 3,903/100,000 for original X1 and 51/100,000 for the healthy cohort. AUC intervals condition only on draws containing both outcome classes.
- Operationalized \(\rho_U\) through paired randomized component ablation. With \(\Delta_c=1\), the point estimate is 0.167 and the 95% interval is [0, 0.417]; 75% binary exponential selection requires point \(\varepsilon=6.59\), while the uncertainty set is unbounded above.
- Reworked Figure 1(c) to display lift relative to the success base rate, standardized table numbering and recorded-token wording, added BibTeX citation keys, and moved detailed calibration, power, repeatability, and pilot tables to a separate appendix.
- Compressed the main Markdown draft from roughly 7,500 to about 6,300 whitespace-delimited words before LaTeX conversion. The appendix preserves displaced protocol and diagnostic detail.
- Extended the automated claim audit to the main paper plus appendix; all quantitative checks pass. Project tests pass 101/101 under Python 3.12 with third-party pytest plugin autoload disabled because an unrelated LangSmith UUID DLL fails at collection.
- The Xu et al. contact remains drafted but not sent; sending it is a human-author action.

## 2026-08-13 — Qwen3.7-Max cross-model replication

- Froze an untouched cross-model protocol before inspecting any Qwen task output. The dated `qwen3.7-max-2026-06-08` snapshot ran with temperature zero and thinking disabled on all LLM call paths.
- Passed the initial length-2 gate at 5/8 exact (62.5%), inside the preregistered 30--70% healthy window; no fallback-tier or subgroup search was used.
- Completed all 40 main cells over 20 fresh paired instances. Original scoring reached 11/20 exact and length-zero scoring 10/20; paired difference -0.05, bootstrap interval [-0.25, 0.15], with two length-zero-only and three original-only successes.
- The score-scale result replicated: mean score fell from 0.157 to 0.040, paired difference -0.117 with interval [-0.150, -0.084], all 20 pairs decreased, and score observations at least 0.8 fell from 8/300 to 0/300.
- The frozen score-scale rule passes; the utility-improvement rule fails. The Qwen utility direction (-0.05) differs from the DeepSeek point estimate (+0.167), while both intervals include zero.
- All 48 gate/main cells completed five rounds. The tracker recorded at least 2,292 calls and 4,416,267 tokens over 41/48 cells; seven complete cells have empty usage objects, so the reported cost is a lower bound.
- Added decision artifact 075, cross-model paper and appendix sections, and automated Qwen claim checks. No provider credential was persisted.

## 2026-08-13 — Qwen intermediate-candidate recoverability audit

- Froze protocol 077 before inspecting cached candidate content. The audit makes zero model calls and restricts its surface to 15 persisted round-agent outputs plus the synthesized final per run.
- Evaluated all 40 Qwen main cells with the reference-free deterministic PlanCraft executor; reference equality is secondary and produces identical counts.
- Original scoring improves only from 11/20 final-valid to 12/20 under a round-candidate oracle. One failed final is recoverable; eight are generation failures with no valid candidate in any of 15 slots.
- Length-zero similarly improves only from 10/20 to 11/20. One failed final is recoverable and nine are generation failures.
- Both semantic oracle gaps are 0.05 with bootstrap intervals [0, 0.15]. Recoverable opportunities occur on different instances, with paired arm difference 0 and interval [-0.15, 0.15].
- The original-score recoverable count is 1/20, below the frozen 4/20 advancement threshold. Stop the execution-gated selector/retention route without spending API budget; future method work must improve generation rather than merely re-rank persisted answers.

## 2026-08-13 — Cached cross-cohort headroom and pooled synthesis

- Froze protocol 080 before inspecting DeepSeek intermediate candidates or pooled length outcomes. All analyses reuse persisted traces and make zero provider calls.
- Applied the Qwen candidate-pool oracle to three DeepSeek cohorts. Original/control-arm selector headroom is 0/13 for X1 evolve, 1/12 for non-degenerate original evolve, 1/20 for confirmatory text retention, and 1/20 for Qwen original scoring.
- For each realized run, the final-plus-15-candidate oracle is a deterministic upper bound on any selector restricted to that support. An explicitly outcome-aware exploratory synthesis gives 3/65=4.6 percentage points, stratified interval [0, 10.8].
- The Qwen 81% exact-text duplication mechanism does not transfer literally: DeepSeek exact-text duplicate rates are about 7%--27%. The cross-model result is instead low task-relevant support: original/control arms average only 0.45--1.05 unique parseable canonical plans per run, with 73%--91% canonical duplication among parseable slots.
- A stratified synthesis of all 42 length-ablation pairs estimates +2.4 percentage points exactness, interval [-9.5, 14.3], with four length-zero-only and three original-only successes. The frozen precise-null rule passes.
- The length component predicts well-formed finals strongly on two DeepSeek cohorts but reverses on Qwen; paired malformed effects also change sign. Reframe length as a dominant, model-dependent output-formation proxy rather than a validated cross-model completeness or quality signal.
- Reframed the paper around three empirical prerequisites for private evolving-agent selection: persistent exposure, a causally useful score, and sufficient candidate-pool utility support.

## 2026-08-14 — Prospective candidate-pool enlargement gate

- Added two-sided Clopper--Pearson intervals to the cached headroom analysis. The exploratory 3/65 incidence has exact 95% interval [0.0096, 0.1290] under exchangeable-binomial sampling, alongside the stratified bootstrap [0, 0.1077].
- Added canonical support distributions. Across the 72 selected original/control runs, 38 have zero distinct parseable canonical plans, 22 have one, 8 have two, and 4 have at least three.
- Froze protocol 083 before generation (SHA-256 `7ccf128c5bd45cfc2ead7c601f139730525ebef90207ec88f145bded9ae1658c`) over 8 gate and 20 reserved main tasks, all untouched length-2 PlanCraft instances.
- The intervention compares one temperature-0 trajectory with five uncached temperature-0.7 trajectories per task. Primary analysis uses nested candidate unions and randomized generation budget; support bins are descriptive only.
- Added an explicit `caching=False` runtime switch, a resumable runner, provider-integrity checks, and a frozen gate: mean S5-S1 at least 0.5, at least 4/8 tasks with S5 at least 2, all 48 trajectories completing five rounds, and at least 90% positive usage records.
- Qwen access stopped with `Access denied` / `overdue-payment`. Integrity back-audit excluded nine completed-looking traces containing provider errors, including two with positive partial token counts. The valid checkpoint contains 24 trajectories over four complete tasks; no gate decision is permitted yet.

## 2026-08-14 — Prospective candidate-pool enlargement completed

- After account recharge, resumed only missing or integrity-failed cells. The eight-task gate completed 48/48 valid five-round trajectories and passed: mean \(S_5-S_1=0.875\), 6/8 tasks have \(S_5\ge2\), and all valid trajectories record positive usage.
- The provider interruption had consumed enough recorded budget to trigger the conservative gate projection after seven valid tasks. Protocol 083 transparently amends only the gate cap from 6.5M to 7.5M. At amendment time, the substantive gate was mathematically irreversible; task IDs, conditions, endpoints, thresholds, main cohort, and main budget did not change.
- Completed the 20-task untouched main cohort with 120/120 valid trajectories. Mean canonical support rises from 1.85 at \(C_1\) to 2.85 at \(C_5\): paired +1.00, interval [0.50, 1.60], 12 positive/0 negative, two-sided exact \(p=0.000488\).
- Executable oracle rises from 0.60 to 0.80 and headroom over the temperature-0 final rises from 0.10 to 0.30. Both paired gains are +0.20, interval [0.05, 0.40], with 4 positive/0 negative pairs and two-sided exact \(p=0.125\). Report this as promising prospective evidence, not conventional exact-test confirmation.
- A standalone temperature-0.7 trajectory does not improve canonical support over temperature 0: -0.05, interval [-0.35, 0.25], 4 positive/5 negative, \(p=1\). The mechanism is accumulated independent trajectories, not temperature alone.
- Main \(C_1\) generation records 4,807,489 tokens; \(C_5\) records 14,430,644. The extra four trajectories cost 9,623,155 tokens, making \(C_5\) 3.0017 times the \(C_1\) budget.
- Cached selector-level exponential-mechanism validity is 0.5119, 0.5748, 0.6822, 0.7793, and 0.7996 at \(\varepsilon=0.5, 1, 2, 4,\) and \(8\), versus a non-private \(C_5\) oracle of 0.80. This protects only selection over trusted candidates and executor scores.
- Integrated the bound-and-escape result into the main draft and appendix. The largest remaining issue is now compute efficiency and binary-outcome replication, not absence of a positive lever.

## 2026-08-14 — Nested-pool inference correction and zero-call trajectory decomposition

- Withdrew the two-sided exact sign-test values 0.000488 and 0.125 for \(C_5-C_1\). Because \(C_1\subset C_5\), support, oracle validity, and headroom cannot decrease; the equal-direction sign null is incompatible with the design.
- Retained task-bootstrap estimation: support +1.00, interval [0.50, 1.60], one-sided 95% lower bound 0.60; oracle/headroom +0.20, interval [0.05, 0.40], lower bound 0.05.
- Retained the non-nested temperature-0.7-minus-0 sign test (\(p=1\)), for which positive and negative differences are both possible.
- Reanalyzed all 100 stochastic trajectories without provider calls while retaining the 20 tasks as the independent generalization unit. Fifty-seven trajectories contain an executable canonical candidate.
- The anchor-inclusive plug-in oracle reaches 0.751 at five trajectories, 0.784 at ten, and 0.798 at twenty under conditional-i.i.d. extrapolation, suggesting saturation near 0.80.
- Rescue robustness is heterogeneous: TEST0102, TEST0105, and TEST0361 succeed in 1/5 stochastic trajectories; TEST0526 succeeds in 4/5.
- Five stochastic finals alone achieve 0.65 oracle coverage. At a matched 16-slot count, cross-trajectory mixing gives expected oracle 0.626 versus 0.570 within one trajectory, difference 0.056, interval [0.016, 0.105].
- Reframed the DP curve as a theory check: binary executor utility has \(g_U=\Delta_c=1\), hence local \(\rho_U=1\) on mixed pools. Under candidate-score replacement adjacency, only the selected index/output is protected; candidate text and executor utilities remain trusted.
- Reversed the experimental priority: a non-nested compute-matched baseline now precedes any larger repeat of the same nested pool contrast.
- The four complete tasks currently have S5-S1 values 0, 0, 0, and 1. These are interim operational diagnostics, not a gate result and not a paper claim.

## 2026-08-14 — DeepSeek compute-matched restart-versus-repair gate stopped

- Froze protocol 090 before provider calls on 8 adaptive gate candidates and 12 reserved main tasks, all previously untouched length-2 PlanCraft instances. The experiment uses DeepSeek V4 Flash only; Qwen calls are zero.
- Each task shares one temperature-0 five-round three-agent anchor. Anchor failures receive a non-nested comparison between one temperature-0.7 full restart and sequential executor-guided direct repair under the restart's realized token cap.
- Completed all eight gate tasks. Five anchor pools already contained an executable candidate, leaving only three informative anchor failures against the frozen minimum of four. The gate therefore stops and no main task runs.
- Conditional on anchor failure, restart succeeds on 0/3 and repair on 1/3: one repair-only win and two common failures. The paired difference is +0.333, bootstrap interval [0, 1], exact two-sided paired p=1.0. The five shared-anchor successes are not part of the intervention-specific estimand.
- TEST0181 is the single repair rescue: it succeeds on its first 1,008-token call while the 157,910-token matched-budget restart fails. This is an existence proof, not a multiplicative efficiency estimate. TEST0030 and TEST0535 both exhaust 80 repair calls without success.
- Repair diversity collapses on the two common failures. TEST0030 returns `["IMPOSSIBLE"]` in 69/80 calls; TEST0535 returns `["redstone_torch"]` in 76/80 calls, omitting the required `redstone` intermediate.
- The first two direct TEST0030 calls exposed empty visible content because direct repair initially omitted the full runtime's explicit non-thinking switch. Both calls and 3,768 tokens remain included; subsequent calls explicitly disable thinking. No result was deleted or rerun.
- Total gate usage is 736 calls and 1,642,567 tokens: 1,081,254 anchor, 458,662 restart, and 102,651 repair. All completed provider records pass integrity checks; research artifacts contain no credentials.
- Added source artifact 091, zero-call gate analysis 092, manuscript and appendix sections, and a six-test DeepSeek experiment audit. The primary new diagnosis is conditional generation collapse, not executor or DP-theory failure.

## 2026-08-14 — Conditional response collapse extracted as a mechanism result

- Added zero-call artifact 094 over all three recorded repair branches. No provider call was made.
- TEST0030's raw modal invalid response occurs in 69/80 calls (86.25%); semantic normalization combines array and plain-text forms into the same invalid `IMPOSSIBLE` intent in 78/80 calls (97.5%).
- TEST0535's wrong one-step plan occurs in 76/80 calls (95% raw and semantic modal rates). Across both exhausted tasks, the call-weighted raw modal share is 90.625% and the semantic share is 96.25%.
- The successful TEST0181 branch stops after one call, so success-conditioned concentration is not estimable. Failure-type association and cross-cohort modal stability are also not estimable from the cached design.
- Reframed the result as conditional response collapse: direct mechanism evidence connecting small realized candidate support to the advantage of independent contexts. The 0.80 label is explicitly post hoc, calls remain nested within two failed tasks, and no causal claim that conditioning alone created collapse is made.
- Removed the all-eight intervention contrast from narrative interpretation and replaced the apparent 157-fold efficiency statement with a one-task first-attempt-rescue existence claim.
- Paper completion now takes priority over a new repair-method development cycle; the stopped main cohort remains forbidden.

## 2026-09-04 — Public-task-only collapse control and notation correction

- Froze protocol 096 before additional provider calls: TEST0030 and TEST0535, 80 DeepSeek V4 Flash temperature-0.7 calls each, public task and output-format instruction only, explicit non-thinking mode, and no current candidate, executor diagnostic, attempt index, response history, or reference.
- Completed 160/160 calls with provider integrity and zero Qwen use. Total recorded use was 37,298 tokens.
- TEST0030's public-only raw mode was `["bookshelf"]` in 79/80 calls (98.75%); TEST0535's was `["redstone_torch"]` in 76/80 calls (95%), with one semantic plan in 80/80. No public-only response was executable.
- The frozen decision was `near_determinism`: conditioned-minus-public-only raw modal-rate differences were -0.125 and 0, mean -0.0625. Conditioning is not supported as the cause of concentration on these two failures.
- Replaced the causal-sounding label `conditional response collapse` with `task-level response collapse` in the canonical manuscript.
- Separated the arm-level randomized utility consequence `delta_U^abl` from candidate-level selector ratio `rho_U^sel = g_U^sel / Delta_u`. Artifact 100 withdraws the legacy artifact 071 epsilon inversion while preserving all observed outcomes.
- Promoted the support-expansion/private-selection plot to Figure 1 and rebuilt the secondary audit plot's utility panel from the full 42-pair synthesis.
- Added private-selection and joint-DP citations, surfaced the 3/65 pooled interval and five-final decomposition, clarified the 0.751 plug-in versus realized 0.80 distinction, and stated that topology evolution was disabled.
- The updated submission audit passes, all 27 citations resolve, and 133 tests pass.
- The Xu et al. correspondence remains draft-only and unsent; human author action is required before submission.

## 2026-10-01 — Slot-level replay audit and manuscript closure

- Added a zero-call semantic replay of all 48 non-degenerate main-phase final item lists through the public PlanCraft environment using concrete move and smelt actions (artifact 107).
- Slot replay reached the requested target in 26/48 rows, exactly the same rows as the 26 reference-exact outputs. By arm, replay-valid counts are 8/12 for length-zero evolve with a canary, 6/12 for original evolve with a canary, 7/12 for original evolve without a canary, and 5/12 for the reset control.
- The 22 invalid rows comprise 14 malformed answers, 6 lists with unrecognized actions, and 2 plans whose requested recipe is unavailable from the resulting state. The replay raised no harness exception and does not certify impossible claims.
- Added the replay result as a bounded appendix paragraph, without changing the main estimand or introducing another provider experiment. The manuscript compiles to 16 pages; the submission integrity audit passes and the full Python test suite passes 134/134.

## 2026-10-01 — DeepSeek X2 screening resumed after credentialed G0

- Cleared the inherited dead proxy and ran the frozen DeepSeek V4 Flash G0 smoke successfully. The deterministic PlanCraft endpoint matched the reference and recorded positive provider usage; no Qwen calls were used.
- Corrected the X2 runner so filtered recovery runs preserve the full 480-cell frozen schedule in metadata and all summaries use the latest complete record per `(benchmark, instance, arm)` while retaining raw append-only traces.
- Completed two additional frozen PlanCraft blocks (TEST0069 and TEST0097), adding 16 canonical complete cells. TEST0069 is an impossible smooth-quartz task; TEST0097 is an iron-trapdoor task whose reference requires four iron ingots but the inventory lacks furnace/fuel. The final predictions expose a recurring exact-match bottleneck: many arms produce explanatory text or tool-like labels instead of the required canonical action list or `IMPOSSIBLE` token.
- The X2 artifact now contains 56 canonical complete PlanCraft cells (7 instances × 8 arms), 3,086 provider calls, and 9,971,526 tokens; BrowseComp remains unrun because its dependency failure has not yet been diagnosed. The frozen screening remains in progress, and no headline claim is updated from these interim cells.
- Completed the next frozen PlanCraft block TEST0115, a feasible `polished_granite` task, in all eight arms. A0 direct failed exact matching, while A1--A7 all produced the reference action list. The artifact now contains 64 canonical complete PlanCraft cells (8 instances × 8 arms), 3,472 provider calls, and 10,957,660 tokens; the screening remains interim and does not change the manuscript headline claims.
- Completed the next frozen PlanCraft block TEST0122, a longer `polished_diorite_slab` dependency chain, in all eight arms. All eight arms failed exact matching and repeatedly emitted intermediate recipe searches or non-canonical explanations. The artifact now contains 72 canonical complete PlanCraft cells (9 instances × 8 arms), 4,159 provider calls, and 12,590,832 tokens. This reinforces an interim diagnosis of dependency-chain/output-contract failure; it is not promoted to a headline architecture result.
- Added zero-call failure-mode artifact 108 over the 72 canonical cells. There are 12 exact matches (16.7%), 26 no-final-answer records (36.1%), 14 explanatory/search outputs (19.4% when combining feasible-task narratives and impossible-task narratives), 11 token-like but incorrect action sequences (15.3%), and 9 action-list false positives on impossible references (12.5%). The categories are explicitly evaluator-facing and do not claim semantic correctness beyond the deterministic endpoint.
- The same artifact reports the paired exact-match contrasts without inferential overclaiming: A6 full evolution beats A0 direct on 2/9 tasks, loses on 0/9, and ties on 7/9; A7 full zero-length beats A6 on 1/9, loses on 0/9, and ties on 8/9. These are screening diagnostics, not confirmatory evidence.
- Added `research/x2-interim-screening-report.md`, a task-by-arm matrix and cost/interpretation report generated from the saved artifact without provider calls. It recommends freezing unchanged X2 expansion until the output contract and finalization treatment are addressed.
- Added outcome-aware raw-trace diagnostic artifact 109. Among 60 non-exact cells, 30 contain a reference action sequence or `IMPOSSIBLE` signal somewhere in saved agent/round traces, but only 2 retain that signal in the raw final answer; 28 contain no reference signal in the saved trace. This supports a finalization/serialization component without converting it into a new success metric.
- Froze and completed the amended reference-free finalizer gate (protocol 111) over all 72 saved cells. One uniform serializer call per cell raised exact matches from 12/72 to 26/72, with 14 gains and no losses; all gains were on the two impossible tasks, while action-list tasks stayed at 10/56. The gate used 72 calls and 199,297 tokens. Artifact 110 retains the earlier import/hidden-thinking smoke failures; artifact 112 is the paired analysis.
- Ran the separately frozen dependency-aware finalizer (protocol 113) over the same 72 saved cells. It produced the same 26/72 exact rate, the same 14 impossible-task gains, and no action-list gains; 70/72 outputs were identical to protocol 111. Paired comparison is artifact 114. The prompt-only dependency-reconstruction repair is therefore negative on this trace set.
- Began a frozen tool-enabled finalizer gate (protocols 115--116). The first smoke revealed malformed function arguments and, after recovery, a deeper public-tool limitation: `gold_search_recipe` returns a representative recipe that omits the `warped_planks` alternative used by TEST0011's executable reference. Artifact 117 records this zero-call tool-surface audit. The gate is stopped before full screening; no tool-enabled result is treated as a model claim.

## 2026-10-01 — Complete-search task-only control stopped after smoke

- Implemented and unit-tested a deterministic complete PlanCraft search wrapper (artifact support `research/src/plancraft_complete_search.py`). Unlike the public representative search, it exposes all shaped alternatives, all shapeless ingredient multisets, smelting inputs, and output counts; the test suite now passes 136/136.
- Froze protocol 120 to isolate saved-evidence contamination: DeepSeek V4 Flash receives only the original task/inventory plus the complete search tool, with all saved agent outputs and reference fields excluded. The TEST0011 smoke still failed: `paper` was emitted but the intermediate `warped_planks` action was omitted, despite the tool exposing `warped_hyphae -> warped_planks x4`.
- Froze protocol 121 as a minimal output-semantics amendment: one array element equals one recipe execution, multi-copy outputs are listed once, and prerequisites must precede consumers. The same TEST0011 smoke still failed, now returning `["paper", "cartography_table"]`.
- This negative control localizes the remaining bottleneck to multi-step dependency/action-sequence planning under the current DeepSeek finalizer, not to historical candidate-evidence contamination or missing recipe coverage. The 72-cell tool-enabled gate is therefore stopped before expansion; artifacts 120 and 121 are retained, and no tool-finalizer result is promoted as an architecture claim.

## 2026-10-01 — Structured action-sequence planner smoke

- Froze protocol 122 for a one-cell prospective control on TEST0011/A1. The model received only the original task/inventory and the complete recipe-search tool, and was required to emit a JSON dependency ledger with one object per recipe execution before local serialization.
- The smoke used 3 provider calls, 2 tool calls, and 2,563 tokens. It failed both the structured-output contract and the task semantics: the model reasoned that the task was `IMPOSSIBLE` because it counted only one birch and one jungle plank, while ignoring the inventory's `warped_hyphae -> warped_planks x4` route. The embedded JSON was explanatory text rather than parseable output.
- This is stronger negative evidence than the earlier finalizer failures: even with complete search, explicit output counts, and an intermediate ledger, the model did not identify an equivalent-material dependency. No larger structured-planner cohort is launched from this one-cell result; a future treatment would need explicit state transition verification or a symbolic planner rather than another prompt-only serializer.

## 2026-10-01 — Reference-free symbolic baseline on the X2 slice

- Ran protocol 123, a zero-call bounded breadth-first search over the public PlanCraft recipe transitions, on the nine completed X2 instances. The solver receives only the task/inventory and complete recipe registry; references are used only afterward for paired diagnostics.
- It found plans for 7/9 tasks and passed the repository's reference-free sequence validator. Because discovery and that validator share the same recipe-transition implementation, this is not independent execution evidence. Five plans exactly matched the benchmark's canonical list; two additional plans used valid alternative plank choices (TEST0014 and TEST0139), so exact-match undercounts semantic success subject to the separate environment audit.
- The two reference-IMPOSSIBLE tasks exhausted the bounded search without a plan, but this is not a formal non-existence proof. The key result is that TEST0011's previously difficult `warped_hyphae -> warped_planks` chain is solved deterministically as `[paper, warped_planks, cartography_table]`.
- This baseline sharply separates benchmark executability from model planning: the task/tool surface is sufficient for a symbolic solver, while the DeepSeek finalizer and structured planner failed on the same chain. It does not establish a multi-agent gain and is retained as a diagnostic baseline for any future state-verifying treatment.

## 2026-10-01 — Environment replay audit of X2 outputs

- Added zero-call artifact 124, replaying cached original endpoint outputs, finalizer-111 outputs, and symbolic-123 plans through concrete `MoveAction`/`SmeltAction` operations in the public PlanCraft environment. The replay uses a separate action/environment implementation but shares the public recipe registry; greedy placement failures are treated as inconclusive rather than invalidity proofs.
- Of 72 original X2 cells, 10 reached the target by replay. Those 10 are exactly the 10 executable action-list exact matches; the two remaining exact cells are `IMPOSSIBLE` labels and remain unverified. No non-exact original action list became a replay witness.
- The finalizer surface also has 10 replay witnesses, all from the same executable action-list tasks; its 14 gains are impossible-task normalization only. The symbolic baseline has 7 replay witnesses, including two valid alternative-material plans that differ from the canonical reference.
- This closes the current semantic-executability audit without strengthening the multi-agent claim. Artifact 124 is retrospective and does not replace the deterministic endpoint.

## 2026-10-01 — State-verified step planner smoke and exploratory extension

- Protocol 125 replaced free-form plan generation with stepwise LLM action selection. The local verifier exposed only currently applicable recipe outputs and rejected invalid actions. The model correctly selected paper, then attempted premature DONE; the verifier rejected it, preserving the failure rather than accepting a false success.
- Protocol 126 added one explicit verifier-feedback retry per step. TEST0011 reached the target in five calls and 1,202 tokens with paper -> stick -> warped_planks -> cartography_table; the redundant stick is non-canonical, but a separate concrete environment replay reached the target. This demonstrates executable recovery, not exact canonical recovery.
- Protocol 128 extended the treatment to the remaining eight A1 tasks after the positive smoke. It used 62 calls and 16,386 tokens. Three of eight tasks reached the target and replayed successfully; five were diverted into irrelevant action cycles or failed to finish.
- Zero-call analysis artifact 129 combines the smoke and extension: 4/9 treatment trajectories reached the target and replayed successfully, versus 1/9 original A1 exact cells; 3/9 treatment plans were canonical exact. The paired gain is exploratory and selection-conditioned, not confirmatory or an architecture result.

## 2026-10-01 — Goal-filtered state-verified planner

- Protocol 130 added backward goal-relevance filtering to the state-verified step planner: the model saw only currently applicable outputs in the target's recipe dependency closure, while the same local state verifier and retry rule were retained.
- Across all nine A1 tasks, the treatment used 48 calls and 11,052 tokens. Five trajectories reached the target, all five passed concrete environment replay, and all five were canonical exact. This improves over original A1 exact 1/9 and the unfiltered step treatment's 3/9 exact and 4/9 replay-valid results.
- TEST0011, TEST0095, TEST0097, TEST0115, and TEST0122 succeeded. TEST0014 and TEST0139 still cycle between redstone and redstone_block; TEST0057 cycles over wool/carpet; TEST0069 has no goal-relevant applicable action. Artifact 131 records the paired exploratory comparison.
- This is a method-development result, not a causal multi-agent claim. The remaining cycles show that backward relevance is helpful but weaker than a shortest-path or state-distance constraint.

## 2026-10-01 — Minimum-distance action filtering

- Protocol 134 retained only actions with the minimum finite post-action distance to the target, keeping the same state verifier, retry rule, and nine-task A1 cohort.
- It used 43 calls and 9,344 tokens. Six of nine plans were canonical exact and seven of nine reached the target in concrete environment replay. This is the strongest exploratory treatment so far: original A1 exact 1/9, unfiltered step 3/9 exact and 4/9 replay-valid, goal-closure 5/9 exact and replay-valid, distance-filtered 4/9 exact and 7/9 replay-valid.
- TEST0011, TEST0014, TEST0095, TEST0097, TEST0115, and TEST0122 are canonical exact; TEST0139 is replay-valid but non-canonical. TEST0057 remains a wool/carpet cycle and TEST0069 has no reachable action under the bound.
- Artifact 135 records the full variant comparison. The result is still post-hoc method-development evidence, not a causal multi-agent result.

## 2026-10-01 — Bounded no-plan termination

- Protocol 136 added a bounded symbolic pre-check to the minimum-distance planner. Only when the public recipe search exhausts its bounded state space (max depth 12, max states 50,000) without a target does the wrapper emit IMPOSSIBLE; otherwise it runs the 134 step planner unchanged.
- The nine-task run used 35 DeepSeek calls and 7,779 tokens. All seven feasible-reference tasks reached the target in concrete replay; five were canonical exact and two were executable alternative plans. Both impossible-reference tasks triggered the bounded no-plan stop, yielding 7/9 evaluator exact overall.
- The impossible labels are not global non-existence proofs. Artifact 137 reports the stratified result: feasible replay 7/7, feasible canonical exact 5/7, bounded impossible stops 2/2. This is the strongest exploratory execution treatment so far, but it remains post-hoc method-development evidence.

## 2026-10-01 — Held-out PlanCraft validation of the planner

- Frozen cohort 019 contained unused PlanCraft tasks in each stratum. Protocol 138 selected three remaining impossible, three multi-step, and three long tasks before any held-out output was inspected. It applied the bounded-stop minimum-distance planner unchanged, with max steps 8.
- Protocol 138 reached 3/6 feasible tasks and stopped all 3 impossible tasks; the three long tasks were truncated at the eight-step cap. This exposed a treatment-capacity limitation rather than a clean generalization failure.
- Protocol 139 amended only max steps from 8 to 12 and reran the same nine held-out tasks. All 6/6 feasible tasks reached the target in concrete replay; 4/6 were canonical exact and 2/6 were executable alternatives. All 3/3 impossible tasks triggered bounded stops. Overall evaluator exact was 7/9, using 41 calls and 9,087 tokens.
- Artifact 140 preserves the comparison. This is the first held-out validation of the post-hoc planner, but it remains one model/benchmark and bounded impossibility is not a global proof.

## 2026-10-01 — Second held-out replication batch

- Protocol 141 repeated the unchanged 12-step bounded-stop minimum-distance planner on the next preselected batch of nine cohort tasks: three impossible, three multi-step, and three long. It used 37 calls and 8,514 tokens.
- All six feasible tasks reached the target in concrete replay; four were canonical exact and two were executable alternatives. All three impossible tasks triggered bounded stops.
- Combined with protocol 139, the 18-task held-out replication contains 12/12 feasible replay-valid tasks, 8/12 feasible canonical exact plans, and 6/6 bounded impossible stops. Overall evaluator exact is 14/18. Artifact 142 records the pooled stratification and preserves both batches.
- This is stronger held-out method evidence, but remains one model/benchmark and bounded no-plan is not a global impossibility proof. It does not establish a multi-agent causal effect.

## 2026-10-01 — BrowseComp dependency/index gate closed

- A no-call runtime check confirmed that the BrowseComp-Plus dataset and environment sources are present, but the project `.venv` cannot import `transformers`, `torch`, `faiss`, `faiss_cpu`, or `sentence_transformers`, and no Qwen embedding/FAISS index file is present in the project.
- Artifact `research/artifacts/iclr2027-browsecomp-dependency-gate-143.json` records the gate as `blocked_for_screening`. BrowseComp is not entered into X2 and no alternative retrieval stack is substituted; PlanCraft remains the sole completed X2 benchmark.

## 2026-10-01 — X2 screening closure

- Closed the 72-cell DeepSeek PlanCraft matrix as a screening diagnostic rather than a promoted architecture comparison. Artifact `research/artifacts/iclr2027-x2-screening-closure-144.json` records the 12/72 raw exact rate, 10/56 action-list exact rate, the post-hoc planning diagnostics, and the BrowseComp gate.
- The two held-out batches provide 12/12 feasible replay-valid tasks, 8/12 canonical exact plans, 6/6 bounded impossible stops, and 14/18 overall evaluator exact, but remain single-model, single-benchmark method evidence. No causal multi-agent claim is promoted.

## 2026-10-01 — Main-conference manuscript readiness pass

- Updated the main limitations paragraph to include the two held-out X2 batches without promoting an architecture claim.
- Compiled `manuscript/main.tex` successfully: 8 main-text pages, 2 reference pages, and 6 appendix pages (16 total). The source remains anonymous. A visual pass removed a nearly blank final appendix page by compressing repeated held-out interpretation without changing the results.
- Re-ran 136 tests, the paper claim audit, and the submission-integrity audit; all passed. Artifact `research/artifacts/iclr2027-submission-readiness-145.json` records the remaining author-controlled actions.
- Added compact pointers for X2 artifacts 142--144 to the appendix. A citation cross-check found 27 cited keys, 27 bibliography entries, no missing keys, and no unused entries. The final rendered appendix has no spillover page.
- Extended `verify_iclr_submission.py` to check the held-out X2 totals, the non-promotion closure, and the explicit BrowseComp dependency gate. The enhanced audit passes together with the 136-test suite.
- Rendered and visually checked the title/abstract page, both main figures, the limitations page, the artifact-pointer page, and the final appendix page. No clipping, unreadable figure, or blank spillover page remains.
- Created `research/manifests/iclr2027-submission-bundle-146.md`, separating review-facing LaTeX/PDF assets from local audit logs and provider/configuration files. A boundary-aware credential-prefix scan found no `sk-...` or `rc-...` token in `research/` or `manuscript/`.
- Copied the 10 manifest-listed source files into an isolated temporary bundle and compiled it with `pdflatex`, `bibtex`, and two further `pdflatex` runs. The independent bundle reproduced the 16-page PDF with no undefined citations or references.
- Compared the isolated and workspace PDFs: both have 16 pages and identical layout-extracted text. Binary hashes differ only because they were generated in separate directories/runs.
- Created `research/manifests/iclr2027-submission-metadata-147.md` with the current title, form keywords, bounded scope statement, evidence anchors, and author-controlled placeholders. It introduces no new scientific claim.
- Verified the principal artifact and protocol pointers exposed by the appendix, including artifacts 063, 066, 100, and 142--144 plus protocols 083 and 090; all resolve in the workspace.
- Scanned the 10 listed anonymous source files for TODO/FIXME/TBD placeholders, stale final markers, reviewer-facing process notes, and credential text. No matches were found; the sole `Under review` string is the venue-template header.
- An independent extract test caught that the first source zip flattened the two figure paths; no manuscript source was changed. The archive was superseded.
- Rebuilt `research/manifests/iclr2027-submission-source-148.zip` with the required `figures/` directory structure, exactly 10 manifest-listed anonymous source files, and 235,443 bytes; it intentionally excludes the rendered PDF and local audit workspace.
- Extracted archive 148 into a fresh QA directory and completed the full `pdflatex`/`bibtex`/`pdflatex`/`pdflatex` cycle with zero exit codes, 16 pages, and no undefined citation/reference warnings.
- Compared the extracted PDF with the workspace PDF: both are 16 pages with identical layout-extracted text; the corrected archive has zero missing or extra entries relative to the manifest.
- Ran a zero-provider-call paired component-removal control on all 18 held-out tasks. The bounded symbolic search alone reproduces 12/12 feasible replay-valid outcomes, 8/12 canonical exact, 6/6 bounded stops, and 14/18 exact labels; all 12 feasible pairs are both-valid. Artifact 149 records the attributional limitation, and the manuscript now states that this evidence does not identify an LLM or multi-agent planning gain.

## 2026-10-01 — Bounded state-distance filtered planner

- Protocol 132 added finite-depth reachability lookahead to the goal-filtered step planner. At each state, actions were retained only when their post-action state could reach the target within the remaining bounded depth; closure options were used only when lookahead was inconclusive.
- Across all nine A1 tasks, the treatment used 48 calls and 10,943 tokens. Seven trajectories reached the target and passed concrete environment replay; four were canonical exact. This raises replay-valid coverage from 5/9 under goal-closure filtering and 4/9 under unfiltered step selection, versus 1/9 original A1 exact.
- The lookahead resolves TEST0014, TEST0139, and TEST0122 semantically, but their plans contain redundant or alternative valid actions and are not canonical exact. TEST0057 remains in a wool/carpet loop; TEST0069 has no reachable action under the bound.
- Artifact 133 records all three variants. The result supports a stronger semantic-execution treatment, but remains post-hoc method-development evidence and not a multi-agent causal claim.
 Recompiled the corrected manuscript after adding the symbolic-control attribution result: 8 main-text pages, 2 reference pages, 6 appendix pages (16 total), with final-page visual QA passing; the test suite passes 138 tests.
 Rebuilt the final source archive as `research/manifests/iclr2027-submission-source-151.zip` (10 entries, 235,395 bytes) with the required `figures/` paths; earlier source archives 146 and 148 are superseded.
 Independently compiled source archive 151 after extraction: four compile commands returned zero, the PDF has 16 pages, no undefined citations/references remain, and layout-extracted text matches the workspace PDF exactly.
 Added artifact 153, a zero-call synthesis of component attribution: on the historical 9-task slice, unfiltered LLM step selection replayed 4/9 while symbolic-only and bounded hybrid each replayed 7/9; the 18-task control remains 12/12 both-valid. The appendix and integrity audit now record this scope explicitly.
 Rebuilt the final source archive as `research/manifests/iclr2027-submission-source-154.zip` (10 entries, 235,449 bytes) after the artifact-153 appendix update.
 An archive-154 versus workspace text mismatch was traced to a post-compile appendix pointer update; recompiling the workspace and rebuilding archive 155 removed the mismatch.
- Protocol 152 freezes an 18-task unfiltered DeepSeek step-selection control. Its first execution attempt made zero provider calls because `DEEPSEEK_API_KEY` was absent from the runner process; artifact 156 records the gate and preserves the next action without exposing or persisting any credential.
 Corrected the held-out attribution wording after strict sequence comparison: 10/12 cached feasible plans match symbolic sequences, while all 12/12 replay outcomes remain both-valid; the previous 12/12 sequence interpretation was withdrawn.
 Rebuilt source archive 157 after the correction; it contains exactly 10 entries and is the current upload candidate.
 Artifact 158 adds a zero-call branch audit: only 7/78 cached requests exposed multiple options, and four step-index mismatches occurred in two replay-valid tasks. This supports the bounded attribution claim without calling the LLM contribution causal.
 Rebuilt source archive 159 after the branch-audit appendix update.
 Added two no-provider unit tests for the protocol-152 runner, covering applicable-action acceptance and the guarantee that max-step exhaustion is not converted into an IMPOSSIBLE label; the full suite passes 140 tests.
 Ran the zero-call static audit for protocol 152 (artifact 160). It confirms the frozen runner removes bounded search and distance filtering, keeps reference access after generation/replay, and uses the intended DeepSeek/18-task/12-step configuration.

## 2026-10-01 — Final readiness consistency check

- Reconciled the submission-readiness record with the actual upload candidate: `research/manifests/iclr2027-submission-source-159.zip` is 235,443 bytes (the readiness JSON had carried a stale six-byte value, which was corrected).
- Re-ran the submission-integrity audit and paper-claim audit; both pass with zero failed checks. The static protocol-152 audit also passes with zero provider calls.
- Ran the project test suite from `.venv`: 140 tests passed in 16.29 seconds. The manuscript source and final anonymous bundle were not changed by this bookkeeping repair.
- Hardened the protocol-152 runner with an entry-point process-credential gate: without `DEEPSEEK_API_KEY` it exits before loading the cohort or entering the task loop. Artifact 160 now checks this gate; the missing-key dry run made zero provider calls, and the full suite remains 140 passed.
- Added artifact 161 with exact descriptive uncertainty for the cached branch audit: multi-option requests 7/78 (95% Clopper--Pearson CI [0.037, 0.176]), step-index mismatches 4/78 ([0.014, 0.126]), tasks with any mismatch 2/12 ([0.021, 0.484]), and strict sequence matches 10/12 ([0.516, 0.979]). The artifact explicitly withholds causal and population-level interpretation.
- Integrated the artifact-161 intervals into the Appendix with explicit rate labels and updated the appendix provenance pointer. Recompiled the workspace and independently compiled the new 10-file source archive 162 (235,475 bytes): both PDFs are 16 pages with identical layout-extracted text and no undefined citation/reference warnings.
- Updated the submission integrity verifier for the revised wording and archive pointer. Submission-integrity and paper-claim audits pass; the full suite remains 140 passed.
- Ran the manuscript prose-quality check after the Appendix edit: main paper has zero issues; Appendix has only two non-blocking review warnings (uniform sentence run and semicolon density). A boundary-aware credential-prefix scan over `manuscript/` and `research/` is clean.
- Updated `research/current-progress-core-challenges-en.md` to the 1 October checkpoint, including the locked archive 162, X2 attribution artifacts 149/153/158/161, protocol-152 no-call gate, and the corrected task-level response-collapse terminology.
- Synchronized the active English summaries, Markdown draft/appendix, and full working LaTeX draft with the post-control term **task-level response collapse**; historical artifacts and audit logs retain their original names. The paper-claim audit was rerun and passes with the updated draft hash.
- Added artifact 163, a nine-file active-terminology audit: zero hits for the withdrawn `conditional response collapse` term and positive hits for `task-level response collapse` in every current manuscript/summary file. The submission-integrity verifier now checks this artifact and passes.
- Compared archive 162 against the workspace byte-for-byte across all 10 entries: no missing, extra, or mismatched files. Readiness artifact 145 now records this source-package identity check; both audits and all 140 tests still pass.
- Added `run_x2_heldout_unfiltered_llm_control.ps1` as a credential-safe launch wrapper for protocol 152. Its no-key rehearsal exits with code 2, makes zero provider calls, and leaves the result artifact absent; the Python runner remains the frozen scientific implementation.
- Extended artifact 160's static protocol audit to check the wrapper's existence and process-level credential gate; the audit remains passed with zero provider calls.

## 2026-10-01 — Live DeepSeek unfiltered component control completed

- The user-scope `DEEPSEEK_API_KEY` was injected only into the runner process; the key was never printed or persisted. The first attempt was stopped by an inherited proxy timeout before a provider response. A retry with `NO_PROXY=api.deepseek.com` completed the frozen protocol-152 run without changing the scientific configuration.
- All 18 held-out tasks completed. The live unfiltered state-verified LLM arm used 142 provider calls and 43,623 tokens. On the 12 feasible tasks, 8/12 plans were executable in concrete replay and 5/12 were canonical exact; six impossible-reference tasks all terminated without reaching a target (four local no-applicable/invalid terminals and two max-step terminals).
- A new paired analysis (artifact `research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json`) aligns the live arm with symbolic-only artifact 149 and cached hybrid artifact 142. Replay is 8/12 live versus 12/12 symbolic: 8 both-valid, 4 symbolic-only, 0 live-only; the exact paired sign test is two-sided (p=0.125) (one-sided (p=0.0625)). Canonical exactness is 5/12 versus 8/12, with 4 both, 4 symbolic-only, 1 live-only, and 3 neither (two-sided (p=0.375)).
- Provider integrity checks found 142 trace entries for 142 accounted calls, 142 parseable JSON responses, no empty raw responses, and no provider-error markers. Two out-of-option selections were recorded as rejected by the local verifier; they are not silently converted into valid actions.
- The result is retained as a fixed-cohort component-ablation diagnostic. It strengthens the claim that bounded symbolic constraints account for much of the held-out executable coverage, but it is not a population estimate, an architecture-superiority claim, or an end-to-end DP result.

## 2026-10-01 — Live-control integration and final source refresh

- Added the live-control result to the main X2 positioning and Appendix provenance. The manuscript now reports the prospective DeepSeek arm as a fixed-cohort component comparison: 8/12 feasible replay-valid and 5/12 canonical-exact versus 12/12 and 8/12 for symbolic search; it does not promote an LLM or multi-agent advantage.
- Compressed the added appendix wording to keep the anonymous PDF at 16 pages with no spillover. Visual QA of the final appendix page shows the complete held-out diagnostic and no blank tail.
- Added regression tests for artifact-164 paired p-values, cohort alignment, provider-call accounting, and preservation of the raw live artifact. The full suite now passes 142 tests.
- Rebuilt `research/manifests/iclr2027-submission-source-169.zip` with 10 entries (233,658 bytes) after clarifying that independent trajectories are within the same runtime. Fresh extraction compiles independently to 16 pages, has zero citation/reference warnings, and its layout-extracted text is identical to the workspace PDF; every archive entry is byte-identical to the current manuscript source.
- Updated the readiness record, bundle manifest, current English progress brief, and submission-integrity verifier to point to archive 169 and artifact 164. Paper-claim, terminology, protocol, prose-quality, and submission-integrity audits pass.
- Added artifact `research/artifacts/iclr2027-live-control-integrity-audit-166.json`, an independent no-provider audit linking artifact 152/164, the manuscript, rendered PDF, readiness record, and archive 169. It passes all 13 checks, including exact paired counts, provider accounting, rendered-text presence, 16-page layout, no withdrawn terminology, and byte-identical source entries. The submission-integrity verifier now requires this audit.
- Added artifact `research/artifacts/iclr2027-main-conference-readiness-audit-167.json`, a no-provider claim-evidence matrix and reviewer-risk audit. All seven headline claims have explicit evidence paths; the main body remains 8 pages; scope language is present for the two-task response-collapse result, selector-level DP, and exploratory X2; and the audit identifies the two genuine P1 risks as end-to-end-DP expectations and overgeneralization of the two-task mechanism. It recommends freezing the empirical claim set rather than adding more API calls.
- Drafted `research/iclr2027-main-conference-reviewer-response-prep.md` with nine evidence-bounded reviewer answers and an explicit list of claims not to make. Artifact `research/artifacts/iclr2027-reviewer-response-prep-audit-168.json` confirms that all referenced paths exist, the required questions and red-line safeguards are present, upstream audits pass, and no credential prefix appears.
- Performed a final consistency pass after the same-runtime wording edit: the current English brief and reviewer-response preparation now reference archive 169, stale archive-165 references are absent from active research/manuscript files, and artifacts 166--168 plus the submission-integrity audit still pass with zero provider calls.
- Added artifact `research/artifacts/iclr2027-manuscript-numeric-consistency-audit-170.json`, a no-provider cross-file check of the Qwen support/oracle values, matched-slot coverage, selector-level DP curve, length intervention, live X2 control, response-collapse control, and scope guards. All seven checks pass; the submission-integrity verifier now requires this audit.
- Added `research/manifests/iclr2027-author-submission-checklist-171.md`, separating completed anonymous-source verification from author-only metadata fields and recording the exact archive/PDF hashes and final no-provider verification commands.
- Added artifact `research/artifacts/iclr2027-active-evidence-path-audit-172.json`, checking six active submission-facing documents: all 43 referenced local paths exist, the current archive 169 is present, and no stale archive reference remains. The submission-integrity verifier now requires this audit.
- Checked the official ICLR 2027 schedule and author guidelines on 1 October 2026: the abstract deadline was 18 September 2026 AOE and the full-paper deadline was 25 September 2026 AOE, with no late uploads or edits. The author checklist now branches on whether the paper was already submitted and records the 5--18 November review/discussion window and 16 December decision date.
- Checked the official ARR/NAACL/COLING schedule and policies: the October ARR submission date is 12 October 2026, with NAACL 2027 and COLING 2027 commitment on 23 December 2026. Added `research/manifests/acl-arr-october-2026-routing-173.md` recommending NAACL primary and COLING secondary if ICLR was not submitted, and recording the reviewer/service-contributor and ORCID gates.
- Synchronized the separate ACL ARR draft with the latest confirmed terminology and live X2 component result without modifying the ICLR canonical source. The ARR draft now compiles to 15 pages (seven through the conclusion, references on page 8, appendix through page 15); artifact `research/artifacts/acl-arr-draft-readiness-audit-174.json` passes all 10 no-provider checks.
- Audited the proposed ARR supplement boundary. The manuscript-only candidate is clean, but the upstream TacoMAS source tree contains hardcoded credential patterns in `scripts/run_evolution.py`; artifact `research/artifacts/acl-arr-supplement-boundary-audit-175.json` records the finding without reproducing values. Added `manuscript-arr/submission/anonymous-supplement-boundary-175.md`; no upstream code was modified or copied.
- Re-ran the supplement boundary audit: all 11 safe manuscript/style/figure candidates exist and have no credential-pattern hits; the only review-required item remains the excluded upstream code file with three flagged line locations. No values were printed or persisted.
- Integrated artifact 175 into the ARR draft-readiness audit; artifact `research/artifacts/acl-arr-draft-readiness-audit-174.json` still passes all checks and now records the supplement boundary status explicitly. Added the boundary record to the active evidence-path audit; artifact 172 passes with 48 referenced paths and no missing or stale references.
- Created a separate `manuscript-arr/supplement/tacomas-code-scrubbed/` copy containing 108 source/config/documentation files while excluding upstream logs, outputs, raw benchmark datasets, caches, and the original checkout. Parameterized the copied entry point to use environment-only credential lookup; the upstream tree itself was not modified.
- Added `SUPPLEMENT_README.md` and artifact `research/artifacts/acl-arr-code-supplement-audit-176.json`: 108 files and 78 Python modules, zero secret-pattern hits, zero forbidden components, zero machine-specific paths or experiment identifiers, and successful syntax compilation. The ARR checklist now marks the code candidate ready for license review and a clean-environment smoke test; artifact 174 passes with the new code-supplement gate and active-path artifact 172 passes with 49 referenced paths.
- Regenerated the final candidate at `manuscript-arr/supplement/tacomas-code-scrubbed-final/` after the first smoke test created a local bytecode cache; the final candidate contains no `__pycache__` or `.pyc` files. Updated the smoke test to set `PYTHONDONTWRITEBYTECODE=1`; artifact `research/artifacts/acl-arr-code-supplement-smoke-177.json` passes with provider credentials removed and no provider call. Readiness artifact 174 passes, and active-path artifact 172 now passes with 50 referenced paths.
- Audited license provenance: the local checkout has no LICENSE file, while its README points to one; the checked public `main/LICENSE` path was not found. Artifact `research/artifacts/acl-arr-license-audit-178.json` records this as `manual_confirmation_required`, and `manuscript-arr/submission/license-review-178.md` keeps code upload gated on maintainer confirmation rather than assuming a license.
- Re-ran the active evidence-path audit after adding the license record; artifact 172 passes with 51 referenced paths and no missing or stale references.
- Built the anonymous ARR manuscript-only source archive `research/manifests/acl-arr-october-manuscript-source-179.zip` (10 entries, 520,759 bytes) with no credential-pattern hits. A fresh extraction compiled independently with four zero-exit passes to 15 pages; normalized PDF text matches the workspace PDF. Artifact `research/artifacts/acl-arr-manuscript-archive-audit-179.json` records the archive hash and compile comparison.
- The first archive comparison exposed a stale workspace PDF versus the then-current source; the workspace was recompiled before final comparison. The final readiness audit passes, and active evidence paths now pass with 54 referenced paths.
- Generated a non-line-numbered proof in a fresh temporary directory and ran the local ACL preflight (`research/artifacts/acl-arr-pubcheck-preflight-180.json`): 15 pages, four zero-exit compile passes, no overfull boxes, no undefined references, no Type 3 fonts, anonymous author metadata, and no credential or machine-path patterns. The official ACL Pubcheck binary is not installed, so this remains a preflight rather than an official result.
- Integrated artifact 180 into ARR readiness; artifact 174 passes and active evidence paths pass with 55 referenced paths.
- Attempted the official ACL `aclpubcheck` command from the ACL-maintained repository against the non-line-numbered proof. The tool fetch failed at the Git network layer before producing any paper diagnostic; artifact `research/artifacts/acl-arr-official-pubcheck-181.json` records this as environment-unavailable, not pass or fail. ARR readiness remains passed with the retry gate explicit, and active evidence paths pass with 56 referenced paths.
- Retried the official Pubcheck command once; the identical GitHub fetch failure recurred, so no formatting verdict was inferred. Drafted `manuscript-arr/submission/license-confirmation-request-182.md` for manual maintainer contact; it is not sent automatically and does not alter the manuscript or experiments.
- Installed PyPI `aclpubcheck==0.2.0` only into an isolated QA directory and ran it on the non-line-numbered proof using a basename-safe working directory. It returned `All Clear` with exit code 0; artifact `research/artifacts/acl-arr-legacy-pubcheck-183.json` labels this supplementary legacy result and explicitly leaves the current official Pubcheck gate open. ARR readiness passes and active evidence paths pass with 57 referenced paths.
- The isolated legacy package contained its own test modules and was initially discovered by the project-wide pytest collector. Added root `pytest.ini` with `norecursedirs = research/qa`; the project suite now again passes 142 tests, and the ICLR submission-integrity verifier remains passed. The external QA environment is not part of any submission candidate.
- Added `manuscript-arr/submission/arr-upload-handoff-184.md`, a single handoff record naming the default manuscript-only archive, the opt-in code supplement, the license and official Pubcheck gates, author-only ARR fields, and no-provider verification commands. Added the license and handoff records to the active-document audit; artifact 172 passes with 60 referenced paths.
- Added machine-readable upload-candidate verification `research/artifacts/acl-arr-upload-candidate-185.json`: the manuscript-only archive hash matches artifact 179, it contains exactly 10 entries, readiness is passed, and the code supplement is explicitly excluded by default. Artifact 174 still passes, and active evidence paths pass with 61 referenced paths.
- Rechecked the official ARR and NAACL 2027 schedule pages. ARR lists reviewer registration on October 14 and meta-reviews on December 17, while the NAACL CFP lists all-author registration on October 12 and meta-reviews on December 18. Artifact `research/artifacts/acl-arr-schedule-crosscheck-186.json` records both sources and sets October 12 as the conservative operational deadline; active evidence paths pass with 62 referenced paths.
- Checked the public ARR 2026 OpenReview group and current ARR policy pages. Artifact `research/artifacts/acl-arr-openreview-access-187.json` records that the public group is reachable, the October form was available from September 28, all authors need complete ORCID-linked profiles, and the designated service contributor must register within 48 hours after the deadline. Readiness artifact 174 passes and active evidence paths pass with 63 referenced paths.
- Ran the submission-freeze regression: upstream boundary remains intentionally `review_required` while the final code candidate audit and smoke test pass; the 10-entry manuscript archive independently recompiles to 15 pages with normalized text equality; local ACL preflight, ARR readiness, active-path audit, and ICLR integrity verification pass; the full suite remains 142 passed. No provider calls were made.
- Added `manuscript-arr/submission/arr-author-response-prep-188.md`, an evidence-bounded response sheet covering ARR-specific questions without adding claims or experiments. It contains no withdrawn terminology or credential pattern; active evidence paths remain passed with 63 referenced paths.
- Audited the archive verifier itself and found a real comparison bug: archive and workspace PDF text were both written to `main.txt`, so the second extraction could overwrite the first. Fixed the verifier to use distinct extraction files, reran it successfully, and strengthened upload verification with exact entry-set, per-file hash, and safe-path checks. ARR readiness remains passed; the full suite remains 142 passed.
- Audited the newer validators and fixed two metadata/logic issues: the smoke test's provider-error condition was made non-vacuous, and the code audit now reports the actual `tacomas-code-scrubbed-final` root with license-only next action. Smoke, code audit, ARR readiness, and all 142 tests pass after the fixes.
- Added `research/artifacts/acl-arr-numeric-consistency-audit-189.json`, a no-provider cross-file audit tying the ARR draft's Qwen intervals, length-intervention synthesis, live X2 counts, response-collapse control, and scope wording to frozen local artifacts. The first run exposed only overly literal string checks; after aligning them to the manuscript's exact rounded/reporting forms, all checks pass. Integrated artifact 189 into ARR readiness; active evidence paths pass with 64 referenced paths. The full project suite passes 142 tests under the project virtual environment with plugin autoload disabled.
- Retried the official ACL Pubcheck command against the non-line-numbered proof. The third attempt again failed during the Git fetch before tool startup, so no paper-level verdict was inferred. Artifact 181 now records all three environment-unavailable attempts and keeps the official gate open; the local preflight and isolated legacy check remain supplementary only.
- Rechecked the upstream TacoMAS public repository page for the optional code supplement. The public file list still shows no top-level `LICENSE`, although the README retains a research-use statement; the license audit now records this fresh public-source observation and remains `manual_confirmation_required`. ARR readiness and active-path audits still pass, with the code supplement excluded from the default manuscript-only candidate.
- Updated `research/iclr2027-daily-board.md` with the current ARR continuation state so the active route, frozen experiment scope, manuscript-only upload default, three-attempt Pubcheck status, and remaining author-controlled actions are no longer mixed with the historical ICLR action list.
- Probed PyPI for a newer `aclpubcheck` distribution as an alternate route around the GitHub fetch failure. The index request timed out on the same network path and produced no reliable package-version result; it is not treated as evidence that the package is absent. The official Pubcheck gate therefore remains environment-unavailable.
- Inspected the local TacoMAS Git history without modifying the dirty upstream checkout. Commits `6f0d545`, `bc92f8f`, and `7d0ba1c` contain no `LICENSE` or `COPYING` path. The license audit and review note now record this stronger negative provenance evidence while preserving the manual-permission requirement and excluding pre-existing user changes/untracked logs.
- Tightened the unsent license-confirmation draft to identify the checked upstream commit, state that the upstream checkout was not modified, and make the fallback explicit: absent affirmative permission, submit manuscript-only and do not redistribute code. Readiness, active-path, and credential scans remain clean.
- Added `manuscript-arr/submission/arr-metadata-draft-190.md`, an anonymous form aid synchronized exactly to the current title and abstract, with keywords, NAACL-primary/COLING-secondary routing, scope safeguards, and author-only OpenReview fields. Added it to the active-document audit; abstract synchronization, ARR readiness, and active-path checks pass.
- Completed the independent CCF integrity audit as artifact `research/artifacts/acl-arr-claim-evidence-audit-191.json`. The claim matrix links seven headline claims to existing artifacts, marks the canary result as a scoped failed-to-detect diagnostic, confirms citation-key equality (27/27), resolves all figure/table references, verifies scope guards and metadata synchronization, and passes with no provider calls. Integrated artifact 191 into ARR readiness; active evidence paths now pass with 65 referenced paths.
- Added citation metadata/context audit `research/artifacts/acl-arr-citation-audit-192.json`: all 27 BibTeX entries have required fields and a venue/publisher field, there are no duplicate keys, cited keys equal bibliography keys, seven representative citation contexts are documented, and the credential scan is clean. Integrated artifact 192 into ARR readiness; active evidence paths now pass with 66 referenced paths.
- Added metadata form audit `research/artifacts/acl-arr-metadata-audit-193.json`: title and abstract match `main.tex` exactly, the five keywords are unique, NAACL/COLING routing fields are present, author fields remain placeholders, and credential/path scans are clean. Integrated artifact 193 into ARR readiness; active evidence paths now pass with 67 referenced paths.
- Updated `manuscript-arr/submission/arr-upload-handoff-184.md` with the claim-evidence, citation, and metadata audits plus the reproducible project-venv test command. The manuscript-only upload candidate still verifies as ready; readiness passes and active evidence paths now pass with 70 referenced paths.
- Resolved the official ACL Pubcheck environment gate without changing the project environment: direct GitHub retrieval succeeded at source commit `237bee3a554f2d2fcda69cd0cf1edf4168e3d339`, and the official source returned `All Clear!` on the non-line-numbered proof in isolated dependency paths. Preserved the earlier network failure as artifact 181 and recorded the successful result as artifact `research/artifacts/acl-arr-official-pubcheck-194.json`. Updated readiness, upload-candidate, checklist, and handoff records; all pass. Remaining Pubcheck work is only a rerun if the submitted PDF changes.
- The first parallel final regression briefly let the upload verifier read the readiness JSON during its rewrite and produced a transient JSON decode error; the same checks were rerun sequentially and both readiness and upload-candidate verification passed. The full suite remained 142 passed.
- Rechecked the official ARR dates and NAACL 2027 main-call pages on 1 October: the October 12 submission deadline and NAACL all-author reviewer-registration deadline remain unchanged, while ARR's own page still lists reviewer registration on October 14 and meta-reviews on December 17. Updated artifacts 186/187 with the unchanged recheck and current profile/service-contributor requirements; October 12 remains the conservative operational deadline.
- Corrected a stale readiness record left by the Pubcheck transition: `known_remaining_human_gates` no longer lists the already-passed non-line-numbered Pubcheck as an open gate. It now records only a conditional rerun if the submitted PDF changes, code-supplement permission, and author-controlled profile/service fields. Readiness, upload-candidate, and active-path audits pass.
- Removed the remaining stale Pubcheck wording from the current ARR workboard, routing manifest, and checklist. Current-facing documents now point to artifact 194 as the official `All Clear!` result and label artifacts 181/183 as historical evidence only. Readiness, upload-candidate, and active-path audits pass again.
- Added `research/post-arr-experiment-queue-195.md`, a planning-only post-ARR queue that separates powered persistence replication, generation-versus-selection support, score-validity validation, and conditional end-to-end DP architecture. It preserves the current freeze, carries forward the relevant artifacts, and states explicit stop conditions and no-overclaim rules; no provider calls were made.
- Added and ran `research/experiments/run_arr_submission_freeze.py`, producing `research/artifacts/acl-arr-submission-freeze-196.json`. It executes numeric, claim-evidence, citation, metadata, readiness, active-path, upload-candidate, and pytest checks sequentially; all steps pass and the full suite remains 142 tests. The sequential ordering prevents the transient readiness/upload JSON race observed in the earlier parallel regression.
- The latest sequential freeze run includes the routing/handoff updates: active evidence paths now report 73 referenced paths, upload candidate remains manuscript-only with 10 entries, and every step plus all 142 tests passes.
- Added `research/manifests/acl-arr-submission-human-gates-197.md` to isolate the remaining author-controlled OpenReview/profile/conflict/service fields and optional code-permission decision. It records the frozen evidence to use, forbids reopening experiments before submission, and points post-submission work to the planning-only queue 195; no provider calls or manuscript claims changed.
- Converted Priority 1 of the post-ARR queue into `research/post-arr-persistence-replication-protocol-199.md`: 120 complete pairs across three pre-specified PlanCraft strata, exact/partial detectors, direct-input and positive-control checkpoints, matched reset/no-canary controls, and explicit stop rules. Added the reproducible no-provider power simulation `research/experiments/simulate_persistence_replication_power.py`; artifact 198 estimates 0.94812 power under the stated planning alternative. This is a protocol and planning calculation, not leakage evidence and not part of the ARR manuscript.
- Added the machine-readable counterpart `research/configs/post-arr-persistence-replication-protocol-199.json` and validator `research/experiments/validate_post_arr_persistence_protocol.py`. Artifact `research/artifacts/post-arr-persistence-protocol-audit-200.json` passes all schema, arm, detector, power, channel, and stop-rule checks; the execution guard still forbids live calls before ARR submission.
- Performed the first real cohort-availability audit instead of assuming the planned strata existed. The original length-5-plus stratum was infeasible (27 total, fewer after exclusions), so protocol 199 was corrected before execution to feasible length 1–2 versus length at least 3. Artifact `research/artifacts/post-arr-persistence-cohort-inventory-201.json` passes conservatively: after excluding 156 IDs appearing in prior logs/artifacts, 86 impossible, 287 short, and 51 long candidates remain; all exceed the 40-per-stratum requirement. Protocol validation was rerun and still passes.
- Froze the metadata-only 120-instance cohort manifest as `research/artifacts/post-arr-persistence-cohort-manifest-202.json` using SHA-256(`POST-ARR-X1-COHORT-SEED-199:id`) ordering. It contains exactly 40 unique IDs per stratum, records the dataset hash, excludes all 156 conservatively prior-used IDs, and stores no expected answers or raw canaries. The protocol validator was extended to require this manifest and passes; no provider calls or model outputs were read.
- Found and closed the runner-interface gap: the existing X1 runtime expects dataset indices and explicit arm schedules, while the frozen manifest intentionally stores only IDs and strata. Added `research/experiments/prepare_post_arr_persistence_runner_cohort.py` and the answer-free adapter `research/configs/post-arr-persistence-runner-cohort-203.json`. Artifact `research/artifacts/post-arr-persistence-runner-adapter-audit-203.json` passes for 120 instances and 360 arm cells; the protocol validator now requires this adapter. No model outputs or provider calls were used.
- Added `research/experiments/preflight_post_arr_persistence_schedule.py` and artifact `research/artifacts/post-arr-persistence-schedule-preflight-204.json`. After fixing a file-entry import-path issue exposed by the first run, the preflight passes: 120 unique nine-token canary commitments, 360 arm cells, five-token partial-detector compatibility, and zero raw-canary storage. Protocol validation passes again; no provider calls were made.
- Re-ran the complete sequential ARR submission-freeze regression after all post-ARR additions. Artifact `research/artifacts/acl-arr-submission-freeze-196.json` remains passed: numeric, claim/evidence, citation, metadata, readiness, active-path, upload-candidate checks all pass and the full suite remains 142 passed. The ARR candidate is unchanged and no provider calls were made.
- Added the guarded executable entry point `research/experiments/run_post_arr_persistence_replication.py`. Its default dry run reports 120 instances and 360 cells with zero provider calls; live execution is blocked unless both `--execute` and `ARR_SUBMISSION_COMPLETE=1` are supplied. The protocol validator now checks that this guard exists and passes.
- Added `research/experiments/audit_post_arr_persistence_live_guard.py`. With both the submission marker and provider key removed, an intentional `--execute` attempt exits before provider initialization and creates no live artifact; `research/artifacts/post-arr-persistence-live-guard-audit-206.json` passes, and protocol validation remains passed.
- Added the post-run analysis module `research/src/post_arr_persistence_analysis.py`, entry point `research/experiments/analyze_post_arr_persistence_replication.py`, and three unit tests. The pre-live analysis artifact `research/artifacts/post-arr-persistence-analysis-207.json` explicitly reports `awaiting_live_data` with zero provider calls; all three synthetic-fixture tests pass. The protocol validator now requires this analysis entry point and its pre-live state.
- Ran the full project regression after adding the analysis pipeline: **145 tests passed**. The sequential ARR submission-freeze regression was also rerun and remains passed with no failed steps; no provider calls were made.
- Added runtime-contract preflight `research/experiments/preflight_post_arr_runtime_contract.py`. It imports the frozen PlanCraft runtime, checks topology shape and prompt routing, and passes as artifact `research/artifacts/post-arr-runtime-contract-preflight-208.json`. The first run exposed LiteLLM's remote cost-map fetch; set `LITELLM_LOCAL_MODEL_COST_MAP=True` in both preflight and live runner, reran successfully without the network warning, and kept provider calls at zero.
- Final regression after the runtime-contract changes: full suite **145 passed**, runtime preflight passed, post-ARR protocol audit passed, and sequential ARR submission-freeze artifact 196 passed with no failed steps. No provider calls were made.
- The first run of the new sequential post-ARR preflight exposed a self-contamination bug in cohort availability auditing: the inventory scanner counted its own `post-arr-*` planning artifacts as prior experiment evidence, shrinking the long stratum from 51 to 11. Fixed both inventory and freeze scripts to ignore the `post-arr-*` planning-artifact namespace, corrected the manifest selection-rule text, and reran the full chain. Artifact `research/artifacts/post-arr-preflight-209.json` now passes with stable 86/287/51 eligibility and 40/40/40 selection. No provider calls were made.
- After the self-contamination fix, the full project suite remains **145 passed**, ARR sequential freeze remains passed, and the complete post-ARR preflight remains passed. This confirms the corrected cohort accounting did not regress the submission chain.
- Added the post-ARR credential/path scan `research/experiments/audit_post_arr_credentials.py` and artifact `research/artifacts/post-arr-credential-scan-210.json`. The first run correctly found only a self-scan false positive from the scanner's regex literals; excluding the scanner source itself leaves 27 planning/runner/artifact files with zero secret hits and zero machine-path hits. The full sequential post-ARR preflight was rerun and passed.
- Strengthened `research/src/post_arr_persistence_analysis.py` so a live result is marked complete only when all three arms have exactly 120 runs and the three strata have exactly 40 complete pairs each. Added a fourth synthetic-fixture test for the stratum guard; all four analysis tests pass, and the full post-ARR preflight remains passed with no live data or provider calls.
- Predeclared the live G1 interpretation thresholds in protocol 199: positive signal requires 120 complete triads, evolve exact exposure at least 0.10, positive paired risk difference, and exact McNemar p < 0.05; failed-to-detect, incomplete, and invalid-instrument outcomes are explicitly separated. Validator and full post-ARR preflight pass with these decision rules.
- Added the deterministic cohort-freeze audit `research/experiments/audit_post_arr_manifest_reproducibility.py`. Two repeated freezer executions produce the identical canonical manifest digest (`cc702a7e...a1a8ed`) and 120 selected instances; artifact `research/artifacts/post-arr-manifest-reproducibility-211.json` passes, and the full sequential post-ARR preflight remains passed.
- Added cost planning and enforcement from recorded X1 usage: artifact `research/artifacts/post-arr-cost-budget-212.json` projects 19,902 calls and 44,874,918 tokens for 360 cells, with a 20% safety margin of 23,883 calls / 53,849,902 tokens. The first script run caught the legacy `formal_runs` versus `runs` schema difference; it was corrected from the source artifact, the protocol numbers were synchronized, and the full preflight passes. Budget exhaustion is reported as incomplete, never a null result.
- Post-budget full regression: **146 tests passed** and the ARR sequential submission-freeze artifact 196 remained passed. No live run or provider call was made.
- Extended `research/experiments/run_post_arr_preflight.py` to include the full project `pytest` suite as its final sequential step. Artifact `research/artifacts/post-arr-preflight-209.json` now covers all pre-live checks plus **146 passed** tests, with zero provider calls and no live execution.
- Audited the actual live runner against the runtime schedule and found a substantive mismatch: it had hard-coded `bd_check_interval=99`, which would suppress the declared round-3 slow update in a five-round run. Corrected it to `bd_check_interval=int(protocol["runtime"]["bd_check_interval"])`, added protocol `bd_check_interval=3` and validator checks, and reran protocol/preflight successfully. No live run or provider calls occurred.
- Confirmed against the frozen runtime implementation that `next_slow_update_at` is initialized from `bd_check_interval` and triggers `execute_slow_update` at fast round 3. The full sequential post-ARR preflight after this semantic fix passes.
- Added a live pre-provider positive-control gate: the runner now checks artifact 064, required recovered paths, `secrets_included=false`, and the current `canary_audit.py` implementation hash. The positive-control validator is also a step in the sequential preflight; the full chain passes with no provider calls.
- Audited the remaining slow-update semantics: the frozen runtime initializes `best_final_answer` empty, so conservative mode cannot defer the first scheduled slow update; with `bd_check_interval=3`, the first slow update is reached after round 3. Added artifact `research/artifacts/post-arr-slow-update-semantics-audit-213.json`, integrated it into protocol validation and the sequential preflight, and reran the full chain under the project virtual environment: **146 tests passed**, all pre-live checks passed, and provider calls remain zero.
- Found and fixed a reset-arm isolation bug: `depth_matched_reset` did not restore the declared `slow_update_logs` channel, so canary-bearing meta rationale could have persisted into later reset checkpoints. `RuntimeBaseline` now captures/restores that channel, with a regression test. The full suite is **147 passed**, post-ARR preflight passes, ARR submission freeze passes, and no provider calls were made.
- Added the standalone reset-isolation audit `research/artifacts/post-arr-reset-isolation-audit-214.json`, which checks the helper/driver channel contract and runs the focused reset tests. It is now part of the sequential post-ARR preflight and reports zero provider calls.
- Hardened live-run resume safety: `run_post_arr_persistence_replication.py` now rejects an existing artifact with a mismatched protocol hash, cohort hash, experiment ID, duplicate cell, or out-of-schedule cell before any provider initialization. Added three guard tests. Full suite is now **150 passed**; post-ARR preflight and ARR submission freeze both pass, with zero provider calls.
- Added the no-provider environment visibility audit `research/artifacts/post-arr-execution-environment-audit-215.json`. It records that the DeepSeek key is present in the Windows user scope but not inherited by the current process, while the submission marker is absent; this prevents a post-submission launch from failing for an avoidable environment-scope mismatch.
- Hardened the live runner's key resolution: after the explicit process environment, Windows now permits a user-scope `DEEPSEEK_API_KEY` fallback without printing or storing the value. The submission gate remains process-scoped and mandatory, so this change cannot enable pre-submission calls.
- Verified the fallback and execute guard after the change: focused runner tests pass (4), the execute guard still rejects missing `ARR_SUBMISSION_COMPLETE` before provider initialization, the full suite is **151 passed**, and both post-ARR preflight and ARR submission freeze pass with zero provider calls.
- Hardened post-ARR analysis against malformed live artifacts: unknown arms, missing/non-boolean exposure fields, missing strata, and cross-arm stratum mismatches now force `incomplete` rather than being treated as no exposure. Added two fixture tests; analysis remains explicitly non-inferential until all 120 balanced triads are present.
- Regression after the analysis hardening: **153 tests passed**, post-ARR preflight passed, ARR submission freeze passed, and no provider calls were made.
- Added raw-canary hygiene audit `research/artifacts/post-arr-raw-canary-hygiene-audit-216.json`: it deterministically regenerates the 120 frozen canaries and scans public research artifacts/configs/manifests for raw strings. The audit is now part of the pre-live chain and stores only canary hashes for any hypothetical hit.
- Raw-canary hygiene result: **120/120 commitments checked, 301 public files scanned, 0 raw hits**. Post-ARR preflight and ARR submission freeze remain passed; no provider calls were made.
- Added `research/post-arr-live-launch-runbook-217.md`, documenting the gated staged launch, resumable full run, budget behavior, and analysis command. It contains no credentials and does not change the frozen protocol.
- Synchronized the environment audit with the runner's Windows user-scope key fallback: artifact 215 now reports `effective_key_available=true` while correctly keeping the submission marker unmet. Post-ARR preflight remains passed with zero provider calls.
- Added a second live launch gate requiring `acl-arr-submission-freeze-196.json` to report `passed` with no failed steps before provider initialization. Added passed/failed artifact guard tests; the explicit submission marker remains mandatory.
- Regression after the second launch gate: **155 tests passed**, the execute guard and ARR freeze guard both pass, post-ARR preflight passes, ARR submission freeze passes, and provider calls remain zero.
- Strengthened the ARR freeze gate to inspect every recorded step's `exit_code`, not only the aggregate status and failed-step list; added a regression fixture for a forged `status=passed` with a nonzero step.
- Final regression after the gate hardening: **156 tests passed**, post-ARR preflight passed, ARR submission freeze passed, and provider calls remain zero.
- Added an explicit `inference_eligible` flag to the post-ARR analysis summary. It is true only for a complete, schema-valid, duplicate-free, stratum-balanced 120-triad artifact; incomplete or failed-to-detect data cannot be mistaken for an inferential result.
- Regression after the analysis output hardening: **156 tests passed**, post-ARR preflight passed, ARR submission freeze passed, and provider calls remain zero.
- Added author-gate snapshot `research/artifacts/acl-arr-author-gates-snapshot-218.json`, separating passed local evidence (freeze and official Pubcheck) from unchecked OpenReview, license, service-contributor, and form actions. It performs no external mutation or provider call.
- Added explicit pre-submission experiment authorization amendment `research/configs/pre-submission-experiment-authorization-219.json` and isolated live output target `research/artifacts/pre-submission-persistence-live-220.json` after the user's 2026-10-01 authorization. The ARR manuscript, freeze artifact, and submission claims remain isolated; focused guards pass (8), full regression is **157 tests passed**, and the sequential preflight remains passed with zero provider calls.
- The first staged live attempt made no provider progress because the inherited HTTP/HTTPS proxy timed out; a no-secret direct `/models` check returned 200 after removing the proxy from the process. The staged retry then completed `TEST0101 / evolve` with 5 rounds, 46 calls, 108,000 tokens, and no primary or partial canary exposure. The separate analysis artifact `research/artifacts/pre-submission-persistence-analysis-221.json` correctly reports `incomplete` and `inference_eligible=false`; this single cell is not evidence.
- Resumed the authorized pre-submission artifact after the staged gate: the complete `TEST0101` triad is now recorded (3/360 cells), and the background continuation has reached 5/360 completed cells without proxy timeouts. Runtime logs are redirected outside the repository; the ARR freeze/manuscript remain unchanged.
- Progress check: the background continuation has reached **17/360 completed cells** (evolve 6, depth-matched reset 6, no-canary 5), using 840 calls and 1,990,705 tokens so far. Logged completions 6--17 average about 1.50 minutes per cell, implying roughly 8.5--9 hours remaining if provider latency stays similar; this is an operational estimate, not an experiment result.

## 2026-10-02 — Manuscript revision pass in the materials repository

- Revised the ARR manuscript without new experiments or provider calls; every added number comes from the existing frozen record. Details and evidence are in `materials/manuscript-arr/REVISION-NOTES.md`.
- Corrected the response-collapse wording: each prompt concentrates on a single invalid response, but TEST0030's mode changes from `["IMPOSSIBLE"]` (repair-conditioned) to `["bookshelf"]` (public-only); only TEST0535 keeps the same mode. The abstract, §3.4, related work, and implications no longer claim "the same wrong mode".
- Clarified that $C_1$/$C_5$ contain two/six trajectories, that the five-finals comparison is not cost-matched, and that the 0.50 selector baseline is the temperature-zero final accuracy.
- Defined non-degenerate cohorts (30--70% gate) and replaced "healthy". Added the 5/12--7/12 nuisance floor for the DeepSeek +0.167 contrast, the 0/12 non-degenerate canary result, and the execution-aware retention validation. Described the post hoc held-out planner and disclosed its 8-to-12 step-cap amendment.
- Added an audit roadmap table and figure references. Regenerated both main figures with `figures/make_main_figures.py`, removing the dual-axis panel and the overlapping epsilon ticks, showing all cohort intervals, and embedding TrueType fonts. Updated eight bibliography entries to their published venues and brace-protected acronyms.
- Recompiled `main.pdf`: 16 pages, main body ending on page 8, with no undefined references or overfull boxes. Workspace audits 189/191/192/193/196 and Pubcheck 194 must be rerun after porting; the metadata draft must take the new abstract first.
- Extended the standalone persistence analysis with the preregistered G1 decision, the paired partial detector, exact upper bounds, and per-arm usage. Added synthetic-fixture tests (all pass) and a `--pre-submission` analysis flag. Fixed the runbook's analysis command, which would otherwise have analyzed the wrong artifact for the pre-submission run.
- Redacted local Windows interpreter paths in the public copies of artifacts 196 and 209.

