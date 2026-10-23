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


def make_results_table(summary_path, out=None):
    """Таблица текущих результатов для слайда: TeX-фрагмент, числа берутся из сводки."""
    s = json.loads(Path(summary_path).read_text())
    out = Path(out or REPO / "slides" / "figs" / "oslide_results.tex")
    r1, r2 = s["runs"]["run1"]["patients"], s["runs"]["run2"]["patients"]
    f = lambda v: fmt(v).replace(",", "{,}")
    row = lambda name, a, b: f"{name} & {f(a)} & {f(b)} \\\\"
    lines = [
        "% сгенерировано code/oslide/plot.py из results/summary.json — не править вручную",
        "\\begin{tabular}{@{}l@{\\hspace{4pt}}c@{\\hspace{6pt}}c@{}}",
        "& P1 & P2 \\\\ \\hline",
        "\\multicolumn{3}{@{}l}{\\textit{Этап 1: корреляция $r$}} \\\\",
        row("\\quad статья", r2["P1"]["stage1"]["paper"], r2["P2"]["stage1"]["paper"]),
        row("\\quad воспроизведение", r2["P1"]["stage1"]["value"], r2["P2"]["stage1"]["value"]),
        "\\multicolumn{3}{@{}l}{\\textit{Этап 2: accuracy, 27 классов}} \\\\",
        row("\\quad статья", r2["P1"]["stage2"]["paper"], r2["P2"]["stage2"]["paper"]),
        row("\\quad код группы (видит будущее)", r1["P1"]["stage2"]["value"], r1["P2"]["stage2"]["value"]),
        row("\\quad \\textbf{причинно~--- база для TCN}", r2["P1"]["stage2"]["value"], r2["P2"]["stage2"]["value"]),
        "\\end{tabular}",
    ]
    out.write_text("\n".join(lines) + "\n")
    print("таблица:", out)


def make_tcn_diagram(out=None, levels=4, kernel=2, width=16, dx=0.2, dy=0.36):
    """Рецептивное поле причинной TCN: выход в момент t зависит только от прошлого.

    Слой l (1..levels) — свёртка с ядром kernel и расширением d = 2**(l-1).
    Генерирует TikZ-фрагмент; активные узлы — те, от которых зависит выход в t.
    """
    out = Path(out or REPO / "slides" / "figs" / "tcn_rf.tex")
    T = width - 1
    active = {levels: {T}}
    for l in range(levels, 0, -1):
        d = 2 ** (l - 1)
        active[l - 1] = {tau - j * d for tau in active[l] for j in range(kernel) if tau - j * d >= 0}
    rf = 1 + (kernel - 1) * sum(2 ** (l - 1) for l in range(1, levels + 1))
    L = ["% сгенерировано code/oslide/plot.py (make_tcn_diagram) — не править вручную",
         "\\begin{tikzpicture}[font=\\tiny]"]
    for l in range(1, levels + 1):
        d = 2 ** (l - 1)
        for tau in active[l]:
            for j in range(kernel):
                c = tau - j * d
                if c >= 0:
                    L.append(f"\\draw[runB!80!black, line width=0.5pt] ({tau*dx:.2f},{l*dy:.2f}) -- ({c*dx:.2f},{(l-1)*dy:.2f});")
    for l in range(levels + 1):
        for tau in range(width):
            on = tau in active[l]
            style = "fill=runB, draw=runB!70!black" if on else "fill=white, draw=gray!60"
            L.append(f"\\fill[{style}] ({tau*dx:.2f},{l*dy:.2f}) circle (1.1pt);")
        name = "вход $e_m$" if l == 0 else f"$d={2**(l-1)}$"
        L.append(f"\\node[anchor=east, gray!70!black] at (-0.12,{l*dy:.2f}) {{{name}}};")
    L.append(f"\\node[anchor=west] at ({T*dx+0.12:.2f},{levels*dy:.2f}) {{выход в $t$}};")
    L.append(f"\\draw[-stealth, gray] (0,-0.22) -- ({T*dx+0.3:.2f},-0.22) node[right] {{время}};")
    L.append(f"\\node[anchor=north] at ({T*dx/2:.2f},-0.26) {{рецептивное поле {rf} отсчётов, только прошлое}};")
    L.append("\\end{tikzpicture}")
    out.write_text("\n".join(L) + "\n")
    print("схема TCN:", out, f"(рецептивное поле {rf})")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--summary", default=str(HERE / "results" / "summary.json"))
    ap.add_argument("--out", default=None, help="путь без расширения")
    a = ap.parse_args()
    make_figure(a.summary, a.out)
    make_results_table(a.summary)
    make_tcn_diagram()
