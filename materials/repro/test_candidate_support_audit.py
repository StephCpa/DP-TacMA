"""Synthetic-fixture tests for the protocol-234 candidate-support audit.

Run from this directory: ``python test_candidate_support_audit.py`` (or pytest).
A fake adapter stands in for the workspace parser, executor and traces; no
candidate text from the study and no provider is touched.
"""

from __future__ import annotations

import contextlib
import csv
import io
import json
import math
from pathlib import Path
import re
import tempfile

import candidate_support_adapter as adapter
import candidate_support_audit as audit
from candidate_parsers import IMPOSSIBLE, p1_normalize, p2_parse
import make_candidate_support_figures as figures
import run_candidate_support_audit as runner

# --------------------------------------------------------------- fake workspace
TASKS = {
    "T1": {"valid": {("oak_planks", "chest")}, "reference": ("oak_planks", "chest")},
    "T2": {"valid": {("stick",), ("stick", "torch")}, "reference": ("stick", "torch")},
    "T3": {"valid": set(), "reference": IMPOSSIBLE},
}


def fake_p0(text: str, task: dict) -> tuple[object, str]:
    """A strict P0: bare JSON array of lower-case identifiers, or exactly IMPOSSIBLE."""

    if text == IMPOSSIBLE:
        return IMPOSSIBLE, "ok"
    try:
        value = json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None, "json_error"
    if not isinstance(value, list) or not value or not all(isinstance(v, str) and re.fullmatch(r"[a-z0-9_]+", v) for v in value):
        return None, "schema_error"
    return tuple(value), "ok"


def fake_execute(plan: object, task: dict) -> bool:
    return isinstance(plan, tuple) and plan in task["valid"]


def fake_reference(plan: object, task: dict) -> bool:
    return plan == task["reference"]


def u1_slot(cohort: str, run: str, task: str, i: int, text: str, *, failed: bool, final: bool = False) -> dict:
    return {"slot_uid": f"{cohort}/{run}/{i}", "universe": "U1", "cohort": cohort, "run_id": run, "task_id": task,
            "semantic_eligible": task != "T3", "run_p0_failed": failed, "is_final": final, "text": text}


def fixture_slots() -> list[dict]:
    slots = []
    # R1 (cohort X): success under P0.
    slots += [u1_slot("X", "R1", "T1", 0, '["oak_planks", "chest"]', failed=False),
              u1_slot("X", "R1", "T1", 1, "I think we should craft a chest.", failed=False),
              u1_slot("X", "R1", "T1", 2, '["oak_planks", "chest"]', failed=False, final=True)]
    # R2 (cohort X): P0 generation failure, but a fenced valid plan is present (P1/P2 rescue it).
    slots += [u1_slot("X", "R2", "T2", 0, '```json\n["Stick", "Torch"]\n```', failed=True),
              u1_slot("X", "R2", "T2", 1, '```json\n["Stick", "Torch"]\n```', failed=True),  # duplicate text
              u1_slot("X", "R2", "T2", 2, "", failed=True),
              u1_slot("X", "R2", "T2", 3, '["planks"]', failed=True, final=True)]
    # R3 (cohort Y): genuine generation failure; prose only.
    slots += [u1_slot("Y", "R3", "T1", 0, "Craft planks, then a chest.", failed=True),
              u1_slot("Y", "R3", "T1", 1, '["oak_planks", "Chest!"]', failed=True),
              u1_slot("Y", "R3", "T1", 2, '["chest"]', failed=True, final=True)]
    # R4 (cohort Y): selection failure under P0 (valid round candidate, invalid final).
    slots += [u1_slot("Y", "R4", "T2", 0, '["stick"]', failed=True),
              u1_slot("Y", "R4", "T2", 1, "nothing useful", failed=True),
              u1_slot("Y", "R4", "T2", 2, '["torch"]', failed=True, final=True)]
    # R5: IMPOSSIBLE-reference task, not semantically eligible.
    slots += [u1_slot("Y", "R5", "T3", 0, IMPOSSIBLE, failed=True, final=True)]
    # U2 pool: one task, anchor (0) plus trajectories 1..2.
    for traj, texts in ((0, ['["planks"]', "prose"]), (1, ['["stick"]', "prose"]), (2, ['["stick", "torch"]', '["x"]'])):
        for i, text in enumerate(texts):
            slots.append({"slot_uid": f"pool/T2/t{traj}/{i}", "universe": "U2", "cohort": "qwen_pool",
                          "run_id": f"T2/t{traj}", "task_id": "T2", "semantic_eligible": True, "is_final": False,
                          "trajectory": traj, "text": text, "recorded_score": float(len(text)),
                          "judge_score": None, "env_success": i == 0})
    return slots


