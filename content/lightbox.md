Title: Как прикрутить lightbox к блогу на движке Pelican
Date: 2014-02-13 16:50
Tags: pelican
Category: IT
Author: Swasher


Движок pelican из коробки умеет вставлять изображения в верстку только нативного размера. По ширине они опрезаются соответственно ширине колонки.


### Cтавим плагин pelican-lightbox

Проверяем зависимости:

    ::console
    # pip install beautifulsoup4

Плагин находится тут [https://github.com/jprine/pelican-plugins/tree/master/lightbox][]

В `pelicanconf.py` смотрим следущие переменные:

    ::ini
    PLUGIN_PATH = '/home/swasher/blog/pelican-plugins'
    PLUGINS = ['lightbox', 'liquid_tags.img']
    
Первая указывает на директорию с плагинами, вторая перечисляет подключенные плагины. Скачиваем плагин в `$PLUGIN_PATH`,
добавляем `'lightbox'`в `$PLUGINS`

### Ставим плагин Liquid-style Tags

Этот плагин предназначен для того, чтобы мы могли использовать в markdown теги типа \{% %\}. 

Устанавливаем аналогично предыдущему. Плагин скачиваем в гитхаба [Liquid-style Tags][].


### Скачиваем Lightbox 

Скачиваем lightbox2.6.zip с [вебсайта][]. Распаковываем и копируем папки `css`, `img` и `js` в нашу тему в `static/lightbox`. Проверяем соответствие путей с шаблоном.

### Редактируем шаблон

Добавляем в файл `base.html` в секцию `head` загрузку скриптов. Может отличаться в других шаблонах, я использую модифицированную Subtle тему. 

    <!-- Lightbox2 support -->
    <script src="{{ SITEURL }}/theme/lightbox/js/jquery-1.10.2.min.js"></script>
    <script src="{{ SITEURL }}/theme/lightbox/js/lightbox-2.6.min.js"></script>
    <link href="{{ SITEURL }}/theme/lightbox/css/lightbox.css" rel="stylesheet" type="text/css" />


-------------

На этом установка завершена. Вставка картинок производится имеет следующий синтаксис:
    
    ::jinja2
    {% img  [class name(s)]  path/to/image  [width [height]] \
    [title text | "title text" ["alt text"]] %}

Class name для библиотеки lightbox2 - `lb-image`. Путь к картинкам указываем относительно директории content нашего блога.
Самый употребляемый способ такой:

    ::jinja2
    {% img lb-image \
    images/risunok.png 780 %}
    
где 780 - это ширина картинки в пикселях.
    
> Самый простой способ доставить картинки на сервер - это Dropbox. Ставим на сервере Dropbox, в его папке делаем хардлинк на нашу /images, и с рабочего
> компьютера закидываем туда наши пикчи. Также становится простым и удобным редактирование картинок.

Ну и напоследок - кортинка с эффектом lightbox!

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457945760/beer.jpg 780 Beer %}

  
  [https://github.com/jprine/pelican-plugins/tree/master/lightbox]: https://github.com/jprine/pelican-plugins/tree/master/lightbox
  [вебсайта]: http://lokeshdhakar.com/projects/lightbox2/releases/
  [Liquid-style Tags]: https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags