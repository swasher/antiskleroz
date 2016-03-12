Title: YAMJ на Linux-системе - установка и настройка
Date: 2010-11-24 14:35
Category: Popcorn
Tags: linux, popcorn, yamj
Author: Swasher

Конфигурация железа:
--------------------

Имеется домашняя сеть 192.168.0.0/24, в ней плеер PCH-A200, подключенный
по ethernet, винта нет. Сервер под Ubuntu x64, дисковый массив 3х2гб в
Raid0 под Btrfs. Контент льется через rtorrent под управлением
rutorrent. Раздаются фильмы по протоколу NFS. Так же настроена Самба для
доступа с виндовых машин, так как настроить NFS под виндой не удалось.

#### Описание путей:

**/home/swasher/yamj** - скрипты джукбокса **/mnt/raid/video** -
видеоконтент **/mnt/raid/yamj** - собственно, сам каталог с выводом
Yamj, сюда смотрит А200 чтобы увидеть "стенку".<!--more-->

Установка YAMJ
--------------

Используем сборку от Avalanche. Распаковывем ее в `/home/swasher/yamj`.
Устанавливаем Java (я ставил open, не сановскую):

    apt-get install openjdk-6-jre

Ubuntu Maverick 10.10: в оффициальном репозитории mediainfo нет, ставим
используя репозиторий:

   sudo add-apt-repository ppa:nilarimogard/webupd8
   sudo apt-get update
   sudo apt-get install mediainfo

Делаем исполняемым

    chmod 755 MovieJukebox.sh

