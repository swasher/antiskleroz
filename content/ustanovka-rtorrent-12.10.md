Title: Установка rTorrent + ruTorrent на Ubuntu Server 10.12 из репозитария
Date: 2013-01-28 17:51
Category: Popcorn
Tags: torrent, rtorrrent, rutorrent, ubuntu

Случилась неприятность - в сервере сдох системный винт. Появился повод попробовать устнновать связку libtorrent+
rtorrent из стандартного репозитория Ubuntu, благо в 12.10 они последних версий. Если все пройдет гладко, это 
руководство заменит собой прошлую [статью](|filename|Установка-rtorrent-rutorrent-на-ubuntu-server-10-04.md), в которой установка производилась с исходников. На текущий момент версии
пакетов в репозитории Ubuntu и на [http://libtorrent.rakshasa.no/] совпадают: **libtorrent 0.13.2-1** и **rtorrent 0.9.2-1**

Установка
---------

Итак, обновляемся, ставим неколько необходимых пакетов и устанвливаем rtorrent:

    :::console
    $ apt-get update && apt-get upgrade
    $ apt-get install -y subversion php5-cgi screen apache2-utils php5-cli
    $ apt-get install -y rtorrent

Некоторую инфу о пакете можем посмотреть в `/usr/share/doc/rtorrent` и есть стандартный man, который нас впрочем мало интересует.
В настройке "костыля" для запуска сервиса за последние лет пять ничего не изменилось, поэтому применяем старый способ - заводим
нового юзера, от его имени скриптом при запуске систему запускаем "демона" в менеджере консолей screen.

Директории и права
------------------

Добавляем юзера

    :::console
    $ useradd rtorrent

Устанавливаем пароль

    :::console
    $ passwd rtorrent

Создаем папки

    ::console
    $ cd /home
    $ mkdir rtorrent
    $ cd rtorrent
    $ mkdir torrents
    $ mkdir session

Меням владельца

    :::console
    $ chown -R rtorrent /home/rtorrent/
    $ chgrp -R rtorrent /home/rtorrent/

Создаем файл настроек

    :::console
    $ cd /home/rtorrent
    $ touch rtorrent.rc
    $ nano rtorrent.rc

с примерно таким содержимым (пути меняем на актуальные):

    ::properties
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

    ##############ВСТАВИТЬ АКТУАЛЬНОЕ СОДЕРЖИМОЕ###################

При необходимости правим пути и устанавливаем права на файл конфигурации

    ::console
    $ chmod 666 .rtorrent.rc
    $ chown -R rtorrent /home/rtorrent/.rtorrent.rc
    $ chgrp -R rtorrent /home/rtorrent/.rtorrent.rc

Lighttpd
--------

Переходим к настройке веб сервера для rutorrent.

    ::console
    $ apt-get install lighttpd

##### fastcgi

Открываем конфиг fastcgi и копируем в конец:

    :::lighttpd
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

##### Аутентификация

Открываем конфиг auth и копируем в конец:

    :::lighttpd
    auth.backend                   = "htdigest"
    auth.backend.htdigest.userfile = "/etc/lighttpd/htdigest"

    auth.require = ( "/RPC2" =>
        (
            "method" => "digest",
            "realm" => "rTorrent RPC",
            "require" => "user=rtorrent"
        )
    )


Создаем пароль, который будет запрашиваться при доступе через веб-интерфейс:

    :::cobsole
    cd /etc/lighttpd
    htdigest -c /etc/lighttpd/htdigest "rTorrent RPC" rtorrent


##### SCGI

Создаем новый конфиг `/etc/lighttpd/conf-available/10-scgi.conf`

Копипастим туда следуюший код:

    :::lighttpd
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

##### конфиг lighttpd

Настраиваем веб-сервер так, чтобы к оболочке rutorrent можно было обращаться по веб-адресу. Так мы сможем видеть нашу стенку "из интернета".
Для этого надо настроить DNS на наш IP адрес, и указать доменное имя в конфиге.

Для защиты используем plain-аутентификацию, ничего сверх-секретного в стенке нет. Пароль и логин доступа хранится в файле `/etc/lighttpd/.lighttpdpassword-YAMJ` в открытом виде:

    vasya:pass
    masha:secretpass

В строке require перечисляем юзеров, которым предоставлен доступ.

    ::lighttpd
    $HTTP["host"] =~ "yamj.swasher.pp.ua" {
    server.document-root = "/home/swasher/juke-web/"
        auth.backend = "plain"
        auth.backend.plain.userfile = "/etc/lighttpd/.lighttpdpassword-YAMJ"
        auth.require = ( "" =>
            (
            "method" => "basic",
            "realm" => "Password protected area",
            "require" => "user=vasya|user=masha"
            )
        )
    }


##### Стартуем
Включаем моды и рестартим сервер

    ::console
    $ lighttpd-enable-mod auth
    $ lighttpd-enable-mod scgi
    $ lighttpd-enable-mod fastcgi
    $ service lighttpd force-reload


Или вместо lighttpd пробуем Apache
----------------------------------

    ::console
    apt-get install apache2 libapache2-mod-scgi libapache2-mod-php5
    a2enmod scgi
    a2enmod php5


Имя сервера

    ::console
    nano /etc/apache2/conf.d/fqdn

    then add

    ServerName localhost


В конфиг апача apache2.conf прописываем:

    # rutorrent
    SCGIMount /RPC2 127.0.0.1:5000


Rutorrent
--------------

Ставим из svn последнюю версию:

    ::console
    $ cd /var/www/
    $ svn checkout http://rutorrent.googlecode.com/svn/trunk/rutorrent

Редактируем файл конфиг `/var/www/rutorrent/conf/config.php`. Параметр `$topdirectory` устанавливаем на корень файлохранилища,
у нас `/mnt/raid/`. Не забываем о слеше в конце пути. Ставим плагины

    ::console
    $ cd /var/www/rutorrent/plugins
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/erasedata

    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/trafic
    $ chmod 666 /var/www/rutorrent/share/settings

    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/datadir
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/tracklabels
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/diskspace
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/_getdir
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/cpuload
    $ svn co http://rutorrent.googlecode.com/svn/trunk/plugins/geoip

Для geoip устанавливаем расширение php:

    ::console
    $ apt-get install -y php5-geoip && /etc/init.d/lighttpd force-reload

Владельцем файлов rutorrent устанавливаем www-data:

    ::console
    $ cd /var/www
    $ chown -R www-data:www-data rutorrent


Все плагины могут запускаться одной командой в .rtorrent.rc (запускать их при выключенном rutorrent'e необходимо, например,
для сбора статистики). Cледующая строка показывает, как запустить плагины для юзера tom, расположенные в /var/www/rutorrent:

    ::xml
    execute = {sh,-c,/usr/bin/php /var/www/rutorrent/php/initplugins.php tom &}
                                                                         ^^^ - мы не используем
                                                               пользователя вовсе, пишем пробел
Обращаем внимание на правильность путей к php и rutorrent.



##### А note on upgrading plugins

Крайне важно помнить, когда мы обновляем плагины, мы должны действовать
следующим образом:

1.  stop rtorrent
2.  upgrade the plugin(s)
3.  restart rtorrent

Отказ от остановки rtorrent может привести к сбою работы.

> **TODO обдумать**
>
>     cd rutorrent
>     sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins
>
> Удаляем ненужные плагины, затем в файле /rutorent/plugins/.svn/entries
> убираем по две строчки для каждого ненужного плагина, чтобы они не
> обновлялись – имя плагина и слово dir. В дальнейшем обновляем и ядро и
> плагины командой `svn up *` из папки /var/www/rutorrent


Демон
-----

Так как консольный клиент не умеет (!!!) работать как демон, скачиваем костыли, позволяющие обойти этот идиотизм. (заметим, что
костыль этот изобрел сам криворукий кодер)

    ::console
    $ sudo wget http://libtorrent.rakshasa.no/attachment/wiki/RTorrentCommonTasks/\
        rtorrentInit.sh?format=raw -O /etc/init.d/rtorrent

Редактируем костыль `/etc/init.d/rtorrent`, - пишем своего пользователя `user=rtorrent`

Делаем костыль самодвижущимся и добавляем его в автозапуск.

    ::console
    $ sudo chmod +x /etc/init.d/rtorrent
    $ sudo update-rc.d rtorrent defaults
    $ sudo /etc/init.d/rtorrent start



Проверка демона Cron-ом
-----------------------

Так как сие произведение исскуства имеет счастье регулярно падать, стелим соломку:

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

    ::bash
    */5 * * * * /home/rtorrent/retorrent.sh


Тюнинг
------

Если при добавлении торрента в путь добавить вложенние директории, rtorrent их сам не создат, и закачка будет висеть в паузе по причине "path not found".
Чтобы папки создавались автоматически, нужно настроить это в `.rtorrent.rc`

    ::ini
    system.method.set_key=event.download.inserted_new, create_struct,\
        "d.open= ;f.multicall=default,"execute={sh,/home/rtorrent/creator.sh,\
        $f.get_frozen_path=}\""

И создаем исполняемый скрипт **creator.sh** следующего содержания:

    ::bash
    #!/bin/sh
    dir=`dirname "${1}"`
    mkdir -p "${dir}"


При добавлении нового торрента будет запускаться скрипт **creator.sh**, который и создать нужные папки.




-------

##### Заметка с форума о памяти (возможно устарело)
This has to do with the memory settings of rtorrent, not the rtGUI connected to it. It usually means you have too 
many upload/download slots with large buffer sizes set and it is chewing up all available memory.

Each slot, upload and download requires memory to hold the data as it is read from or before it is written to the HDD. 
These settings are found in .rtorrent.rc in your home directory.

I think by default the send_buffer_size is 4MB (can vary from system to system, check using cat /proc/sys/net/ipv4/tcp_wmem). 
So for each upload peer rtorrent takes 4MB of memory. On a 512MB system if your rtorrent is set to ~100 upload slots 
your approaching 400MB of memory used. This doesn't even account for the memory used in downloads or by the system.

I have mine set to 

    send_buffer_size = 1M
    receive_buffer_size = 25K

with maximum global uploads between 200 and 400. This is on a 1GB system, with rtorrent being told to use a max of 800MB. 
Keeps speeds high and never runs out of memory. Of course there is overhead memory used so settings need to be tweaked for 
each system. Just remember that setting max_peers and max_global_peers to the biggest numbers possible does not translate to more download speed. 

Such is the info I have gleaned so far (who watched Warehouse 13 :)) from various sources. It seems to be correct, my rtorrent 
is performing great since I tweaked these settings. It actually sustains high speed uploads will downloading.
