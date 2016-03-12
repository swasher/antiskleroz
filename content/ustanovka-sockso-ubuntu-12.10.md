Title: Sockso
Date: 2012-12-13 03:02
Tags: sockso, music
Category: Popcorn
Author: Swasher

Sockso кроссплатформенный сервер с открытым исходным кодом, предназначенный для хранения, организации и прослушивания музыки. Все что ему нужно для работы - установленная Java. Устанавливается все это довольно просто.

Качаем исходники

    ::console
    $ cd ~
    $ wget http://sockso.googlecode.com/files/sockso-1.5.3.zip

Распаковываем

    ::console
    $ unzip sockso-1.5.3.zip
    $ sudo mkdir /usr/share/sockso
    $ sudo cp -R sockso-1.3.5/* /usr/share/sockso/
    $ sudo mkdir /var/sockso
    $ sudo chmod -R 0755 /var/sockso


Устанавливаем яву. В Ubuntu 12.10 используется OpenJDK7 в качестве явы по-умолчанию.

>[UBUNTU Quantal Quetzal Release Notes][01] Java Toolchain.
>Ubuntu 12.10 ships OpenJDK7 as the default Java implementation. This brings improved performance, new features and better compatibility with other Java 7 implementations.
>Use of the OpenJDK6 is now deprecated and the openjdk-6-* packages in universe for Ubuntu 12.10 will not be provided in future releases of Ubuntu.

    ::console
    $ sudo apt-get install openjdk-7-jre-headless

Запускаем сервер

    ::console
    $ sudo sh /usr/share/sockso/linux.sh --nogui --datadir /var/sockso

Появляется приглашение sockso. Можно написать `help`, чтобы увидеть список возможных команд.
Пробуем добавить директорию с музыкой:

    ::console
    #SoCkSo#> coladd /home/swasher/music
    >Directory added!

Также на этом этапе необходимо добавить пользователя, чтобы позже можно было удаленно управлять сервером через веб-админку. Пользователь создается командой useradd, параметры - имя, пароль, email и последний параметр указывает является ли пользователь администратором (1 -да, 0 - нет).

    ::console
    #SockSo#>useradd swasher swasher_password swasher@mail.ru 1

После создания пользователя выходим

    ::console
    #SockSo#>exit

Скопируем стартовый скрипт

    ::console
    $ sudo cp /usr/share/sockso/scripts/init.d/sockso /etc/init.d/sockso.pl

Создадим файл для управления сервером `sudo nano /etc/init.d/sockso`

    ::bash
    #!/bin/bash
    perl /etc/init.d/sockso.pl $1

Поправим пути в стартовом скрипте `sudoedit /etc/init.d/sockso.pl`

    ::perl
    use constant SOCKSO_DIR => "/usr/share/sockso/";
    system( 'sh linux.sh --nogui --datadir /var/sockso > /dev/null 2>&1 &' );

И запустим сервер.

    ::console
    $ sudo chmod +x /etc/init.d/sockso
    $ sudo chmod +x /etc/init.d/sockso.pl
    $ sudo /etc/init.d/sockso start

Чтобы сервер стартовал автоматически можно выполнить следующее

    ::console
    $ sudo update-rc.d sockso defaults

Если вы ничего не меняли в конфигах, сервер будет доступен на порту 4444

Оригинал стаьи: [Установка сервера музыки Sockso на Ubuntu Server 11.04][02]

[01]:https://wiki.ubuntu.com/QuantalQuetzal/ReleaseNotes/UbuntuServer#QuantalQuetzal.2BAC8-ReleaseNotes.2BAC8-CommonInfrastructure.Java_Toolchain
[02]:http://jarmush.ru/record/43
