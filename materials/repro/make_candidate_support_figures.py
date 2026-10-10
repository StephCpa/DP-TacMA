"""Draw the protocol-234 figures and cost table from analysis 235.

Usage: ``python make_candidate_support_figures.py <analysis-235.json> <output-dir>``.
Reads only the analysis JSON (no candidate text) and writes:

  candidate-support-funnel.{pdf,png}     A: slots -> accepted -> executor-valid -> reference-exact
  run-reclassification.{pdf,png}         B: where the P0-failed runs land under P0, P1, P2, human census
  selector-vs-support.{pdf,png}          C: selector replay over C1..C5 (round-only pool, P0)
  selector-cost-table.{tex,md}           selector means at C1 and C5, paired contrasts, pool costs
"""

from __future__ import annotations

import json
from pathlib import Path
import sys
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

plt.rcParams.update({
    "pdf.fonttype": 42, "ps.fonttype": 42, "font.family": "DejaVu Sans", "font.size": 8,
    "axes.titlesize": 8.5, "axes.labelsize": 8, "xtick.labelsize": 7.5, "ytick.labelsize": 7.5,
    "legend.fontsize": 6.5, "axes.spines.top": False, "axes.spines.right": False,
    "axes.edgecolor": "#52514e", "axes.linewidth": 0.8, "xtick.color": "#52514e", "ytick.color": "#52514e",
    "axes.grid": True, "axes.grid.axis": "y", "grid.color": "#e4e3df", "grid.linewidth": 0.6,
    "savefig.dpi": 300, "savefig.bbox": "tight", "savefig.pad_inches": 0.02,
})
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, REF = "#0b0b0b", "#52514e", "#8a8984"
PARSER_COLORS = {"P0": INK, "P1": BLUE, "P2": ORANGE}
PARSER_STYLES = {"P0": ("o", "-"), "P1": ("s", "--"), "P2": ("^", ":")}  # P1 and P2 often coincide
SELECTORS = {
    "B6_oracle": ("oracle (offline)", INK, "-"),
    "B4_composite": ("0.85/0.15 composite", BLUE, "-"),
    "B0_recorded": ("recorded score", BLUE, ":"),
    "B2_length_only": ("length only", ORANGE, "-"),
    "B3_success_only": ("success only", MUTED, "--"),
    "B5_judge": ("judge", REF, "-."),
    "B1_random": ("random", AQUA, "-"),
}


def save(fig, out: Path, stem: str) -> None:
    fig.savefig(out / f"{stem}.pdf", metadata={"CreationDate": None})
    fig.savefig(out / f"{stem}.png", metadata={"Software": None})
    plt.close(fig)


def funnel_figure(analysis: dict[str, Any], out: Path) -> None:
    u1 = analysis["funnel"]["U1"]
    pools = analysis["funnel"]["U2_nested_pools_round_only"]
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.3), gridspec_kw={"wspace": 0.45, "width_ratios": [1.3, 1]})
    ax = axes[0]
    stages = ["accepted", "executor_valid", "reference_exact"]
    labels = ["parser-accepted", "executor-valid", "reference-exact"]
    width = 0.26
    ax.bar([-1], [u1["recorded_slots"]], width=0.5, color=REF)
    ax.bar([0], [u1["with_text"]], width=0.5, color=MUTED)
    for k, parser in enumerate(("P0", "P1", "P2")):
        xs = [i + 1 + (k - 1) * width for i in range(len(stages))]
        ax.bar(xs, [u1[parser][s] for s in stages], width=width, color=PARSER_COLORS[parser], label=parser)
    ax.set_xticks(range(-1, len(stages) + 1), ["recorded", "with text", *labels], rotation=20, ha="right")
    ax.set_ylabel("Candidate slots (headroom cohorts)")
    ax.set_title("(a) Slot funnel", loc="left")
    ax.legend(frameon=False, loc="upper right")
    ax = axes[1]
    keys = sorted(pools, key=lambda k: int(k[1:]))
    for parser in ("P0", "P1", "P2"):
        marker, style = PARSER_STYLES[parser]
        ax.plot(range(1, len(keys) + 1), [pools[k][parser]["executor_valid"] for k in keys], marker=marker, ms=3.5,
                lw=1.6, ls=style, color=PARSER_COLORS[parser], label=parser)
    ax.set_xticks(range(1, len(keys) + 1), [f"$C_{k[1:]}$" for k in keys])
    ax.set_ylabel("Executor-valid round slots")
    ax.set_title("(b) Nested pools", loc="left")
    ax.legend(frameon=False, loc="upper left")
    save(fig, out, "candidate-support-funnel")


