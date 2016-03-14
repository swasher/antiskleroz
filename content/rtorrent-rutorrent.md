Title: Установка и настройка rTorrent + ruTorrent
Date: 2010-05-06 16:49
Category: Popcorn
Tags: torrent, ubuntu
Author: Swasher

ПЕРЕРАБОТАНО СЕНТЯБРЬ 2013 ГОДА
================================

**Ubuntu 3.8.0-26 x64**  
**libtorrent-0.13.3 (unstable)**  
**rtorrent-0.9.3 (unstable)**  

Эта статья является переработанной версией [предыдущей](|filename|Установка-rtorrent-rutorrent-на-ubuntu-server-10-04.md). 
Далее я буду только обновлять эту статью, при выходе новых версий и при появлении каких-то новых ньюансов.

ПЕРЕРАБОТАНО 2015 ГОД
===============================

**Ubuntu 15.10 Wily x64**  
**libtorrent-0.13.6 (stable)**  
**rtorrent-0.9.6 (stable)**  

Systemd, nginx и другое

СКРИПТ АВТОМАТИЧЕСКОЙ УСТАНОВКИ
===============================

По этому мануалу написан скрипт, который автоматически производит все указанные действия.
[Ссылка на github.]

Описывается установка торрент-клиента rTorrent и веб интерфейса к нему
ruTorrent на Debian-подобную систему. По состоянию на 28.11.2010
необходимо использовать stable-релизы libtorrent-0.12.6 и
rtorrent-0.8.6. На svn-версиях rutorrent работать не будет. rtorrent будет запускаться скриптом 
как демон и работать под менеджером консолей screen
Пользователь, из-под которого запускается скрин - **rtorrent** 

Prerequisites
-------------

Обновляемся:

    ::console
    $ sudo apt-get update && sudo apt-get upgrade && sudo apt-get dist-upgrade

В случае, если до этого уже был установлен rtorrent, или его компоненты, удаляем их:

    ::console
    apt-get purge rtorrent libtorrent11 libxmlrpc-c3 libxmlrpc-c3-dev \
    libxmlrpc-core-c3 libxmlrpc-core-c3-dev

Cтавим необходимые пакеты

    ::console
    $ sudo apt-get install screen php5 php5-geoip php5-cgi php5-cli apache2-utils curl \
    subversion make autoconf autotools-dev automake libtool libcurl4-openssl-dev \
    libsigc++-2.0-dev pkg-config libncurses5-dev checkinstall g++ \
    libcppunit-dev


Добавляем юзера

    ::console
    useradd -c "Torrent User" -d /home/rtorrent -m -s /bin/bash rtorrent

Устанавливаем пароль  
***TODO*** где будет использоваться пароль???

    ::console
    passwd rtorrent

Создаем папки

    ::console
    $ cd /home/rtorrent
    $ mkdir torrents session

Меням владельца

    ::console
    $ chown -R rtorrent:rtorrent /home/rtorrent/

Rtorrent+libtorrent
-------------------

Ставим xmlrpc из svn (не из под рута). Ранее использовалась advanced версия, по [последним мануалам] - везде юзают stable

    ::console
    $ cd ~
    $ svn co https://xmlrpc-c.svn.sourceforge.net/svnroot/xmlrpc-c/stable xmlrpc-c
    $ cd xmlrpc-с
    $ ./configure --prefix=/usr \
      --enable-libxml2-backend \
      --disable-libwww-client \
      --disable-wininet-client \
      --disable-abyss-server \
      --disable-cgi-server
        # --enable-libxml2-backend  To lose some weight and not statically link in expat.
        # --disable-libwww-client   Don't build the Libwww client transport
        # --disable-wininet-client  Don't build the Wininet client transport
        # --disable-abyss-server    Disable the C++ version of the library as well as the C version.
        # --disable-cgi-server      Don't build the CGI server module
        # --disable-cplusplus       Add this options if the compiling stops with some syntax error
    $ make
    $ sudo checkinstall -D --pkgversion=1 -y

Последней командой мы собираем и устанавливаем дебиан-пакет, который в последствии можно удалить командой `dpkg -r xmlrpc`

