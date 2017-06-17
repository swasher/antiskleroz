Title: Подключение из Pycharm к базе PostreSQL, находящейся в контейнере Vagrant
Date: 2017-06-17 23:51
Tags: pycharm, vagrant, postgres
Category: IT
Author: Swasher

Начинаем с проверки `pg_hba.conf`, там должна быть такая строка:

    host     <dbname>     <dbuser>    <ip-vagrant-machine>/16        md5
    
Далее, создаем новое подключение к базе данных и настраиваем ssh-туннель:

![](http://res.cloudinary.com/swasher/image/upload/v1497733119/blog/Data_Sources_and_Drivers_2017-06-17_23.57.33.png "SSH Tunnel")

В этом окне настривается ssh-туннель от PyCharm к Vagrant. Так как Vagrant у нас
локальный, то адрес - 127.0.0.1, порт - 2222, юзер - vagrant (если специально не 
менялось Vagrantfile). Далее указываем ключ, примерный путь, который лежит внутри 
проекта, что-то типа `C:\Users\<user>\PycharmProjects\<project>\.vagrant\machines\default\virtualbox\private_key`
Пасс-фраза для этого ключа - пустая.

Далее настраиваем доступ к самой базе:

![](http://res.cloudinary.com/swasher/image/upload/v1497733938/blog/Data_Sources_and_Drivers_2017-06-18_00.12.07.png "Postgres connect")

Здесь IP - это внутренний IP контейнера, он должен быть доступен с нашего десктопа, проверяем пингом.
Пользователь и пароль - от нашей базы данных.

Когда все настроено, нажимаем "Test connection" для проверки соеденения.

![](https://media.giphy.com/media/N2h8gg1FALgIM/giphy.gif)

