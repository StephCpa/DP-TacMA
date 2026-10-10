"""Workspace adapter for the protocol-234 candidate-support audit.

Wire every hook to the code that produced the cached headroom analysis (081)
and the Qwen nested-pool study (087/088): the same trace store, P0 canonical
parser, reference-free executor, and offline reference comparator. Reusing
them unchanged is what makes P0 the paper's parser. Do not write new parsing
or scoring logic here. Until a hook is wired it raises NotImplementedError, so
the runner cannot read texts or produce numbers by accident.

The adapter never calls a provider: every text, score and outcome is read from
existing traces.
"""

from __future__ import annotations

from typing import Any, Iterator


def iter_slots() -> Iterator[dict[str, Any]]:
    """Yield one record per recorded candidate slot, in a stable order.

    U1 (headroom): the 1,152 slots of the four Table-3 original/control
    cohorts (72 runs x 16 slots: 15 agent-round outputs plus the final answer).
    U2 (pool): every slot of the 20-task Qwen nested-pool study (anchor plus
    five stochastic trajectories, 16 slots each).

    Required keys:
      slot_uid           stable unique id, e.g. "<cohort>/<run_id>/<round>/<agent>"
      universe           "U1" or "U2"
      cohort             Table-3 cohort name (U1) or "qwen_pool" (U2)
      run_id             U1: run id; U2: "<task_id>/t<trajectory>"
      task_id            PlanCraft instance id
      semantic_eligible  False for IMPOSSIBLE-reference tasks
      run_p0_failed      U1 only: the run's final answer is not executor-valid under P0
      is_final           True for the final answer slot
      trajectory         U2 only: 0 = anchor, 1..5 = stochastic trajectories
      text               the raw recorded candidate text ("" if none)
    Optional keys (None when not recorded; never recomputed with a model):
      recorded_score     the runtime selection score of this candidate
      judge_score        the slow-update judge score, if any
      env_success        the recorded environment-success flag used by the composite
    """

    raise NotImplementedError("wire to the 081/088 trace store")


def task_lookup(task_id: str) -> Any:
    """Return the task object the parser and executor take."""

    raise NotImplementedError("wire to the protocol-083 task loader")


def p0_parse(text: str, task: Any) -> tuple[Any, str]:
    """Run the unchanged P0 parser and canonicalizer.

    Return ``(plan, "ok")`` on acceptance and ``(None, reason)`` on rejection,
    where ``reason`` is P0's own failure category (e.g. "json_error",
    "unknown_item"); use "rejected" if P0 does not expose one.
    """

    raise NotImplementedError("wire to the P0 canonical parser")


def execute(plan: Any, task: Any) -> bool:
    """Reference-free executor verdict for a plan.

    ``plan`` is either a P0 plan object or a P2/human plan: the string
    "IMPOSSIBLE" or a tuple of lower-case item ids. Convert the latter to the
    executor's input with the same canonicalizer P0 uses; do not repair it.
    """

    raise NotImplementedError("wire to the reference-free PlanCraft executor")


def reference_exact(plan: Any, task: Any) -> bool:
    """Offline reference-exactness check for the same plan forms as ``execute``."""

    raise NotImplementedError("wire to the offline reference comparator")


def ablation_runs() -> dict[str, dict[str, Any]]:
    """Return the per-run records of every score-ablation cell.

    ``{cell: {"control_arm", "treated_arm", "runs": [...]}}``; each run has
    ``arm``, ``task_id``, ``semantic_eligible``, ``exec_valid`` (final answer
    executor-valid) and ``ref_exact`` (final answer reference-exact). Include
    the initial 10-pair DeepSeek length cohort, which the cached 081 rows lack.
    """

    raise NotImplementedError("wire to the score-ablation run records")


def pool_costs() -> dict[str, dict[str, Any]]:
    """Optional: recorded generation cost of each nested pool, for the cost table.

    ``{"C1": {"calls": int, "tokens": int, "judge_calls": int | None}, ..., "C5": {...}}``
    summed over the 20 Qwen pool tasks. Leave unwired to omit the cost columns.
    """

    raise NotImplementedError("wire to the 088 per-trajectory usage records")
