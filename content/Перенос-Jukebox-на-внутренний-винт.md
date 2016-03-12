Title: Перенос Jukebox на внутренний винт
Date: 2012-01-31 14:06
Category: Popcorn
Tags: jukebox, nmt, popcorn, rtorrent, yamj
Author: Swasher

Как известно, NMT в стандартной конфигурации не позволяет одновременно
подключать более одной шары. В следствии этого мы имеем
множество неудобств. В этой статье я описываю, как подключить несколько
шар одновременно. Кроме этого, у меня в NMT по случаю завелся внутренний
винчестер, и было решено перенести файлы Jukebox-а на этот винт, потому
как при разрастании стенки она стала притормаживать при чтении по сети.
Схему работы я разработал такую:

- rtorrent, закончив закачку, выполняет скрипт remove_mjbignore.sh. Этот скрипт создает флаг.
- Cron каждые 5 минут запускает скрипт yamj-update.sh
- Этот скрипт проверяет наличие флага, если флага нет, то ничего не происходит.
- Если флаг есть, то



    1. Выполняется проверка, не запущен ли скрипт уже 
    2. Удаляется флаг 
    3. Запускается yamj 
    4. Запускается синхронизация локального jukebox с удаленным на NMT 

Синхронизацию можно было делать двумя способами - или
установить на NMT сервис rsync, и запускать клиент на серваке, или наоборот, сервис rsync работает на сервере, а запускается клиент на
попкорне. Я выбрал второй вариант, из соображений экономии ресурсов на попкорне. Лишний демон будет постоянно кушать память. Первоначально я
использовал [скрипты LTU от Падавана][], но затем я отказался от них, по причине того, что они вносят слишком много ненужных мне изменений в
систему. Хотя среди них есть и полезные, как-то:

-   установка локали ru_RU.UTF-8
-   UTF8 в mc (вероятно, вследствии предыдущего пункта)
-   HDD\_SPINDOWN\_TIME=30 увеличивает время до остановки шпинделя
-   HDD\_APM\_DISABLE=1 HDD перестает парковать головки через каждые 8
    секунд бездействия. Позволяет остановить рост параметра
    Load\_Cycle\_Count
-   HDD\_AAM\_QUIET=1 Переводит Advanced Acoustic Management в тихий
    режим.

Эти нюансы надо будет проработать.

Мой выбор пал на opkg. [OPKG][]это очень легкий менеджер управления
пакетами. Синтаксис команд аналогичен дебиановскому apt-get.


Установка local opgp
-----------------------

Установку NMT community software installer я здесь не описываю, это
достаточно стандартная процедура, в интернете множество мануалов.
Устанавливаем через CSI пакет local (на данный момент local 0.1.8-nmt1).
Заходим телнетом на NMT и устанавливаем [dropbear][]- легковесный
ssh-сервер.

    opkg update
    opkg install start-stop-daemon
    opkg install dropbear

Теперь мы можем зайти ssh-клиентом. Порт по умолчанию установлен 2223, a
пароль - 1234. Первым делом мы меняем пароль рута. Он устанавливается
каждый раз при загрузке системы скриптом
/share/Apps/local/etc/init.d/51dropbear.sh в блоке

    if [ ! -f /etc/shadow.dropbear ]; then
        cp -f /etc/shadow /etc/shadow.dropbear
        echo -e "1234\n1234"|/usr/bin/passwd root
    fi

Далее по тексту используется стандартный пароль 1234

Установка NetworkMounter
---------------------------

[NetworkMounter][] это скрипт, который монтирует сетевые шары согласно
конфиг-файлу. Написано, что должен установливаться из репозиториев CSI,
однако у меня в Инсталлере его нет. Поэтому вот ссылка на архив
[NetworkMounterC200][]. Устанавливаем через CSI, заходим через ssh и
редактируем файл `/share/Apps/NetworkMounter/config.ini`. У меня выглядит
файл так:

    [Video]
    type= "nfs"
    path= "/share/Video"
    share= "192.168.0.20:/mnt/raid/video"
    user= ""
    password= ""
    options>= "tcp,rsize=32768,wsize=32768,rw,soft,nolock"

    [Music]
    type= "nfs"
    path= "/share/Music"
    share= "192.168.0.20:/mnt/raid/music"
    user= ""
    password= ""
    options>= "tcp,rsize=32768,wsize=32768,rw,soft,nolock"

    [Eversion]
    type= "nfs"
    path= "/share/Eversion"
    share= "192.168.0.20:/home/swasher/jukebox"
    user= ""
    password= ""
    options>= "tcp,rsize=32768,wsize=32768,rw,soft,nolock"

    [Liza]
    type= "nfs"
    path= "/share/Liza"
    share= "192.168.0.20:/mnt/raid/liza"
    user= ""
    password= ""
    options>= "tcp,rsize=32768,wsize=32768,rw,soft,nolock"


