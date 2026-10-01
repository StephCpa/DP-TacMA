# X1 live replication launch runbook

The default launch is post-ARR. Before submission, the same replication may be
started only under the separately recorded user authorization amendment
`research/configs/pre-submission-experiment-authorization-219.json`. The new
artifact is separate from the frozen ARR package and cannot change its
manuscript, claims, or submission files.

## Pre-launch checks

Run from the project root with the project virtual environment:

```powershell
.\.venv\Scripts\python.exe research\experiments\run_post_arr_preflight.py
```

The preflight must report `passed`. Do not edit the frozen protocol, cohort,
or existing live artifact by hand.

## Staged launch (pre-submission authorization)

For the currently authorized pre-submission run, set the authorization marker
in the same PowerShell process. Do not set `ARR_SUBMISSION_COMPLETE`:

```powershell
$env:PRE_SUBMISSION_EXPERIMENT_AUTHORIZED = "1"
```

Use the separate output artifact for a one-cell smoke of the live path:

```powershell
.\.venv\Scripts\python.exe research\experiments\run_post_arr_persistence_replication.py --execute --pre-submission-authorized --max-new-runs 1
```

If the staged cell completes, resume the same artifact for the full schedule:

```powershell
.\.venv\Scripts\python.exe research\experiments\run_post_arr_persistence_replication.py --execute --pre-submission-authorized
```

## Staged launch (post-submission)

In the same PowerShell process used for the run, set the explicit marker:

```powershell
$env:ARR_SUBMISSION_COMPLETE = "1"
```

The runner first checks a process-level `DEEPSEEK_API_KEY`; on Windows it then
falls back to the existing user-scope key without printing or persisting it.
Only `ARR_SUBMISSION_COMPLETE=1` must be set in the current process. For a
one-cell smoke of the live path, use:

```powershell
.\.venv\Scripts\python.exe research\experiments\run_post_arr_persistence_replication.py --execute --max-new-runs 1
```

If the staged cell completes, resume the same artifact for the full schedule:

```powershell
.\.venv\Scripts\python.exe research\experiments\run_post_arr_persistence_replication.py --execute
```

The runner is idempotent by `(instance_id, arm)`, rejects protocol/cohort hash
changes and duplicate cells, and stops before the next cell at the declared
call/token budget. A budget stop is reported as incomplete, never as a null.

## Analysis

After the artifact reports `complete`, run the command that matches the launch
path. The default reads the post-submission artifact 205; the authorized
pre-submission run writes artifact 220 and must be analyzed with
`--pre-submission` (equivalently, explicit `--input`/`--output` paths), or the
script reports `awaiting_live_data` for the wrong file.

```powershell
# Pre-submission authorization (artifact 220 -> analysis 221)
.\.venv\Scripts\python.exe research\experiments\analyze_post_arr_persistence_replication.py --pre-submission

# Post-submission launch (artifact 205 -> analysis 207)
.\.venv\Scripts\python.exe research\experiments\analyze_post_arr_persistence_replication.py
```

The summary's `g1_decision` field applies the protocol-199 decision rule
(`positive_persistence_signal`, `failed_to_detect`, or `incomplete`); the
positive-control instrument check remains a runner precondition. The secondary
five-token partial detector, one-sided exact upper bounds, and per-arm usage
means are reported alongside it.

Only a complete 120-triad artifact with balanced strata is inferentially
eligible. Incomplete, malformed, or failed-to-detect outcomes remain scoped by
the protocol and must not be relabeled as privacy evidence.
