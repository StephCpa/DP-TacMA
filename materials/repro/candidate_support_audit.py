"""Analysis library for the parser-independent candidate-support audit (protocol 234).

Pure functions over slot records; the workspace adapter supplies texts, the P0
parser, the executor and reference checks. No provider calls.

Slot record fields (adapter): slot_uid, universe ("U1" headroom or "U2" pool),
cohort, run_id, task_id, semantic_eligible, run_p0_failed (U1), is_final,
trajectory (U2: 0 = anchor, 1..5 stochastic), text, recorded_score,
judge_score, env_success (each optional).
"""

from __future__ import annotations

from collections import defaultdict
import csv
import hashlib
import json
import math
import random
from typing import Any, Callable, Iterable

from candidate_parsers import IMPOSSIBLE, ParseResult, p1_normalize, p2_parse

PARSERS = ("P0", "P1", "P2")
INTENTS = ("A0", "A1", "A2", "A3")
EXECUTABLE_INTENTS = {"A2", "A3"}
PACKET_COLUMNS = ["audit_id", "text", "p0_reason", "p1_reason", "p2_reason", "p2_plan"]
LABEL_COLUMNS = ["audit_id", "intent", "format_failure", "human_plan", "notes"]


# ----------------------------------------------------------------- statistics
def binomial_cdf(k: int, n: int, p: float) -> float:
    return sum(math.comb(n, i) * p**i * (1 - p) ** (n - i) for i in range(k + 1))


def exact_upper(k: int, n: int, alpha: float = 0.05) -> float | None:
    """One-sided exact (Clopper-Pearson) upper bound."""

    if n == 0:
        return None
    if k >= n:
        return 1.0
    low, high = k / n, 1.0
    for _ in range(80):
        mid = (low + high) / 2
        if binomial_cdf(k, n, mid) > alpha:
            low = mid
        else:
            high = mid
    return high


def exact_interval(k: int, n: int) -> list[float | None]:
    """Two-sided 95% Clopper-Pearson interval."""

    if n == 0:
        return [None, None]
    lower = 0.0 if k == 0 else 1 - exact_upper(n - k, n, 0.025)
    return [lower, exact_upper(k, n, 0.025)]


def mcnemar_exact_p(first_only: int, second_only: int) -> float:
    n = first_only + second_only
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, i) for i in range(min(first_only, second_only) + 1)) / 2**n)


def bootstrap_mean_ci(values: list[float], *, seed: int, draws: int = 10_000) -> list[float | None]:
    if not values:
        return [None, None]
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(values[rng.randrange(n)] for _ in range(n)) / n for _ in range(draws))
    return [means[int(0.025 * (draws - 1))], means[int(0.975 * (draws - 1))]]


def cohen_kappa(pairs: list[tuple[str, str]]) -> float | None:
    if not pairs:
        return None
    labels = sorted({a for a, _ in pairs} | {b for _, b in pairs})
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    expected = sum(
        (sum(a == lab for a, _ in pairs) / n) * (sum(b == lab for _, b in pairs) / n) for lab in labels
    )
    return 1.0 if expected == 1 else (observed - expected) / (1 - expected)


# ------------------------------------------------------------------ reparsing
def _plan_json(plan: tuple[str, ...] | str | None) -> Any:
    return list(plan) if isinstance(plan, tuple) else plan


def reparse(
    slots: Iterable[dict[str, Any]],
    *,
    p0_parse: Callable[[str, Any], tuple[Any, str]],
    execute: Callable[[Any, Any], bool],
    reference_exact: Callable[[Any, Any], bool],
    task_lookup: Callable[[str], Any],
) -> list[dict[str, Any]]:
    """Run P0, P1 and P2 on every slot and execute every accepted plan."""

    rows = []
    for slot in slots:
        task = task_lookup(slot["task_id"])
        text = slot.get("text") or ""
        results: dict[str, ParseResult] = {}
        plan, reason = p0_parse(text, task)
        results["P0"] = ParseResult(plan, reason if plan is None else "ok")
        plan, reason = p0_parse(p1_normalize(text), task) if text.strip() else (None, "empty")
        results["P1"] = ParseResult(plan, reason if plan is None else "ok")
        results["P2"] = p2_parse(text)
        parsed = {}
        for name, result in results.items():
            valid = bool(result.accepted and execute(result.plan, task))
            parsed[name] = {
                "accepted": result.accepted,
                "reason": result.reason,
                "plan": _plan_json(result.plan),
                "valid": valid,
                "reference_exact": bool(result.accepted and reference_exact(result.plan, task)),
                "state": slot_state(text, result.accepted, valid, bool(result.accepted and reference_exact(result.plan, task))),
            }
        rows.append({**{k: v for k, v in slot.items() if k != "text"}, "text_sha256": sha(text), "length": len(text), "parses": parsed})
    return rows


