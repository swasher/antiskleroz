Title: Установка на сервер ИБП Eaton
Date: 2012-11-26 13:36
Category: IT
Tags: nut, linux
Author: Swasher
Slug: install-ups-eaton

Эта заметка об установке ИБП [Eaton E-Series NV-600H] на Ubuntu Server 12.10 Quantal
x64 (ядро 3.5.0-18). В процессе написания статьи было принято решение
заменить UPS на [Powercom King Pro 1000-AP] с COM-портом. Поэтому
основная статья содержит информацию по Eaton'у, а в некоторых местах по
обоим УПС-ам. Заключительная глава содержит информацию, специфическую
для Powercom'a.

1. Подключаем ИБП к компьютеру
------------------------------

Если ИБП подключен к COM порту, то можно посмотреть номера COM портов
командой: `dmesg|grep ttyS`. Если ИБП подключен к USB порту, то можно
посмотреть какие устройства подключены к USB командами:
`lsusb`, `dmesg|grep USB`

2. Устанавливаем NUT
--------------------

Ставим пакеты (далее все от рута) 

    ::console
    $ apt-get update && apt-get install nut nut-cgi

3. Редактируем конфигурационные файлы NUT
-----------------------------------------

Назначение:

- **ups.conf** - настройки UPS драйвера для сбора данных
- **upsd.conf **- настройка основного демона upsd для Network UPS Tools.
- **upsd.users -** контроль доступа к UPS демону (профили пользователей)
- **upsmon.conf **- настройки монитора UPS демона 

Подключаем наш UPS к USB, смотрим вывод lsusb:

    ::console
    $ lsusb

    Bus 003 Device 002: ID 0665:5161 Cypress Semiconductor USB to Serial

#### /etc/nut/nut.conf

    MODE=standalone

Наш сервер upsd работает в автономном режиме

#### /etc/ups.conf

Ищем название драйвера для нашего упса на этой
[страничке]. Наш драйвер называется [blazer].

![Alt text](images/eaton-blazer-driver.png "Optional title")

Что мы и записываем в секции `[eaton]`.

    [eaton]
        driver = blazer_usb
        port = /dev/usb/hiddev0
        bus = "003"
        port = "002"
        vendorid = 0665
        productid = 5161
        desc = "my new ups Eaton Powerware E series NV600"

Остальные значения берем из `lsusb`.

### upsd.users

Контроль доступа до UPS-демона (профили пользователей). Именно в этом
файле вы указываете, кто и в какой мере будет контролировать и работать
с утилитой.

    [monuser]
        password = [PASS]
        actions = SET
        instcmds = ALL
        upsmon master


### upsd.conf 

**upsd** отвечает за передачу данных от драйвера
клиентским программам в сети. **upsd **должен находится под управлением
и, по возможности, как единственный источник состояния и мониторинга
клиентов, таких как**upsmon**. **upsd **использует этот файл для
контроля доступа к серверу и для установки других значений различных
конфигурации. Этот файл содержит подробные сведения об управлении
доступом, таким образом, обеспечивается безопасность.

    LISTEN 127.0.0.1 3493

### upsmon.conf

**upsmon** предоставляет основные функции, которая собирается найти в
программе мониторинга UPS, например это безопасное завершений работы при
сбое питания. В многоуровневой схеме утилиты NUT это клиент.

    ::plain
    MONITOR eaton@localhost 1 monuser [PASS] master

Здесь мы прописали в директиве MONITOR идентификатор ИБП Eaton (мы его
задавали в /etc/nut/ups.conf), далее через @ машину, на которой настроен
и запущен демон upsd (мы его настроили на предыдущем шаге), далее цифрой
1 мы указали количество потребителей, которое защищает наш ИБП (если
задать 0, то при отключении питания демон upsd будет сигнализировать,
однако выключать машину не будет, подробнее см. камменты в upsmon.conf);

далее идет имя пользователя и пароль, заданные в файле
/etc/nut/upsd.users; 

слово master задает, что данная машина будет
отключена последней (в случае, если конфигурация предусматривает ведомые
машины). 

Прописываем также директиву SHUTDOWNCMD в случае, если нам
нужно выключить машину в случае сбоя по питанию. 

Значение опций:

