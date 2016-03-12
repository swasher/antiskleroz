Title: Настройка связки nginx-mysql-php для установки CMS
Date: 2014-09-01 11:11
Tags: nginx, mysql, php
Category: IT
Author: Swasher
Slug: server-setup-nginx-mysql-php

Описывается типичная настройка сервера для использования движков на php, таких как wordpress, modx, koken и
многих других. В качестве веб-сервера используется nginx, операционная система - любая debian-based. 
Протестировано на Ubuntu 14.04 x64.


Установка Nginx
---------------------------------------------

	::console
    $ sudo apt-get update
    $ sudo apt-get install nginx
    
Проверяем в браузере `http://<OUR IP>`

Должна появиться заставка Welcome to Nginx! Как установить свежий nginx из PPA - [в моей заметке]({filename}how-to-install-latest-nginx.md)

Установка и первоначальная настройка MySql для продакшн-сервера
---------------------------------------------

Теперь у нас есть веб-сервер, нам нужно установить MySQL, систему управления базами данных. 

Устанавливаем простой командой

	::console
    $ sudo apt-get install mysql-server

У вас будет запрошен root (административный) пароль для системы MySQL.

MySQL теперь установлен, но его конфигурация не завершена.

Первое, мы должны дать команду для генерации структуры директорий, это нужно для хранения баз и информации.
Скрипт mysql_install_db предназначен только для создания новых таблиц привилегий MySQL.

	::console
	$ sudo mysql_install_db
    
Далее, нам нужно запустить простой скрипт для обезпечения безопастности MySQL, который запросит у 
нас разрешение модифицировать некоторые настройки по-умолчанию. Запускаем скрипт командой:

	::console
    $ sudo mysql_secure_installation
    
У вас будет запрошен пароль root, который мы ввели во время инсталляции.
Далее, программа спросит, хотите ли вы изменить пароль.
Если пароль для root выбран правильный, надежный пароль, тогда его менать не нужно, нажимаем "N" и "ENTER"
Далее, нам будет предложено удалить тестовых пользователей и тестовые базы данных. 
Нужно просто нажимать "ENTER", чтобы удалить опасные настройки по умолчанию.
Как только скрипт будет завершен, установку MySQL можно считать оконченной.

Создадим базу данных на примере Modx. Созадние баз для других CMS абсолютно аналогично. 
Заходим в консоль MySQL (`mysql -u root -p`) и пишем:

    ::sql
    CREATE DATABASE modx;
    
Теперь нужно создать пользователя, для нашей базы. Там же в консоли

    ::sql
    CREATE USER 'modxuser'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON modx.* To 'modxuser'@'localhost' IDENTIFIED BY 'password';
    
Внимание! Это не тот же пароль, что выше для root, а новый.
Выходим из консоли mysql командой `exit`.


Установка PHP
---------------------------------------------

Теперь у нас установлен nginx, чтобы обслуживать веб-страницы, и MySQL для хранения и управления данными. Но нам нужно
еще что-то, чтобы соеденить эти две части и создать динамический контент. Тут нам поможен PHP.

Посколько nginx не умеет нативно обрабатывать php запросы (как и многие другие веб-серверы), нам нужно установить php5-fpm,
что расшифровывается как "fastCGI process manager". Он интерпретирует php-запросы и затем передает результат веб-серверу.

Кроме этого, нужно установить модуль, который позволит взаимодействовать с mysql.

    ::console
    $ sudo apt-get install php5-fpm php5-mysql php5-curl
    
    
#### Configure the PHP Processor

Теперь у нас есть установленный компонент php, но нужно произвести небольшую настройку для обеспечения безопастности.

Откроем следующий файл, используя root-привелегии

    ::console
    $ sudo nano /etc/php5/fpm/php.ini

Здесь нам нужно найти параметр cgi.fix_pathinfo.
Обычно он закоментирован с точкой-запятой (;) и по умолчанию установлен в 1.

Это чрезвычайно небезопасно установка. Уязвимость состоит в том, что пользователь может иметь возможность выполнить 
запрос PHP таким способом, который обычно был бы ему запрещен.

Раскоментируем этот параметр и установим его в '0':

    ::php
    cgi.fix_pathinfo=0

