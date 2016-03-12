Title: Полезные команды и утилиты Linux
Date: 2010-09-23 13:06
Category: IT
Tags: linux, ubuntu
Author: Swasher
Slug: linux-commands


Общее
-----

Определить релиз системы

    ::console
    $ lsb_release -a

Узнать, где находится бинарник исполняемой команды

    ::console
    $ which ruby

Найти файл

    ::console
    $ find /var -name mod_magnet.so
    
    $ updatedb #обновляем базу
    $ locate mod_magnet.so 

Кто логинился, в какой терминал?

    ::console
    $ w
    $ last
    $ who -a

Сколько памяти? Сколько свопится?

    ::console
    $ free -m

Какой аптайм

    ::console
    $ uptime


Изменение редактора по-умолчанию

    ::console
    $ update-alternatives --config editor

Терминал (tty - это железный терминал через ядро, pts - эмулированный, например через ssh или mc)

    ::console
    $ tty


Сервисы
--------

Управление сервисами, cli. Так же можно включать/выключать 
автостарт, напр. `sysv-rc-conf ntp on `

    ::console
    $ sudo sysv-rc-conf

Железо
--------

Модель материнки, процессора, других железяк

    ::console
    $ dmidecode
    $ lspci

Правильно ли установлена сетевая карта? Полу-дуплекс? 10 мегабит? TX/RX ошибки?

    ::console
    $ ethtool eth0

Процессы
--------

Cписок запущенных процессов.

    ::console
    $ ps aux

Вместо довольно подробного `ps aux`, `pstree` показывает информащию о запущенных процессах в сжатом виде

    ::console
    $ pstree -a

Запуск процесса с пониженным или повышенным приоритетом ввода-вывода. Класс 1 для "real time", 2 для "best-effort", 3 для "idle".

    ::console
    $ ionice -c 3 programm_name -c

Пользователи и группы
---------------------

Список всех пользвоателей (системных и локальных)

    ::console
    $ awk -F":" '{ print "Linux_name: " $1 "\t\tFull_Name: " $5 }' /etc/passwd

В каких группах пользователь swasher?

    ::console
    $ groups swasher

Добавить пользователя в группу

    ::console
    # -a is important!
    $ usermod -aG group-name username  

Создать пользователя rtorrent, c комментарием (-с), пользовательской директорией (-d), которую нужно создать (-m), и с шеллом bash (-s)

    ::console
    $ useradd -c "Torrent User" -d /home/rtorrent -m -s /bin/bash rtorrent
    
Лог подключений к серверу
    
    ::console
    $ last


Сеть (web)
---------------

Как отключить IPv6 протокол

    ::console
    $ sudo nano /etc/default/grub
    > GRUB_CMDLINE_LINUX="ipv6.disable=1"
    $ sudo update-grub2 Check if IPV6

Проверить текущее состояние IPv6:

    :::console
    $ [ -f /proc/net/if\_inet6 ] && echo 'IPv6 ready system!' || echo 'No IPv6 support found!'

Поиск DNS имени по IP (запись name =)

    nslookup <IP>

Ping и traceroute в одном флаконе

    ::console
    mtr google.com
    
Как узнать свой внешний IP (на сайте ifconfig.me еще много примеров)

    ::console
    $ curl ifconfig.me

Аналогично определяется geo-ip информация
    
    ::console
    $ curl ipinfo.io
    
Ping плюс Trace в одном флаконе

    ::console
    $ mtr mail.ru


Сеть (ethernet)
--------------

В файле `/etc/network/interface` указываем адрес, маску и (если надо) шлюз

    ::config
    auto lo
    iface lo inet loopback 

    auto eth0
    iface eth0 inet static
    address 192.168.0.20
    netmask 255.255.255.0
    gateway 192.168.0.1

В файле `/etc/resolv.conf` указываем днс-сервер

    ::bash
    nameserver 8.8.8.8 #(это гугловский dns-сервер)

В Ubuntu с 12 версии изменился способ указания DNS. Теперь он указывается в файле `/etc/network/interface`:

    ::text
    dns-nameservers 24.56.100.20 192.168.69.2 208.67.222.222 208.67.220.220 8.8.8.8 8.8.4.4
    
Проверить открытые порты
    
    ::console
    $ nc -zv localhost 8070-8090    
    
