Title: Pelican
Date: 2012-12-06 00:57
Tags: blog, pelican
Category: IT
Slug: install-pelican
Author: Swasher

Лог установки блога на Pelican
------------------------------

Installing Pelican
==================

    ::console
    $ sudo -s #установку делаем от рута
    $ apt-get update && apt-get upgrade
    $ apt-get install python-pip #если pip еще не установлен
    $ pip install pelican

Вытянуло:

- feedgenerator (to generate the Atom feeds),
- jinja2 (for templating support),
- docutils (for supporting reStructuredText as an input format),
- pitz,
- pygments (for syntax highlighting),
- blinker,
- unidecode.

Доустанавливаем Маркдаун

    ::console
    $ pip install Markdown

Дополнительно можно установить

- Typogrify (for typographical enhancements)

Для апгрейда используем команду

    ::console
    $ pip install --upgrade pelican

Создадим директорию для нашего блога

    ::console
    $ mkdir ~/blog/
    $ cd ~/blog

Теперь мы можем запустить команду Пеликан quickstart, которая задаст несколько вопросов
о настройках сайта:

    ::console
    $ pelican-quickstart

Отвечаем на вопросы. Эти ответы влияют на содержание файлов настройки (Makefile, pelicanconf.py, publishconf.py)
Впоследствии можно все откорректировать вручную.

Создаем пробный файл `test.md` в директории content. Файл должен иметь стандартную шапку. Вот шаблон:

    ::txt
    Date: 2010-12-03
    Title: My super title
    Tags: thats, awesome
    Slug: my-super-post

    This is the content of my super blog post.

Для создания HTML-контента можно запускать непосредственно pelican с ключами,
указывающими, что откуда брать, как обрабатывать и куда складывать. Для
упрощения этого процесса можно использовать Makefile. Например, команда

    ::console
    $ make html

перегенерирует контент в статик-html. Смотрим в blog/output, там будет лежать готовый 'сайт' нашего блога.

Когда я активно редактирую статью, мне удобно, чтобы сайт обновлялся автоматически при внесении правок.
Для этого я запускаю devserver:

    ::console
    $ make devserver
    $ ./develop_server.sh stop

Вторая команда, соответственно, для остановки девелоп-сервера.

Тут я намеренно не описываю инсталяцию Пеликана в защищенное виртуальное окружение (virtualenv), потому что
имхо на рабочем сервере в ней нет надобности. Она, скорее, для разработки, когда нужно, чтобы крутилось много 
проектов, зачастую с разными версиями пакетов.

Настройка lighttpd
==================

Добавляем виртуальный хост, на примере сервера Lighttpd. Прописываем в lighttpd.conf:

    ::lighttpd
    $HTTP["host"] =~ "blog.swasher.pp.ua" {
        server.document-root = "/home/swasher/blog/output/"
    }

Рестарт

    ::console    
    $ service lighttpd force-reload

Проверяем, заходим в браузер на наш сайт `blog.swasher.pp.ua`. Тут нужно проверить правильность 
настройки DNS у нашего регистратора домена, и локально, чтобы этот домен виделся из 
локальной сети. Обычно это настраивается в роутере.

Настройка Samba
===============

Для измения файлов по сетки, настроим самбу. Для начала настроим права доступа.

    ::console
    $ chown swasher:swasher -R blog/content/

В конфиг самбы добавим:

    ::samba
    [pelican] comment = Pelican
    path = /home/swasher/blog/content
    browseable = yes
    read only = no
    guest ok = yes
    create mask = 0644
    force user = swasher

Как установить новую тему
=========================

    ::console
    $ cd /usr/local/lib/python2.7/dist-packages/pelican/themes/
    $ git clone https://github.com/thulio/pelican-subtle-theme

Для примения новой темы добавляем в Makefile такую строку (без кавычек):

    ::ini
    PELICANOPTS=-t /usr/local/lib/python2.7/dist-packages/pelican/themes/pelican-subtle-theme/

Или же используем встроенную утилиту [pelican-themes]. Например, если у нас есть кастомизированная тема, можно сделать сим-линк на нее:

    ::console
    $ pelican-themes -s /home/swasher/blog/themes/subtle/

Все должно уже работать
============

Все, наш блог виден, загружается и работает. В продолжении будет написано, 
как я настраивал дизайн, шрифты, хранение и вставку картинок, Markdown-редактор, перенос статей с 
Вордпресс, настройку комментариев etc.


Ссылки
======
1. Пеликан
2. Маркдаун

[pelican-themes]: http://pelican.readthedocs.org/en/2.7.2/pelican-themes.html