def reparsed() -> list[dict]:
    return audit.reparse(fixture_slots(), p0_parse=fake_p0, execute=fake_execute,
                         reference_exact=fake_reference, task_lookup=TASKS.__getitem__)


def install_fake_adapter() -> None:
    adapter.iter_slots = lambda: iter(fixture_slots())
    adapter.task_lookup = TASKS.__getitem__
    adapter.p0_parse = fake_p0
    adapter.execute = fake_execute
    adapter.reference_exact = fake_reference
    adapter.pool_costs = lambda: {f"C{j}": {"calls": 10 * j, "tokens": 1000 * j, "judge_calls": None} for j in (1, 2)}
    adapter.ablation_runs = lambda: {"length": {"control_arm": "orig", "treated_arm": "zero", "runs": [
        {"arm": "orig", "task_id": "T1", "semantic_eligible": True, "exec_valid": False, "ref_exact": False},
        {"arm": "zero", "task_id": "T1", "semantic_eligible": True, "exec_valid": True, "ref_exact": True},
        {"arm": "orig", "task_id": "T2", "semantic_eligible": True, "exec_valid": True, "ref_exact": True},
        {"arm": "zero", "task_id": "T2", "semantic_eligible": True, "exec_valid": True, "ref_exact": True},
    ]}}


# ---------------------------------------------------------------------- parsers
def test_p2_parser_cases() -> None:
    cases = {
        '["oak_planks", "chest"]': ("oak_planks", "chest"),
        '```json\n["Oak_Planks", "minecraft:chest"]\n```': ("oak_planks", "chest"),
        'Answer: ["stick"] done.': ("stick",),
        "“IMPOSSIBLE”": IMPOSSIBLE,
        "impossible.": IMPOSSIBLE,
        '["IMPOSSIBLE"]': IMPOSSIBLE,
        '["stick"] and again ["stick"]': ("stick",),
        "［“stick”，“torch”］": ("stick", "torch"),
    }
    for text, plan in cases.items():
        result = p2_parse(text)
        assert result.accepted and result.plan == plan, (text, result)
    rejects = {
        "": "empty", None: "empty", "   ": "empty",
        "craft a chest": "no_string_array",
        '["stick"] or ["torch"]': "ambiguous_multiple_plans",
        '["oak planks!"]': "non_identifier_item",
        "[1, 2]": "no_string_array",
        "[]": "no_string_array",
    }
    for text, reason in rejects.items():
        result = p2_parse(text)
        assert not result.accepted and result.reason == reason, (text, result)


def test_p1_normalize_only_changes_format() -> None:
    assert p1_normalize('```json\n[" Stick ", "TORCH"]\n```') == '["stick", "torch"]'
    assert p1_normalize("“IMPOSSIBLE”") == '"IMPOSSIBLE"'
    assert p1_normalize("  IMPOSSIBLE \r\n") == "IMPOSSIBLE"
    # Prose is never interpreted.
    assert p1_normalize("Craft planks, then a chest.") == "Craft planks, then a chest."
    assert fake_p0(p1_normalize("Craft planks, then a chest."), TASKS["T1"])[0] is None


