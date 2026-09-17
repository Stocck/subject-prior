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
        <td> Сергей Исаевич Гуров, PhD/DSc </td>
    </tr>
    <tr>
        <td align="left"> <b> Advisor </b> </td>
        <td> Name Surname, PhD/DSc </td>
    </tr>
</table>

## Assets

- [LinkReview](LINKREVIEW.md)
- [Code](code)
- [Paper](paper/main.pdf)
- [Slides](slides/main.pdf)

## Abstract

Интерфейсы мозг-компьютер платят за межсубъектную вариативность калибровкой: новый пользователь сначала обязан дать размеченные данные, и только потом декодер начинает работать, инчае сильно просидает качетсво модели для нового пользователя. Репозиторий проверяет, можно ли снизить эту цену, если описать пользователя явно. Вместо отдельной модели на каждого человека или полного игнорирования того, кто перед нами, индивидуальность вводится как латентная переменная с популяционным априорным распределением и выводится из короткой немеченой записи — так один общий энкодер настраивается на нового человека без разметки.

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