Так же можно уставить пользвотельскую утилиту `xmlrpc`

    ::console
    $ cd tools
    $ make
    $ make install

Как ей пользоваться, описано например тут [http://libtorrent.rakshasa.no/wiki/RTorrentXMLRPCGuide]

Далее, аналогично собираем libtorrent (не из под рута)

    ::console
    $ cd ~
    $ curl http://libtorrent.rakshasa.no/downloads/libtorrent-0.13.3.tar.gz | tar xz
    $ cd libtorrent-0.13.3
    $ ./autogen.sh
    $ ./configure --prefix=/usr --disable-debug --with-posix-fallocate
        # Возможные опции --enable-ipv6 --enable-static --disable-shared 
        # --disable-debug --disable-cplusplus[помогает при ошибках]
        # compiling libtorrent with --with-posix-fallocate is recommended 
        # for xfs, ext4 and btrfs filesystems, which have native 
        # fallocate syscall support. They will see no delay during preallocation and no 
        # fragmented filesystem. Pre-allocation on 
        # others filesystems will cause a delay but will not fragment the files.
    $ make -j2
    $ sudo checkinstall -D -y


Собираем rtorrent

    ::console
    $ curl http://libtorrent.rakshasa.no/downloads/rtorrent-0.9.3.tar.gz | tar xz
    $ cd rtorrent-0.9.3
    $ ./autogen.sh
    $ ./configure --prefix=/usr --with-xmlrpc-c
    $ make -j2
    $ sudo checkinstall -D -y
    $ sudo ldconfig

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
    system.method.set_key=event.download.inserted_new,create_struct,"d.open= ; \
    f.multicall=default,
    "execute={sh,/home/rtorrent/creator.sh,$f.get_frozen_path=}\""

**или** берем официальный конфиг с комментариями:

    ::console
    $ wget http://libtorrent.rakshasa.no/export/1303/trunk/rtorrent/doc/rtorrent.rc \
        -O /home/rtorrent/.rtorrent.rc

и правим нужные настройки. Устанавливаем права на файл конфигурации

    ::console
    $ chmod 666 .rtorrent.rc
    $ chown -R rtorrent:rtorrent /home/rtorrent/.rtorrent.rc

Lighttpd
--------

Переходим к настройке веб сервера для rutorrent.

    ::console
    $ apt-get install lighttpd

##### Fastcgi

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


Nginx
--------

По сравнению с lighttpd, тут все просто. Ставим пакет nginx, основной конфиг не трогаем, 
в директории `/etc/nginx/sites-available` создаем конфиг, например, `rtorrent.swasher.pp.ua`,
и делаем на него символическую сссылку в `sites-enabled`

Аутентификацию по логину и паролю я решил не применять, вместо этого я использую
фильтрацию по IP - я хожу на свой rtorrent, в основном, из дома или с работы, поэтому 
мне так удобнее.

Вот текст конфига

    ::: nginx
    server {
    #    listen 80 default_server;
    #    listen [::]:80 default_server ipv6only=on;
    
        charset utf-8;
    
        root /home/swasher/nginx/ruTorrent;
        index index.php index.html index.htm;
        server_name swasher.pp.ua;
    
        #access_log  /var/log/nginx/rtorrent-access.log;
        error_log   /var/log/nginx/rtorrent-error.log;
    

        location / {
            # First attempt to serve request as file, then
            # as directory, then fall back to displaying a 404.
            allow   1.2.3.4/24;
            allow   11.22.33.44;
            allow   12.34.56.78;
            deny    all;
            try_files $uri $uri/ =404;
        }
    
         location /RPC2 {
            include scgi_params;
            # Тут должно быть значение, соотв. rtorrent.rc
            scgi_pass 127.0.0.1:5000;
        }
    
    
        location ~ \.php$ {
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            # NOTE: You should have "cgi.fix_pathinfo = 0;" in php.ini
    
            # With php5-cgi alone:
            # fastcgi_pass 127.0.0.1:9000;
    
            # With php5-fpm:
            # Тут должно быть значение, соотв. php-fpm
            fastcgi_pass unix:/var/run/php5-fpm.sock;
            fastcgi_index index.php;
            #include fastcgi_params;
            include fastcgi.conf;
        }
    }
  


Rutorrent
---------

Ставим из svn последнюю версию:

    ::console
    $ cd /var/www/
    $ svn checkout http://rutorrent.googlecode.com/svn/trunk/rutorrent

Редактируем файл конфиг `/var/www/rutorrent/conf/config.php`. Параметр `\$topdirectory` устанавливаем на корень файлового хранилища , у нас `/mnt/raid/`

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

Владельцем файлов rutorrent устанавливаем www-data:

    ::console
    $ cd /var/www
    $ chown -R www-data:www-data rutorrent

Все плагины могут запускаться одной командой в .rtorrent.rc
(запускать их при выключенном rutorrent'e необходимо, например, для
сбора статистики). Следующая строка показывает, как запустить плагины для юзера tom,
расположенные в /var/www/rutorrent

    ::xml
    execute = {sh,-c,/usr/bin/php /var/www/rutorrent/php/initplugins.php tom &}
                                                                         ^^^ - мы не
                                                             используем пользователя
                                                                 вовсе, пишем пробел

Обращаем внимание на правильность путей к php и rutorrent.

##### Про обновление плагинов

Крайне важно помнить, когда мы обновляем плагины, мы должны действовать
следующим образом:

1.  stop rtorrent
2.  upgrade the plugin(s)
3.  restart rtorrent

Обновление плагинов без остановки rtorrent может привести к непредсказуемому поведению.

> **TODO обдумать**
>
>     cd rutorrent
>     sudo svn checkout http://rutorrent.googlecode.com/svn/trunk/plugins
>
> Удаляем ненужные плагины, затем в файле /rutorent/plugins/.svn/entries
> убираем по две строчки для каждого ненужного плагина, чтобы они не
> обновлялись – имя плагина и слово dir. В дальнейшем обновляем и ядро и
> плагины командой svn up \* из папки /var/www/rutorrent

Демон (upstart)
---------------

Rtorrent, будучи консольным клиентом, не умеет работать как демон, что немного странно.
Для автоматического старта rtorrent при загрузке системы используем скрипт от Rakshasa

    ::console
    $ sudo wget http://libtorrent.rakshasa.no/attachment/wiki/RTorrentCommonTasks \
        /rtorrentInit.sh?format=raw -O /etc/init.d/rtorrent

Редактируем файл `/etc/init.d/rtorrent`, в переменную user пишем нашего пользователя

    ::console
    user=rtorrent

Для Debian и Ubuntu, сразу после строки `#!/bin/sh`, вставляем следующий код. Подробнее тут - [LSBInitScripts]

    ::text
    ### BEGIN INIT INFO
    # Provides:          rtorrent_autostart
    # Required-Start:    $local_fs $remote_fs $network $syslog $netdaemons
    # Required-Stop:     $local_fs $remote_fs
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: rtorrent script using screen(1)
    # Description:       rtorrent script using screen(1) to keep torrents working \
    # without the user logging in
    ### END INIT INFO

Делаем скрипт исполняемым и добавляем его в автозапуск.

    ::console
    $ sudo chmod +x /etc/init.d/rtorrent
    $ sudo update-rc.d rtorrent defaults
    $ sudo /etc/init.d/rtorrent start

##### Проверка демона Cron-ом

>**Это не работает, поскольку rtorrent может не работать, но висеть в процессах. Попробовать сделать проверку на отклик xmlrpc, и убийство процесса через kill**

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
                echo `date`" : trying start rtorrent - started OK!" >> \
                /home/rtorrent/start.rtorrent.log
            else
                echo `date`" : trying start rtorrent - FAIL!" >> \
                /home/rtorrent/start.rtorrent.log
           fi
    fi

редактируем кронтаб рута (можно и не рута, я захотел так)

    ::console
    $ sudo crontab -u root -e

Добавляем строку, запускающую этот скрипт раз в пять минут

    ::plain
    */5 * * * * /home/rtorrent/retorrent.sh
    
Демон (Systemd)
----------------------------

Удаляем:

- /etc/init.d/rtorrent
- из крона - проверку, запущен ли процесс

Создаем конфиг /etc/systemd/system/rtorrent.service

    ::ini
    [Unit]
    Description=rTorrent
    
    [Service]
    Type=forking
    User=USERNAME
    ExecStart=/usr/bin/screen -d -m -S rtorrent /usr/bin/rtorrent
    ExecStop=/usr/bin/killall -w -s 2 rtorrent
    WorkingDirectory=/home/USERNAME
    
    [Install]
    WantedBy=multi-user.target

Включаем сервис

    ::console
    $ sudo systemctl enable rtorrent.service
    
и проверяем статус нашего нового сервиса

    ::console
    $ sudo systemctl status rtorrent.service
    
Соответственно команды остановки/запуска сервиса будут

    ::console
    $ sudo systemctl stop rtorrent.service
    $ sudo systemctl start rtorrent.service
    
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

**плагин HTTPRPC**

Я столкнулся с проблемой, которую долго не мог побороть. Состоит она в том, что при большом кол-ве торрентов объем данных, пересылаемых
XMLRPC, становится слишком большой. Rutorent тормозит, сыпет в лог сообщения "Время запроса к rTorrent истекло.", потом и вовсе падает. 
Для решения этой проблемы автором Rutorrent уважаемым Novik был написан плагин HTTPRPC, который переносит часть логики на сервер, таким 
образом уменьшая трафик, но увеличивая вычислительную нагрузку на сервер, что нас вполне устраивает. Ставится он просто:

    ::console
    $ service rtorrent stop
    $ cp httprpc /var/www/rutorrent/plugins
    $ lighttpd-disable-mod scgi
    $ service lighttpd force-reload
    $ servoce rtorrent start

Дебаг
-----

Куда смотреть, если ничего не работает.

* Лог lighttpd - находится в `/var/log/lighttpd/error.log`. Для включения в него вывода fastcgi нужно включить в конфиг команду `fastcgi.debug = 1`.
Более полный лог веб сервера можно получить, используя [эти переменные](http://redmine.lighttpd.net/projects/1/wiki/DebugVariables)

* Логи rtorrent - для их получения нужно добавить в конфиг следующие строки:

        ::console
        log.execute = /home/rtorrent/exec.log
        log.xmlrpc  = /home/rtorrent/xmlrpc.log

* Логи rutorrent - в файле `/var/www/rutorrent/conf/config.php` ищем строку `$log_file = '/tmp/errors.log';` - расположение
лога можно поменять на более удобное

* Наконец, полезную информацию можно выудить из dmesg (с ключем -T для отображения времени) и /var/log/syslog

* Утилита xmlrpc - должна получать ответ от сервера (от 5000 порта??). Подробно 
тут [RTorrent XMLRPC Guide]. Например, `xmlrpc localhost system.listMethods`

* rtorrent может не запускаться, если был удален пользователь rtorrent, а затем создан новый. Нужно проверить 
владельца директории `/var/run/screen/S-rtorrent` - должен быть rtorrent:rtorrent, или просто удалить ее.

* При нарушении прав доступа на файлы и папки rutorrent исправляем таким образом:

        :console
        $ cd /var/www/rutorrent
        $ chown -R www-data:www-data share/
        $ find share/ -type d -exec chmod 777 {} \;
        $ find share/ -type f -exec chmod 666 {} \;

* Rtorrent может не запускаться, если не может по какой-то причине получить права на файл `../rtorrent/session/rtorrent.lock`. Достаточно удалить этот файл.


[последним мануалам]: https://github.com/Notos/seedbox-from-scratch/blob/v2.1.9/seedbox-from-scratch.sh
[LSBInitScripts]: https://wiki.debian.org/LSBInitScripts
[RTorrent XMLRPC Guide]: http://libtorrent.rakshasa.no/wiki/RTorrentXMLRPCGuide
[Ссылка на github.]: https://github.com/swasher/rinstall