- MINSUPPLIES - указываем количество блоков питания которые должны
получать мощность сохраняя систему запущенной. Большинство систем имеют
один БП. Но мощные сервера, например HP NetServer LH4, могут работать с
2 из 4 БП и ему нужно ставить 2. 
- SHUTDOWNCMD - upsmon выполняет эту команду, когда систему необходимо выключить. 
- NOTIFYCMD - upsmon отправляет сообщение при происшествиях. 
- POLLFREQ - опрос мониторами с частотой (измеряется в секундах) для обычной деятельности. Вы можете
отрегулировать это частоту опроса, чтобы upsmon не “зашумлял” вашу сеть,
но не вносите слишком большие значения тк. оно может пропустить
отключение питания. 
- POLLFREQALERT - опрос UPS с частотой в секундах.
Можно сделать значение поменьше, чем POLLFREQ для лучшей
чувствительности работы батареи. 
- HOSTSYNC - как долго upsmon будет ждать перед переходом к следующему upsmon. master upsmon использует это число
при ожидании slaves чтобы отключиться после того как он установил флаг
принудительное завершение работы (FSD). И если slaves не отключаться
после этого тайм аута, то выключение продолжится без них. 
- DEADTIME - интервал ожидания перед объявлением статуса UPS как «мертвый». upsmon
требует, чтобы UPS предоставлял свою статус информацию, каждые несколько
секунд (см. POLLFREQ и POLLFREQALERT). Если статус загрузки, UPS помечен
fails. И если оно остается fails более чем DEADTIME секунд, то UPS
помечается «мертвый». 
- POWERDOWNFLAG - флаг файла для форсирования завершения работы UPS в master системе. 
- NOTIFYMSG - изменение сообщения, отправленные upsmon при возникновении определенных событий.
- NOTIFYFLAG - изменение поведения upsmon при возникновении событий NOTIFY. 
- RBWARNTIME - предупреждение замены аккумулятора в секундах.
- NOCOMMWARNTIME - предупреждение по времени при не общении к UPS в секундах. 
- FINALDELAY - через сколько секунд выполнить SHUTDOWNCMD после сообщения  сервером команды от упса NOTIFY_SHUTDOWN.

4. Установка прав
-----------------