def slot_state(text: str | None, accepted: bool, valid: bool, ref_exact: bool) -> str:
    if not (text or "").strip():
        return "no_text"
    if not accepted:
        return "format_invalid"
    if not valid:
        return "executor_invalid"
    return "executor_valid_reference_exact" if ref_exact else "executor_valid_not_reference_exact"


def sha(text: str | None) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()


# ------------------------------------------------------- run classes (U1)
def run_classes(rows: list[dict[str, Any]], parser: str) -> dict[str, str]:
    """success / selection_failure / generation_failure per eligible U1 run."""

    by_run: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["universe"] == "U1" and row.get("semantic_eligible", True):
            by_run[row["run_id"]].append(row)
    classes = {}
    for run_id, slots in by_run.items():
        final_valid = any(s["parses"][parser]["valid"] for s in slots if s.get("is_final"))
        any_valid = any(s["parses"][parser]["valid"] for s in slots)
        classes[run_id] = "success" if final_valid else ("selection_failure" if any_valid else "generation_failure")
    return classes


RUN_CLASSES = ("success", "selection_failure", "generation_failure")


def migration(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Where the P0-failed runs land under each parser, with the full P0-by-parser matrix."""

    base = run_classes(rows, "P0")
    failed = sorted(r for r, c in base.items() if c != "success")
    out = {"p0_failed_runs": len(failed), "p0_generation_failures": sum(base[r] == "generation_failure" for r in failed)}
    for parser in PARSERS:
        classes = run_classes(rows, parser)
        out[parser] = {c: sum(classes[r] == c for r in failed) for c in RUN_CLASSES}
        out[parser]["reclassified_from_generation"] = sorted(
            r for r in failed if base[r] == "generation_failure" and classes[r] != "generation_failure"
        )
        out[parser]["matrix_p0_rows"] = {a: {b: sum(base[r] == a and classes[r] == b for r in base) for b in RUN_CLASSES}
                                         for a in RUN_CLASSES}
    return out


def funnel(rows: list[dict[str, Any]], universe: str = "U1") -> dict[str, Any]:
    use = [r for r in rows if r["universe"] == universe]
    out = {"recorded_slots": len(use), "with_text": sum(r["length"] > 0 for r in use)}
    for parser in PARSERS:
        out[parser] = {
            "accepted": sum(r["parses"][parser]["accepted"] for r in use),
            "executor_valid": sum(r["parses"][parser]["valid"] for r in use),
            "reference_exact": sum(r["parses"][parser]["valid"] and r["parses"][parser]["reference_exact"] for r in use),
        }
    out["accepted_by_any_parser"] = sum(any(r["parses"][p]["accepted"] for p in PARSERS) for r in use)
    out["rejection_reasons"] = {p: _counts(r["parses"][p]["reason"] for r in use if not r["parses"][p]["accepted"])
                                for p in PARSERS}
    out["states"] = {p: _counts(r["parses"][p]["state"] for r in use) for p in PARSERS}
    out["by_cohort"] = {}
    for cohort in sorted({r["cohort"] for r in use}):
        sub = [r for r in use if r["cohort"] == cohort]
        out["by_cohort"][cohort] = {p: sum(r["parses"][p]["accepted"] for r in sub) for p in PARSERS} | {"slots": len(sub)}
    return out


def _counts(values: Iterable[str]) -> dict[str, int]:
    out: dict[str, int] = defaultdict(int)
    for v in values:
        out[v] += 1
    return dict(sorted(out.items()))


def pool_funnel(rows: list[dict[str, Any]], pools: int = 5, round_only: bool = True) -> dict[str, Any]:
    """Slots, parser acceptance and executor validity in each nested U2 pool C_j (summed over tasks)."""

    use = [r for r in rows if r["universe"] == "U2" and (not round_only or not r.get("is_final"))]
    out = {}
    for j in range(1, pools + 1):
        pool = [r for r in use if r["trajectory"] <= j]
        out[f"C{j}"] = {"slots": len(pool)} | {
            p: {
                "accepted": sum(r["parses"][p]["accepted"] for r in pool),
                "executor_valid": sum(r["parses"][p]["valid"] for r in pool),
                "unique_valid_plans_per_task": _mean_unique_valid(pool, p),
            }
            for p in PARSERS
        }
    return out


def _mean_unique_valid(pool: list[dict[str, Any]], parser: str) -> float | None:
    plans: dict[str, set[str]] = {r["task_id"]: set() for r in pool}
    for r in pool:
        if r["parses"][parser]["valid"]:
            plans[r["task_id"]].add(json.dumps(r["parses"][parser]["plan"]))
    return sum(len(v) for v in plans.values()) / len(plans) if plans else None


# ------------------------------------------------------------ audit packet
def _unique_units(rows: list[dict[str, Any]], texts: dict[str, str]) -> list[dict[str, Any]]:
    units: dict[tuple[str, str], dict[str, Any]] = {}
    for row in rows:
        if row["universe"] != "U1" or not row.get("semantic_eligible", True):
            continue
        key = (row["run_id"], row["text_sha256"])
        unit = units.setdefault(key, {
            "run_id": row["run_id"], "cohort": row["cohort"], "text_sha256": row["text_sha256"],
            "run_p0_failed": bool(row.get("run_p0_failed")), "slot_uids": [], "text": texts[row["slot_uid"]],
            "p0_accepted": row["parses"]["P0"]["accepted"],
            "reasons": {p: row["parses"][p]["reason"] for p in PARSERS}, "p2_plan": row["parses"]["P2"]["plan"],
        })
        unit["slot_uids"].append(row["slot_uid"])
    return list(units.values())


def build_audit_packet(
    rows: list[dict[str, Any]],
    texts: dict[str, str],
    *,
    seed: int = 234,
    overlap: float = 0.30,
    secondary_per_cohort: int = 60,
    controls: int = 60,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    """Return blinded packets for annotators A and B and the private key."""

    rng = random.Random(seed)
    units = _unique_units(rows, texts)
    census = [u for u in units if u["run_p0_failed"] and not u["p0_accepted"]]
    selected = [(u, "census", 1.0) for u in census]
    for cohort in sorted({u["cohort"] for u in units}):
        pool = sorted((u for u in units if u["cohort"] == cohort and not u["run_p0_failed"] and not u["p0_accepted"]),
                      key=lambda u: (u["run_id"], u["text_sha256"]))
        take = rng.sample(pool, min(secondary_per_cohort, len(pool)))
        selected += [(u, "secondary", len(pool) / len(take)) for u in take]
    accepted = sorted((u for u in units if u["p0_accepted"]), key=lambda u: (u["run_id"], u["text_sha256"]))
    selected += [(u, "control", 1.0) for u in rng.sample(accepted, min(controls, len(accepted)))]

    key: dict[str, Any] = {"seed": seed, "items": {}}
    packet = []
    for unit, stratum, weight in selected:
        audit_id = hashlib.sha256(f"{seed}:{unit['run_id']}:{unit['text_sha256']}".encode()).hexdigest()[:12]
        key["items"][audit_id] = {
            "run_id": unit["run_id"], "cohort": unit["cohort"], "stratum": stratum, "weight": weight,
            "slot_uids": unit["slot_uids"], "p0_accepted": unit["p0_accepted"], "run_p0_failed": unit["run_p0_failed"],
            "p0_reason": unit["reasons"]["P0"],
        }
        packet.append({
            "audit_id": audit_id, "text": unit["text"], "p0_reason": unit["reasons"]["P0"],
            "p1_reason": unit["reasons"]["P1"], "p2_reason": unit["reasons"]["P2"],
            "p2_plan": json.dumps(unit["p2_plan"], ensure_ascii=False) if unit["p2_plan"] is not None else "",
        })
    census_ids = sorted(a for a, v in key["items"].items() if v["stratum"] == "census")
    overlap_ids = set(rng.sample(census_ids, round(overlap * len(census_ids))))
    b_ids = overlap_ids | {a for a, v in key["items"].items() if v["stratum"] != "census"}
    key["annotator_b_ids"] = sorted(b_ids)
    packet_a = packet[:]
    rng.shuffle(packet_a)
    packet_b = [p for p in packet if p["audit_id"] in b_ids]
    rng.shuffle(packet_b)
    return packet_a, packet_b, key


def second_pass_ids(labels_a: dict[str, dict[str, str]], key: dict[str, Any]) -> list[str]:
    """Items A labelled A2/A3 that B has not seen: B must label them too."""

    b_ids = set(key["annotator_b_ids"])
    return sorted(i for i, lab in labels_a.items() if lab["intent"] in EXECUTABLE_INTENTS and i not in b_ids)


def write_csv(path: str, rows: list[dict[str, Any]], columns: list[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            writer.writerow({c: row.get(c, "") for c in columns})


def read_labels(path: str) -> dict[str, dict[str, str]]:
    with open(path, newline="", encoding="utf-8") as handle:
        return {row["audit_id"]: row for row in csv.DictReader(handle)}


# ----------------------------------------------------------------- ingestion
def _plan_given(label: dict[str, str]) -> bool:
    return bool((label.get("human_plan") or "").strip())


def finalize_labels(
    labels_a: dict[str, dict[str, str]],
    labels_b: dict[str, dict[str, str]],
    adjudication: dict[str, dict[str, str]],
) -> tuple[dict[str, dict[str, str]], dict[str, Any]]:
    """Merge annotators; disagreements must be adjudicated."""

    final, missing = {}, []
    both = sorted(set(labels_a) & set(labels_b))
    for audit_id, label in labels_a.items():
        if audit_id in labels_b:
            other = labels_b[audit_id]
            agree = label["intent"] == other["intent"] and _plan_given(label) == _plan_given(other) and (
                p2_parse(label.get("human_plan")).plan == p2_parse(other.get("human_plan")).plan
            )
            if agree:
                final[audit_id] = label
            elif audit_id in adjudication:
                final[audit_id] = adjudication[audit_id]
            else:
                missing.append(audit_id)
        else:
            final[audit_id] = label
    agreement = {
        "double_labelled": len(both),
        "kappa_intent": cohen_kappa([(labels_a[i]["intent"], labels_b[i]["intent"]) for i in both]),
        "kappa_plan_given": cohen_kappa([(str(_plan_given(labels_a[i])), str(_plan_given(labels_b[i]))) for i in both]),
        "unadjudicated_disagreements": missing,
    }
    return final, agreement


def score_human_plans(
    final: dict[str, dict[str, str]],
    key: dict[str, Any],
    *,
    execute: Callable[[Any, Any], bool],
    reference_exact: Callable[[Any, Any], bool],
    task_lookup: Callable[[str], Any],
    run_task: dict[str, str],
) -> dict[str, dict[str, Any]]:
    scored = {}
    for audit_id, label in final.items():
        item = key["items"][audit_id]
        plan = p2_parse(label.get("human_plan")).plan if label["intent"] in EXECUTABLE_INTENTS else None
        task = task_lookup(run_task[item["run_id"]])
        valid = bool(plan is not None and execute(plan, task))
        ref = bool(valid and reference_exact(plan, task))
        scored[audit_id] = {
            **item, "intent": label["intent"], "format_failure": label.get("format_failure", ""),
            "human_plan_parsed": plan is not None, "human_valid": valid, "human_reference_exact": ref,
            # E0 non-executable, E1 canonical plan but executor-invalid, E2 executor-valid, E3 also reference-exact.
            "execution_status": "E3" if ref else "E2" if valid else "E1" if plan is not None else "E0",
        }
    return scored


# ----------------------------------------------------------------- estimates
def estimate_false_negatives(scored: dict[str, dict[str, Any]], *, seed: int = 234, draws: int = 10_000) -> dict[str, Any]:
    rejected = [v for v in scored.values() if not v["p0_accepted"]]
    k, n = sum(v["human_valid"] for v in rejected), len(rejected)
    weights = [v["weight"] for v in rejected]
    weighted = sum(w * v["human_valid"] for w, v in zip(weights, rejected)) / sum(weights) if rejected else None
    # Run-clustered, stratum-preserving bootstrap of the weighted estimate.
    rng = random.Random(seed)
    clusters: dict[tuple[tuple[str, str], str], list[dict[str, Any]]] = defaultdict(list)
    for v in rejected:
        clusters[((v["stratum"], v["cohort"]), v["run_id"])].append(v)
    strata: dict[tuple[str, str], list[list[dict[str, Any]]]] = defaultdict(list)
    for (stratum, _), members in clusters.items():
        strata[stratum].append(members)
    estimates = []
    for _ in range(draws if rejected else 0):
        sample = [m for groups in strata.values() for g in (rng.choice(groups) for _ in groups) for m in g]
        total = sum(m["weight"] for m in sample)
        estimates.append(sum(m["weight"] * m["human_valid"] for m in sample) / total)
    estimates.sort()
    boot_upper = estimates[int(0.95 * (len(estimates) - 1))] if estimates else None
    exact_up = exact_upper(k, n)
    controls = [v for v in scored.values() if v["p0_accepted"]]

    def by(field: str) -> dict[str, Any]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for v in rejected:
            groups[str(v[field])].append(v)
        return {g: {"k": sum(x["human_valid"] for x in vs), "n": len(vs), "exact_95": exact_interval(sum(x["human_valid"] for x in vs), len(vs))}
                for g, vs in sorted(groups.items())}

    return {
        "rejected_audited": n,
        "human_valid": k,
        "unweighted": k / n if n else None,
        "unweighted_exact_95": exact_interval(k, n),
        "unweighted_one_sided_upper": exact_up,
        "weighted": weighted,
        "weighted_cluster_bootstrap_one_sided_upper": boot_upper,
        "decision_upper": max(x for x in (exact_up, boot_upper) if x is not None) if n else None,
        "by_cohort": by("cohort"),
        "by_p0_reason": by("p0_reason"),
        "by_run_failed": by("run_p0_failed"),
        "accepted_controls": {"n": len(controls), "human_valid": sum(v["human_valid"] for v in controls)},
    }


def census_reclassification(scored: dict[str, dict[str, Any]], p0_classes: dict[str, str]) -> dict[str, Any]:
    gen_runs = sorted(r for r, c in p0_classes.items() if c == "generation_failure")
    hits = sorted({v["run_id"] for v in scored.values() if v["stratum"] == "census" and v["human_valid"]} & set(gen_runs))
    return {"p0_generation_failures": len(gen_runs), "reclassified_runs": hits, "reclassified": len(hits),
            "generation_failures_after_census": len(gen_runs) - len(hits)}


def decide(census: dict[str, Any], mig: dict[str, Any], q_fn: dict[str, Any]) -> dict[str, Any]:
    parser_moves = {p: len(mig[p]["reclassified_from_generation"]) for p in ("P1", "P2")}
    worst = max([census["reclassified"], *parser_moves.values()])
    upper = q_fn["decision_upper"]
    if worst <= 2 and upper is not None and upper <= 0.05:
        tier = "tier_A_robust"
    elif worst <= 9:
        tier = "tier_B_qualified"
    else:
        tier = "tier_C_weakened"
    pooled = upper or 0.0
    flagged = sorted(c for c, v in q_fn["by_cohort"].items()
                     if v["n"] and pooled and exact_upper(v["k"], v["n"]) > 2 * pooled)
    return {"tier": tier, "max_reclassified_runs": worst, "census_reclassified": census["reclassified"],
            "parser_reclassified": parser_moves, "q_fn_decision_upper": upper, "provider_flags": flagged}


# ---------------------------------------------------------- selector replay
def _expected_choice(cands: list[dict[str, Any]], score: Callable[[dict[str, Any]], float | None], value: Callable[[dict[str, Any]], float]) -> float | None:
    """Expected value of the argmax of score, uniform over ties; None if no score."""

    scored = [(score(c), c) for c in cands]
    if not scored or any(s is None for s, _ in scored):
        return None
    best = max(s for s, _ in scored)
    tied = [c for s, c in scored if s == best]
    return sum(value(c) for c in tied) / len(tied)


ENDPOINTS = ("executable_validity", "reference_exactness")


def selector_values(cands: list[dict[str, Any]], parser: str = "P0",
                    endpoint: str = "executable_validity") -> dict[str, float | None]:
    """Expected endpoint value of each selector's choice; B6 picks a valid (then reference-exact) candidate."""

    if endpoint == "executable_validity":
        valid = lambda c: float(c["parses"][parser]["valid"])  # noqa: E731
    else:
        valid = lambda c: float(c["parses"][parser]["valid"] and c["parses"][parser]["reference_exact"])  # noqa: E731
    composite = lambda c: (0.85 * min(1.0, c["length"] / 800) + 0.15 * float(c["env_success"])  # noqa: E731
                           if c.get("env_success") is not None else None)
    return {
        "B1_random": sum(valid(c) for c in cands) / len(cands) if cands else None,
        "B0_recorded": _expected_choice(cands, lambda c: c.get("recorded_score"), valid),
        "B2_length_only": _expected_choice(cands, lambda c: float(c["length"]), valid),
        "B3_success_only": _expected_choice(cands, lambda c: None if c.get("env_success") is None else float(c["env_success"]), valid),
        "B4_composite": _expected_choice(cands, composite, valid),
        "B5_judge": _expected_choice(cands, lambda c: c.get("judge_score"), valid),
        "B6_oracle": float(any(valid(c) for c in cands)) if cands else None,
    }


def replay_pools(rows: list[dict[str, Any]], *, parser: str = "P0", pools: int = 5, round_only: bool = True,
                 slot_matched: int | None = None, endpoint: str = "executable_validity",
                 seed: int = 234, draws: int = 200) -> dict[str, Any]:
    """Replay every selector on the nested U2 pools C_1..C_pools with task-level summaries."""

    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row["universe"] == "U2" and (not round_only or not row.get("is_final")):
            by_task[row["task_id"]].append(row)
    rng = random.Random(seed)
    out: dict[str, Any] = {}
    for j in range(1, pools + 1):
        per_task: dict[str, dict[str, float | None]] = {}
        for task, cands in sorted(by_task.items()):
            pool = [c for c in cands if c["trajectory"] <= j]
            if slot_matched:
                samples = [selector_values(rng.sample(pool, min(slot_matched, len(pool))), parser, endpoint)
                           for _ in range(draws)]
                per_task[task] = {k: (None if any(s[k] is None for s in samples) else sum(s[k] for s in samples) / draws) for k in samples[0]}
            else:
                per_task[task] = selector_values(pool, parser, endpoint)
        summary = {}
        if not slot_matched:
            pools_now = {task: [c for c in cands if c["trajectory"] <= j] for task, cands in sorted(by_task.items())}
            replay_means = sorted(
                sum(selector_values([rng.choice(pool)], parser, endpoint)["B1_random"] for pool in pools_now.values())
                / len(pools_now)
                for _ in range(1000)
            )
        for name in next(iter(per_task.values())):
            vals = [v[name] for v in per_task.values()]
            if all(x is not None for x in vals):
                summary[name] = {"mean": sum(vals) / len(vals), "task_bootstrap_95": bootstrap_mean_ci(vals, seed=seed)}
        for base in ("B4_composite", "B1_random"):
            if base in summary:
                for name in summary:
                    if name != base:
                        diffs = [per_task[t][name] - per_task[t][base] for t in per_task]
                        summary[name][f"minus_{base}_95"] = bootstrap_mean_ci(diffs, seed=seed)
        if not slot_matched and "B1_random" in summary:
            summary["B1_random"]["seeded_replays_1000_95"] = [replay_means[24], replay_means[974]]
        out[f"C{j}"] = summary
    return out


# ------------------------------------------------------------ dual endpoints
def dual_endpoints(runs: list[dict[str, Any]], control_arm: str, treated_arm: str, *, seed: int = 234) -> dict[str, Any]:
    """Paired treated-minus-control contrasts under executable validity, reference exactness, and both."""

    ctrl = {r["task_id"]: r for r in runs if r["arm"] == control_arm}
    trt = {r["task_id"]: r for r in runs if r["arm"] == treated_arm}
    tasks = sorted(set(ctrl) & set(trt))
    out = {}
    for name, fn, eligible_only in (
        ("executable_validity", lambda r: r["exec_valid"], True),
        ("reference_exactness", lambda r: r["ref_exact"], False),
        ("both", lambda r: r["exec_valid"] and r["ref_exact"], False),
    ):
        use = [t for t in tasks if not eligible_only or (ctrl[t].get("semantic_eligible", True) and trt[t].get("semantic_eligible", True))]
        diffs = [int(bool(fn(trt[t]))) - int(bool(fn(ctrl[t]))) for t in use]
        a, b = sum(d == 1 for d in diffs), sum(d == -1 for d in diffs)
        out[name] = {"pairs": len(use), "difference": sum(diffs) / len(use) if use else None,
                     "bootstrap_95": bootstrap_mean_ci(diffs, seed=seed), "discordant": [a, b], "exact_mcnemar_p": mcnemar_exact_p(a, b)}
    return out
