"""Regenerate the two main-text figures from the values reported in the paper.

Every number below is copied from the frozen results quoted in main.tex and
appendix.tex (section noted beside each block); no model output is read and no
provider call is made. Run from this directory:

    python make_main_figures.py

Outputs: qwen-candidate-pool-enlargement.{pdf,png} and
evolution-audit-main-results.{pdf,png}.
"""

from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Fonts are embedded as TrueType (Type 42); ACL Pubcheck rejects Type 3 fonts.
plt.rcParams.update({
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "font.family": "DejaVu Sans",
    "font.size": 8,
    "axes.titlesize": 8.5,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#52514e",
    "axes.linewidth": 0.8,
    "xtick.color": "#52514e",
    "ytick.color": "#52514e",
    "axes.labelcolor": "#0b0b0b",
    "axes.titleweight": "regular",
    "axes.grid": True,
    "axes.grid.axis": "y",
    "grid.color": "#e4e3df",
    "grid.linewidth": 0.6,
    "savefig.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.02,
})

# Validated categorical slots (all-pairs CVD-safe); aqua is always direct-labelled.
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED, REF = "#0b0b0b", "#52514e", "#8a8984"


def save(fig, stem: str) -> None:
    # Omit timestamps so regenerating unchanged figures leaves the files unchanged.
    fig.savefig(f"{stem}.pdf", metadata={"CreationDate": None})
    fig.savefig(f"{stem}.png", metadata={"Software": None})
    plt.close(fig)


def candidate_pool_figure() -> None:
    # Section 3.3 and appendix "Prospective candidate-pool enlargement"; intervals
    # are task-cluster bootstraps from artifacts 088 and 231 (20 tasks).
    trajectories = [2, 3, 4, 5, 6]  # C_1..C_5: greedy anchor + j stochastic
    support = [1.85, 2.15, 2.35, 2.60, 2.85]
    oracle = [0.60, 0.70, 0.70, 0.80, 0.80]
    oracle_ci = [(0.40, 0.80), (0.50, 0.90), (0.50, 0.90), (0.60, 0.95), (0.60, 0.95)]
    plug_in = [0.660, 0.700, 0.722, 0.738, 0.751]  # fresh-draw expectation, n = 1..5
    plug_in_ci = [(0.470, 0.840), (0.512, 0.878), (0.546, 0.897), (0.559, 0.909), (0.567, 0.917)]
    baseline_final = 0.50  # temperature-zero final answer
    # Uniform choice among the j+1 trajectory final answers in C_j (artifact 237).
    random_final = [0.500, 0.517, 0.525, 0.550, 0.542]

    fig, axes = plt.subplots(1, 2, figsize=(5.4, 2.2), gridspec_kw={"wspace": 0.38})
    ticks = [f"$C_{j}$\n({t})" for j, t in enumerate(trajectories, start=1)]

    ax = axes[0]
    ax.plot(trajectories, support, color=BLUE, lw=2, marker="o", ms=4.5)
    for x, y in zip(trajectories, support):
        ax.annotate(f"{y:.2f}", (x, y), textcoords="offset points", xytext=(4, -10),
                    ha="left", fontsize=6.5, color=MUTED)
    ax.text(2.0, 3.0, "$C_5-C_1$: +1.00 [0.50, 1.60]", fontsize=6.5, color=INK, va="top")
    ax.set_xlim(1.6, 6.6)
    ax.set_ylim(1.5, 3.1)
    ax.set_xticks(trajectories, ticks)
    ax.set_xlabel("Nested pool (trajectories)")
    ax.set_ylabel("Unique canonical plans / task")
    ax.set_title("(a) Recorded canonical support", loc="left")

    ax = axes[1]
    ax.axhline(baseline_final, color=REF, lw=1, ls=":")
    ax.fill_between(trajectories, [lo for lo, _ in plug_in_ci], [hi for _, hi in plug_in_ci],
                    color=ORANGE, alpha=0.15, linewidth=0)
    ax.plot(trajectories, plug_in, color=ORANGE, lw=1.6, ls="--", marker="s", ms=3.5,
            label="fresh-draw extrapolation")
    for x, (lo, hi) in zip(trajectories, oracle_ci):
        ax.plot([x + 0.06, x + 0.06], [lo, hi], color=BLUE, lw=1.2)
    ax.plot([t + 0.06 for t in trajectories], oracle, color=BLUE, lw=2, marker="o", ms=4.5,
            label="realized offline oracle")
    ax.plot(trajectories, random_final, color=AQUA, lw=1.6, marker="^", ms=3.5)
    ax.text(4.56, 0.488, "random final", fontsize=6.5, color=AQUA, va="top", ha="center")
    ax.text(2.16, 0.375, "baseline final 0.50", fontsize=6.5, color=MUTED, va="bottom", ha="left")
    ax.legend(loc="upper left", frameon=False, handlelength=2.2, borderaxespad=0.2)
    ax.set_xlim(1.6, 6.4)
    ax.set_ylim(0.35, 1.15)
    ax.set_yticks([0.4, 0.6, 0.8, 1.0])
    ax.set_xticks(trajectories, ticks)
    ax.set_xlabel("Nested pool (trajectories)")
    ax.set_ylabel("Task-level executable rate")
    ax.set_title("(b) Offline executable oracle", loc="left")

    save(fig, "qwen-candidate-pool-enlargement")