Редактируем recommended settings for 1G of memory:

    java -Xms128m -Xmx512m -classpath .:./resources:./lib/* com.moviejukebox.MovieJukebox "$@"

recommended settings for 2G of memory:

    java -Xms128m -Xmx1024m -classpath .:./resources:./lib/* com.moviejukebox.MovieJukebox "$@"

recommended settings for 3G of memory:

    java -Xms128m -Xmx2049m -classpath .:./resources:./lib/* com.moviejukebox.MovieJukebox "$@"

Так же много где упоминается опция **-Djava.awt.headless=true**, которую
рекомендуют указывать при ошибках явы, другие используют ее по умолчанию:

    java -Djava.awt.headless=true -Xms128m -Xmx1024m -classpath .:./resources:./lib/* com.moviejukebox.MovieJukebox "$@"

У меня пока все работает без нее. Добавляем в `/home/swasher/yamj/properties/moviejukebox.properties` путь 
для mediainfo:

   mediainfo.home=/usr/bin/

и куда сохранять вывод джукбокса

   mjb.jukeboxRoot=/mnt/backup/testnas

library.xml приводим к следующему виду

    <libraries>
       <library>
           <!--(откуда брать файла - локальный путь, если лежат локально с джукбоксом)-->
           <path>/mnt/backup/testnas</path>
           <!--(сетевой путь - как эту шару с фильмами видит плеер)-->
           <playerpath>file:///opt/sybhttpd/localhost.drives/NETWORK_SHARE/test/</playerpath>
           <exclude name="sample,tmp/,temp/,RECYCLE.BIN/"/>
           <description>PROBA</description>
           <prebuf></prebuf>
           <scrapeLibrary>true</scrapeLibrary>
      </library>
    </libraries>

Запускаем

    sudo ./MovieJukebox.sh library.xml


Работа YAMJ с несколькими дисками.
----------------------------------

Настроим систему таким образом, чтобы на NMT имелось несколько сетевых
шар, в нашем примере Tvshow и Movies, и каждая из них имела свою стенку.
Поступим следующим образом - создадим несколько файлов library.xml для
каждой стенки, а запускать скрипт будем с параметром "-о" и указывать
путь сохранения файлов. Создадим xml файлы: **library\_video.xml**

    <libraries>
       <library>
        <path>/mnt/raid/video</path>
        <playerpath>file:///opt/sybhttpd/localhost.drives/NETWORK_SHARE/Movies</playerpath>
        <exclude name="sample,tmp/,temp/,RECYCLE.BIN/"/>
        <description>Swasher Movie </description>
        <prebuf></prebuf>
        <scrapeLibrary>true</scrapeLibrary>
       </library>
    </libraries>

**library\_tvshow.xml**

    <libraries>
        <library>
            <path>/mnt/raid/tvshow</path>
            <playerpath>file:///opt/sybhttpd/localhost.drives/NETWORK_SHARE/TVshow</playerpath>
            <exclude name="sample,tmp/,temp/,RECYCLE.BIN/"/>
            <description>Swasher TVshow</description>
            <prebuf></prebuf>
            <scrapeLibrary>true</scrapeLibrary>
        </library>
    </libraries>


Для удобства запуска создадим shell скрипт:

    ::::bash
    #!/bin/sh
    ./MovieJukebox.sh -o /mnt/raid/video -c library_video.xml
    ./MovieJukebox.sh -o /mnt/raid/tvshow -c library_tvshow.xml

Этот скрипт последовательно запускает Джукбокс сначала для фильмов в
папке /mnt/raid/video, которую видно на NMT через шару video, складывает
в эту же папку свой вывод, - это описано в library, а потом то же
повторяет для папки /mnt/raid/tvshow с сериалами.

Настройка нераспознанных фильмов
--------------------------------

В случае, если видео не распознается по названию, используем NFO файлы.
Стандартный NFO для кинофильма выглядит так:

    <movie>
    <thumb>http://st.kinopoisk.ru/im/poster/1/1/6/kinopoisk.ru-Brothers-1166032.jpg</thumb>
    <id moviedb="kinopoisk">253761</id>
    </movie>

В нем мы указываем, откуда тянуть картинку (это опционально, но я
выбираю покрасивше), и индекс фильма на кинопоиске. Стандартный YAMJ
нуждается в настройке для работы с русскоязычними ресурсами, в сборке от
avalanch это уже настроено. У меня возникла странная трабла с файлами
NFO, подозреваю что Midnight Commander их как-менял по своему разумению.
Поэтому я использовал расширение nf, для чего добавил в
moviejukebox.properties строчку filename.nfo.extensions=nf Важно
понимать, как должен называться NFO файл. Общее правило таково - если
фильм состоит только из файлов - то nfo мы называем как файл. Это чаще
всего относится к фильмам в mkv или avi. Например:

    ::::xml
    /mnt/raid/video/Безудержная/Abandoned [BD-Remux].nfo
    /mnt/raid/video/Безудержная/Abandoned [BD-Remux].mkv

Если же фильм состоит из папок, то nfo должен называться, как папка
уровнем выше. Это фильмы в DVD или Bluray формате. Например:

    ::::xml
    /mnt/raid/video/Оттепель/The_Thaw/BDMV/...
    /mnt/raid/video/Оттепель/The_Thaw/The_Thaw.nfo

Сериалы
-------

Ситуация с сериалами следующая. Во первых, серии должны именоваться в
соответствии с [конвенцией][]. В общих чертах это выглядит так (название
сериала).sXXeXX.(остальная информация), например:

    House.s01e01.Pilot.avi
    Chuck S01xE01.avi

Далее, обязательно, чтобы сериал был на сайте [http://thetvdb.com][].
Именно оттуда тянется инфа. Насколько я понимаю, других вариантов на
сегодняшний день нет, только заполнять руками NFO. Если сериал не
определился по именам файлов, то ложим в корень файл \<папка с
сериалом\>.nfo, где пишем:

    <tvshow>
        <id>73255</id>
    </tvshow>

где 73255 - код на thetvdb.com

Сеты
----

Сеты предназначены для объеденения нескольких фильмов в один набор,
например всех частей "Крепкого орешка" или 4-ре части BBC: Планета
Земля. Для этого в каждом фильме создаем nfo-файл:

    <movie>
    <thumb>http://st.kinopoisk.ru/im/poster/7/2/9/kinopoisk.ru-Planet-Earth-729440.jpg</thumb>
    <id moviedb="kinopoisk">279548</id>
    <sets>
            <set order="1">Планета Земля</set>
    </sets>
    </movie>

Вместо еденички, соответственно, ставим номер фильма в сете. Есть так же
небольшой трюк, позволяющий установить кастомную обложку на сет. Для
этого рядом с nfo-файлом следует поместить jpg, назвав его следующим
образом: Set\_\<set name\>\_1.jpg, для нашего примера будет Set\_Планета
Земля\_1.jpg. Для чего тут \_1, я не знаю, но работает.

Тонкая настройка
----------------

Если надо как-то пометить группы фильмов, то сделать это можно через
жанры, создав свой. Это делается добавление строчки в NFO:

    <movie>
    <thumb>http://st.kinopoisk.ru/im/poster/1/1/6/kinopoisk.ru-Brothers-1166032.jpg</thumb>
    <id moviedb="kinopoisk">253761</id>
    <genre>Новый жанр</genre>
    </movie>

Но просто так жанр не добавится, надо поменять настройку кинопоиска в
`moviejukebox.properties`
    
    kinopoisk.NFOpriority=true

Это означает, что NFO имеет приоритет на скачанной скрепером инфой. Однако данный способ
имеет большой минус - кастомный жанр **замещает** все жанры, взятые скрепером.



  [конвенцией]: http://code.google.com/p/moviejukebox/wiki/TVSeriesNaming
  [http://thetvdb.com]: http://thetvdb.com
