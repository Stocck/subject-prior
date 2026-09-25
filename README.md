# Иерархическая байесовская модель индивидуальных различий для переносимых представлений нейросигнала.

<!-- Change `kisnikser/m1p-template` to `intsystems/your-repository`-->
[![License](https://badgen.net/github/license/kisnikser/m1p-template?color=green)](https://github.com/kisnikser/m1p-template/blob/main/LICENSE)
[![GitHub Contributors](https://img.shields.io/github/contributors/kisnikser/m1p-template)](https://github.com/kisnikser/m1p-template/graphs/contributors)
[![GitHub Issues](https://img.shields.io/github/issues-closed/kisnikser/m1p-template.svg?color=0088ff)](https://github.com/kisnikser/m1p-template/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr-closed/kisnikser/m1p-template.svg?color=7f29d6)](https://github.com/kisnikser/m1p-template/pulls)

<table>
    <tr>
        <td align="left"> <b> Author </b> </td>
        <td> Михаил Плигин </td>
    </tr>
    <tr>
        <td align="left"> <b> Consultant </b> </td>
        <td> Осадчий Алексей Евгеньевич, DSc </td>
    </tr>
    <tr>
        <td align="left"> <b> Advisor </b> </td>
        <td> Сергей Исаевич Гуров, PhD </td>
    </tr>
</table>

## Assets

- [LinkReview](LINKREVIEW.md)
- [Code](code)
- [Paper](paper/main.pdf)
- [Slides](slides/main.pdf)

## Abstract
    *Актуальность.* Декодеры речи на глубоких нейросетях выигрывают в точности ценой прозрачности: по их весам трудно проверить, опирается ли решение на нейронную активность, а не на мышечные и акустические артефакты, что критично для клинических интерфейсов мозг–компьютер.
    *Цель работы.* Предложить архитектуру для классификации слов по внутричерепной электроэнцефалографии, которая сохраняет интерпретируемый блок детектора огибающей из работы \cite{Petrosyan2022} и превосходит исходную модель по точности. 
    *Методы.* В работе рассматривается модель с обучаемыми пространственными и полосовыми фильтрами, выпрямлением и сглаживанием, веса которых переводятся в пространственные и частотные паттерны, — а двунаправленный блок долгой краткосрочной памяти заменён причинной временной свёрточной сетью с расширенными  свёртками. Модель обучалась по двухэтапной схеме исходной работы: регрессия лог-мел-спектрограммы речи, затем классификация 26 слов и тишины по промежуточным признакам. Сравнение с воспроизведённой исходной моделью и её вариантом без временного модуля проведено на данных двух пациентов, и открытых данных \cite{Verwoert2022}. 
    *Результаты.* Предложенная модель достигает точности $[X1] \%$ и $[X2] \%$ (для 1 и 2 пациента соответственно) против $[B1]\%$ и $[B2]\%$ у воспроизведённой исходной архитектуры при уровне случайного угадывания $3,7\%$. Пространственные и частотные паттерны блок детектора огибающей после замены временного модуля сохраняются и указывают на [область коры] и диапазон $[f_1,f_2]Hz$.
    *Значимость.* Интерпретируемость первых слоёв, не ограничивает точность: резерв качества компактного декодера речи лежит во временном модуле, и его замена повышает точность без потери возможности проверить нейронное происхождение признаков.

## Citation

If you find our work helpful, please cite us.
```BibTeX
@article{citekey,
    title={Title},
    author={Name Surname, Name Surname (consultant), Name Surname (advisor)},
    year={2025}
}
```

## Licence

Our project is MIT licensed. See [LICENSE](LICENSE) for details.