Заодно установим правильную тайм-зону:

    ::php
    date.timezone = Europe/Kiev
    
После этого сохраняем и закрываем файл.

Теперь, нужно перезапустить php-процессор командой 

    ::console
    $ sudo service php5-fpm restart
    
Это применит внесенные изменения.

Конфигурация Nginx для работы с PHP
---------------------------------------------

Удаляем дефолтный сайт

    ::console
    $ rm /etc/nginx/sites-enabled/default

Создаем в директории `/etc/nginx/sites-available/` новый сайт, например `/etc/nginx/sites-available/glpi`

Конфигурация может отличаться для разных CMS, но шаблон примерно такой:

    ::nginx
    server {
        listen       80;
        server_name  glpi;
    
        charset utf-8;
    
        access_log /var/log/nginx/nginx.access.glpi.log;
        error_log /var/log/nginx/nginx.error.glpi.log;
        
        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    
        location / {
            root   /path/to/our/cms;
            index  index.php index.html index.htm;
        }
    
        location ~ \.php$ {
            include fastcgi_params;
            fastcgi_pass   127.0.0.1:9000;
            fastcgi_index  index.php;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
            fastcgi_param PATH_INFO $fastcgi_script_name;
        }
    }        
    
Рабочий конфиг для wordpress (ubuntu 14.10):

    server {
        listen       80;
        server_name  wordpress.domen.com;
        root   /home/swasher/wordpress;
        index  index.php index.html index.htm;
    
        charset utf-8;
    
        access_log /var/log/nginx/nginx.access.wordpress.log;
        error_log /var/log/nginx/nginx.error.wordpress.log;
    
        error_page  404              /404.html;
    
        # redirect server error pages to the static page /50x.html
        #error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   /usr/share/nginx/html;
        }
    
        location / {
            try_files $uri $uri/ /index.php?q=$uri&$args;
        }
    
        location ~ \.php$ {
            try_files $uri =404;
            fastcgi_split_path_info ^(.+\.php)(/.+)$;
            fastcgi_pass unix:/var/run/php5-fpm.sock;
            fastcgi_index index.php;
            include fastcgi_params;
            fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        }
    
    }
    
Правим пути. Если у сервера нет FQDN, то ставим `server_name <local ip>;`

Так же нужно привести к общему виду порт или сокет, который слушает php5-fpm. 
Иначе будет ошибка в error.log:

    2013/10/31 15:52:01 [error] 26394#0: *1 connect() failed (111: Connection refused)
    while connecting to upstream, client: **.**.**.**,
    server: localhost, request: "GET / HTTP/1.1", upstream: "fastcgi://127.0.0.1:9000",
    host: "somehost.com"

Вариантов два:

*Первый*

/etc/php5/fpm/pool.d/www.conf

    ; listen = /var/run/php5-fpm.sock
    listen = 127.0.0.1:9000
    
/etc/nginx/sites-available/my_site.conf

    #fastcgi_pass   unix:/var/run/php5-fpm.sock;
    fastcgi_pass   127.0.0.1:9000;


*Второй*

/etc/php5/fpm/pool.d/www.conf

    listen = /var/run/php5-fpm.sock
    ; listen = 127.0.0.1:9000

/etc/nginx/sites-available/my_site.conf

    fastcgi_pass   unix:/var/run/php5-fpm.sock;
    #fastcgi_pass   127.0.0.1:9000;
    
У меня заработал только второй.


Включаем конфигурацию
----------------------------------------------

Теперь нужно подключить файл конфигурации 

    ::console
    $ cd /etc/nginx/sites-enabled/
    $ ln -s ../sites-available/lgpi lgpi

Рестарт демонов php5-fpm и nginx

    ::console
    $ service php5-fpm restart
    $ servece nginx restart

Проверяем
---------------------------------------------

Проверяем, что PHP работает - в корне сервера созадем файл info.php

    ::php
    <?php
    phpinfo();
    ?>

и браузером смотрим `http://server_domain_name_or_IP/info.php`

Porfit!
------------------------------------------------

Теперь осталось скачать нужный пакет с CMS, распаковать его в корень нашего сайт, и далее следовать инструкции
из настройки CMS, чаще всего - перейти браузером по адресу `http://server_domain_name_or_IP`