def selector_calculation_figure() -> None:
    # Appendix: fixed-pool selector calculation over cached C_5 candidates (artifact 100).
    eps = [0.5, 1, 2, 4, 8]
    dp = [0.5119, 0.5748, 0.6822, 0.7793, 0.7996]
    fig, ax = plt.subplots(figsize=(3.2, 2.0))
    ax.axhline(0.80, color=MUTED, lw=1, ls="--")
    ax.axhline(0.50, color=REF, lw=1, ls=":")
    ax.plot(eps, dp, color=BLUE, lw=2, marker="o", ms=4.5)
    ax.set_xscale("log", base=2)
    ax.set_xticks(eps, [f"{e:g}\n({2 * e:g})" for e in eps])
    ax.minorticks_off()
    ax.set_xlim(0.4, 10)
    ax.text(0.45, 0.81, "non-private offline oracle 0.80", fontsize=6.5, color=MUTED, va="bottom")
    ax.text(9.5, 0.49, "baseline final 0.50", fontsize=6.5, color=MUTED, va="top", ha="right")
    for e, v in zip(eps[:-1], dp[:-1]):
        ax.annotate(f"{v:.3f}", (e, v), textcoords="offset points", xytext=(5, -4),
                    fontsize=6.5, color=MUTED, va="top")
    ax.set_ylim(0.45, 0.88)
    ax.set_xlabel(r"$\varepsilon$, monotone calibration (general calibration)")
    ax.set_ylabel("Expected executable selection")
    save(fig, "selector-calculation")