def reclassification_figure(analysis: dict[str, Any], out: Path) -> None:
    mig = analysis["parser_migration"]
    census = analysis["census_reclassification"]
    failed = mig["p0_failed_runs"]
    rows = {p: (mig[p]["generation_failure"], 0, mig[p]["selection_failure"], mig[p]["success"]) for p in ("P0", "P1", "P2")}
    p0_selection = failed - mig["p0_generation_failures"]
    rows["human census"] = (census["generation_failures_after_census"], census["reclassified"], p0_selection, 0)
    names = ["generation failure", "valid candidate found by audit", "selection failure", "valid final"]
    colors = [INK, ORANGE, BLUE, AQUA]
    fig, ax = plt.subplots(figsize=(4.6, 1.9))
    labels = list(rows)
    for y, label in enumerate(labels):
        left = 0
        for value, color in zip(rows[label], colors):
            if value:
                ax.barh(y, value, left=left, color=color, height=0.6)
                ax.text(left + value / 2, y, str(value), color="white", ha="center", va="center", fontsize=6.5)
            left += value
    for name, color in zip(names, colors):
        ax.barh([0], [0], color=color, label=name)
    ax.set_yticks(range(len(labels)), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, failed)
    ax.set_xlabel(f"P0-failed eligible runs (n = {failed})")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.45, -0.32), ncol=2, frameon=False)
    save(fig, out, "run-reclassification")


def selector_figure(analysis: dict[str, Any], out: Path) -> None:
    replay = analysis["selector_replay"]["P0"]
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 2.4), gridspec_kw={"wspace": 0.3}, sharey=True)
    for ax, endpoint, title in zip(axes, ("executable_validity", "reference_exactness"),
                                   ("(a) Executable validity", "(b) Reference exactness")):
        pools = replay[endpoint]["round_only"]
        keys = sorted(pools, key=lambda k: int(k[1:]))
        xs = range(1, len(keys) + 1)
        for name, (label, color, style) in SELECTORS.items():
            if all(name in pools[k] for k in keys):
                ax.plot(xs, [pools[k][name]["mean"] for k in keys], color=color, ls=style, lw=1.6, marker="o", ms=3,
                        label=label)
        matched = replay[endpoint]["slot_matched_16"]
        if all("B6_oracle" in matched[k] for k in keys):
            ax.plot(xs, [matched[k]["B6_oracle"]["mean"] for k in keys], color=INK, ls=(0, (1, 2)), lw=1.2,
                    label="oracle, 16 slots")
        ax.set_xticks(list(xs), [f"$C_{k[1:]}$" for k in keys])
        ax.set_ylim(0, 1.02)
        ax.set_title(title, loc="left")
    axes[0].set_ylabel("Task-level rate (round-only pool)")
    axes[1].legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    save(fig, out, "selector-vs-support")


def cost_table(analysis: dict[str, Any], out: Path) -> None:
    pools = analysis["selector_replay"]["P0"]["executable_validity"]["round_only"]
    last = f"C{max(int(k[1:]) for k in pools)}"
    costs = analysis.get("pool_costs") or {}

    def fmt(x: float | None) -> str:
        return "--" if x is None else f"{x:.3f}"

    def ci(v: list[float | None] | None) -> str:
        return "--" if not v or v[0] is None else f"[{v[0]:.2f}, {v[1]:.2f}]"

    rows = []
    for name, (label, _, _) in SELECTORS.items():
        if name not in pools["C1"] or name not in pools[last]:
            continue
        rows.append((label, fmt(pools["C1"][name]["mean"]), fmt(pools[last][name]["mean"]),
                     ci(pools[last][name].get("minus_B4_composite_95")), ci(pools[last][name].get("minus_B1_random_95"))))
    head = ("Selector", "C1", last, f"{last} minus composite", f"{last} minus random")
    tokens = "; ".join(f"{k}: {v.get('tokens'):,} tokens, {v.get('calls'):,} calls" for k, v in sorted(costs.items())
                      if v.get("tokens") is not None) or "pool costs not provided"
    md = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(r) + " |" for r in rows]
    (out / "selector-cost-table.md").write_text("\n".join(md) + f"\n\nRecorded generation cost: {tokens}.\n", encoding="utf-8")
    tex = ["\\begin{tabular}{lrrcc}", "\\toprule", " & ".join(head).replace("minus", "$-$") + " \\\\", "\\midrule"]
    tex += [" & ".join(r) + " \\\\" for r in rows]
    tex += ["\\bottomrule", "\\end{tabular}"]
    (out / "selector-cost-table.tex").write_text("\n".join(tex) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit(__doc__)
    analysis = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    out = Path(argv[1])
    out.mkdir(parents=True, exist_ok=True)
    funnel_figure(analysis, out)
    reclassification_figure(analysis, out)
    selector_figure(analysis, out)
    cost_table(analysis, out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
