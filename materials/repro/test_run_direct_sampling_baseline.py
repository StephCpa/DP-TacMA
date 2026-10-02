"""Runner tests with a fake adapter: resume, integrity replacement, analysis.

Run from this directory: ``python test_run_direct_sampling_baseline.py``.
No provider is contacted.
"""

from __future__ import annotations

import itertools
import json
import os
from pathlib import Path
import tempfile

import direct_sampling_adapter as adapter
import run_direct_sampling_baseline as runner

PROTOCOL = {
    "experiment_id": "TEST-227",
    "status": "frozen",
    "arms": [{"name": "qwen_direct", "calls_per_task": 4}, {"name": "deepseek_direct", "calls_per_task": 4}],
    "budget": {"max_total_calls": 1000, "max_total_tokens": 10**7},
    "cohort": {"comparators": {"known_aggregates": {"C5_tokens": 1000}}},
    "decision_rules": {"scope": "test"},
    "outputs": {"analysis_artifact": "analysis.json"},
}


def _install_fake_adapter(fail_first: int = 0) -> None:
    counter = itertools.count()
    adapter.load_tasks = lambda: [{"task_id": f"T{i:02d}"} for i in range(20)]
    adapter.build_messages = lambda task: [{"role": "user", "content": task["task_id"]}]

    def call_model(arm, messages):
        n = next(counter)
        if n < fail_first:
            return {"text": "", "total_tokens": None, "error": "provider_error"}
        ok = messages[0]["content"] < "T10" and n % 4 == 0
        return {"text": "plan" if ok else "IMPOSSIBLE", "total_tokens": 10, "error": None}

    adapter.call_model = call_model
    adapter.semantic_key = lambda text, task: text
    adapter.canonical_plan = lambda text, task: None if text == "IMPOSSIBLE" else text
    adapter.is_executable = lambda plan, task: plan == "plan"
    adapter.load_comparators = lambda: {f"T{i:02d}": {"C5": i < 16, "C1": i < 12, "baseline_final": i < 10} for i in range(20)}


def test_resume_replacement_and_analysis() -> None:
    _install_fake_adapter(fail_first=2)
    os.environ["DIRECT_SAMPLING_227_AUTHORIZED"] = "1"
    with tempfile.TemporaryDirectory() as tmp:
        live = Path(tmp) / "live.json"
        runner.execute(PROTOCOL, live, "hash", max_new_calls=50)
        partial = json.loads(live.read_text())
        assert partial["status"] == "in_progress" and len(partial["calls"]) == 50
        runner.execute(PROTOCOL, live, "hash", max_new_calls=0)
        payload = json.loads(live.read_text())
        assert payload["status"] == "complete"
        valid = [c for c in payload["calls"] if c["valid"]]
        assert len(valid) == 2 * 20 * 4 and len(payload["calls"]) == len(valid) + 2
        result = runner.analyze(PROTOCOL, live, Path(tmp) / "analysis.json")
        assert result["arms"]["qwen_direct"]["status"] == "complete"
        assert result["arms"]["qwen_direct"]["contrasts"]["C5"]["tasks"] == 20
        try:
            runner.execute(PROTOCOL, live, "other-hash", max_new_calls=1)
        except RuntimeError:
            pass
        else:
            raise AssertionError("a protocol-hash mismatch must be rejected")


def test_unfrozen_protocol_blocks_live_calls() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        try:
            runner.execute({**PROTOCOL, "status": "draft_not_frozen"}, Path(tmp) / "x.json", "h", 1)
        except SystemExit as exc:
            assert "not frozen" in str(exc)
        else:
            raise AssertionError("an unfrozen protocol must block execution")


if __name__ == "__main__":
    test_resume_replacement_and_analysis()
    test_unfrozen_protocol_blocks_live_calls()
    print("all tests passed")
