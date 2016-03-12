Title: Установка rTorrent + ruTorrent на ubuntu server (10.04)
Date: 2010-05-06 16:49
Category: Popcorn
Tags: torrent, ubuntu
Author: Swasher


Описывается установка торрент-клиента rTorrent и веб интерфейса к нему
ruTorrent на Debian-подобную систему. По состоянию на 28.11.2010
необходимо использовать stable-релизы libtorrent-0.12.6 и
rtorrent-0.8.6. На svn-версиях rutorrent работать не будет. rtorrent будет запускаться скриптом как демон и работать под менеджером консолей screen
Пользователь, из-под которого запускается скрин - **rtorrent** 

Prerequisites
-------------

Обновляемся:

    ::console
    $ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade

Cтавим необходимые пакеты

    ::console
    $ sudo apt-get install screen php5 php5-geoip php5-cgi php5-cli apache2-utils curl \
    subversion make autoconf autotools-dev automake libtool libcurl4-openssl-dev \
    libsigc++-2.0-dev pkg-config libncurses5-dev checkinstall g++


Добавляем юзера

    ::console
    useradd rtorrent

Устанавливаем пароль

    ::console
    passwd rtorrent

Создаем папки

    ::console
    $ cd /home/rtorrent
    $ mkdir torrents
    $ mkdir session

Меням владельца

    ::console
    $ chown -R rtorrent /home/rtorrent/
    $ chgrp -R rtorrent /home/rtorrent/

Rtorrent+libtorrent
-------------------

Ставим xml-rpc из svn (не из под рута)

    ::console
    $ cd ~
    $ svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/advanced xmlrpc-c
    $ cd xmlrpc-c
    $ ./configure --prefix=/usr
    $ make
    $ sudo checkinstall -D

Пользователь, из-под которого запускается скрин - **rtorrent** в третьем
пункте меню ставим версию - "1", например, иначе не установится. Последней командой мы
собираем и устанвливаем дибиан-пакет, который в последствии можно удалить командой `dpkg -r xmlrpc`

Далее, собираем libtorrent (не из под рута)

    ::console
    $ cd ~
    $ wget http://libtorrent.rakshasa.no/downloads/libtorrent-0.12.6.tar.gz
    $ tar zxfv libtorrent-0.12.6.tar.gz
    $ cd libtorrent-0.12.6
    $ ./autogen.sh
    ## ./configure --prefix=/usr   вместо этого
    ## мы собираем с поддержкой преаллокайта
    $ ./configure --prefix=/usr --disable-debug --with-posix-fallocate
    $ make
    $ sudo checkinstall -D

Собираем rtorrent

    ::console
    $ cd ~
    $ wget http://libtorrent.rakshasa.no/downloads/rtorrent-0.8.6.tar.gz
    $ tar zxfv rtorrent-0.8.6.tar.gz
    $ cd rtorrent-0.8.6
    $ ./autogen.sh
    $ ./configure --with-xmlrpc-c --prefix=/usr
    $ make
    $ sudo checkinstall -D

В поле Description вводим rtorrent.

Далее создаем файл конфигурации:

    ::console
    $ cd /home/rtorrent
    $ nano rtorrent.rc

с примерно таким содержимым: (пути папки и т.д. прописываешь свои)

    ::conf
    directory = /home/rtorrent/torrents/
    session = /home/rtorrent/session/
    scgi_port = 127.0.0.1:5000
    encoding_list = UTF-8

    min_peers = 10
    max_peers = 125
    min_peers_seed = 10
    max_uploads = 0
    download_rate = 675
    upload_rate = 900
    port_range = 6789-6789
    port_random = no
    check_hash = yes
    peer_exchange = yes
    check_hash = yes
    use_udp_trackers = yes
    encryption = allow_incoming,try_outgoing,enable_retry

    #Завершение программы при нехватке свободного места
    schedule = low_diskspace,5,60,close_low_diskspace=300M

    #Использование fallocate
    system.file_allocate.set = yes

    #Автоматическое создание папки назначения
    system.method.set_key=event.download.inserted_new,create_struct,"d.open= ; f.multicall=default,  
    "execute={sh,/home/rtorrent/creator.sh,$f.get_frozen_path=}\""

**или** берем официальный конфиг с комментариями:

    ::console
    $ wget http://libtorrent.rakshasa.no/export/1169/trunk/rtorrent/doc/rtorrent.rc \
        -O /home/rtorrent/.rtorrent.rc