# --------------------------------------------------------------------- reparse
def test_reparse_states_and_no_text() -> None:
    rows = reparsed()
    assert all("text" not in r for r in rows)
    by_uid = {r["slot_uid"]: r for r in rows}
    fenced = by_uid["X/R2/0"]["parses"]
    assert not fenced["P0"]["accepted"] and fenced["P0"]["reason"] == "json_error"
    assert fenced["P1"]["valid"] and fenced["P2"]["valid"]
    assert fenced["P2"]["state"] == "executor_valid_reference_exact"
    assert by_uid["X/R2/2"]["parses"]["P0"]["state"] == "no_text"
    assert by_uid["X/R2/3"]["parses"]["P0"]["state"] == "executor_invalid"
    assert by_uid["Y/R4/0"]["parses"]["P0"]["state"] == "executor_valid_not_reference_exact"
    assert by_uid["Y/R3/0"]["parses"]["P2"]["state"] == "format_invalid"
    assert by_uid["X/R1/0"]["text_sha256"] == audit.sha('["oak_planks", "chest"]')


def test_run_classes_and_migration() -> None:
    rows = reparsed()
    p0 = audit.run_classes(rows, "P0")
    assert p0 == {"R1": "success", "R2": "generation_failure", "R3": "generation_failure", "R4": "selection_failure"}
    mig = audit.migration(rows)
    assert mig["p0_failed_runs"] == 3 and mig["p0_generation_failures"] == 2
    assert mig["P0"]["reclassified_from_generation"] == []
    assert mig["P1"]["reclassified_from_generation"] == ["R2"]
    assert mig["P2"]["reclassified_from_generation"] == ["R2"]
    assert mig["P2"]["matrix_p0_rows"]["generation_failure"] == {"success": 0, "selection_failure": 1, "generation_failure": 1}
    fun = audit.funnel(rows, "U1")
    assert fun["recorded_slots"] == 14 and fun["with_text"] == 13
    assert fun["P0"]["accepted"] < fun["P1"]["accepted"]
    assert fun["rejection_reasons"]["P0"]["json_error"] >= 1


# ---------------------------------------------------------------------- packet
def _packet(seed: int = 234):
    rows = reparsed()
    texts = {s["slot_uid"]: s["text"] for s in fixture_slots()}
    return rows, audit.build_audit_packet(rows, texts, seed=seed, secondary_per_cohort=60, controls=60)


def test_packet_blinding_census_and_overlap() -> None:
    rows, (packet_a, packet_b, key) = _packet()
    assert all(set(p) == set(audit.PACKET_COLUMNS) for p in packet_a)
    forbidden = {"cohort", "run_id", "task_id", "stratum", "weight", "run_p0_failed", "reference", "slot_uids"}
    assert not forbidden & set(audit.PACKET_COLUMNS)
    for p in packet_a:
        assert not re.search(r"\bR\d\b|\bX\b|\bY\b", p["audit_id"])
    # Census: every unique P0-rejected text in P0-failed eligible runs, duplicates collapsed.
    census = [v for v in key["items"].values() if v["stratum"] == "census"]
    expected = {(r["run_id"], r["text_sha256"]) for r in rows
                if r["universe"] == "U1" and r["semantic_eligible"] and r["run_p0_failed"] and not r["parses"]["P0"]["accepted"]}
    assert len(census) == len(expected)
    dup = [v for v in census if v["run_id"] == "R2" and len(v["slot_uids"]) == 2]
    assert len(dup) == 1
    assert all(not v["run_id"] == "R5" for v in key["items"].values())  # ineligible run excluded
    # Annotator B: seeded ~30% of census plus every non-census item.
    b = set(key["annotator_b_ids"])
    census_ids = {a for a, v in key["items"].items() if v["stratum"] == "census"}
    assert len(b & census_ids) == round(0.30 * len(census_ids))
    assert {a for a, v in key["items"].items() if v["stratum"] != "census"} <= b
    assert {p["audit_id"] for p in packet_b} == b
    # Deterministic for a seed.
    assert _packet()[1][2] == key


def test_second_pass_ids() -> None:
    _, (packet_a, _, key) = _packet()
    labels = {p["audit_id"]: {"intent": "A0"} for p in packet_a}
    outside = sorted(set(labels) - set(key["annotator_b_ids"]))
    labels[outside[0]]["intent"] = "A3"
    assert audit.second_pass_ids(labels, key) == [outside[0]]


