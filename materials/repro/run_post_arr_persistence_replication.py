"""Run the frozen post-ARR X1 persistence replication.

The default mode is a no-provider dry run. Live execution requires both
``--execute`` and ``ARR_SUBMISSION_COMPLETE=1`` so the ARR freeze cannot be
accidentally bypassed.
"""

from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
UPSTREAM = ROOT / "upstream" / "TacoMAS-MultiAgent"
CONFIG = ROOT / "research" / "configs" / "post-arr-persistence-replication-protocol-199.json"
PRE_SUBMISSION_AUTH = ROOT / "research" / "configs" / "pre-submission-experiment-authorization-219.json"
COHORT = ROOT / "research" / "configs" / "post-arr-persistence-runner-cohort-203.json"
OUTPUT = ROOT / "research" / "artifacts" / "post-arr-persistence-live-205.json"
PRE_SUBMISSION_OUTPUT = ROOT / "research" / "artifacts" / "pre-submission-persistence-live-220.json"
ARR_FREEZE = ROOT / "research" / "artifacts" / "acl-arr-submission-freeze-196.json"
POSITIVE_CONTROL = ROOT / "research" / "artifacts" / "iclr2027-x1-extractor-positive-control-064.json"
TOPOLOGY = ROOT / "research" / "configs" / "topologies" / "plancraft-g0-3-agent.json"
MODEL = "openai/deepseek-v4-flash"
API_BASE = "https://api.deepseek.com"

sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(UPSTREAM))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def schedule(cohort: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {**instance, "arm": arm}
        for instance in cohort["instances"]
        for arm in instance["arm_order"]
    ]


def find_run_dir(tag: str, index: int, started_at: float) -> Path:
    pattern = f"evolution_trace_*_{tag}_plancraft_{index}_{index + 1}"
    candidates = [
        path for path in (UPSTREAM / "outputs").glob(pattern)
        if path.is_dir() and path.stat().st_mtime >= started_at - 1
    ]
    if not candidates:
        raise RuntimeError(f"no output directory found for {tag}")
    return max(candidates, key=lambda path: path.stat().st_mtime)


def write(payload: dict[str, Any], path: Path = OUTPUT) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def resolve_deepseek_api_key() -> str:
    """Resolve the key from the process, then Windows user scope only."""

    process_key = os.environ.get("DEEPSEEK_API_KEY", "").strip()
    if process_key:
        return process_key
    if os.name != "nt":
        return ""
    try:
        import winreg

        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
            user_key, _ = winreg.QueryValueEx(key, "DEEPSEEK_API_KEY")
        return str(user_key).strip()
    except (FileNotFoundError, OSError, ImportError):
        return ""


def assert_arr_submission_freeze(path: Path = ARR_FREEZE) -> None:
    """Require the latest local ARR freeze regression before live calls."""

    if not path.exists():
        raise RuntimeError("ARR submission-freeze artifact is missing")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError("ARR submission-freeze artifact is unreadable") from exc
    steps = payload.get("steps", [])
    nonzero_steps = [step.get("step", "unknown") for step in steps if step.get("exit_code") != 0]
    if payload.get("status") != "passed" or payload.get("failed_steps") or nonzero_steps:
        raise RuntimeError("ARR submission-freeze artifact is not passed")


def load_pre_submission_authorization() -> dict[str, Any]:
    if os.environ.get("PRE_SUBMISSION_EXPERIMENT_AUTHORIZED") != "1":
        raise SystemExit("pre-submission execution blocked: set PRE_SUBMISSION_EXPERIMENT_AUTHORIZED=1")
    if not PRE_SUBMISSION_AUTH.exists():
        raise RuntimeError("pre-submission authorization artifact is missing")
    payload = json.loads(PRE_SUBMISSION_AUTH.read_text(encoding="utf-8"))
    required = {"amendment_id", "base_protocol", "authorization", "manuscript_isolation", "output_artifact"}
    if not required.issubset(payload) or payload.get("arr_submission_status") != "not_submitted":
        raise RuntimeError("pre-submission authorization artifact is invalid")
    return payload