и правим нужные настройки. Устанавливаем права на файл конфигурации

    ::console
    $ chmod 777 .rtorrent.rc
    $ chown -R rtorrent /home/rtorrent/.rtorrent.rc
    $ chgrp -R rtorrent /home/rtorrent/.rtorrent.rc

Lighttpd
--------

Включаем файлы конфигурации для lighttpd 

а) **fastcgi**

    ::console
    $ ln -s /etc/lighttpd/conf-available/10-fastcgi.conf /etc/lighttpd/conf-enabled/10-fastcgi.conf

Открываем `/etc/lighttpd/conf-available/10-fastcgi.conf` и пастим в конец 

    ::lighttpd
    fastcgi.server = ( ".php" =>
         ((
            "bin-path" => "/usr/bin/php5-cgi",
            "socket" => "/tmp/php.socket",
            "max-procs" => 2,
            "idle-timeout" => 20,
            "bin-environment" => (
            "PHP_FCGI_CHILDREN" => "1",
            "PHP_FCGI_MAX_REQUESTS" => "10000"
         ),
            "bin-copy-environment" => (
            "PATH", "SHELL", "USER"
         ),
         "broken-scriptfilename" => "enable"
         ))
    )

б) **auth**

    ::console
    ln -s /etc/lighttpd/conf-available/05-auth.conf /etc/lighttpd/conf-enabled/05-auth.conf

Добавляем следующую секцию в `05-auth.conf`

    ::lighttpd
    server.modules                += ( "mod_auth" )

    auth.backend                   = "htdigest"
    auth.backend.htdigest.userfile = "/etc/lighttpd/htdigest"

    auth.require = ( "/RPC2" =>
            (
                    "method" => "digest",
                    "realm" => "rTorrent RPC",
                    "require" => "user=rtorrent"
            )
    )

c) **scgi** Создаем конфиг scgi

    ::console
    nano /etc/lighttpd/conf-available/10-scgi.conf

копипастим туда следуюший код:

    ::lighttpd
    server.modules += ( "mod_scgi" )

    scgi.server = (
                    "/RPC2" =>
                      ( "127.0.0.1" =>
                        (
                          "host" => "127.0.0.1",
                          "port" => 5000,
                          "check-local" => "disable",
                          "disable-time" => 0,
                        )
                      )
                  )

делаем симлинк

    ::console
    $ ln -s /etc/lighttpd/conf-available/10-scgi.conf /etc/lighttpd/conf-enabled/10-scgi.conf

Создаем пароль, который будет спрашиваться при доступе через веб-морду:

    ::console
    $ cd /etc/lighttpd
    $ htdigest -c /etc/lighttpd/htdigest "rTorrent RPC" rtorrent


Rutorrent
---------

Рискнем хоть веб-морду дернуть из svn:

    ::console
    $ cd /var/www/
    $ svn checkout http://rutorrent.googlecode.com/svn/trunk/rutorrent

Редактируем файл конфиг `/var/www/rutorrent/conf/config.php`
Параметр `\$topdirectory` устанавливаем на помойку, у нас `/mnt/raid/`

Плагины

    ::console
    $ cd /var/www/rutorrent/plugins
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/erasedata

    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/trafic
    $ chmod 777 /var/www/rutorrent/share/settings

    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/datadir
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/tracklabels
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/diskspace
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/_getdir
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/cpuload
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/geoip

Для geoip устанавливаем расширение php:

    ::console
    $ apt-get install php5-geoip && /etc/init.d/lighttpd force-reload

Все плагины могут запускаться одной командой в .rtorrent.rc
(запускать их при выключенном rutorrent'e необходимо, например, для
сбора статистики). Отредактируйте строку запуска:

1. php path Your path may be different
2. rutorrent location Rutorrent may be installed in a different location on your syste
3. webusername you may or may not be using web authentication, if you aren't, remove the
username entirely, if you are, edit it accordingly

следующая строка показывает, как запустить плагины для юзера tom,
расположенные в /var/www/rutorrent

    ::conf
    execute = {sh,-c,/usr/bin/php /var/www/rutorrent/php/initplugins.php tom &}
                                                                         ^^^ - мы не
                                                             используем пользователя
                                                                 вовсе, пишем пробел


##### А note on upgrading plugins

Крайне важно помнить, когда мы обновляем плагины, мы должны действовать
следующим образом:

1.  stop rtorrent
2.  upgrade the plugin(s)
3.  restart rtorrent