# ---------------------------------------------------------------- statistics
def test_exact_bounds_match_known_values() -> None:
    assert math.isclose(audit.exact_upper(0, 120), 1 - 0.05 ** (1 / 120), rel_tol=1e-9)
    assert math.isclose(audit.exact_upper(0, 60), 1 - 0.05 ** (1 / 60), rel_tol=1e-9)
    low, high = audit.exact_interval(43, 46)
    assert round(low, 3) == 0.821 and round(high, 3) == 0.986
    assert audit.exact_interval(0, 10)[0] == 0.0 and round(audit.exact_interval(0, 10)[1], 3) == 0.308
    assert audit.mcnemar_exact_p(2, 0) == 0.5 and audit.mcnemar_exact_p(2, 3) == 1.0
    assert audit.cohen_kappa([("A0", "A0"), ("A2", "A2")]) == 1.0
    assert math.isclose(audit.cohen_kappa([("a", "a"), ("a", "b"), ("b", "b"), ("b", "a")]), 0.0)


def test_finalize_labels_requires_adjudication() -> None:
    a = {"1": {"intent": "A0", "human_plan": ""}, "2": {"intent": "A2", "human_plan": '["stick"]'},
         "3": {"intent": "A3", "human_plan": '["stick"]'}}
    b = {"2": {"intent": "A2", "human_plan": '["Stick"]'}, "3": {"intent": "A3", "human_plan": '["torch"]'}}
    final, agreement = audit.finalize_labels(a, b, {})
    assert agreement["unadjudicated_disagreements"] == ["3"] and "3" not in final
    final, agreement = audit.finalize_labels(a, b, {"3": {"intent": "A1", "human_plan": ""}})
    assert final["3"]["intent"] == "A1" and agreement["double_labelled"] == 2


def _scored(valid_flags: list[bool], cohort: str = "X") -> dict:
    return {str(i): {"run_id": f"R{i % 7}", "cohort": cohort, "stratum": "census", "weight": 1.0, "p0_accepted": False,
                     "run_p0_failed": True, "p0_reason": "json_error", "intent": "A3" if v else "A0", "human_valid": v}
            for i, v in enumerate(valid_flags)}


def test_q_fn_and_decision_tiers() -> None:
    clean = audit.estimate_false_negatives(_scored([False] * 60), draws=200)
    assert clean["human_valid"] == 0 and math.isclose(clean["unweighted_one_sided_upper"], 1 - 0.05 ** (1 / 60))
    assert clean["decision_upper"] <= 0.05
    mig = {p: {"reclassified_from_generation": []} for p in ("P1", "P2")}
    census = {"reclassified": 1}
    assert audit.decide(census, mig, clean)["tier"] == "tier_A_robust"
    assert audit.decide({"reclassified": 4}, mig, clean)["tier"] == "tier_B_qualified"
    mig_c = {"P1": {"reclassified_from_generation": [f"R{i}" for i in range(10)]}, "P2": {"reclassified_from_generation": []}}
    assert audit.decide(census, mig_c, clean)["tier"] == "tier_C_weakened"
    noisy = audit.estimate_false_negatives(_scored([True] * 5 + [False] * 55), draws=200)
    assert noisy["decision_upper"] > 0.05
    assert audit.decide(census, mig, noisy)["tier"] == "tier_B_qualified"
    mixed = {**_scored([False] * 60), **{f"y{i}": v for i, v in enumerate(_scored([True] * 3 + [False] * 7, "Y").values())}}
    decision = audit.decide(census, mig, audit.estimate_false_negatives(mixed, draws=200))
    assert decision["provider_flags"] == ["Y"]


def test_census_reclassification() -> None:
    scored = _scored([True, False])
    scored["0"]["run_id"] = "R2"
    out = audit.census_reclassification(scored, {"R2": "generation_failure", "R3": "generation_failure", "R1": "success"})
    assert out == {"p0_generation_failures": 2, "reclassified_runs": ["R2"], "reclassified": 1,
                   "generation_failures_after_census": 1}


