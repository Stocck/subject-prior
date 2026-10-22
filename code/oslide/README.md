# O-slide: этап 1 воспроизводится, этап 2 — нет

Рисунок к one-slide talk ([slides/oslide.pdf](../../slides/oslide.pdf)): два воспроизведения Petrosyan et al. (2022),
доля от результата статьи на этапе 1 (корреляция мел-спектрограммы) и этапе 2 (accuracy 27 классов).

```bash
pip install -r code/oslide/requirements.txt
python code/oslide/main.py --plot     # вычисления -> results/summary.json, затем рисунок -> slides/figs/oslide.{pdf,png}
python code/oslide/plot.py            # только перерисовать из готовой сводки
cd slides && pdflatex oslide.tex      # или xelatex
```

| Файл | Что |
|---|---|
| `main.py` | основной модуль: читает метрики прогонов, считает доли от статьи и погрешности, пишет `results/summary.json` |
| `plot.py` | только рисунок, читает `results/summary.json` |
| `data/repro_baseline_cv_summary_seed0.json` | прогон 1 «код группы»: агрегаты 6-fold CV (6/8 каналов, `filtfilt`), режим R2 — выбор чекпойнта по val |
| `data/repro_speech_decoding.json` | прогон 2 «по тексту статьи»: все каналы, причинный FIR, одно разбиение; числа перенесены из отчёта Comet `stocck/speech-decoding` вручную |

Погрешности: прогон 1 — SD по 6 фолдам (не доверительный интервал: обучающие выборки фолдов перекрываются);
прогон 2 — биномиальная SE по test (200 и 230 сегментов). Прогон 2 — вариант `res8-narrow, 50k` (меняется флагом `--run2-variant`).

**Чего здесь нет.** Сами обучения запускаются вне этого репозитория: прогон 1 — `exp_subject-prior/code/baseline_repro`
(`run_cv.py`, затем `summarize_cv.py`), прогон 2 — `speech_decoding` (`bash run_all.sh`). Клинические данные в репозиторий не кладутся.
Акустическая утечка (microphone effect) не проверена.
