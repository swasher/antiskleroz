Title: Настройка vsftpd с использованием virtual users
Date: 2010-11-25 18:13
Category: IT
Tags: linux, ubuntu, vsftpd
Author: Swasher


В этой заметке я расскажу, как настроить ftp сервер под Ubuntu-подобной
системой, используя схему авторизации с виртуальными пользователями
через [pam][]. Тестирование проходило на `Ubuntu 10.10 (Maverick Meerkat) x64`.
Как обычно, устанавливаем сервер: 

    ::console
    $ apt-get install vsftpd

Сначала приводим в должный вид файл `/etc/vsftpd.conf`.

Запрещаем анонимуса

    ::conf
    # Allow anonymous FTP? (Beware - allowed by default if you comment this out).
    anonymous_enable=NO

Это надо включить для использования списка юзеров

    ::conf
    # Uncomment this to allow local users to log in.
    local_enable=YES

Разрешение на запись

    ::conf
    # Uncomment this to enable any form of FTP write command.
    write_enable=YES

Запрещаем любые действия анонимам

    ::conf
    # Uncomment this to allow the anonymous FTP user to upload files. This only
    # has an effect if the above global write enable is activated. Also, you will
    # obviously need to create a directory writable by the FTP user.
    anon_upload_enable=NO

    # Uncomment this if you want the anonymous FTP user to be able to create
    # new directories.
    anon_mkdir_write_enable=NO
    anon_other_write_enable=NO

Строка приветствия

    ::conf
    #You may fully customise the login banner string:
    ftpd_banner=Тут могла быть ваша реклама.

Запрещаем юзерам "выходить" из назначенной им директории.

    ::conf
    # You may restrict local users to their home directories.  See the FAQ for
    # the possible risks in this before using chroot_local_user or
    # chroot_list_enable below.
    chroot_local_user=YES


> ДОРАБОТАТЬ
> Маски создания

    pam_service_name=vsftpd

    guest_enable=YES
    guest_username=virtual
    user_config_dir=/etc/vsftpd/users_config

    chown_username=virtual
    #anon_umask=0007
    #file_open_mode=0777
    #local_umask=777

    anon_umask=0x666
    #file_open_mode=0666
    #local_umask=555


Создаем директорию, где будут хранится файлы настройки:

    ::console
    $ cd /etc 
    $ mkdir vsftpd 
    $ chmod 700 vsftpd 

Создаем в нашей папке файл, в котором будет
хранится логины и пароли: 

    ::console
    $ cd vsftpd 
    $ touch logins.txt 
    $ chmod 600 logins.txt 

Файл этот текстовый и имеет такую структуру - `<логин> <пароль>`. Например:

    ::conf
    vasya secretpassword
    masha 123

Создадим директорию для хранения пользовательских конфигов:

    ::console
    $ cd /etc/vsftpd 
    $ mkdir users_config 

Далее создаем два скрипта, один для конвертации logins.txt в файл базу данных беркли,
второй - для автоматического добавления пользователей.

**convert.sh**

    ::bash
    #!/bin/bash

    db4.8_load -T -t hash -f logins.txt logins.db
    chmod 600 logins.db


**create.sh**

    ::bash
    #!/bin/bash

    USER=$1
    PASS=$2

    echo "$USER"+"$PASS"

    #Добавление юзера и апдейт базы
    echo "$USER" >> logins.txt
    echo "$PASS" >> logins.txt
    db4.8_load -T -t hash -f logins.txt logins.db
    chmod 600 logins.db

    #Создание папки
    mkdir /home/ftp/$USER
    chown virtual:virtual /home/ftp/$USER
    chmod 555 /home/ftp/$USER

    #Создание конфига
    cd /etc/vsftpd/users_config/
    touch "$USER"
    echo "local_root=/home/ftp/$USER" >> "$USER"
    echo "write_enable=YES" >> "$USER"
    echo "anon_mkdir_write_enable=YES" >> "$USER"
    echo "anon_other_write_enable=YES" >> "$USER"
    echo "anon_upload_enable=YES" >> "$USER"
    echo "chroot_local_user=YES" >> "$USER"

> ДОБАВИТЬ ЧТО ДЕЛАЕТ СКРИПТ


