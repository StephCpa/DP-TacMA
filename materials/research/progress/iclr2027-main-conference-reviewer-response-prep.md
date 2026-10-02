# ICLR 2027 main-conference reviewer-response preparation

Status: internal evidence-backed response sheet, 1 October 2026. It is derived from the frozen manuscript and local artifacts; it is not a new empirical claim and does not authorize additional provider calls.

## Core positioning

This work is an empirical audit of the premises required before private selection is meaningful in a test-time evolving LLM-agent pipeline. It is not an end-to-end private-agent construction, a general leakage-prevalence study, or a causal demonstration that multi-agent evolution improves task utility. The evidence follows a phenomenon--failed obvious fix--working escape arc:

1. The audited setting does not pass the persistent-canary gate.
2. The released score is causally dominated by output length, and fixed candidate pools provide little selector headroom.
3. Independent trajectories enlarge executable support, whereas direct repair can remain concentrated on a wrong endpoint. Selector-level DP is informative only after support exists.

## Likely reviewer questions and evidence-bounded answers

### 1. Why is this an ICLR paper if it does not introduce a new DP mechanism?

The contribution is a falsifiable measurement order for privacy--utility claims in evolving agent systems. A formal mechanism can protect a score while the score has weak semantic validity, the persistent channel is not detected, or the candidate pool contains no useful alternative. We measure these failure modes with executable endpoints, prospective interventions, and a candidate-support bound, then test the least expensive escape that changes support. The selector calculation is deliberately narrow and illustrative; the paper does not present it as an end-to-end privacy solution.

Evidence: `manuscript/main.tex:27--39,190--197,227`; `research/artifacts/iclr2027-signal-selector-notation-correction-100.json`.

### 2. Does zero observed canary exposure prove that the system is private?

No. The result is a bounded failed-to-detect outcome under one model, one injection route, a five-round horizon, and fixed topology. Positive controls recover declared channels, and state mutation is observed, so the result is not explained by a completely inert extractor. The completed three-arm replication has zero events in 120 evolve instances, giving a one-sided 95% upper bound of 2.5%; the earlier 0/20 estimate and 13.9% bound are retained only as historical low-power results. The correct conclusion is that this specified setting did not pass the leakage gate, not that evolving agents do not leak.

Evidence: `manuscript/main.tex:22,110,241`; `research/artifacts/iclr2027-x1-operational-events-034.json`; `research/artifacts/pre-submission-persistence-replication-result-223.json`.

### 3. What exactly is causal about the score result?

The prospective length-term intervention changes the released score scale in every study: the score drops from 0.429 to 0.069 in the initial DeepSeek pairs, by -0.308 in the non-degenerate DeepSeek replication, and by -0.117 in Qwen. The pooled executable exactness effect across 42 paired runs is only +0.024 with 95% interval [-0.095, 0.143], and the two healthy-regime point estimates have opposite signs. Thus the causal conclusion is that the length component controls the score scale; deleting it is not a demonstrated utility improvement. The specific weight 0.85 is not claimed to have an independent semantic justification.

Evidence: `manuscript/main.tex:114--124`; `research/artifacts/iclr2027-qwen-cross-model-length-decision-075.json`; `research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json`.

### 4. Is the candidate-pool oracle just an oracle with access to the reference answer?

No. Candidate validity is computed by a reference-free executor; reference equality is retained only as an offline secondary endpoint. The oracle is therefore an upper bound for selectors restricted to the recorded candidate surface and binary target-reaching utility. Its headroom is 0--8.3 percentage points across four frozen cohorts. It does not bound newly generated repairs, hidden reasoning, unrecorded tool interactions, or population-level performance.

Evidence: `manuscript/main.tex:131--151`; `manuscript/appendix.tex:131--141`; `research/artifacts/iclr2027-cached-headroom-meta-analysis-081.json`.

### 5. Does the Qwen result show that multi-agent evolution is beneficial?

No. Five independent stochastic trajectories on 20 untouched tasks raise executable-oracle accuracy from 0.60 to 0.80 and increase canonical support by 1.00 plan, at roughly three times the token cost. The matched 16-slot comparison is 0.626 across independent trajectories versus 0.570 within one shared trajectory. All trajectories use the same three-agent runtime, so the result identifies an allocation effect among restarted contexts, not a causal architectural advantage for multi-agent evolution.