# ------------------------------------------------------------------ selectors
def _cand(valid: bool, length: int, score=None, success=None, judge=None, traj=1, final=False) -> dict:
    return {"universe": "U2", "task_id": "T", "trajectory": traj, "is_final": final, "length": length,
            "recorded_score": score, "env_success": success, "judge_score": judge,
            "parses": {p: {"valid": valid} for p in audit.PARSERS}}


def test_selector_expectations() -> None:
    pool = [_cand(True, 100, 1.0, False), _cand(False, 900, 2.0, True), _cand(False, 900, 0.5, False)]
    v = audit.selector_values(pool)
    assert math.isclose(v["B1_random"], 1 / 3)
    assert v["B0_recorded"] == 0.0 and v["B2_length_only"] == 0.0 and v["B6_oracle"] == 1.0
    assert v["B3_success_only"] == 0.0 and v["B4_composite"] == 0.0 and v["B5_judge"] is None
    tied = [_cand(True, 10, 1.0), _cand(False, 10, 1.0)]
    assert audit.selector_values(tied)["B0_recorded"] == 0.5
    for c in pool:
        for p in audit.PARSERS:
            c["parses"][p]["reference_exact"] = False
    ref = audit.selector_values(pool, endpoint="reference_exactness")
    assert ref["B6_oracle"] == 0.0 and ref["B1_random"] == 0.0


def test_replay_pools_round_only_and_slot_matched() -> None:
    rows = [_cand(False, 10, traj=0), _cand(False, 20, traj=1), _cand(True, 5, traj=2), _cand(True, 50, traj=2, final=True)]
    for r in rows:
        r["env_success"] = False
    out = audit.replay_pools(rows, pools=2, draws=50)
    assert out["C1"]["B6_oracle"]["mean"] == 0.0 and out["C2"]["B6_oracle"]["mean"] == 1.0
    assert math.isclose(out["C2"]["B1_random"]["mean"], 1 / 3)
    assert "seeded_replays_1000_95" in out["C2"]["B1_random"]
    assert out["C2"]["B2_length_only"]["mean"] == 0.0
    inclusive = audit.replay_pools(rows, pools=2, round_only=False, draws=50)
    assert inclusive["C2"]["B2_length_only"]["mean"] == 1.0
    matched = audit.replay_pools(rows, pools=2, slot_matched=1, draws=400)
    assert abs(matched["C2"]["B6_oracle"]["mean"] - 1 / 3) < 0.1


def test_dual_endpoints() -> None:
    install_fake_adapter()
    spec = adapter.ablation_runs()["length"]
    out = audit.dual_endpoints(spec["runs"], spec["control_arm"], spec["treated_arm"])
    for name in ("executable_validity", "reference_exactness", "both"):
        assert out[name]["pairs"] == 2 and out[name]["difference"] == 0.5 and out[name]["discordant"] == [1, 0]


# --------------------------------------------------------------------- runner
def _write_protocol(tmp: Path, status: str) -> Path:
    source = runner.PROTOCOL
    protocol = json.loads(source.read_text(encoding="utf-8"))
    protocol["status"] = status
    path = tmp / "protocol.json"
    path.write_text(json.dumps(protocol), encoding="utf-8")
    return path


def _fill_labels(path: Path, packet: Path, intent_for) -> None:
    with open(packet, newline="", encoding="utf-8") as handle:
        items = list(csv.DictReader(handle))
    rows = []
    for item in items:
        intent, plan = intent_for(item)
        rows.append({"audit_id": item["audit_id"], "intent": intent, "format_failure": "F2", "human_plan": plan})
    audit.write_csv(str(path), rows, audit.LABEL_COLUMNS)


def test_runner_refuses_unfrozen_and_reports_unwired_hooks() -> None:
    import importlib
    importlib.reload(adapter)
    assert not any(runner.check().values())
    assert runner._pool_costs() is None
    with tempfile.TemporaryDirectory() as tmp:
        path = _write_protocol(Path(tmp), "draft_not_frozen")
        try:
            runner.main(["--reparse", "--protocol", str(path), "--work-dir", tmp])
        except SystemExit as exc:
            assert "not frozen" in str(exc)
        else:
            raise AssertionError("an unfrozen protocol must block text access")


