Title: Скрипты для создания NFO-файлов YAMJ
Date: 2011-10-19 10:10
Category: Popcorn
Tags: yamj
Author: Swasher


Довольно часто мне приходится делать NFO для фильмов, которые YAMJ не
определил самостоятельно. Скелет NFO всегда один и тот же:

    :::xml
    <movie>
    <thumb></thumb>
    <id moviedb=kinopoisk></id>
    </movie>

в него подставляется id с кинопоиска и линк на постер. А вот название
NFO-шки может быть разное - это либо название папки с фильмом, либо
название самого файла. Решив как-то автоматизировать этот процесс,
написал два скрипта, которые генерят файл с нужным названием,
соответственно, либо для папки, либо для файла. Так как фильмы у меня
хранятся на линуксовом сервере, соответственно скрипты под линукс.
Скрипты нужно поместить в какую-нибудь папку, которая прописана в путях
(переменная окружение $PATH), например /bin. Пользоваться ими нужно так
- чтобы сделать nfo для папки, заходим в нужную папку и пишем в
командной строке: `nfodir` Все, создан nfo с нужным названием и шаблоном
внутри. Чтобы создать nfo для файла, пишем так: `nfofile <имя файла>`.

Я сделал еще удобнее - использовал user menu в midnight commander,
вызывается по кнопке F2. Для этого в файле mc.menu нужно дописать
следующее:

    + ! t t
    f     MAKE NFO
          echo %p
          nffile.sh %p


Символ `f`   во второй строке - это горячая клавиша. Файл этот может
располагаться в разных местах, в зависимости от дистрибутива. У меня в
Ubuntu он лежит в `/etc/mc`, а может быть в домашней директории или в
`/usr/share/mc`. Вот сами скрипты:

**nfodir** Скрипт для папки.

    ::bash
    #!/bin/bash

    fullfoldername=`pwd`
    foldername=$(basename "$fullfoldername")
    nfoname="$foldername".nf

    touch "$nfoname"

    echo "<movie>" > "$nfoname"
    echo "<thumb></thumb>" >> "$nfoname"
    echo "<id moviedb=\"kinopoisk\"></id>" >> "$nfoname"
    echo "</movie>" >> "$nfoname"

**nfofile** Скрипт для файла

    ::bash
    #!/bin/bash

    if [ $# -eq 0 ]; then
        echo "Filename missing"; exit 0
    fi

    filename=$(basename "$1")
    extension="${filename##*.}"
    filename="${filename%.*}"

    nfoname="$filename".nf
    touch "$nfoname"

    echo "<movie>" > "$nfoname"
    echo "<thumb></thumb>" >> "$nfoname"
    echo "<id moviedb=\"kinopoisk\"></id>" >> "$nfoname"
    echo "</movie>" >> "$nfoname"




Скрипты просты и понятны, думаю их не составит труда подогнать под свой конфиг.