Права на конфиги:

    ::console
    $ chown root:nut /etc/nut/* 
    $ chmod 755 /etc/nut
    $ chmod 644 /etc/nut/upsset.conf
    $ chmod 644 /etc/nut/hosts.conf
    $ chmod 644 /etc/nut/upsstats.html
    $ chmod 644 /etc/nut/upsstats-single.html

Это официальная инфа из файла `/usr/share/doc/nut-cgi/README.Debian`

A note on USB device permissions: you need to have udev rules refreshed.
Depending on your system and package versions, you may have to issue:

    ::console
    $ sudo udevadm trigger --subsystem-match=usb --action=change

and to unplug/replug your UPS USB cord. Then start nut using `service nut start`.


5. Запуск NUT
-------------

Запуск: `/etc/init.d/nut start`. Проверяем:

    ::console
    $ /etc/init.d/nut status

    Checking status of Network UPS Tools
    * upsd is running
    * upsmon is running

6. Проверка работы
------------------

Перезагружаемся. Или вместо перезагрузки можно сделать:

    ::console
    $ sudo udevadm control --reload-rules
    $ sudo udevadm trigger
    $ sudo service nut restart

Пробуем получить ответ от ups'а:

    ::console
    $ upsc eaton@localhost

    battery.voltage: 13.50
    battery.voltage.nominal: 12.0
    beeper.status: enabled
    device.type: ups
    driver.name: blazer_usb
    driver.parameter.bus: 003
    driver.parameter.pollinterval: 2
    driver.parameter.port: 002
    driver.parameter.productid: 5161
    driver.parameter.vendorid: 0665
    driver.version: 2.6.3
    driver.version.internal: 0.04
    input.current.nominal: 2.0
    input.frequency: 49.6
    input.frequency.nominal: 50
    input.voltage: 236.7
    input.voltage.fault: 236.7
    input.voltage.nominal: 230
    output.voltage: 237.2
    ups.delay.shutdown: 30
    ups.delay.start: 180
    ups.load: 7
    ups.productid: 5161
    ups.status: OL
    ups.temperature: 25.0
    ups.type: offline / line interactive
    ups.vendorid: 0665


Если ответ получен - значит половина дела сделана, связь с упсом есть. Если 
нет, копаем настройки, начиная с драйвера, порта и т.д. 

Далее необходимо проверить, работает ли принудительное завершение системы: 
`upsmon -c fsd`. Если все работает правильно, ОС завершит работу, компьютер 
будет принудительно отключен от
электросети (ИБП выключится). В зависимости от производителя, ИБП будет
оставаться выключенным от нескольких секунд до нескольких минут, затем
включится. Вывести список команд, поддерживаемых данным упсом:

    ::console
    $ upscmd -l eaton@localhost
    Instant commands supported on UPS [eaton]:

    beeper.toggle - Toggle the UPS beeper
    load.off - Turn off the load immediately
    load.on - Turn on the load immediately
    shutdown.return - Turn off the load and return when power is back
    shutdown.stayoff - Turn off the load and remain off
    shutdown.stop - Stop a shutdown in progress
    test.battery.start - Start a battery test
    test.battery.start.deep - Start a deep battery test
    test.battery.start.quick - Start a quick battery test
    test.battery.stop - Stop the battery test


Можно запустить, например, тест батареи, командой

    ::console
    $ upscmd -u monuser -p [PASS] eaton test.battery.start

После настройки, происходит следующее: при отключении питания, UPS
ждет пока напряжение battery.voltage упадет до
default.battery.voltage.low = 10.60, посылает команду выключить сервер.
И ждет возобновление подачи питания, как только в сети появляется
напряжение, он автоматически включает сервер.

7. Делаем автостарт NUT при загрузке системы
--------------------------------------------

In progress

8. Тестирование отключений и команды для отладки
------------------------------------------------

In progress - стоит копипаста!!!!!!!!!!! Сначала нужно посмотреть, как
будет вести себя upsdrvctl без фактического отключения системы. Для
этого используется параметр `-t`:

    upsdrvctl -t shutdown

Эмуляция сигнала Fast Shutdown FSD возникающего при малом
заряде батареи осуществляется следующей командой на сервере:

    upsmon -c fsd

Если все работает правильно, ОС завершит работу, затем компьютер будет
принудительно отключен от электросети (ИБП выключится). ~~***КОПИПАСТА В
зависимости от производителя, ИБП будет оставаться выключенным от
нескольких секунд до нескольких минут, затем включится. У меня ИБП
отключается через три минуты (настраивается в ИБП) и включается через
пару секунд.***~~ Использование драйвера для получения дополнительной
информации. В Ubuntu 12.10 драйвера лежат в /lib/nut. Получить помощь
можно с ключом -h:

    ./powercom  -h 
    ./blazer_usb  -h

Лог работы драйвера можно получить так:

    ::console
    $ blazer_usb -DDD -a eaton > eaton.log 2>&1

9. Установка и настройка http-сервера Lighttpd
----------------------------------------------

Включаем мод cgi:

    ::console
    $ lighty-enable-mod cgi

    Available modules: auth access accesslog cgi evasive evhost expire fastcgi flv-streaming no-www proxy rrdtool scgi simple-vhost ssi ssl status userdir usertrack fastcgi-php phpmyadmin debian-doc 
    Already enabled modules: auth fastcgi scgi phpmyadmin javascript-alias 
    Enabling cgi: ok
    Run /etc/init.d/lighttpd force-reload to enable changes

Перезапускаем веб-сервер `/etc/init.d/lighttpd force-reload`
Тут есть возможность сделать дыру в систему, связанную со скриптами cgi. Но мне
просмотр статистики "из-вне" не нужен, поэтому конфигурируем http сервер
так, что он будет доступен только изнутри офисной или домашней сети. Для
этого в локальный сервер DNS добавляем запись, связывающую наш сервер с
каким-то именем, например, nut.swasher.pp.ua. На моем Mikrotik-e это
выглядит как-то так: [![][1]][] Таким образом, по этому URL'у роутер
будет перенаправлять нас на сайт статистики, а снаружи злоумышленнику
будет попасть на него невозможно, так как в мире такой записи DNS не
существует, а сами файлы расположены вне основной web-директории. Можно
было написать короче, например nut.server или даже просто nut. Затем
добавляем в конфиг lighttpd.conf настройку нашего хоста
nut.swasher.pp.ua:

    ::lighttpd
    $HTTP["host"] =~ "nut.swasher.pp.ua" {
       server.document-root = "/usr/share/nut/www/"
    }

Пробуем зайти браузером.  

10. Дополнение - устанавливаем UPS Powercom KIN-1000AP и COM интерфейсом
------------------------------------------------------------------------

Смотрим, где висит наш сом-порт:

    ::console
    $ dmesg | grep tty

    [    0.000000] console [tty0] enabled
    [    0.942794] serial8250: ttyS0 at I/O 0x3f8 (irq = 4) is a 16550A
    [    0.964229] 00:08: ttyS0 at I/O 0x3f8 (irq = 4) is a 16550A


Соответствующий адрес com-порта смотрим в биосе. Обычно это /dev/ttyS0
Смотрим, под каким юзером у нас напущен демон upsd:

    ::console
    $ ps aux | grep ups
    root       348  0.0  0.0  17232   640 ?        S    19:48   0:00 upstart-udev-bridge --daemon
    root       624  0.0  0.0  15188   412 ?        S    19:48   0:00 upstart-socket-bridge --daemon
    nut       1170  0.0  0.0  17032   724 ?        Ss   19:48   0:00 /sbin/upsd
    root      1172  0.0  0.0  17000   812 ?        Ss   19:48   0:00 /sbin/upsmon
    nut       1174  0.0  0.0  17000   788 ?        S    19:48   0:00 /sbin/upsmon
    root      2944  0.0  0.0  17000   816 ?        Ss   21:12   0:00 upsmon
    nut       2945  0.0  0.0  17000   796 ?        S    21:12   0:00 upsmon
    root      3266  0.0  0.0   9404   876 pts/6    S+   21:32   0:00 grep --color=auto ups


Это пользователь **nut**. Устанавливаем нашему com-порту группу nut,
чтобы туда мог писать процесс: 

    ::console
    $ chown root:nut /dev/ttyS0


[Eaton E-Series NV-600H]: http://powerquality.eaton.ru/Products-services/Backup-Power-UPS/e-series-NV-UPS.aspx?cx=67  "Оффициальный сайт"
[Powercom King Pro 1000-AP]: http://powercom.ua/ru/products/item/23/
[http://www.networkupstools.org/stable-hcl.html]: http://www.networkupstools.org/stable-hcl.html
[blazer]: http://www.networkupstools.org/docs/man/blazer.html
[страничке]: http://www.networkupstools.org/stable-hcl.html