Как писал на форуме человек, приближенный к Syabas, якобы в NMT
используется только одна шара для экономии ресурсов. Не знаю, насколько
это соответствует действительности, по моему опыту ничего не тормозит,
но на всякий случай количеством шар не злоупотребляем, подключаем только
необходимое. Здесь у меня отдельные шары для фильмов - эта шара
используется Jukebox-ом, который лежит на внутреннем hdd, шара для
музыки, мультики дочери, и тестовая шара стенки на Java. Все шары
монтируются во внутренне пространство SATA (`/share/opt/sybhttpd/localhost.drives/SATA_DISK/`), таким образом, с точки
зрения NMT, эти все файлы расположены на внутреннем hdd.

Установка rsync
------------------

Со стороны NMT все банально: `opkg install rsync` Еще несколько
настроек, суть который объясняется далее. Создадим два файла, первый
файл просто содержит пароль для доступа к rsync серверу

    cd /share/Apps
    mkdir swasher
    touch pass
    echo "secretpass" > pass

Отредактируем `/share/start_app.sh`, добавляем chmod между маркером и
edit 0. Это нужно потому, что если у файла с паролем не выставлены
привелегии "только для рута", rsync его не пропустит.

    #M_A_R_K_E_R_do_not_remove_me
    chmod 600 /share/Apps/swasher/pass
    exit 0

На серверной машине устанавливаем сервис rsync apt-get install rsync и
настраиваем nano /etc/rsyncd.conf

    ::::bash
    #Файл приветствия
    #motd file = /etc/motd

    #Лог файл
    log file = /var/log/rsyncd.log

    #Писать в лог о скачивании файлов
    transfer logging = true

    #Описание секции
    [jukebox]
        # Комментарий
        comment = Jukebox directory
        # Путь к директории
        path = /home/swasher/jukesync
        # Под каким uid'ом работать
        uid = root
        # Только чтение
        read only = true
        # Разрешать просмотр файлов
        list = yes
        # Хосты, которым разрешен доступ
        hosts allow = 192.168.0.14
        # Разрешенные пользователи
        auth users = nmt
        # Путь к файлу с паролями
        secrets file = /etc/rsyncd.scrt

Затем создаем файл с логином и паролем
    
    ::::bash
    echo 'login:password' > /etc/rsyncd.scrt
    chmod 600 /etc/rsyncd.scrt
    chown root:root /etc/rsyncd.scrt

Логин мы используем в следующей строке(nmt), а пароль должен лежать в
файле на NMT (plaintext) и указываться через `--password-file=`. Забегая
вперед, скажу, что синхронизируемся мы такой строкой

    ::::bash    
    rsync -r -h --delete-before --whole-file --size-only -v --progress \
    --password-file=/share/Apps/swasher/pass nmt@192.168.0.20::jukebox /share/YAMJ/

Используемые ключи: 

* -r - синхронизировать источник и все вложенные папки (рекурсия) 
* -h - numbers is human redable 
* --delete-before - удаляем файлы, которые отсутствуют на источнике 
* --whole-file - отключаем delta-xfer алгоритм, передаем файл целиком. Увеличивается нагрузка на 
сеть, уменьшается на cpu 
* --size-only - сравниваем изменение файла только по размеру. Использование этой опции связано с особенностью YAMJ-а,
который каждый раз при запуске перезаписывает очень много не измененных служебных файлов. Время создания 
которых, конечно, меняется, и rsync их будет каждый раз синхронизировать. Можно было использовать --checksum,
но проверка контрольных сумм слишком нагружает процессор. Сравнение только по размеру чревато 
неточностями, понаблюдаю, как будет работать. Зато очень быстро. 
* -v --progress - вывод инфы в консоль (для отладки)

Советы по оптимизации rsync-а приветствуются!

Настройки для использования удаленного jukebox
-------------------------------------------------

