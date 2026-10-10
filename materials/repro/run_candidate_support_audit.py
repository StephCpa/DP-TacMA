"""Run the protocol-234 parser-independent candidate-support audit.

Stages (no stage makes a provider call):

  --check        validate the protocol and report which adapter hooks are wired;
                 reads no candidate text. Allowed before freezing.
  --reparse      run P0, P1 and P2 over every recorded slot and execute each
                 accepted plan. Writes slot rows without raw text.
  --packet       build the blinded annotator packets (A, B) and the private key.
  --second-pass  after annotator A finishes, write the extra packet B must label
                 (items A marked A2/A3 that B has not seen).
  --analyze      merge labels, score human plans, estimate q_FN, reclassify the
                 P0-failed runs, replay selectors, compare endpoints, and apply
                 the frozen decision rules. Writes analysis 235.

Every stage except --check requires protocol status "frozen", and later stages
refuse to mix outputs made under a different protocol hash. The packet directory
holds candidate texts and the de-blinding key: it gets a ``.gitignore`` and must
never be copied into a public package.
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

import candidate_support_adapter as adapter  # noqa: E402
import candidate_support_audit as audit  # noqa: E402

PROTOCOL = ROOT / "research" / "protocols" / "candidate-support-audit-protocol-234.json"
WORK = ROOT / "research" / "artifacts" / "candidate-support-audit-234"
PACKET = ROOT / "research" / "artifacts" / "candidate-support-audit-packet-234"
ANALYSIS = ROOT / "research" / "artifacts" / "candidate-support-audit-analysis-235.json"
HOOKS = ("iter_slots", "task_lookup", "p0_parse", "execute", "reference_exact", "ablation_runs", "pool_costs")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)


def read_json(path: Path, protocol_sha: str) -> Any:
    if not path.exists():
        raise SystemExit(f"missing {path}; run the earlier stage first")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("protocol_sha256") != protocol_sha:
        raise SystemExit(f"{path.name} was produced under a different protocol hash; do not mix outputs")
    return payload


def load_protocol(path: Path, *, require_frozen: bool) -> tuple[dict[str, Any], str]:
    protocol = json.loads(path.read_text(encoding="utf-8"))
    if require_frozen and protocol.get("status") != "frozen":
        raise SystemExit("protocol 234 is not frozen; no candidate text was read")
    return protocol, sha256(path)


def check() -> dict[str, Any]:
    """Report which hooks are wired without calling any of them on real data."""

    wired = {}
    for name in HOOKS:
        code = getattr(getattr(adapter, name), "__code__", None)
        wired[name] = code is None or "NotImplementedError" not in code.co_names
    return wired


def stage_reparse(protocol_sha: str, work: Path) -> dict[str, Any]:
    rows = audit.reparse(adapter.iter_slots(), p0_parse=adapter.p0_parse, execute=adapter.execute,
                         reference_exact=adapter.reference_exact, task_lookup=adapter.task_lookup)
    payload = {"protocol_sha256": protocol_sha, "provider_calls": 0, "texts_included": False, "rows": rows}
    write_json(work / "reparse.json", payload)
    summary = {"slots": len(rows), "funnel_U1": audit.funnel(rows, "U1"), "migration": audit.migration(rows)}
    write_json(work / "reparse-summary.json", {"protocol_sha256": protocol_sha, **summary})
    return summary


def _texts() -> dict[str, str]:
    return {s["slot_uid"]: s.get("text") or "" for s in adapter.iter_slots()}


def _private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    (path / ".gitignore").write_text("# candidate texts and the de-blinding key: never commit or publish\n*\n", encoding="utf-8")


def stage_packet(protocol: dict[str, Any], protocol_sha: str, work: Path, packet_dir: Path) -> dict[str, Any]:
    rows = read_json(work / "reparse.json", protocol_sha)["rows"]
    seed = protocol["statistics"]["seed"]
    params = protocol["audit"].get("parameters", {})
    packet_a, packet_b, key = audit.build_audit_packet(
        rows, _texts(), seed=seed, overlap=params.get("overlap_fraction_annotator_b", 0.30),
        secondary_per_cohort=params.get("secondary_per_cohort", 60), controls=params.get("accepted_controls", 60))
    _private_dir(packet_dir)
    audit.write_csv(str(packet_dir / "packet-annotator-a.csv"), packet_a, audit.PACKET_COLUMNS)
    audit.write_csv(str(packet_dir / "packet-annotator-b.csv"), packet_b, audit.PACKET_COLUMNS)
    for name, items in (("labels-annotator-a.csv", packet_a), ("labels-annotator-b.csv", packet_b)):
        audit.write_csv(str(packet_dir / name), [{"audit_id": p["audit_id"]} for p in items], audit.LABEL_COLUMNS)
    write_json(packet_dir / "private-key.json", {"protocol_sha256": protocol_sha, **key})
    strata = {s: sum(v["stratum"] == s for v in key["items"].values()) for s in ("census", "secondary", "control")}
    return {"items_a": len(packet_a), "items_b": len(packet_b), "strata": strata}


def stage_second_pass(protocol_sha: str, packet_dir: Path) -> dict[str, Any]:
    key = read_json(packet_dir / "private-key.json", protocol_sha)
    labels_a = audit.read_labels(str(packet_dir / "labels-annotator-a.csv"))
    unlabelled = [i for i in key["items"] if not (labels_a.get(i, {}).get("intent") or "").strip()]
    if unlabelled:
        raise SystemExit(f"annotator A has {len(unlabelled)} unlabelled items")
    extra = set(audit.second_pass_ids(labels_a, key))
    packet = [p for p in _read_packet(packet_dir / "packet-annotator-a.csv") if p["audit_id"] in extra]
    audit.write_csv(str(packet_dir / "packet-annotator-b-second-pass.csv"), packet, audit.PACKET_COLUMNS)
    audit.write_csv(str(packet_dir / "labels-annotator-b-second-pass.csv"), [{"audit_id": p["audit_id"]} for p in packet],
                    audit.LABEL_COLUMNS)
    return {"second_pass_items": len(packet)}


def _read_packet(path: Path) -> list[dict[str, str]]:
    return list(audit.read_labels(str(path)).values())


def _optional_labels(path: Path) -> dict[str, dict[str, str]]:
    return audit.read_labels(str(path)) if path.exists() else {}


def stage_analyze(protocol: dict[str, Any], protocol_sha: str, work: Path, packet_dir: Path, output: Path) -> dict[str, Any]:
    seed = protocol["statistics"]["seed"]
    rows = read_json(work / "reparse.json", protocol_sha)["rows"]
    key = read_json(packet_dir / "private-key.json", protocol_sha)
    labels_a = audit.read_labels(str(packet_dir / "labels-annotator-a.csv"))
    labels_b = {**_optional_labels(packet_dir / "labels-annotator-b.csv"),
                **_optional_labels(packet_dir / "labels-annotator-b-second-pass.csv")}
    labels_b = {k: v for k, v in labels_b.items() if (v.get("intent") or "").strip()}
    missing_b = sorted((set(key["annotator_b_ids"]) | set(audit.second_pass_ids(labels_a, key))) - set(labels_b))
    if missing_b:
        raise SystemExit(f"annotator B has not labelled {len(missing_b)} required items")
    final, agreement = audit.finalize_labels(labels_a, labels_b, _optional_labels(packet_dir / "adjudication.csv"))
    if agreement["unadjudicated_disagreements"]:
        raise SystemExit(f"{len(agreement['unadjudicated_disagreements'])} disagreements need adjudication.csv")
    run_task = {r["run_id"]: r["task_id"] for r in rows}
    scored = audit.score_human_plans(final, key, execute=adapter.execute, reference_exact=adapter.reference_exact,
                                     task_lookup=adapter.task_lookup, run_task=run_task)
    q_fn = audit.estimate_false_negatives(scored, seed=seed)
    mig = audit.migration(rows)
    census = audit.census_reclassification(scored, audit.run_classes(rows, "P0"))
    selectors = {
        parser: {
            endpoint: {
                "round_only": audit.replay_pools(rows, parser=parser, endpoint=endpoint, seed=seed),
                "final_inclusive": audit.replay_pools(rows, parser=parser, endpoint=endpoint, round_only=False, seed=seed),
                "slot_matched_16": audit.replay_pools(rows, parser=parser, endpoint=endpoint, slot_matched=16, seed=seed),
            }
            for endpoint in audit.ENDPOINTS
        }
        for parser in audit.PARSERS
    }
    endpoints = {cell: audit.dual_endpoints(spec["runs"], spec["control_arm"], spec["treated_arm"], seed=seed)
                 for cell, spec in adapter.ablation_runs().items()}
    result = {
        "artifact": "candidate-support-audit-analysis-235",
        "protocol_sha256": protocol_sha,
        "provider_calls": 0,
        "texts_included": False,
        "funnel": {"U1": audit.funnel(rows, "U1"), "U2": audit.funnel(rows, "U2"),
                   "U2_nested_pools_round_only": audit.pool_funnel(rows)},
        "pool_costs": _pool_costs(),
        "parser_migration": mig,
        "agreement": agreement,
        "q_fn": q_fn,
        "census_reclassification": census,
        "intent_counts": audit._counts(v["intent"] for v in scored.values()),
        "executable_intent_without_parseable_human_plan": sorted(
            i for i, v in scored.items() if v["intent"] in audit.EXECUTABLE_INTENTS and not v["human_plan_parsed"]),
        "format_failure_counts": audit._counts(v["format_failure"] for v in scored.values() if not v["p0_accepted"]),
        "execution_status_counts": {
            "p0_rejected": audit._counts(v["execution_status"] for v in scored.values() if not v["p0_accepted"]),
            "p0_accepted_controls": audit._counts(v["execution_status"] for v in scored.values() if v["p0_accepted"]),
        },
        "selector_replay": selectors,
        "endpoint_ablation": endpoints,
        "decision": audit.decide(census, mig, q_fn),
    }
    write_json(output, result)
    return result["decision"]


def _pool_costs() -> dict[str, Any] | None:
    try:
        return adapter.pool_costs()
    except NotImplementedError:
        return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    stage = parser.add_mutually_exclusive_group(required=True)
    for name in ("check", "reparse", "packet", "second-pass", "analyze"):
        stage.add_argument(f"--{name}", action="store_true")
    parser.add_argument("--protocol", type=Path, default=PROTOCOL)
    parser.add_argument("--work-dir", type=Path, default=WORK)
    parser.add_argument("--packet-dir", type=Path, default=PACKET)
    parser.add_argument("--output", type=Path, default=ANALYSIS)
    args = parser.parse_args(argv)

    if args.check:
        protocol, protocol_sha = load_protocol(args.protocol, require_frozen=False)
        report = {"protocol_status": protocol.get("status"), "protocol_sha256": protocol_sha, "hooks_wired": check()}
    else:
        protocol, protocol_sha = load_protocol(args.protocol, require_frozen=True)
        if args.reparse:
            report = stage_reparse(protocol_sha, args.work_dir)
        elif args.packet:
            report = stage_packet(protocol, protocol_sha, args.work_dir, args.packet_dir)
        elif args.second_pass:
            report = stage_second_pass(protocol_sha, args.packet_dir)
        else:
            report = stage_analyze(protocol, protocol_sha, args.work_dir, args.packet_dir, args.output)
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
