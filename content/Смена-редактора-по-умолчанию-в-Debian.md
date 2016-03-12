Title: Debian/Ubuntu: смена редактора по-умолчанию
Date: 2012-02-07 11:16
Category: IT
Tags: mc, ubuntu
Author: Swasher
Slug: ubuntu-change-default-editor

Debian и Ubuntu используют для visudo, crontab и других подобных задач тесктовый редактор, заданный в системе "по-умолчанию"
Для изменения этого редактора используем команду `update-alternatives`. Просто запускаем ее в окне терминала: 

    :::console
    $ sudo update-alternatives --config editor

В моей системе есть выбор из шести вариантов:

      Selection    Alternative
    -----------------------------------------------
              1    /bin/ed
              2    /bin/nano
              3    /usr/bin/vim.tiny
    *+        4    /usr/bin/vim.gnome
              5    /usr/bin/mcedit-debian
              6    /usr/bin/emacs21


Нажимаем `Enter`, чтобы оставить как есть, или нажимаем соответствующую цифру. Знак `+` указывает на системный редактор "по-умолчанию", а звездочка - на текущий выбранный редактор.