Открытые порты (Listening services)

    :::console
    $ netstat -ntlp
    $ netstat -nulp
    $ netstat -nxlp

    keys:
    -n - использовать IP вместо имен (может быть более наглядно)
    -p - показывть PID и имя программы на сокете или порту
    -l - показывать только открытые порты
    -t - tcp, -u - udp, -x - Unix domain socket
    
Кто занимает/слушает порт
    
    ::console
    $ lsof -iTCP:80 -sTCP:LISTEN
    
Samba
-----

Сканирование подсети на наличие samba-ресурсов

    ::console
    nbtscan 192.168.0.0/24
    
Ресурсы на хосте

    ::console
    smbclient -U <user> -L <host>

Кто мастер-браузер?

    ::console
    nmblookup -M -
    
Монтирование (может понадобиться `apt-get install cifs.utils`)

    ::console
    mount -t cifs -o username=alexey //ALEXEY/work /mnt/work

Как сохранить executable bit при редактировании файлов через Samba? Archive=>Owner, System=>Group, Hidden=>World

    ::samba
    [data]
      path = /home/samba/data
      browseable = yes
      guest ok = yes
      writeable = yes
      map archive = no
      map system = no
      map hidden = no


Дисковая система
-------------------

Информация о HDD

    ::console
    $ hdparm -I /dev/sda #directly from drive
    $ hdparm -i /dev/sda #from kernel
    $ fdisk -l -u

Поиск всех дисковых устройств

    ::console
    $ blkid

Активность процессов в записи/чтении на диск. Ключи `-o` только активные процессы/нити, `-P` -только процессы

    ::console
    $ iotop

Примонтировать ISO

    ::console
    $ mount -o loop some.iso /mnt/point

Удаление Partition Table

    ::console
    $ dd if=/dev/zero of=/dev/sda count=1 bs=1k

Тест скорости чтения

    ::console
    $ hdparm -t /dev/sdb 

Тест скорости чтения посредством dd

    ::console
    $ dd if=/dev/sdb of=/dev/null bs=128K count=20000

Тест скорости записи посредством dd

    ::console
    #убивает раздел, запись производится на физический диск
    $ dd if=/dev/zero of=/dev/sdb bs=128K count=20000
    #безопасно, запись в файл
    $ dd if=/dev/zero of=/mnt/hd/000.dd bs=128K count=100000

Статистика по утилизации дисков. Показать шесть отчетов с двухсекундным интервалом для всех устройств. 

    ::console
    $ iostat -d 2 6


Файловая система
----------------

Какой процесс использует данный файл?

    ::console
    $ lsof /etc/passw
    
Свободное место на винчестерах. Ключи `-h` human-readable, `-T` вывод типов файловых систем

    ::console
    $ df -h
        
Сколько весит папка? Ключ `-h` правильно сортирует human-readable формат
        
    ::console
    $ du -h --max-depth=1 | sort -h
    
Рекурсивно сравнить две директории и найти все отличающиеся файлы (длинные ключи `--brief --recursive`) 

    ::console
    $ diff -qr dir1/ dir2/


iSCSI
-----

Обнаружить таргеты на удаленном сервере

    ::console
    iscsiadm -m discovery st -p 192.168.0.1 -t st