Failure to stop/start rtorrent can result in plugins not behaving as
you'd expect.

> **TODO обдумать**
>
>     cd rutorrent
>     sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins
>
> Удаляем ненужные плагины, затем в файле /rutorent/plugins/.svn/entries
> убираем по две строчки для каждого ненужного плагина, чтобы они не
> обновлялись – имя плагина и слово dir. В дальнейшем обновляем и ядро и
> плагины командой svn up \* из папки /var/www/rutorrent

Терь разрешаем пользователю веб сервера пользоваться мордой:

    ::console
    $ sudo chown -R www-data:www-data /var/www/rutorrent

Так как консольный клиент не умеет (!!!) работать как демон,
скачиваем костыли, позволяющие обойти этот идиотизм. (заметим, что
костыль этот изобрел сам криворукий кодер)

    ::console
    $ sudo wget http://libtorrent.rakshasa.no/attachment/wiki/RTorrentCommonTasks \
        /rtorrentInit.sh?format=raw -O /etc/init.d/rtorrent

Редактируем костыль

    ::console
    $ sudo nano /etc/init.d/rtorrent

в user пишем своего пользователя

    user=rtorrent

Делаем костыль самодвижущимся и добавляем его в автозапуск.

    ::console
    $ sudo chmod +x /etc/init.d/rtorrent
    $ sudo update-rc.d rtorrent defaults
    $ sudo /etc/init.d/rtorrent start

Делаем автоматическое создание папки с названием фильма, например,
путь загрузки `/mnt/raid/video//movie.torrent` Для этого добавляем в
.rtorrent.rc следующую строку (можно в конец):

    system.method.set_key=event.download.inserted_new, create_struct,"d.open= ;f.multicall=default,   
   "execute={sh,/home/rtorrent/creator.sh,$f.get_frozen_path=}\""

И создаем исполняемый скрипт **creator.sh** следующего содержания:

    ::bash
    #!/bin/sh
    dir=`dirname "${1}"`
    mkdir -p "${dir}"

Так как сие произведение исскуства имеет счастье регулярно падать,
стелим соломку:

    ::console
    $ cd /home/rtorrent
    $ touch retorrent.sh
    $ chmod +x retorrent.sh
    $ nano retorrent.sh

пастим следующий код:

    ::bash
    #!/bin/sh
    # Скрипт перезапуска rtorrent-a
    # Если процесс запущен - ничего не делаем;
    # Если процесса нет - поднимаем и пишем в лог с проверкой - запустилось или нет.
    if  ps -C "rtorrent" | grep -c "rtorrent" > /dev/null;
        then
            echo "Up" > /dev/null
        else
            echo "Down"  > /dev/null
            /etc/init.d/rtorrent start
            if  ps -C "rtorrent" | grep -c "rtorrent" > /dev/null
            then
                echo `date`" : trying start rtorrent - started OK!" >> /home/rtorrent/start.rtorrent.log
            else
                echo `date`" : trying start rtorrent - FAIL!" >> /home/rtorrent/start.rtorrent.log
           fi
    fi

редактируем кронтаб рута (можно и не рута, я захотел так)

    ::console
    $ sudo crontab -u root -e

Добавляем строку, запускающую этот скрипт раз в пять минут

    ::conf
    */5 * * * * /home/rtorrent/retorrent.sh

----------------

This has to do with the memory settings of rtorrent, not the rtGUI
connected to it. It usually means you have too many upload/download
slots with large buffer sizes set and it is chewing up all available
memory. Each slot, upload and download requires memory to hold the data
as it is read from or before it is written to the HDD. These settings
are found in .rtorrent.rc in your home directory. I think by default the
send\_buffer\_size is 4MB (can vary from system to system, check using
cat /proc/sys/net/ipv4/tcp\_wmem). So for each upload peer rtorrent
takes 4MB of memory. On a 512MB system if your rtorrent is set to \~100
upload slots your approaching 400MB of memory used. This doesn't even
account for the memory used in downloads or by the system. I have mine
set to send\_buffer\_size = 1M receive\_buffer\_size = 25K with maximum
global uploads between 200 and 400. This is on a 1GB system, with
rtorrent being told to use a max of 800MB. Keeps speeds high and never
runs out of memory. Of course there is overhead memory used so settings
need to be tweaked for each system. Just remember that setting
max\_peers and max\_global\_peers to the biggest numbers possible does
not translate to more download speed.


