# Direct-sampling support baseline (protocol 227, draft)

Status: **draft, not frozen**. Machine-readable version:
`materials/research/protocols/direct-sampling-baseline-protocol-227.json`.
Freeze it (set `status` to `frozen`, log its SHA-256, commit) before the first
provider call. Numbers 227–229 are provisional; 222–226 are already used on
main.

## Why this experiment

Reviewers will ask two questions the paper cannot yet answer:

1. **Does the runtime buy anything over cheap sampling?** The nested pool
   $C_5$ reaches 0.80 executable-oracle accuracy on 20 Qwen tasks, but it costs
   14.4M tokens. Nobody has checked whether direct sampling without the
   multi-agent runtime reaches the same support for a fraction of the cost.
2. **Is response collapse common or a two-task anecdote?** Concentration on
   one invalid response is documented only for TEST0030 and TEST0535, both
   selected failures.

Both answers are useful. If direct sampling matches $C_5$, the paper gains a
strong efficiency result. If it collapses across many tasks, the mechanism
claim generalizes from two tasks to a measured prevalence.

## Design

| Item | Choice |
|---|---|
| Tasks | The 20 main-cohort tasks of protocol 083, in their frozen order |
| Primary arm | `qwen3.7-max-2026-06-08`, temperature 0.7, thinking disabled, uncached, 200 calls per task |
| Secondary arm | `deepseek-v4-flash`, same settings, same tasks |
| Prompt | The protocol-096 public-task-only template, unchanged (task + output format; no candidate, diagnostic, history, reference, or tools) |
| Scoring | The protocol-083 canonical parser and reference-free executor; protocol-096 semantic normalization |
| Comparators | Cached per-task $C_5$, $C_1$, and temperature-zero final outcomes from artifact 084 |
| Budget | 8,400 calls and 4M tokens; about 1.9M tokens expected at protocol 096's 233 tokens per call |

**Known asymmetry.** The runtime had recipe-search tools; direct sampling does
not. A direct-sampling deficit therefore cannot be pinned on the multi-agent
structure. Parity or an advantage holds despite strictly less context.

## Endpoints

- **E1 (primary):** the task-level executable oracle over the 200 Qwen calls,
  minus $C_5$ on the same task. Report the paired risk difference, a
  task-bootstrap 95% interval, and an exact two-sided McNemar test. The pools
  are not nested, so a signed test is valid here.
- **E2 (primary):** the share of tasks whose raw modal response fills at least
  80% of calls and is not executable, with an exact 95% interval.
- **Secondary:**
  - E1 against $C_1$ and the temperature-zero final;
  - unbiased coverage at $k = 1, 5, 10, 20, 50, 100, 200$;
  - distinct canonical and executable plans;
  - semantic collapse;
  - token ratio to $C_5$;
  - every endpoint for DeepSeek, plus the paired Qwen-versus-DeepSeek collapse contrast.

## Decision rules (fixed before any output)

- **Parity or better:** direct minus $C_5$ is at least 0. Claim superiority
  only if McNemar $p<0.05$.
- **Runtime advantage:** direct minus $C_5$ is below 0 and $p<0.05$.
- **Inconclusive:** anything else. Report the interval; do not call the arms
  equivalent.
- **Collapse wording:** call collapse "common" or "rare" only if the
  E2 interval lies entirely above or below 0.5.
- **Unit of inference:** tasks, never calls.

## Integrity and stop rules

- A provider error, access-denied or payment text, or missing usage makes a
  call invalid. Invalid calls are retained, excluded from endpoints, and
  replaced once at the same index. An empty visible answer with valid usage
  counts as a valid, non-executable response.
- Stop and report if more than 5% of an arm's calls are invalid.
- Reaching the budget yields `incomplete`, never an inferred null.
- Credentials come only from process environment variables.

## Running it

Code is in `materials/repro/`:

- `run_direct_sampling_baseline.py` is the guarded, resumable runner.
- `direct_sampling_analysis.py` computes the endpoints.
- `direct_sampling_adapter.py` holds the workspace-specific hooks.

Each hook raises `NotImplementedError` until it is wired to the protocol-083
and protocol-096 code, so nothing can run by accident.

```bash
python run_direct_sampling_baseline.py                       # dry run, zero calls
DIRECT_SAMPLING_227_AUTHORIZED=1 python run_direct_sampling_baseline.py --execute --max-new-calls 20   # smoke
DIRECT_SAMPLING_227_AUTHORIZED=1 python run_direct_sampling_baseline.py --execute                      # full, resumable
python run_direct_sampling_baseline.py --analyze             # zero calls
```

Tests with synthetic data and a fake adapter:
`python test_direct_sampling_analysis.py` and
`python test_run_direct_sampling_baseline.py`.

## Paper integration

Report the result in §3.3/§3.4 as a cost-matched comparison and a measured
collapse prevalence. If E2 is high, the "two selected tasks" caveat in §3.4 and
Limitations can be narrowed to the measured cohort. If direct sampling reaches
parity, the Implications paragraph on "efficient diversity" must be rewritten
around that result.