Evidence: `manuscript/main.tex:154--170,223`; `research/artifacts/iclr2027-qwen-candidate-pool-enlargement-decision-085.json`; `research/artifacts/iclr2027-qwen-candidate-pool-trajectory-reanalysis-088.json`.

### 6. Is “task-level response collapse” a general property of LLM decoding?

No. It is a scoped mechanism observation on two selected exhausted DeepSeek tasks. On the conditioned calls, one invalid raw response occupies 86.25% and 95% of 80 calls. The preregistered same-task public-only control removes the candidate, executor diagnostic, attempt index, response history, and reference; the modal rates become 98.75% and 95%, with 0/160 executable responses. The control reverses the initial conditioning explanation. The paper therefore treats this as task/model near-determinism on selected hard failures, not as a prevalence estimate.

Evidence: `manuscript/main.tex:176--188,225`; `manuscript/appendix.tex:182--210`; `research/artifacts/iclr2027-deepseek-unconditioned-collapse-analysis-098.json`.

### 7. Does the live X2 ablation show that LLM choice is unnecessary?

No. On the fixed 18-task held-out cohort, the unfiltered live DeepSeek arm reaches 8/12 feasible targets in replay and 5/12 canonical plans, versus 12/12 and 8/12 for the symbolic control. Replay has four symbolic-only and no live-only pairs (two-sided exact paired p=0.125); canonical matching has four symbolic-only and one live-only pair (p=0.375). The result localizes much of the executable coverage to bounded symbolic constraints while preserving a possible role for model choice. It is a fixed-cohort component ablation, not a population effect or architecture-level causal estimate.

Evidence: `manuscript/main.tex:221`; `manuscript/appendix.tex:227--229`; `research/artifacts/iclr2027-x2-unfiltered-llm-control-analysis-164.json`; `research/artifacts/iclr2027-live-control-integrity-audit-166.json`.

### 8. Why not build an end-to-end private evolving-agent system?

The audit shows why that construction should not be treated as the first measurement. The canary channel is not detected in the tested setting, the released score is dominated by a length proxy, and fixed pools often contain no valid alternative for a selector to recover. The paper therefore evaluates a narrow selector-level release under a stated replacement adjacency and keeps candidate text, prompts, memories, inter-agent messages, topology, and stopping trusted. End-to-end joint privacy is a future architecture, not an unreported result.

Evidence: `manuscript/main.tex:29--39,190--197,213,227`; `manuscript/appendix.tex:231`.

### 9. What is the strongest reproducibility evidence?

All headline experiments have frozen protocols, machine-readable artifacts, deterministic endpoint evaluators, provider-usage ledgers, and explicit stopping or amendment records. The live X2 run has 142 accounted provider traces, 142 parseable JSON responses, no empty responses, and no provider-error marker. Source archive 169 has 10 entries, independently compiles to the same 16-page PDF, and is byte-identical to the current manuscript source. The latest recorded full local test run has 157 passing tests; the reviewer-facing audit itself is rerun after text changes.

Evidence: `research/artifacts/iclr2027-live-control-integrity-audit-166.json`; `research/artifacts/iclr2027-main-conference-readiness-audit-167.json`; `research/manifests/iclr2027-submission-source-169.zip`.

## Claims not to make in a response

- “The system does not leak.” Use “persistent exposure was not detected under the tested setting.”
- “Response collapse is a general LLM phenomenon.” Use “task-level response collapse on two selected hard failures.”
- “Multi-agent evolution improves utility.” Use the independent-trajectory allocation result and its cost, without an architectural causal interpretation.
- “The LLM contributes nothing to X2.” Use the paired live-versus-symbolic component result and retain the one live-only exact pair.
- “The paper provides private TacoMAS.” State that only a narrow selector-level release is analyzed; the evolving transcript remains trusted.

## Recommended response posture

Lead with the audit question and the order-of-operations insight. For every limitation, give the corresponding positive control, frozen endpoint, or bounded interpretation in the same paragraph. Do not promise a new experiment unless the reviewer identifies a claim that the current scope actually requires; the present evidence does not justify spending more provider budget on an unfrozen extension.
