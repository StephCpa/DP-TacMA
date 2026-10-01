"""Analyze the post-ARR X1 live artifact without making provider calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from research.src.post_arr_persistence_analysis import summarize_replication  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=ROOT / "research" / "artifacts" / "post-arr-persistence-live-205.json")
    parser.add_argument("--output", type=Path, default=ROOT / "research" / "artifacts" / "post-arr-persistence-analysis-207.json")
    args = parser.parse_args()
    if not args.input.exists():
        result = {
            "artifact": "post-arr-persistence-analysis-207",
            "status": "awaiting_live_data",
            "mode": "no-provider analysis entrypoint; live artifact not present",
            "input": str(args.input.relative_to(ROOT)).replace("\\", "/"),
            "provider_calls": 0,
        }
    else:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = {
            "artifact": "post-arr-persistence-analysis-207",
            "mode": "cached live-artifact analysis; no provider calls",
            "input": str(args.input.relative_to(ROOT)).replace("\\", "/"),
            "provider_calls": 0,
            "summary": summarize_replication(
                payload.get("runs", []),
                expected_stratum_counts={"impossible": 40, "feasible_short": 40, "feasible_long": 40},
            ),
        }
        result["status"] = result["summary"]["status"]
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
