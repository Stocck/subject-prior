"""O-slide: основной запускаемый модуль (вычисления).

Сводит итоговые метрики двух воспроизведений Petrosyan2022 к общей шкале
«доля от результата статьи» по двум этапам:
  этап 1 — корреляция предсказанной и настоящей мел-спектрограммы на test;
  этап 2 — accuracy классификации 26 слов + тишина (27 классов) на test.

Прогон 1 «код группы»   — data/repro_baseline_cv_summary_seed0.json
                           (агрегаты exp_subject-prior/code/baseline_repro, 6-fold CV, режим R2).
Прогон 2 «текст статьи» — data/repro_speech_decoding.json
                           (числа отчёта speech_decoding / Comet stocck/speech-decoding).

    python code/oslide/main.py            # сводка -> code/oslide/results/summary.json
    python code/oslide/main.py --plot     # то же + рисунок (код рисунка — plot.py)

Обучения здесь не запускаются: модуль работает с сохранёнными метриками прогонов.
"""
import argparse
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"


def run1_group_code(path: Path) -> dict:
    """6-fold CV: среднее ± SD по фолдам, честный выбор чекпойнта по val (R2)."""
    d = json.loads(path.read_text())
    out = {}
    for pid, p in d["patients"].items():
        a = p["agg"]
        out[pid] = {
            "stage1": {"value": a["corr_r2_test"]["mean"], "err": a["corr_r2_test"]["sd"],
                       "paper": p["paper"]["corr"]},
            "stage2": {"value": a["acc_r2_test"]["mean"], "err": a["acc_r2_test"]["sd"],
                       "paper": p["paper"]["acc"]},
        }
    return out


def run2_paper_text(path: Path, variant: str) -> dict:
    """Одно разбиение: точечная оценка, для accuracy — биномиальная SE по test."""
    d = json.loads(path.read_text())
    out = {}
    for pid, p in d["patients"].items():
        acc, n = p["stage2_acc_test"][variant], p["n_test_stage2"]
        out[pid] = {
            "stage1": {"value": p["stage1_r_test"], "err": None,
                       "paper": d["paper"][pid]["stage1_r"]},
            "stage2": {"value": acc, "err": math.sqrt(acc * (1 - acc) / n),
                       "paper": d["paper"][pid]["stage2_acc"]},
        }
    return out


def add_shares(runs: dict) -> dict:
    for run in runs.values():
        for p in run["patients"].values():
            for st in p.values():
                st["share"] = st["value"] / st["paper"]
                st["share_err"] = None if st["err"] is None else st["err"] / st["paper"]
    return runs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(HERE / "results" / "summary.json"))
    ap.add_argument("--run2-variant", default="res8-narrow, 50k",
                    help="вариант классификатора прогона 2 (базовый по выводам отчёта)")
    ap.add_argument("--plot", action="store_true")
    args = ap.parse_args()

    runs = add_shares({
        "run1": {"label": "Прогон 1: код группы",
                 "detail": "6/8 каналов, фильтр с нулевой фазой (filtfilt), классификатор по мел, 6-fold CV",
                 "err_kind": "± SD по 6 фолдам",
                 "patients": run1_group_code(DATA / "repro_baseline_cv_summary_seed0.json")},
        "run2": {"label": "Прогон 2: по тексту статьи",
                 "detail": "30/42 канала, причинный FIR 5–150 Гц, ResNet по признакам LSTM, одно разбиение",
                 "err_kind": "± биномиальная SE",
                 "variant": args.run2_variant,
                 "patients": run2_paper_text(DATA / "repro_speech_decoding.json", args.run2_variant)},
    })
    summary = {"chance_stage2": 1 / 27, "runs": runs}

    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(json.dumps(summary, ensure_ascii=False, indent=1))
    for key, run in runs.items():
        for pid, p in run["patients"].items():
            print(f"{key} {pid}: этап 1 r={p['stage1']['value']:.3f} ({p['stage1']['share']:.0%} статьи), "
                  f"этап 2 acc={p['stage2']['value']:.3f} ({p['stage2']['share']:.0%} статьи)")
    print("сводка:", args.out)

    if args.plot:
        from plot import make_figure, make_results_table, make_tcn_diagram  # рисование отделено от вычислений
        make_figure(args.out)
        make_results_table(args.out)
        make_tcn_diagram()


if __name__ == "__main__":
    main()
