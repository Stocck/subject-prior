"""O-slide: рисунок. Читает только results/summary.json, ничего не вычисляет.

    python code/oslide/plot.py            # -> slides/figs/oslide.pdf и .png
"""
import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
COLORS = {"run1": "#2a78d6", "run2": "#eb6834"}
INK, MUTED, GRID = "#1f1f1e", "#6b6a63", "#dddcd5"


def fmt(x: float) -> str:
    return f"{x:.2f}".replace(".", ",")


def make_figure(summary_path, out_stem=None):
    s = json.loads(Path(summary_path).read_text())
    out_stem = Path(out_stem or REPO / "slides" / "figs" / "oslide")
    out_stem.parent.mkdir(parents=True, exist_ok=True)

    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11.5,
                         "axes.edgecolor": MUTED, "axes.labelcolor": INK,
                         "xtick.color": INK, "ytick.color": MUTED})
    fig, ax = plt.subplots(figsize=(6.4, 3.55))

    stages = [("stage1", "Этап 1: мел-спектрограмма\nкорреляция r"),
              ("stage2", "Этап 2: 26 слов + тишина\naccuracy")]
    runs, pids = ["run1", "run2"], ["P1", "P2"]
    w, gap = 0.18, 0.05
    for gi, (st, title) in enumerate(stages):
        for ri, run in enumerate(runs):
            for pi, pid in enumerate(pids):
                x = gi * 1.25 + (ri * 2 + pi - 1.5) * (w + gap / 2) + (ri - 0.5) * gap
                d = s["runs"][run]["patients"][pid][st]
                ax.bar(x, d["share"], w, color=COLORS[run], zorder=3)
                if d["share_err"]:
                    ax.errorbar(x, d["share"], d["share_err"], color=INK, lw=1, capsize=3, zorder=4)
                top = d["share"] + (d["share_err"] or 0)
                ax.text(x, top + 0.025, fmt(d["value"]), ha="center", va="bottom", fontsize=10, color=INK)
                ax.text(x, -0.035, pid, ha="center", va="top", fontsize=9, color=MUTED)
        ax.text(gi * 1.25, -0.13, title, ha="center", va="top", fontsize=11, color=INK)

    ax.axhline(1.0, color=INK, lw=1.2, ls="--", zorder=2)
    ax.text(1.99, 1.0, "статья\n= 100 %", va="center", ha="left", fontsize=9.5, color=INK)

    ax.set_xlim(-0.6, 1.95)
    ax.set_ylim(0, 1.22)
    ax.set_xticks([])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticklabels(["0", "25 %", "50 %", "75 %", "100 %"])
    ax.set_ylabel("доля от результата статьи")
    ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)

    handles = [plt.Rectangle((0, 0), 1, 1, color=COLORS[r]) for r in runs]
    ax.legend(handles, [s["runs"][r]["label"] for r in runs], loc="upper right",
              bbox_to_anchor=(1.0, 1.13), ncol=2, frameon=False, fontsize=10, handlelength=1.2)
    fig.subplots_adjust(left=0.13, right=0.88, top=0.88, bottom=0.2)
    for ext in ("pdf", "png"):
        fig.savefig(out_stem.with_suffix("." + ext), dpi=220)
    plt.close(fig)
    print("рисунок:", out_stem.with_suffix(".pdf"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default=str(HERE / "results" / "summary.json"))
    ap.add_argument("--out", default=None, help="путь без расширения")
    a = ap.parse_args()
    make_figure(a.summary, a.out)