Вывести список уже подключенных таргетов (опция -P3 - подробный вывод, в конце вывода можно увидеть, какое блочное устройство какому target'у принадлежит).

    ::console
    iscsiadm -m session -P3

Вылогиниться из конкретного таргета

    ::console
    iscsiadm - m session -u -T iqn.2011-09.example:data

Залогиниться во все обнаруженные target'ы

    ::console
    iscsiadm -m node -l

Вылогиниться из всех target'ов

    ::console
    iscsiadm -m node -u

XFS
---

Проверить фрагментацию файла

    ::console
    $ xfs_bmap -v
    #где point - файл возвращает список занимаемых екстентов.

Проверка фрагментации файловой системы

    ::console
    $ xfs_db -c frag -r /dev/hdd1

Дефрагментация

    ::console
    $ xfs_fsr -v 
    #где point -файл, точка монтирования или устройство. Может производится онлайн. 

Дефраг через крон

    ::txt
    30 1 * * * root /usr/sbin/xfs_fsr -t 21600 >/dev/null 2>&1 
    #запускать каждую ночь в 1:30 на шесть часов (опция -t 21600(сек)) 

Предотвращение дефрагментации при монтировании `/etc/fstab`. Устанавливает размер екстента в 512 метров 

    ::bash
    /dev/hda3 /myth xfs defaults,allocsize=512m 0 0 

Опции монтирования для увеличения быстродействия. Отменяет обновление метаданных о времени доступа к файлам и директориям

    ::bash
    /dev/hda3 /myth xfs noatime,nodiratime,allocsize=512m 0 0 


Восстановление при наличии сбоев или противоречий. Производится только на отмонтированной ФС, желательно в single mode (telinit 1)

    ::console
    $ telinit 1 
    $ umount /dev/hda3
    $ xfs_repair /dev/hda3


Btrfs
------------------

**Я получаю ошибку "No space left on device", но df сообщает о достаточном свободном месте.**

Прежде всего, проверьте, сколько места было выделено в файловой системе:

    ::console
    $ sudo btrfs fi show
    Label: 'media'  uuid: 3993e50e-a926-48a4-867f-36b53d924c35
    Total devices 1 FS bytes used 61.61GB
    devid    1 size 133.04GB used 133.04GB path /dev/sdf

Отметим, что в этом случае, все устройства в файловой системе используются полностью. Это ваша первая подсказка.
Затем проверим, сколько использовано места под метаданные:

    ::console
    $ sudo btrfs fi df /mount/point
    Data: total=127.01GB, used=q56.97GB
    System, DUP: total=8.00MB, used=20.00KB
    System: total=4.00MB, used=0.00
    Metadata, DUP: total=3.00GB, used=2.32GB
    Metadata: total=8.00MB, used=0.00

Обратите внимание, что значение **Metadata used** довольно близко (75% или более) к заполнению, но есть много места под данные.
А произошло то, что файловая система выделила все доступное место для данных или метаданных, 
а затем одно из них заполнилось (как правило, это просиходит с метаданными). На данный момент, эту проблему можно решить, 
запустив частичную балансировку:

    ::console
    $ sudo btrfs fi balance start -dusage=5 /mount/point

Обратите внимание, что не должно быть пробела между -d и usage. Эта команда будет пытаться переместить данные 
в пустые или почти пустые чанки данных, что позволяет восстановить свободное пространство для метаданных. Дополнительную 
информацию можно получить по ссылкам: [что делает балансировка] и [опции балансировки]

NFS
---------------

Очистить все шары, затем расшарить только то, что прописано в exportfs

    ::console
    exportfs -au
    exportfs -a


Cron
---------------

Для редактирования файла кронтаба используем команду `crontab -e`. Этой
командой мы открываем для редактирования файл crontab для текущего
пользователя. Если нашему скрипту нужны права супер пользователя, то
нужно редактировать crontab суперпользователя. Делается это командой `sudo crontab -u root -e`. 
Ну а если заменить root на логин другого пользователя, мы сможем редактировать чужой crontab.

Чтобы посмотреть файлcrontab введите команду `crontab -l`. Файл crontab имеет следующую структуру:

    ::bash
    поле1 поле2 поле3 поле4 поле5 команда

Значения первых пяти полей:

1. минуты— число от 0 до 59
2. часы — число от 0 до 23 
3. день месяца — число от 1 до 31 
4. номер месяца в году — число от 1 до 12
5. день недели — число от 0 до 7(0-Вс,1-Пн,2-Вт,3-Ср,4-Чт,5-Пт,6-Сб,7-Вс)

Все поля обязательны для заполнения. Не сложно догадаться что первые 5 отвечают за определения
периодичности запуска команды, а последняя собственно команда или полный
путь к скрипту. Таким образом, чтобы запустить наш скрипт резервного
копирования раз в 10 минут надо вписать следующую строчку:

    ::bash
    */10 * * * * /home/user/backup-script 

**\*** (звездочка) - обозначает все возможные варианты, - то есть, например, если **\*** стоит в дне недели, то это эквивалентно записи 1,2,3,4,5,6,7

/ (прямой слеш) служит для определения периодичности выполнения задания. Например, если нужно будет выполнять скрипт раз в 3 часа, пишем в поле часы `*/3`, а в минуты просто *, если раз в сутки — пишите */23, ну почти сутки.
Так же в одно поле можно вводить несколько значений через запятую, например если хотите выполнять скрипт 1-го, 5-го, и 25-го числа каждого месяца
введите 1,5,25 вместо третей звёздочки. Ещё можно вводить промежуток времени, если, допустим, в часы ввести 12-17 то скрипт будет выполняться
с 12 до 17 включительно раз в час. Ну вот и всё, в заключение несколько примеров:

    ::console
    min   hour    DoM   MoY   DoW      Command
    0      */3    *     *     2,5   /script    #Каждые три часа только по вторникам и пятницам
    15     */3    *     *     *     /script    #Каждые три часа в 15 минут
    45     15     *     *     1     /script    #По понедельникам в 15:45
    13     13     13    *     5     /script    #в пятницу 13 числа в 13 часов 13 минут
    30     00     *     *     0     /script    #Раз в неделя по воскресеньем в 00:30



Apt
--------------------------

Основные команды

    ::console
    $ apt-get update 
    $ apt-get upgrade
    $ apt-get install <package>
    $ apt-get remove [--purge] <package>  # purge для удаления конфигурации
    $ apt-get dist-upgrade                # В UBUNTU ЛУЧШЕ ИСПОЛЬЗОВАТЬ do-release-upgrade 

При применении pinning, просмотреть источник пакета

    ::console
    $ apt-cache policy exim4-daemon-light

Поиск пакетов

    ::console
    $ dpkg --list              #Установленные пакеты
    $ apt-cache search <regex> # Полнотекстовый поиск по всем доступным пакетам (имя и описание)
    $ apt-cache pkgnames       # Все доступные пакеты
    $ apt-cache pkgnames ssh   # Все доступные пакеты, начинающиеся на ssh

Информация о пакетах и обслуживание apt

    ::console
    $ apt-cache show vsftpd # Инфа о пакете
    $ apt-cache stats       # Статистика кеша
    $ apt-get clean         # Удаление полученных deb-файлов
    $ apt-get autoremove    # Удаление завиисмостей после удаления их родительского пакета
    $ apt-get check         # Диагностика и проверка зависимостей   
          
    
Проапгрейдить LTS до Normal
    
    ::console
    $ apt-get install update-manager
    $ nano /etc/update-manager/release-upgrades
    Prompt=normal

#####Pinning
Поставить пакет из следующего релиза (на примере trusty (след. релиз - utopic), и 
пакета ghostscript:

    ::bash
    # Смотрим, какой пакет предлагается текущим релизом

    $ apt-cache policy ghostscript
    ghostscript:
      Installed: (none)
      Candidate: 9.10~dfsg-0ubuntu10.2
      Version table:
         9.10~dfsg-0ubuntu10.2 0
            500 http://ua.archive.ubuntu.com/ubuntu/ trusty-updates/main amd64 Packages
         9.10~dfsg-0ubuntu10 0
            500 http://ua.archive.ubuntu.com/ubuntu/ trusty/main amd64 Packages

    # Версия пакета - 9.10

    # Создаем файл `/etc/apt/preferences.d/ghostscript` 
    Package: ghostscript
    Pin: release a=utopic
    Pin-Priority: 10
    
    # Смотрим, в какой секции содержится нужный пакет. 
    # Если секция явно не указана, то это main
    apt-cache show ghostscript | grep Section
    
    # добавляем репы utopic main в source.list.
    deb http://ua.archive.ubuntu.com/ubuntu/ utopic main restricted
    deb-src http://ua.archive.ubuntu.com/ubuntu/ utopic main restricted
    
    #update и проверяем
    $ apt-get update
    $ apt-cache policy ghostscript
    ghostscript:
      Installed: 9.10~dfsg-0ubuntu10
      Candidate: 9.14~dfsg-0ubuntu3
      Package pin: 9.14~dfsg-0ubuntu3
      Version table:
     *** 9.14~dfsg-0ubuntu3 10
            500 http://ua.archive.ubuntu.com/ubuntu/ utopic/main amd64 Packages
            100 /var/lib/dpkg/status
         9.10~dfsg-0ubuntu10.2 10
            500 http://ua.archive.ubuntu.com/ubuntu/ trusty-updates/main amd64 Packages
         9.10~dfsg-0ubuntu10 10
            500 http://ua.archive.ubuntu.com/ubuntu/ trusty/main amd64 Packages
            
    # Видно, что теперь кандидат на установку - версия 9.14. Можно устанавливать:
    $ apt-get install ghostscript

Bash, команды и приемы
------------------------

Выполнение последней команды с правами рута

    ::console
    $ sudo !!
    
Если зажать Alt или Esc и нажимать точку, мы будем перебирать последние введнные аргументы 
командной строки. Например

    ::console
    $ touch file.txt
    $ nano <Alt-.>
    
Если в начале команды поставить пробел, она не запишется в history. Полезно скрывать команды 
с кофеденциальной информацией

    ::console
    $   mount -t cifs -o username=user,password=SeCrEtPaSsWoRd //share /mnt
    
Замедление вывода. 50 - байт в секунду 
    
    ::console
    $ dmesg | pv -qL 50

Форматирование вывода колонками
   
    ::console
    $ mount | column -t

Очистка экрана - всместо `clear` можно просто нажать `Ctrl-l`

    Ctrl-l
    
Определить тип файла.
    
    $ file my.pdf
    my.pdf: PDF document, version 1.4

Bash, рецепты
-----------------------

Проверить, поднят ли компьютер в сети

    ::console
    nmtstatus=$(arp -v ${ip} | grep Found | awk '{print $6}')

Заменить расширение по шаблону, рекурсивно с текущей папки:

    ::console
    #Работает плохо, файл nf.nf.nf переименует в nfo.nf.nf
    #нужно пофиксить
    find . -type f -iname "*.nf" -exec rename 's/nf/nfo/' {} \;

Заменить рекурсивно права только для файлов или только для директорий

    ::console
    $ find /path/to/base/dir -type d -exec chmod 755 {} + #для директорий
    $ find /path/to/base/dir -type f -exec chmod 644 {} + #для файлов

    Or, if there are many objects to process:

    $ chmod 755 $(find /path/to/base/dir -type d)
    $ chmod 644 $(find /path/to/base/dir -type f)

    Or, to reduce chmod spawning:

    $ find /path/to/base/dir -type d -print0 | xargs -0 chmod 755 
    $ find /path/to/base/dir -type f -print0 | xargs -0 chmod 644

Заменить строку в конфиге

    ::perl
    perl -pi -e "s/X11Forwarding yes/X11Forwarding no/g" /etc/ssh/sshd_config

Если что-то пошло не так, можно проанализировать переменную `$?`

    ::console
    apt-get install rar
    if [ $? -gt 0 ]; then
      set +x verbose
      echo *** ERROR ***
      echo "Looks like something is wrong with apt-get install, aborting."
      set -e
      exit 1
    fi

Получить IP адрес

    ::console
    IPADDRESS1=`ifconfig | sed -n 's/.*inet addr:\([0-9.]\+\)\s.*/\1/p' | grep -v 127 | head -n 1`

Выполнить слудещую команду при (не-)удачном завершении предыдущей

    ::console
    $ apt-get install aaabbb && echo 1 || echo 2

Сортировка

    ::console
    # Сортировка по human-readable размеру директорий
    du -h --max-depth=1 | sort -h
    # Сортировка по столбцу. Опция n (numeric) обязательна для чисел
    ls -l | sort -nk5
    
Архитектура

    ::console
    $ getconf LONG_BIT
    32

Мониторинг и статистика
-----------------------

Мониторинг загрузки канала в реальном времени
    
    ::console
    $ iftop

Что является причиной нагрузки на сервер? Какая средняя нагрузка?

    ::console
    $ top
    $ htop

Мониторинг любых подсистем в реальном времени. Поддерживает плагины

    ::console
    $ dstat --cpu --disk -D total --mem --net

Мониторинг загрузки сети по процессам

    ::console
    $ nethogs

fdisk c визуализацией

    ::console
    $ cfdisk

Анализ размеров директорий (ncurses)

    ::console
    $ ncdu

Python
------

Какая дата была N дней назад (или через N дней)

    ::python
    >>> from datetime import date, timedelta
    >>> print date.today()-timedelta(days=45)
    2013-01-28
    
Быстро поднять веб-сервер в текущей директории на 8000 порту

    ::console
    $ python -m SimpleHTTPServer

[что делает балансировка]: https://btrfs.wiki.kernel.org/index.php/FAQ#What_does_.22balance.22_do.3F
[опции балансировки]: https://btrfs.wiki.kernel.org/index.php/Balance_Filters