Назначаем права: 

    ::console
    $ chmod 700 convert.sh 
    $ chmod 700 create.sh 

Устанавливаем утилиты BerkleyDB: 

    ::console
    $ apt-get install db4.8-util 

В момент написания использовались 4.8, как последние. В скрипте соответственно используется
db4.8_load. Пробуем отконвертить logins.txt: 

    ::console
    ./convert.sh 

Если отработало без ошибок и появился файл logins.db, то версии Беркли
совпадают. Назначим ему права: 

    ::console
    $ chmod 600 logins.db 

Займемся аутентификацией пользователей. За это отвечает служба [PAM][]. Конфиги pam
для каждого клиента (в нашем случае клиент - это сервис vsftpd) лежат в `/etc/pam.d`. В vsftps.conf мы указали, как
наш файл для службы pam будет называться стройкой `pam_service_name=vsftpd`.
приведем его к следующему виду:

    ::conf
    # Standard behaviour for ftpd(8).
    #auth   required        pam_listfile.so item=user sense=deny file=/etc/ftpusers onerr=succeed

    # Note: vsftpd handles anonymous logins on its own. Do not enable pam_ftp.so.

    # Standard pam includes
    #@include common-account
    #@include common-session
    #@include common-auth
    # auth  required        pam_shells.so

    auth required /lib/security/pam_userdb.so db=/etc/vsftpd/logins
    account required /lib/security/pam_userdb.so db=/etc/vsftpd/logins

    #для x64 систем
    auth required /lib/x86_64-linux-gnu/security/pam_userdb.so db=/etc/vsftpd/logins
    account required /lib/x86_64-linux-gnu/security/pam_userdb.so db=/etc/vsftpd/logins

    #session    required     pam_loginuid.so

Важно, что кроме наших двух строк все остальное закомментировано!
Добавим единого пользователя линукс для всех наших "виртуальных" пользователей.
Его имя задано в vsftps.conf.

    ::console
    $ useradd -d /home/ftp virtual

Попробуем добавить нескольких пользователей: 

    ::console
    $ cd /etc/vsftpd
    $ ./create.sh vasya secretpassword 
    $ ./create.sh masha 123 

Смотрим, чтобы не было ошибок, нормальный вывод скрипта должен быть имя+пароль. Рестартим сервис

    ::console
    $ service vsftpd restart 

На этом все, коннектимся!

UPDATE for Ubuntu natty 11.04
--------------

После обновления до 11.04 natty не удается залогинится на ftp - password incorrect. Смотрим логи vsftpd:

    ::log
    vsftpd: PAM unable to dlopen(/lib/security/pam_userdb.so): /lib/security/pam_userdb.so: cannot open shared object file: No such file or directory

Видим, что PAM не находит библиотеку pam_userdb.so. Посмотрим, где находится эта библиотека в новой сборке:

    ::console
    $ updatedb
    $ locate pam_userdb.so
    /lib/x86_64-linux-gnu/security/pam_userdb.so

Обновим файл /etc/pam.d/vsftpd с новым путем к библиотеке. Так же, в
11.04 обновилась библиотека Berkeley DB до версии 5.1, так что мы тоже
обновимся: 

    ::console
    $ apt-get install db5.1-util

и меняем соответствующим образом скрипт `convert.sh`: `db4.8` заменяем на `db5.1`


  [pam]: http://ru.wikipedia.org/wiki/Pluggable_Authentication_Modules

UPDATE vsftpd 2.3.5
-------------------

В 2.3.5 Крис Эванс (Chris Evans) ужесточил политику безопасности для предотвращения эксплуатации потенциальной уязвимости, 
которая есть в старых версиях библотеки glibc. В итоге он запретил chroot() в каталог, в котором разрешена запись пользователю.

Теперь, если пользователь может писать в свою директорию (а не в поддиректории в ней) и при этом в нее 
выполняется chroot (то есть chroot_local_user=YES - пользователь не может по FTP подняться в / в отличие скажем от ssh), то тогда 
это потенциально небезопасно в связи с последними дырами в libc и следует не давать ему авторизацию.

В итоге virtual users в 2.3.5 не работают. Решить эту проблему без костылей можно только обновлением до версии 3.x.x и параметром в vsftpd.conf:

    allow_writeable_chroot=YES

