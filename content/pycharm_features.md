Title: Pycharm: настройка и ньюансы работы
Date: 2014-07-06 21:00
Category: IT
Tags: pycharm
Author: Swasher

### Полезные шоткаты

- `Shift-F6` - переименовать имя переменной или функции 
- `Alt-Click and drag` - выделение вертикального блока (потом можно нажать Home и ввести текст)
- `Ctrl-W` - выделения логической еденицы текста (можно несколько раз подряд) 
- `Ctrl-Shift-V` - вставка из истории буфера
- `Ctrl-Shift-U` - перевод в верхний регистр

### Игнорирование нарушений PEP8

Pycharm умеет отображать нарушения стилистики кода согласно PEP. Это отключается так в настройках Inspections
ищем язык Python, в выпадаеющем меню - PEP8 coding style violation. Дальше идем на страницу [PEP8’s documentation][], 
и ищем код ошибки. Жмем плюсик, и вставляем код:

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457788278/pycharm/1.png 500 %}


### Сохранение файлов с unix-like окончанием строк

Действует только для файлов, созданных после установки этой опции

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457788278/pycharm/2.png 500 %}

### Заключение выделенного текста в качвычки

Очень удобно заключать выделенный текст в кавычки или скобки нажатием одной кнопки. Работает для 
любых скобок или кавычек. Для этого включаем следующую опцию

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457788278/pycharm/3.png 500 %}

### Создание темплейтов для новых файлов

Я использую темплейт для новых записей в блоге. Темплейты могут содержать переменные. Подробнее в [документации
Pycharm][]

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457788278/pycharm/4.png 500 %}

### Подсветка синтаксиса Ruby

Для базовой подсветки синтаксиса Ruby можно воспользоваться плагином [TextMate bundles support](https://github.com/textmate/ruby.tmbundle). 
Сначала его нужно склонировать склонировать куда-нибудь в /user/documents, и затем подключить
в Settings -> Editor -> TextMate Bundles

{% img image http://res.cloudinary.com/swasher/image/upload/c_scale,w_750/v1434196868/pycharm/ruby_syntax.png %}

Там же нужно установить желаемую цветовую схему для плагина.

### Установка правой границы

В питоне, согласно [PEP 0008](https://www.python.org/dev/peps/pep-0008/#maximum-line-length), максимальная длина
строки составляет 80 символов. Pycharm умеет делать автоматический перенос на новую строку при достижении этого
ограничения. Однако, это не всегда удобно и необходимо, и отключить эту фичу можно в настройках:

{% img image http://res.cloudinary.com/swasher/image/upload/c_crop,w_760/v1457613925/pycharm/pycharm_right_margin.png %}


  [PEP8’s documentation]: http://pep8.readthedocs.org/en/latest/intro.html
  [документации Pycharm]: http://www.jetbrains.com/pycharm/webhelp/creating-and-editing-file-templates.html