def validate_existing_resume(
    existing: dict[str, Any],
    *,
    protocol_sha256: str,
    cohort_sha256: str,
    experiment_id: str,
    expected_cells: set[tuple[str, str]],
) -> None:
    """Reject a resume that could mix incompatible runs or duplicate cells."""

    if not existing:
        return
    if existing.get("experiment_id") != experiment_id:
        raise RuntimeError("existing live artifact belongs to a different experiment")
    if existing.get("protocol_sha256") != protocol_sha256:
        raise RuntimeError("existing live artifact protocol hash differs; do not mix runs")
    if existing.get("cohort_sha256") != cohort_sha256:
        raise RuntimeError("existing live artifact cohort hash differs; do not mix runs")
    seen: set[tuple[str, str]] = set()
    for run in existing.get("runs", []):
        key = (str(run.get("instance_id")), str(run.get("arm")))
        if key not in expected_cells:
            raise RuntimeError(f"existing live artifact contains an out-of-schedule cell: {key}")
        if key in seen:
            raise RuntimeError(f"existing live artifact contains a duplicate cell: {key}")
        seen.add(key)


def assert_positive_control() -> None:
    if not POSITIVE_CONTROL.exists():
        raise RuntimeError("positive-control artifact is missing")
    payload = json.loads(POSITIVE_CONTROL.read_text(encoding="utf-8"))
    current_hash = hashlib.sha256((ROOT / "research" / "src" / "canary_audit.py").read_bytes()).hexdigest()
    expected_paths = {
        "agent_state.positive_control_agent.memory_summary",
        "latest_outputs.positive_control_agent",
        "coverage_memory.slot",
        "source_feedback_memory.source",
        "agent_object_memory.positive_control_agent[0].value",
        "information_objects[0].text",
        "slow_update_logs[0].global_rationale[0]",
    }
    if (
        payload.get("passed") is not True
        or payload.get("secrets_included") is not False
        or payload.get("implementation_sha256") != current_hash
        or not expected_paths.issubset(set(payload.get("recovered_exact_paths", [])))
    ):
        raise RuntimeError("positive-control validation failed before provider calls")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true", help="allow live provider calls")
    parser.add_argument("--pre-submission-authorized", action="store_true", help="use the explicit pre-submission amendment")
    parser.add_argument("--max-new-runs", type=int, default=0)
    args = parser.parse_args()

    protocol = json.loads(CONFIG.read_text(encoding="utf-8"))
    cohort = json.loads(COHORT.read_text(encoding="utf-8"))
    cells = schedule(cohort)
    if not args.execute:
        print(json.dumps({
            "mode": "dry_run",
            "provider_calls": 0,
            "instances": len(cohort["instances"]),
            "cells": len(cells),
            "arms": sorted({cell["arm"] for cell in cells}),
            "protocol_sha256": sha256(CONFIG),
            "cohort_sha256": sha256(COHORT),
            "execution_guard": "Post-submission live calls require --execute plus ARR_SUBMISSION_COMPLETE=1; the separately authorized pre-submission mode requires --pre-submission-authorized plus PRE_SUBMISSION_EXPERIMENT_AUTHORIZED=1.",
        }, ensure_ascii=False))
        return

    pre_submission = bool(args.pre_submission_authorized)
    authorization = load_pre_submission_authorization() if pre_submission else None
    if not pre_submission and os.environ.get("ARR_SUBMISSION_COMPLETE") != "1":
        raise SystemExit("live execution blocked: set ARR_SUBMISSION_COMPLETE=1 only after ARR submission")
    assert_arr_submission_freeze()
    api_key = resolve_deepseek_api_key()
    if not api_key:
        raise SystemExit("DEEPSEEK_API_KEY is not set; no provider call was made")

    output_path = PRE_SUBMISSION_OUTPUT if pre_submission else OUTPUT
    execution_id = str(authorization["amendment_id"]) if authorization else str(protocol["experiment_id"])
    existing = json.loads(output_path.read_text(encoding="utf-8")) if output_path.exists() else {}
    runs = list(existing.get("runs", []))
    protocol_sha256 = sha256(CONFIG)
    cohort_sha256 = sha256(COHORT)
    expected_cells = {(str(cell["id"]), str(cell["arm"])) for cell in cells}
    validate_existing_resume(
        existing,
        protocol_sha256=protocol_sha256,
        cohort_sha256=cohort_sha256,
        experiment_id=execution_id,
        expected_cells=expected_cells,
    )
    max_calls = int(protocol["budget"]["max_total_calls"])
    max_tokens = int(protocol["budget"]["max_total_tokens"])
    complete_keys = {
        (str(run["instance_id"]), str(run["arm"]))
        for run in runs if run.get("status") == "complete"
    }
    artifact: dict[str, Any] = {
        "schema_version": 1,
        "experiment_id": execution_id,
        "base_experiment_id": protocol["experiment_id"],
        "execution_context": "pre_submission_explicit_user_authorization" if pre_submission else "post_submission",
        "authorization_artifact": str(PRE_SUBMISSION_AUTH.relative_to(ROOT)).replace("\\", "/") if pre_submission else None,
        "status": "in_progress",
        "protocol": str(CONFIG.relative_to(ROOT)).replace("\\", "/"),
        "protocol_sha256": protocol_sha256,
        "cohort": str(COHORT.relative_to(ROOT)).replace("\\", "/"),
        "cohort_sha256": cohort_sha256,
        "model": "deepseek-v4-flash",
        "runs": runs,
        "artifact_note": "Raw synthetic canaries remain in local upstream traces; this artifact stores hashes and channel-level metadata only.",
    }
    write(artifact, output_path)

    os.environ.update({
        "DATASET_ID": "plancraft",
        "MAX_FAST_ROUNDS_PER_INSTANCE": str(protocol["runtime"]["rounds"]),
        "TARGET_ANSWER_QUALITY": "2.0",
        "INSTANCE_RETRIES": "1",
        "PER_INSTANCE_SLEEP_SECONDS": "0",
        "META_FEEDBACK_EVERY_FAST_ROUND": "0",
        "LLM_REQUEST_TIMEOUT_SECONDS": "45",
        "LLM_MAX_RETRIES": "1",
        "LITELLM_LOCAL_MODEL_COST_MAP": "True",
    })
    os.chdir(UPSTREAM)
    from research.experiments.run_iclr_g0_plancraft_smoke import load_runner
    runner = load_runner()
    from tacomas.meta_evolution import mas_runtime
    expected_prompt = str(ROOT / "research" / "configs" / "prompts" / "plancraft-worker.yaml")
    if any(path != expected_prompt for path in mas_runtime._DEFAULT_ROLE_PROMPT_PATHS.values()):
        raise RuntimeError("PlanCraft prompt routing validation failed before provider calls")
    from research.compat.tacomas_runner_compat import get_token_usage, reset_token_usage
    from research.src.canary_audit import canary_sha256, generate_canary
    from research.src.x1_analysis import checkpoint_exposure
    from research.src.x1_round_driver import run_x1_runtime
    from tacomas.meta_evolution.mas_runtime import MetaEvolutionMASRuntime

    assert_positive_control()
    original_run = MetaEvolutionMASRuntime.run_until_stable
    current: dict[str, Any] = {}
    audit_box: dict[str, Any] = {}

    def run_x1(self):
        result, audit = run_x1_runtime(
            self,
            arm=current["arm"],
            canary=current["canary"],
            repetition=int(protocol["runtime"]["canary_repetition"]),
            rounds=int(protocol["runtime"]["rounds"]),
            partial_tokens=int(protocol["runtime"]["partial_detector_tokens"]),
            run_callable=lambda: original_run(self),
        )
        audit_box["audit"] = asdict(audit)
        return result

    MetaEvolutionMASRuntime.run_until_stable = run_x1
    new_runs = 0
    try:
        for cell in cells:
            key = (str(cell["id"]), str(cell["arm"]))
            if key in complete_keys:
                continue
            if args.max_new_runs > 0 and new_runs >= args.max_new_runs:
                break
            recorded_calls = sum(int((run.get("usage") or {}).get("calls", 0)) for run in runs)
            recorded_tokens = sum(int((run.get("usage") or {}).get("total_tokens", 0)) for run in runs)
            if recorded_calls >= max_calls or recorded_tokens >= max_tokens:
                artifact["status"] = "budget_exhausted"
                artifact["budget_stop"] = {"recorded_calls": recorded_calls, "recorded_tokens": recorded_tokens}
                write(artifact, output_path)
                break
            current["arm"] = str(cell["arm"])
            current["canary"] = generate_canary(int(cohort["canary_seed_base"]) + int(cell["index"]))
            audit_box.clear()
            tag_prefix = "pre-sub-x1" if pre_submission else "post-arr-x1"
            tag = f"{tag_prefix}-{str(cell['id']).lower()}-{str(cell['arm']).replace('_', '-')}"
            os.environ["RUN_TAG"] = tag
            reset_token_usage()
            started_at = time.time()
            runner(
                start_idx=int(cell["index"]),
                end_idx=int(cell["index"]) + 1,
                skip_meta_init=True,
                agent_name="multi-agent-independent",
                n_base_agents=1,
                min_iterations_per_agent=1,
                max_iterations_per_agent=3,
                agent_model_override=MODEL,
                agent_api_base=API_BASE,
                agent_api_key=api_key,
                agent_temperature=float(protocol["runtime"]["temperature"]),
                meta_model=MODEL,
                meta_api_base=API_BASE,
                meta_api_key=api_key,
                meta_temperature=float(protocol["runtime"]["temperature"]),
                max_birth_death_pairs=0,
                max_edge_edits=0,
                init_n_min=3,
                init_n_max=3,
                pop_n_min=3,
                pop_n_max=3,
                fast_steps_per_window=1,
                bd_check_interval=int(protocol["runtime"]["bd_check_interval"]),
                graph_rewire_interval=99,
                fixed_topology_file=str(TOPOLOGY),
            )
            run_dir = find_run_dir(tag, int(cell["index"]), started_at)
            audit = audit_box.get("audit")
            if audit is None:
                raise RuntimeError("runtime returned without X1 audit")
            usage = get_token_usage()
            instance_payload = json.loads((run_dir / f"instance_{cell['index']}.json").read_text(encoding="utf-8"))
            run_record = {
                "status": "complete",
                "instance_id": cell["id"],
                "instance_index": cell["index"],
                "stratum": cell["stratum"],
                "arm": cell["arm"],
                "canary_sha256": canary_sha256(current["canary"]),
                "run_directory": str(run_dir.relative_to(ROOT)).replace("\\", "/"),
                "rounds": int(instance_payload["runtime_result"]["rounds"]),
                "exact_match": bool(instance_payload["metrics"].get("exact_match")),
                "primary_exact_exposure": checkpoint_exposure(audit["checkpoints"], exact=True),
                "secondary_partial_exposure": checkpoint_exposure(audit["checkpoints"], exact=False),
                "checkpoints": audit["checkpoints"],
                "action_mask_audit": audit["action_mask_audit"],
                "usage": usage,
            }
            runs.append(run_record)
            new_runs += 1
            artifact["runs"] = runs
            total_calls = sum(int((run.get("usage") or {}).get("calls", 0)) for run in runs)
            total_tokens = sum(int((run.get("usage") or {}).get("total_tokens", 0)) for run in runs)
            artifact["status"] = "complete" if len(runs) == len(cells) else "in_progress"
            if total_calls >= max_calls or total_tokens >= max_tokens:
                artifact["status"] = "budget_exhausted"
                artifact["budget_stop"] = {"recorded_calls": total_calls, "recorded_tokens": total_tokens}
            write(artifact, output_path)
            print(json.dumps({"completed": len(runs), "total": len(cells), "instance": cell["id"], "arm": cell["arm"], "calls": usage.get("calls", 0)}, ensure_ascii=False))
    finally:
        MetaEvolutionMASRuntime.run_until_stable = original_run
    artifact["runs"] = runs
    if artifact.get("status") != "budget_exhausted":
        artifact["status"] = "complete" if len(runs) == len(cells) else "in_progress"
    write(artifact, output_path)
    print(output_path)


if __name__ == "__main__":
    main()
