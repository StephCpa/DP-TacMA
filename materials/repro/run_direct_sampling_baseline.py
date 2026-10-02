"""Run or analyze the protocol-227 direct-sampling support baseline.

Default mode is a dry run with zero provider calls. Live execution requires a
frozen protocol, ``--execute``, and ``DIRECT_SAMPLING_227_AUTHORIZED=1``. The
run is resumable by ``(arm, task_id, call_index)`` and refuses to mix runs made
under a different protocol hash. ``--analyze`` makes no provider calls.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
# Workspace layout: research/experiments/<this file>; materials layout: repro/<this file>.
ROOT = next((p for p in HERE.parents if (p / "research").is_dir()), HERE.parent)
sys.path.insert(0, str(HERE))

import direct_sampling_adapter as adapter  # noqa: E402
from direct_sampling_analysis import collapse_contrast, summarize_arm  # noqa: E402

PROTOCOL = ROOT / "research" / "protocols" / "direct-sampling-baseline-protocol-227.json"
if not PROTOCOL.exists():
    PROTOCOL = ROOT / "research" / "configs" / "direct-sampling-baseline-protocol-227.json"
SAVE_EVERY = 20


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def load_existing(path: Path, protocol_sha: str) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("protocol_sha256") != protocol_sha:
        raise RuntimeError("existing artifact was produced under a different protocol hash; do not mix runs")
    seen: set[tuple[str, str, int, int]] = set()
    for record in payload.get("calls", []):
        key = (record["arm"], record["task_id"], int(record["call_index"]), int(record.get("attempt", 0)))
        if key in seen:
            raise RuntimeError(f"duplicate call record {key}")
        seen.add(key)
    return payload


def execute(protocol: dict[str, Any], output: Path, protocol_sha: str, max_new_calls: int) -> None:
    if protocol.get("status") != "frozen":
        raise SystemExit("protocol 227 is not frozen; no provider call was made")
    if os.environ.get("DIRECT_SAMPLING_227_AUTHORIZED") != "1":
        raise SystemExit("set DIRECT_SAMPLING_227_AUTHORIZED=1 to authorize live calls")

    tasks = adapter.load_tasks()
    existing = load_existing(output, protocol_sha)
    calls: list[dict[str, Any]] = list(existing.get("calls", []))
    done = {(c["arm"], c["task_id"], int(c["call_index"])) for c in calls if c.get("valid") is True}
    attempts: dict[tuple[str, str, int], int] = {}
    for c in calls:
        key = (c["arm"], c["task_id"], int(c["call_index"]))
        attempts[key] = attempts.get(key, 0) + 1
    payload = {
        "experiment_id": protocol["experiment_id"],
        "protocol_sha256": protocol_sha,
        "status": "in_progress",
        "credentials_included": False,
        "calls": calls,
    }
    budget = protocol["budget"]
    new_calls = 0
    for arm in protocol["arms"]:
        for task in tasks:
            task_id = str(task["task_id"])
            messages = adapter.build_messages(task)
            for index in range(int(arm["calls_per_task"])):
                key = (arm["name"], task_id, index)
                while key not in done:
                    if max_new_calls and new_calls >= max_new_calls:
                        write_atomic(output, payload)
                        return
                    total_calls = len(calls)
                    total_tokens = sum(int(c.get("tokens", 0)) for c in calls)
                    if total_calls >= budget["max_total_calls"] or total_tokens >= budget["max_total_tokens"]:
                        payload["status"] = "budget_exhausted"
                        write_atomic(output, payload)
                        return
                    arm_calls = [c for c in calls if c["arm"] == arm["name"]]
                    invalid = sum(c.get("valid") is not True for c in arm_calls)
                    planned = int(arm["calls_per_task"]) * len(tasks)
                    if invalid > 0.05 * planned:
                        payload["status"] = "stopped_integrity"
                        write_atomic(output, payload)
                        raise SystemExit(f"more than 5% invalid calls in arm {arm['name']}; stopped")
                    result = adapter.call_model(arm, messages)
                    attempt = attempts.get(key, 0)
                    attempts[key] = attempt + 1
                    text = str(result.get("text") or "")
                    valid = result.get("error") is None and result.get("total_tokens") is not None
                    plan = adapter.canonical_plan(text, task) if valid else None
                    record = {
                        "arm": arm["name"],
                        "task_id": task_id,
                        "call_index": index,
                        "attempt": attempt,
                        "valid": valid,
                        "error": result.get("error"),
                        "raw": text,
                        "semantic_key": adapter.semantic_key(text, task) if valid else None,
                        "canonical_plan": plan,
                        "executable": bool(valid and adapter.is_executable(plan, task)),
                        "tokens": int(result.get("total_tokens") or 0),
                    }
                    calls.append(record)
                    new_calls += 1
                    if valid:
                        done.add(key)
                    if new_calls % SAVE_EVERY == 0:
                        write_atomic(output, payload)
    payload["status"] = "complete"
    write_atomic(output, payload)


def analyze(protocol: dict[str, Any], live: Path, output: Path) -> dict[str, Any]:
    payload = json.loads(live.read_text(encoding="utf-8"))
    comparators = adapter.load_comparators()
    arms = {}
    for arm in protocol["arms"]:
        records = [c for c in payload["calls"] if c["arm"] == arm["name"]]
        arms[arm["name"]] = summarize_arm(
            records,
            comparators,
            expected_tasks=20,
            calls_per_task=int(arm["calls_per_task"]),
        )
    result = {
        "artifact": Path(protocol["outputs"]["analysis_artifact"]).stem,
        "mode": "cached analysis; no provider calls",
        "protocol_sha256": payload.get("protocol_sha256"),
        "live_status": payload.get("status"),
        "arms": arms,
        "qwen_vs_deepseek_collapse": collapse_contrast(arms["qwen_direct"], arms["deepseek_direct"])
        if {"qwen_direct", "deepseek_direct"} <= set(arms) else None,
        "token_ratio_qwen_direct_to_C5": arms["qwen_direct"]["tokens"] / protocol["cohort"]["comparators"]["known_aggregates"]["C5_tokens"]
        if "qwen_direct" in arms else None,
        "scope": protocol["decision_rules"]["scope"],
    }
    write_atomic(output, result)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--analyze", action="store_true")
    parser.add_argument("--max-new-calls", type=int, default=0)
    args = parser.parse_args()
    protocol = json.loads(PROTOCOL.read_text(encoding="utf-8"))
    protocol_sha = sha256(PROTOCOL)
    live = ROOT / protocol["outputs"]["live_artifact"]
    if args.analyze:
        result = analyze(protocol, live, ROOT / protocol["outputs"]["analysis_artifact"])
        print(json.dumps({arm: {"status": s["status"], "oracle": s["oracle"], "decision_vs_C5": s["decision_vs_C5"]}
                          for arm, s in result["arms"].items()}))
        return
    if args.execute:
        execute(protocol, live, protocol_sha, args.max_new_calls)
        return
    planned = sum(int(arm["calls_per_task"]) for arm in protocol["arms"]) * 20
    print(json.dumps({
        "mode": "dry_run",
        "provider_calls": 0,
        "protocol_status": protocol.get("status"),
        "protocol_sha256": protocol_sha,
        "arms": [arm["name"] for arm in protocol["arms"]],
        "planned_calls": planned,
        "budget": protocol["budget"],
        "execution_guard": protocol["execution_guard"],
    }))


if __name__ == "__main__":
    main()
