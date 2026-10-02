"""Analyze the post-ARR X1 live artifact without making provider calls."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

try:
    from research.src.post_arr_persistence_analysis import summarize_replication  # noqa: E402
except ImportError:  # standalone copy in materials/repro
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from post_arr_persistence_analysis import summarize_replication  # noqa: E402

ARTIFACTS = ROOT / "research" / "artifacts"


def _display(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return path.name


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument(
        "--pre-submission",
        action="store_true",
        help="analyze the authorized pre-submission artifact 220 and write analysis 222",
    )
    args = parser.parse_args()
    if args.pre_submission:
        default_input = ARTIFACTS / "pre-submission-persistence-live-220.json"
        default_output = ARTIFACTS / "pre-submission-persistence-analysis-222.json"
    else:
        default_input = ARTIFACTS / "post-arr-persistence-live-205.json"
        default_output = ARTIFACTS / "post-arr-persistence-analysis-207.json"
    args.input = (args.input or default_input).resolve()
    args.output = (args.output or default_output).resolve()
    if not args.input.exists():
        result = {
            "artifact": "post-arr-persistence-analysis-207",
            "status": "awaiting_live_data",
            "mode": "no-provider analysis entrypoint; live artifact not present",
            "input": _display(args.input),
            "provider_calls": 0,
        }
    else:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
        result = {
            "artifact": "post-arr-persistence-analysis-207",
            "mode": "cached live-artifact analysis; no provider calls",
            "input": _display(args.input),
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