Пути, которые нужно не забыть указать. в library.xml указываем, где
лежат фильмы и как эту папку видит NMT

    :::xml
    <libraries>
        <library>
            <path>/mnt/raid/video</path>
            <playerpath>file:///opt/sybhttpd/localhost.drives/HARD_DISK/Video</playerpath>
            <exclude name="sample,tmp/,temp/,RECYCLE.BIN/"/>
            <description></description>
            <prebuf></prebuf>
            <scrapeLibrary>true</scrapeLibrary>
        </library>
    </libraries>

 

Модификация скриптов rtorrent
--------------------------------

Тут все очень просто - нам нужно создать флаг в момент окончания
закачки. Для этого мы используем уже существующий скрипт `remove_mjbignore.sh` и приводим его к виду:

    ::::bash
    #!/bin/sh
    rm "${1}""/.mjbignore"
    touch /home/rtorrent/flag_new_present
    echo "${1}">/home/rtorrent/flag_new_present

Здесь мы создаем флаг `flag_new_present` и передаем в него имя
закачавшегося торрента.

Установка sshpass
--------------------

Так как RSA-аутентификацию для dropbear победить не удалось, используем
утилиту sshpass. Она позволяет прозрачно передавать пароль в ssh клиент,
что нам и требуется для написания shell-скрипта. С ubuntu 11.10 идет
версия sshpass 1.04 - она не рабочая. Качаем 1.05 с репозитория от
Ubuntu Precise Pangolin 12.04  [http://packages.ubuntu.com/precise/sshpass][] Устанавливаем
`dpkg -i sshpass_1.05-1_amd64.deb` Использование утилиты очень простое -
она передает пароль из параметра в ssh. Синтаксис:
`sshpass -p [yourpassword] ssh [yourusername]@[host]`

Скрипт запуска YAMJ
-----------------------

    ::::bash
    #!/bin/sh

    #############
    #CONFIG START
    #############

    #путь к yamj
    yamjdir=/home/swasher/yamj

    #путь к файлу флага-новые закачки, генерируется remove_mjbignore.sh
    semafor=/home/rtorrent/flag_new_present

    #куда складывать файлы джукбокса
    jukeboxdir=/home/swasher/jukesync

    #nmt ip
    ip=192.168.0.14

    ###########
    #CONFIG END
    ###########

    #Variables
    processname='MovieJukebox'

    cd ${yamjdir}

    #проверка, не запущен ли yamj уже
    if ps ax | grep -v grep | grep $processname > /dev/null 2>&1
    then
        #уже запущено - выходим
        exit 1;
    fi

    #Проверка, есть ли новые завершенные закачки
    if [ ! -e $semafor ]
    then
        # нет флага - выходим
        exit 0;
    fi

    #отчет о запуске
    movie=`cat ${semafor}`
    echo -e Started at `date -R` "\t" Movie is `basename "${movie}"`>> ${yamjdir}/updatejuke.log

    #запускаем yamj
    sh ${yamjdir}/MovieJukebox.sh -o ${jukeboxdir} -c ${yamjdir}/library_video.xml > null

    #в конце удаляем флаг
    rm /home/rtorrent/flag_new_present

    #проверка доступности NMT
    nmtstatus=$(ping -q -c 1 ${ip} | grep received | awk '{print $4}')

    #обновление удаленного jukebox
    if [ ! $nmtstatus -eq 0 ]; then
        #NMT is up
        sshpass -p 1234 ssh -p 2223 -l root ${ip} "/share/Apps/local/bin/rsync -r -h --delete-before --whole-file --size-only -v --password-file=/share/Apps/swasher/pass  nmt@192.168.0.20::jukebox /share/YAMJ/" > /home/swasher/yamj/rsync.log
    fi

Скрипт подробно комментирован. У меня он лежит в ~ и запускается
кроном каждые пять минут. Добавляем строку в crontab:
`crontab -u root -e` 

    ::::bash
    */5 * * * * /home/swasher/yamj/updatejuke.sh

Нерешенные вопросы - rsync без скрипта на NMT - авоторизация RSA



  [скрипты LTU от Падавана]: http://nmt200.ru/hand/padavan/linux-term-utils-v0-7
  [OPKG]: http://www.networkedmediatank.com/showthread.php?tid=45424&highlight=opkg
  [dropbear]: http://en.wikipedia.org/wiki/Dropbear_(software)
  [NetworkMounter]: http://www.networkedmediatank.com/showthread.php?tid=27011
  [NetworkMounterC200]: http://swasher.pp.ua/wp-content/uploads/2012/01/NetworkMounterC200.zip
  [http://packages.ubuntu.com/precise/sshpass]: http://packages.ubuntu.com/precise/sshpass
