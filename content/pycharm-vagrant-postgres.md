Title: Подключение из Pycharm к PostreSQL в контейнере Vagrant
Date: 2017-06-17 23:51
Tags: pycharm, vagrant, postgres
Category: IT
Author: Swasher

Начинаем с проверки `pg_hba.conf`, там должна быть такие строки:

    host     <dbname>     <dbuser>    <ip-vagrant-machine>/16        md5
    host     <dbname>     <dbuser>    ::1/128                        md5
    
Далее, создаем новое подключение к базе данных и настраиваем ssh-туннель:

{% img lb-image  http://res.cloudinary.com/swasher/image/upload/v1497733119/blog/pycharm_postgres_ssh.png 750 SSH %}

В этом окне настривается ssh-туннель от PyCharm к Vagrant. Так как Vagrant у нас
локальный, то адрес - 127.0.0.1, порт - 2222, юзер - vagrant (если специально не 
менялось Vagrantfile). Далее указываем ключ, примерный путь, который лежит внутри 
проекта, что-то типа 
    
    ::console
    C:\Users\<user>\PycharmProjects\<project>\.vagrant\machines\default\virtualbox\private_key

Пасс-фраза для этого ключа - пустая.

По неизвестной причине, иногда аутентификация с помощью ключа не проходит, тогда изменяем
`Auth type` на `password` и используем логин:пароль `vagrant:vagrant`.

Далее настраиваем доступ к самой базе:

{% img lb-image  http://res.cloudinary.com/swasher/image/upload/v1497733938/blog/pycharm_postgres_general.png 750 General %}

Здесь IP - это внутренний IP контейнера, он должен быть доступен с нашего десктопа, проверяем пингом.
Пользователь и пароль - от нашей базы данных.

Когда все настроено, нажимаем "Test connection" для проверки соеденения.

![](https://media.giphy.com/media/N2h8gg1FALgIM/giphy.gif)

