Title: Обновление rtorrent с 0.8.6 до 0.8.9
Date: 2011-10-09 17:53
Category: Popcorn
Tags: rtorrent
Author: Swasher


Вобщем-то, обновление прошло нормально, но есть несколько моментов, на
которые необходимо обратить внимание. По порядку:

**0. Выключаем rtorrent**, также проверяем, чтобы он не подымался скриптом. Я делаю так:

    /etc/init.d/rtorrent stop
    cd /etc/init.d/
    mv rtorrent _rtorrent

После всех операций по обновлению переименовываем обратно.

**1. libtorrent** Все как обычно, подробно описано в [статье](|filename|Установка-rtorrent-rutorrent-на-ubuntu-server-10-04.md)  по установке
- скачиваем, распаковываем, компилируем, устанавливаем. Новая версия потребовала новых зависимостей - пакеты
libcppunit-1.12-1 и libcppunit-dev. Установим их 

    sudo apt-get install libcppunit-dev

**2. rtorrent** Обновление прошло без запинок. Запускаем в шелл rtorrent и смотрим, обновились ли версии libtorrent/rtorrent. 

**3. rutorrent** Обновляем из svn до версии 3.3:

    cd /var/www/rutorrent svn up 

**4. Плагины rutorrent** Так же обновляем из svn: 

    cd /var/www/rutorrent/plugins svn up \

* С обновлением все. Но возник еще один момент, требующий дополнительного разбирательства. В
предыдущей версии, был глюк с созданием папки при добавлении торрента.
Для решения этой проблемы в rtorrent.rc добавлялась следующая строка:

    system.method.set_key=event.download.inserted_new,create_struct,\
    "d.open= ; f.multicall=default,\"execute={sh,/home/rtorrent/creator.sh,\
    $f.get_frozen_path=}\""

а так же небольшой скрипт. В новой версии вроде бы это уже не работает,
- папки создаются нормально в штатном режиме, поэтому это строку надо
закаментировать. 

UPDATE 20.10.2011 
-----------------

Да, проблема появилась вновь -
фильмы, содержащие структуру папок, не стартуют из-за невозможности
создать папку с названием фильма. 

UPDATE 22.10.2011 
-----------------

С помощью уважаемого Novik-а проблема разрешилась - нужно убрать из этой строки подстроку
default, и в новом виде это будет выглядеть как

    system.method.set_key=event.download.inserted_new,create_struct,  
    "d.open= ; f.multicall=,\"execute={sh,/home/rtorrent/creator.sh,$f.get_frozen_path=}\""

Спасибо Novik!