def audit_figure() -> None:
    fig, axes = plt.subplots(1, 3, figsize=(6.8, 2.2),
                             gridspec_kw={"wspace": 0.55, "width_ratios": [0.95, 1.45, 0.75]})

    # Section 3.1 / Table 2: 0/20 (initial audit) and 0/120 per arm (replication)
    # post-input exposure; whiskers are run-level one-sided 95% upper bounds.
    ax = axes[0]
    arms = ["Evolve", "Reset", "No\ncanary"]
    studies = [("initial, 20/arm", 20, MUTED, -0.17), ("replication, 120/arm", 120, BLUE, 0.17)]
    xs = list(range(len(arms)))
    ax.axhline(0.10, color=ORANGE, lw=1, ls="--")
    # The dashed line is the frozen 10% exposure gate; the caption names it.
    for label, n, color, dx in studies:
        upper = 1 - 0.05 ** (1 / n)
        for x in xs:
            ax.plot([x + dx, x + dx], [0, upper], color=color, lw=1.6, solid_capstyle="round")
            ax.plot([x + dx - 0.09, x + dx + 0.09], [upper, upper], color=color, lw=1.6)
            ax.plot(x + dx, 0, marker="o", color=color, ms=4.5, label=label if x == 0 else None)
        ax.text(2 + dx, upper + 0.004, f"{upper:.1%}", fontsize=6, color=INK, ha="center", va="bottom")
    ax.legend(loc="upper left", frameon=False, fontsize=6, handlelength=1.0, borderaxespad=0.1)
    ax.set_xticks(xs, arms)
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.006, 0.20)
    ax.set_yticks([0, 0.05, 0.10, 0.15])
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_ylabel("Post-input exposure (0 observed)")
    ax.set_title("(a) Canary exposure", loc="left")

    # Section 3.1 / Table 2: length-removed minus released reference exactness.
    # The DeepSeek initial bootstrap interval is degenerate ([0, 0]); the dashed
    # whisker is the exact bound |RD| <= 0.308 from 0/10 discordant pairs (artifact 231).
    ax = axes[1]
    labels = ["DeepSeek\ninitial", "DeepSeek\nnon-deg.", "Qwen\nnon-deg.", "Pooled\n(secondary)"]
    est = [0.000, 0.167, -0.050, 0.024]
    lo = [0.000, 0.000, -0.250, -0.095]
    hi = [0.000, 0.417, 0.150, 0.143]
    ax.axhline(0, color=MUTED, lw=0.8)
    ax.plot([0, 0], [-0.308, 0.308], color=BLUE, lw=1.0, ls=(0, (2, 1.5)))
    for i, (e, l, h) in enumerate(zip(est, lo, hi)):
        color = ORANGE if i == 3 else BLUE
        ax.plot([i, i], [l, h], color=color, lw=1.6, solid_capstyle="round")
        ax.plot(i, e, marker="D" if i == 3 else "o", color=color, ms=5)
        left = i == 3
        ax.annotate(f"{e:+.3f}", (i, e), textcoords="offset points", xytext=(-5 if left else 4, 6 if i == 0 else 0),
                    va="center", ha="right" if left else "left", fontsize=6.5, color=INK)
    ax.text(0.08, -0.29, "exact bound", fontsize=5.8, color=MUTED, va="bottom", ha="left")
    ax.set_xticks(range(4), labels, fontsize=6.3)
    ax.set_xlim(-0.4, 3.4)
    ax.set_ylim(-0.34, 0.47)
    ax.set_yticks([-0.2, 0, 0.2, 0.4])
    ax.set_ylabel("Reference-exact difference\n(length removed minus released)")
    ax.set_title("(b) Length-term removal", loc="left")

    # Appendix "Bootstrap handling" and artifact 231: agent-round observations
    # (15 per run, 60 X1 runs); counts, not a likelihood ratio.
    ax = axes[2]
    groups = ["All\nscores", "Scores\n\u2265 0.8"]
    shares = [75 / 900, 24 / 165]
    counts = ["75/900", "24/165"]
    bars = ax.bar(range(2), shares, width=0.6, color=[MUTED, BLUE], edgecolor="white", linewidth=1.5)
    for bar, s, c in zip(bars, shares, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, s + 0.004, c, ha="center",
                va="bottom", fontsize=6.3, color=INK)
    ax.set_xticks(range(2), groups)
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(0, 0.19)
    ax.set_yticks([0, 0.05, 0.10, 0.15])
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_ylabel("From successful runs")
    ax.set_title("(c) Score observations", loc="left")

    save(fig, "evolution-audit-main-results")


def failure_decomposition_figure() -> None:
    # Section 3.2 / Table 3: semantically eligible original/control runs.
    cohorts = ["DeepSeek X1 evolve", "DeepSeek non-degenerate", "DeepSeek text retention", "Qwen released score"]
    success = [2, 6, 0, 11]
    recoverable = [0, 1, 1, 1]  # failed final, executable candidate in pool
    generation = [11, 5, 19, 8]  # no executable candidate anywhere
    n = [s + r + g for s, r, g in zip(success, recoverable, generation)]

    fig, ax = plt.subplots(figsize=(3.3, 1.75))
    ax.set_axisbelow(True)
    ys = list(range(len(cohorts)))[::-1]
    parts = [
        ("final executable", success, BLUE),
        ("selection failure", recoverable, ORANGE),
        ("generation failure", generation, MUTED),
    ]
    left = [0.0] * len(cohorts)
    for label, counts, color in parts:
        shares = [c / total for c, total in zip(counts, n)]
        ax.barh(ys, shares, left=left, height=0.62, color=color, edgecolor="white", linewidth=1.2, label=label)
        for y, l, share, c in zip(ys, left, shares, counts):
            if c and share >= 0.12:
                ax.text(l + share / 2, y, str(c), ha="center", va="center", fontsize=6.5,
                        color="white")
        left = [l + share for l, share in zip(left, shares)]
    ax.set_yticks(ys, [f"{c} (n={k})" for c, k in zip(cohorts, n)], fontsize=6.5)
    ax.set_xlim(0, 1)
    ax.xaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Share of semantically eligible runs")
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.legend(loc="upper center", bbox_to_anchor=(0.35, -0.30), ncol=3, frameon=False,
              fontsize=6, handlelength=1.2, columnspacing=0.8)
    save(fig, "failure-decomposition")


if __name__ == "__main__":
    candidate_pool_figure()
    audit_figure()
    failure_decomposition_figure()
    selector_calculation_figure()
