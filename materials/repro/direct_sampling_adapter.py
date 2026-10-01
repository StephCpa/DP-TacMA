"""Workspace adapter for the protocol-223 direct-sampling runner.

Every function here must be wired to the exact code already used by protocols
083 (task loading, canonical parser, executor, comparators) and 096 (public-only
prompt, semantic normalization, non-thinking provider calls). Reusing those
implementations unchanged is what makes the comparison valid; do not write new
parsing or scoring logic here. Until wired, each function raises
NotImplementedError, so a live run cannot start by accident.
"""

from __future__ import annotations

from typing import Any


def load_tasks() -> list[dict[str, Any]]:
    """Return the 20 protocol-083 main-cohort tasks in frozen order.

    Each dict needs at least ``task_id`` plus whatever the prompt and executor
    require. Never include the reference answer in the returned object.
    """

    raise NotImplementedError("wire to the protocol-083 cohort loader")


def build_messages(task: dict[str, Any]) -> list[dict[str, str]]:
    """Return the protocol-096 public-task-only messages for ``task``."""

    raise NotImplementedError("wire to the protocol-096 prompt template")


def call_model(arm: dict[str, Any], messages: list[dict[str, str]]) -> dict[str, Any]:
    """Make one uncached call and return ``{"text", "total_tokens", "error"}``.

    Use the arm's model, temperature, and the explicit non-thinking switch from
    the workspace compatibility layer. ``error`` is None on success; set it to a
    short category (never the raw provider message if it could echo a key).
    """

    raise NotImplementedError("wire to the workspace provider client")


def semantic_key(text: str, task: dict[str, Any]) -> str:
    """Return the protocol-096 semantic normalization of a response."""

    raise NotImplementedError("wire to the protocol-096 semantic normalizer")


def canonical_plan(text: str, task: dict[str, Any]) -> str | None:
    """Return the protocol-083 canonical plan string, or None if unparseable."""

    raise NotImplementedError("wire to the protocol-083 canonical parser")


def is_executable(plan: str | None, task: dict[str, Any]) -> bool:
    """Return the reference-free executor verdict used by the protocol-083 oracle."""

    raise NotImplementedError("wire to the reference-free PlanCraft executor")


def load_comparators() -> dict[str, dict[str, bool]]:
    """Return ``{task_id: {"C5": bool, "C1": bool, "baseline_final": bool}}`` from artifact 084."""

    raise NotImplementedError("wire to the cached protocol-083 per-task outcomes")