def test_runner_end_to_end_with_fake_adapter() -> None:
    install_fake_adapter()
    assert all(runner.check().values())
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        protocol = _write_protocol(tmp, "frozen")
        common = ["--protocol", str(protocol), "--work-dir", str(tmp / "work"), "--packet-dir", str(tmp / "packet"),
                  "--output", str(tmp / "analysis.json")]
        runner.main(["--reparse", *common])
        stored = (tmp / "work" / "reparse.json").read_text(encoding="utf-8")
        assert "Craft planks" not in stored and "```" not in stored  # raw texts are never stored
        runner.main(["--packet", *common])
        packet = tmp / "packet"
        assert (packet / ".gitignore").read_text(encoding="utf-8").strip().endswith("*")

        def judge(item):  # a fenced plan is read as an executable intent; everything else is not
            plan = p2_parse(item["text"]).plan
            return ("A3", json.dumps(list(plan))) if isinstance(plan, tuple) and "```" in item["text"] else ("A0", "")

        _fill_labels(packet / "labels-annotator-a.csv", packet / "packet-annotator-a.csv", judge)
        try:
            runner.main(["--analyze", *common])
        except SystemExit as exc:
            assert "annotator B" in str(exc)
        else:
            raise AssertionError("analysis must wait for annotator B")
        runner.main(["--second-pass", *common])
        _fill_labels(packet / "labels-annotator-b.csv", packet / "packet-annotator-b.csv", judge)
        _fill_labels(packet / "labels-annotator-b-second-pass.csv", packet / "packet-annotator-b-second-pass.csv", judge)
        runner.main(["--analyze", *common])
        result = json.loads((tmp / "analysis.json").read_text(encoding="utf-8"))
        assert "Craft planks" not in json.dumps(result)
        assert result["census_reclassification"]["reclassified_runs"] == ["R2"]
        assert result["parser_migration"]["P1"]["reclassified_from_generation"] == ["R2"]
        assert result["decision"]["tier"] in {"tier_A_robust", "tier_B_qualified"}
        assert result["decision"]["census_reclassified"] == 1
        assert result["endpoint_ablation"]["length"]["executable_validity"]["difference"] == 0.5
        replay = result["selector_replay"]["P0"]
        assert replay["executable_validity"]["round_only"]["C2"]["B6_oracle"]["mean"] == 1.0
        assert replay["reference_exactness"]["round_only"]["C2"]["B6_oracle"]["mean"] == 1.0
        assert replay["reference_exactness"]["round_only"]["C1"]["B6_oracle"]["mean"] == 0.0
        assert result["funnel"]["U2_nested_pools_round_only"]["C2"]["P0"]["unique_valid_plans_per_task"] == 2.0
        assert result["execution_status_counts"]["p0_rejected"].get("E3") == 1
        assert result["pool_costs"]["C2"]["tokens"] == 2000
        assert result["executable_intent_without_parseable_human_plan"] == []
        figures.main([str(tmp / "analysis.json"), str(tmp / "figures")])
        for name in ("candidate-support-funnel.pdf", "run-reclassification.pdf", "selector-vs-support.pdf",
                     "selector-cost-table.tex", "selector-cost-table.md"):
            assert (tmp / "figures" / name).stat().st_size > 0, name
        assert "2,000 tokens" in (tmp / "figures" / "selector-cost-table.md").read_text(encoding="utf-8")
        # A changed protocol must not be mixed with earlier outputs.
        text = protocol.read_text(encoding="utf-8").replace('"seed": 234', '"seed": 235')
        protocol.write_text(text, encoding="utf-8")
        try:
            runner.main(["--analyze", *common])
        except SystemExit as exc:
            assert "different protocol hash" in str(exc)
        else:
            raise AssertionError("a protocol change must be rejected")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for test in tests:
        with contextlib.redirect_stdout(io.StringIO()):
            test()
    print(f"all {len(tests)} tests passed")
