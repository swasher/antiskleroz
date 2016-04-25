Title: ODBC
Date: 2016-02-04 11:27
Tags: odbc, ubuntu, linux
Category: IT
Author: Swasher

Установка ODBC соеденения под UBUNTU: три способа

1 - Драйверы от Microsoft
=====================================================

#### Ссылки

[Welcome to the Microsoft ODBC Driver for SQL Server on Linux](https://msdn.microsoft.com/library/hh568451(SQL.110).aspx)

[System Requirements](https://msdn.microsoft.com/en-us/library/hh568452(v=sql.110).aspx)

[DOWNLOAD Microsoft® ODBC Driver 13 (Preview) for SQL Server® - Ubuntu Linux](https://www.microsoft.com/en-us/download/details.aspx?id=50419)

[Installing the Driver Manager](https://msdn.microsoft.com/en-us/library/hh568449(v=sql.110).aspx)

[Installing the Microsoft ODBC Driver for SQL Server on Linux](https://msdn.microsoft.com/en-us/library/hh568454(v=sql.110).aspx)

[Understanding difference between FreeTDS and unixodbc](http://stackoverflow.com/questions/31980980/difference-between-freetds-and-unixodbc)

###Installation steps:

- download Microsoft® ODBC Driver 13 (Preview)
- install Driver Manager
- install Microsoft ODBC Driver

#### Download Microsoft® ODBC Driver 13 (Preview)

Download ubuntu-version archive to home direcory

#### Install Driver Manager

Распковываем: tar xvzf msodbcsql-13.0.0.0.tar.gz

В образовавшейся директории есть файл `build_dm.sh`. Можно запустить `build_dm.sh` для
 установки Driver Manager

Чтобы увидеть список доступных опций, нужно выполнить  `build_dm.sh --help`

Копьютер должен иметь доступ к внешнем фтп, чтобы скачать и установить unixODBC-2.3.1.tar.gz.
Иначе смотрим инструкцию по ручной установке

Запускаем `build_dm.sh`

Вводим YES для продолжения и распаковки файлов. Процесс может занять до 5 минут.

После выполнения скрипта, следуем инструкциям на экране.

Обычно, скрипт пишет, в какую папку зайти и выолнить make install. Эту команду нужно выполнять от рута:

    sudo make install

На этом установка Драйвер Манагера закончена, переходим к установке ODBC драйвера.

#### Install Microsoft ODBC Driver

Возвращаемся в директорию с распакованным архивом.
Там будет файл `install.sh`, выполнив его, мы увидим список доступных опций.

Далее мануал советует сделать бекап файла `/etc/odbcinst.ini`. Если мы ставим на чистую систему, этот файл у нас
пустой. `odbcinst.ini` содержит список драйверов, которые зарегистрированы в `unixODBC Driver Manager`.

Расположение этого файла можно узнать, выполнив команду `odbc_config --odbcinstini`

Перед установкой драйвера полезно выполнить команду `./install.sh verify`. Вывод этой команды
покажет, имеет ли компьютер все зависимости, необходимые для установки ODBC driver on Linux.

    ::console
    $ ./install.sh verify

    Microsoft ODBC Driver 13 for SQL Server Installation Script
    Copyright Microsoft Corp.

    Starting install for Microsoft ODBC Driver 13 for SQL Server

    Checking for 64 bit Linux compatible OS ..................................... OK
    Checking required libs are installed ........................................ OK
    unixODBC utilities (odbc_config and odbcinst) installed ..................... OK
    unixODBC Driver Manager version 2.3.1 installed ............................. OK
    unixODBC Driver Manager configuration correct .............................. OK*
    Microsoft ODBC Driver 13 for SQL Server already installed ............ NOT FOUND

    Install log created at /tmp/msodbcsql.27823.3695.19034/install.log.

    One or more steps may have an *. See README for more information regarding
    these steps.

При этом в логе содержится следущее:

    $ cat install.log
    Verifying on a 64 bit Linux compatible OS
    Checking that required libraries are installed
    Verifying if unixODBC is present
    Verifying that unixODBC is version 2.3.1
    Checking if Microsoft ODBC Driver 13 for SQL Server is already installed in unixODBC 2.3.1

Я не уверен, что означет звезда около предпоследнего пункта, но думаю, это просто
предупреждение о том, что не установлен (пока)  Microsoft ODBC Driver.

Если все прошло хорошо, то запускаем установку драйвера командой `./install.sh install`

Нескольк секунд, и мы получаем отчет об успешной инсталляции:

    Enter YES to accept the license or anything else to terminate the installation: YES

    Checking for 64 bit Linux compatible OS ..................................... OK
    Checking required libs are installed ........................................ OK
    unixODBC utilities (odbc_config and odbcinst) installed ..................... OK
    unixODBC Driver Manager version 2.3.1 installed ............................. OK
    unixODBC Driver Manager configuration correct .............................. OK*
    Microsoft ODBC Driver 13 for SQL Server already installed ............ NOT FOUND
    Microsoft ODBC Driver 13 for SQL Server files copied ........................ OK
    Symbolic links for bcp and sqlcmd created ................................... OK
    Microsoft ODBC Driver 13 for SQL Server registered ................... INSTALLED

    Install log created at /tmp/msodbcsql.4459.5200.6685/install.log.

    One or more steps may have an *. See README for more information regarding
    these steps.

Приведу отрывок из лога. Видно, что куда копировалось:

    ::log
    Accept the license agreement
    License agreement accepted
    Verifying on a 64 bit Linux compatible OS
    Checking that required libraries are installed
    Verifying if unixODBC is present
    Verifying that unixODBC is version 2.3.1
    Checking if Microsoft ODBC Driver 13 for SQL Server is already installed in unixODBC 2.3.1
    /opt/microsoft/msodbcsql/13.0.0.0 exists
    /opt/microsoft/msodbcsql/13.0.0.0/en_US exists
    /opt/microsoft/msodbcsql/13.0.0.0/docs/en_US exists
    /opt/microsoft/msodbcsql/13.0.0.0/include exists
    Copying files
    Copying bin/bcp-13.0.0.0 to /opt/microsoft/msodbcsql/bin
    Setting permissions on bcp-13.0.0.0
    Copying bin/sqlcmd-13.0.0.0 to /opt/microsoft/msodbcsql/bin
    Setting permissions on sqlcmd-13.0.0.0
    Copying lib64/libmsodbcsql-13.0.so.0.0 to /opt/microsoft/msodbcsql/lib64
    Setting permissions on libmsodbcsql-13.0.so.0.0
    Copying install.sh to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on install.sh
    Copying build_dm.sh to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on build_dm.sh
    Copying README to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on README
    Copying LICENSE to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on LICENSE
    Copying WARNING to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on WARNING
    Copying INSTALL to /opt/microsoft/msodbcsql/13.0.0.0
    Setting permissions on INSTALL
    Copying bin/bcp.rll to /opt/microsoft/msodbcsql/13.0.0.0/en_US
    Setting permissions on bcp.rll
    Copying bin/SQLCMD.rll to /opt/microsoft/msodbcsql/13.0.0.0/en_US
    Setting permissions on SQLCMD.rll
    Copying bin/BatchParserGrammar.dfa to /opt/microsoft/msodbcsql/13.0.0.0/en_US
    Setting permissions on BatchParserGrammar.dfa
    Copying bin/BatchParserGrammar.llr to /opt/microsoft/msodbcsql/13.0.0.0/en_US
    Setting permissions on BatchParserGrammar.llr
    Copying lib64/msodbcsqlr13.rll to /opt/microsoft/msodbcsql/13.0.0.0/en_US
    Setting permissions on msodbcsqlr13.rll
    Copying don_US.tar.gz to /opt/microsoft/msodbcsql/13.0.0.0/docs/en_US
    Setting permissions on en_US.tar.gz
    Copying include/msodbcsql.h to /opt/microsoft/msodbcsql/13.0.0.0/include
    Setting permissions on msodbcsql.h
    Extracting documentation from /opt/microsoft/msodbcsql/13.0.0.0/docs/en_US/en_US.tar.gz


#### Путь для динамических библиотек

Как написано в инструкции, нам нужно включить /lib64 в пути поиска библиотек. В убунту для этого служит
директория /etc/ld.so.conf.d (не файл), из которой включаются все конфигурации. Создадим в этой директории
файл `lib64.conf` с простым содержимым: `/usr/lib64`. После выполним команду ldconfig и проверим, какие
библиотеки находятся командой

    $ ldconfig -p | grep odbc

Проверить, удачно ли зарегистрировался драйвер в системе, можно командой

     $ odbcinst -q -d -n "ODBC Driver 13 for SQL Server"

#### Создание DSN

dsn прописываются в файле odbc.ini, который может быть в /etc или в домашней папке.
В домашней директории пользователя создаем ~/.odbc.ini с таким содержимым

    [<DSN>]
    Driver = FreeTDS # как указано в odbcinst ??
    Servername = <SERVERNAME> # from freetds.conf
    Port = 1433
    Database = <DBNAME>

    [MyOdbcApp]
    Driver = ODBC

Строка Sevrer имеет такой [синтаксис](https://msdn.microsoft.com/ru-ru/library/ms130822.aspx):

     Server=[protocol:]Server[,port]

Параметр protocol может иметь значение tcp (TCP/IP), lpc (общая память) или np (именованные каналы).



Troubleshooting
------------------------------

##### Проверка доступности сервера

Клиент должен иметь возможность конектится к MSSQL серверу на нужный порт:

    $ telnet <IP> 1433
    Trying <IP>...
    Connected to <IP>


##### Отсутствие libgss3

При устновке на чистую Ubuntu 15.10 x64 Desktop вывод `./install.sh verify` показал следующее:

    ::console
    $ ./install.sh verify

    Microsoft ODBC Driver 13 for SQL Server Installation Script
    Copyright Microsoft Corp.

    Starting install for Microsoft ODBC Driver 13 for SQL Server

    Checking for 64 bit Linux compatible OS ..................................... OK
    Checking required libs are installed ................................. NOT FOUND
    unixODBC utilities (odbc_config and odbcinst) installed ............ NOT CHECKED
    unixODBC Driver Manager version 2.3.1 installed .................... NOT CHECKED
    unixODBC Driver Manager configuration correct ...................... NOT CHECKED
    Microsoft ODBC Driver 13 for SQL Server already installed .......... NOT CHECKED

    See /tmp/msodbcsql.29709.11575.1866/install.log for more information about installation failures.

А в логе был такой текст:

    ::console
    $ cat install.log
    [Чтв Фев 4 12:54:46 EET 2016] Verifying on a 64 bit Linux compatible OS
    [Чтв Фев 4 12:54:46 EET 2016] Checking that required libraries are installed
    [Чтв Фев 4 12:54:46 EET 2016] The libgss3 library was not found installed in \
        the package database.
    [Чтв Фев 4 12:54:46 EET 2016] See README for which libraries are required for \
        the Microsoft ODBC Driver 13 for SQL Server.

Видим наличие отсутствия библиотеки libgss3. Это Generic Security Services, содержится в universe репах.
Ставится просто

    $ sudo apt-get install libgss3

##### Error code 0x2746

Попытка приконектится к серверу с помощью утилиты isql звершается ошибкой 0x2746:

    ::console
    $ isql <dsn> sa password -vv
    [08001][unixODBC][Microsoft][ODBC Driver 13 for SQL Server]TCP Provider: Error code 0x2746
    [08001][unixODBC][Microsoft][ODBC Driver 13 for SQL Server]Client unable to establish connection
    [ISQL]ERROR: Could not SQLConnect

Посмотрим, что показывает трейс:

    ::console
    $ strace -e trace=network isql <dsn> sa password -vv
    socket(PF_LOCAL, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, 0) = 3
    connect(3, {sa_family=AF_LOCAL, sun_path="/var/run/nscd/socket"}, 110) = -1 ENOENT (No such file or directory)
    socket(PF_LOCAL, SOCK_STREAM|SOCK_CLOEXEC|SOCK_NONBLOCK, 0) = 3
    connect(3, {sa_family=AF_LOCAL, sun_path="/var/run/nscd/socket"}, 110) = -1 ENOENT (No such file or directory)
    socket(PF_INET, SOCK_STREAM|SOCK_CLOEXEC, IPPROTO_IP) = 4
    socket(PF_INET, SOCK_STREAM|SOCK_CLOEXEC, IPPROTO_TCP) = 4
    connect(4, {sa_family=AF_INET, sin_port=htons(1433), sin_addr=inet_addr("<REMOTE_IP>")}, 16) = 0
    setsockopt(4, SOL_TCP, TCP_NODELAY, [1], 4) = 0
    setsockopt(4, SOL_SOCKET, SO_KEEPALIVE, [1], 4) = 0
    setsockopt(4, SOL_TCP, TCP_KEEPIDLE, [30], 4) = 0
    setsockopt(4, SOL_TCP, TCP_KEEPINTVL, [1], 4) = 0
    getpeername(4, {sa_family=AF_INET, sin_port=htons(1433), sin_addr=inet_addr("<REMOTE_IP>")}, [16]) = 0
    getsockname(4, {sa_family=AF_INET, sin_port=htons(50172), sin_addr=inet_addr("192.168.0.249")}, [16]) = 0
    sendto(4, "\22\1\0004\0\0\1\0\0\0\37\0\6\1\0%\0\1\2\0&\0\1\3\0'\0\4\4\0+\0"..., 52, MSG_NOSIGNAL, NULL, 0) = 52
    recvfrom(4, "\4\1\0+\0\0\1\0\0\0\32\0\6\1\0 \0\1\2\0!\0\1\3\0\"\0\0\4\0\"\0"..., 4096, 0, NULL, NULL) = 43
    sendto(4, "\22\1\1C\0\0\0\0\26\3\1\0016\1\0\0012\3\3@\257S\20>EU<\317\t\236\222\221"..., 323, MSG_NOSIGNAL, NULL, 0) = 323
    recvfrom(4, "", 4096, 0, NULL, NULL)    = 0
    shutdown(4, SHUT_WR)                    = 0
    [08001][unixODBC][Microsoft][ODBC Driver 13 for SQL Server]TCP Provider: Error code 0x2746
    [08001][unixODBC][Microsoft][ODBC Driver 13 for SQL Server]Client unable to establish connection
    [ISQL]ERROR: Could not SQLConnect
    +++ exited with 1 +++

Убедимся, что odbc драйвер использует нужные файлы:

    ::console
    $ odbcinst -j
    unixODBC 2.3.1
    DRIVERS............: /etc/odbcinst.ini
    SYSTEM DATA SOURCES: /etc/odbc.ini
    FILE DATA SOURCES..: /etc/ODBCDataSources
    USER DATA SOURCES..: /home/swasher/.odbc.ini
    SQLULEN Size.......: 8
    SQLLEN Size........: 8
    SQLSETPOSIROW Size.: 8


##### Версия unix_odbc

В заметке [Installing the Driver Manager](https://msdn.microsoft.com/en-us/library/hh568449(v=sql.110).aspx) говорится,
что текущий (на 10.02.2016) релиз драйверов от Майкросовт работает только с версией unixODBC 2.3.1 и не поддерживает
версию 2.3.2+. Правильная версия должна установится автоматически скриптом `build_dm.sh`. Проверить текщую версию
можно командой

    $ odbc_config --version


2 - Использование FreeTDS
=========================

##### ССылки

[Confirm the installation](http://www.freetds.org/userguide/confirminstall.htm)
[Troubleshooting ODBC connections](http://www.freetds.org/userguide/odbcdiagnose.htm)

##### Install pre-requesite packages

    ::console
    $ sudo apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc

##### Версии пакетов

После установки проверяем версию FreeTDS драйвера

    ::console
    $ tsql -C
    Compile-time settings (established with the "configure" script)
                                Version: freetds v0.91
                 freetds.conf directory: /etc/freetds
         MS db-lib source compatibility: no
            Sybase binary compatibility: yes
                          Thread safety: yes
                          iconv library: yes
                            TDS version: 4.2
                                  iODBC: no
                               unixodbc: yes
                  SSPI "trusted" logins: no
                               Kerberos: yes

Тут мы видим два важных значения: директория для конфигурации freetds (`freetds.conf directory: /etc/freetds`) и
версию драйвера - `TDS version: 4.2`

##### Расположение конфигурационных файлов

    ::console
    $ odbcinst -j
    unixODBC 2.3.1
    DRIVERS............: /etc/odbcinst.ini
    SYSTEM DATA SOURCES: /etc/odbc.ini
    FILE DATA SOURCES..: /etc/ODBCDataSources
    USER DATA SOURCES..: /home/swasher/.odbc.ini
    SQLULEN Size.......: 8
    SQLLEN Size........: 8
    SQLSETPOSIROW Size.: 8



##### Создание /etc/odbcinst.ini

На этом этапе odbcinst.ini будет пустой. Этот файл выступает как провайдер имени odbc драйвера и
связывает имя драйвера с библиотекой (.so) драйвера, в нашем случае libtdsodbc.so. Найдем путь к найшей библиотеке,
обычно она находится в `/usr/lib/x86_64-linux-gnu/odbc/`:

    ::console
    $ sudo find / -name libtdsodbc.so
    /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so

Теперь мы может создать /etc/odbcinst.ini:

    ::ini
    [FreeTDS]
    Description = FreeTDS Driver v0.91 with protocol v7.2
    Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so
    Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so
    fileusage=1
    dontdlclose=1
    UsageCount=1


FreeTDS - это произвольное имя драйвера, которое будет использоватся при создании соеденений с сервером SQL


##### Now open /etc/freetds/freetds.conf and create a new section:

[leshafolc]
host = <IP>
Port = 1433
tds version = 7.1

Так мы создаем сервер (ServerName -> mssql) для использования в odbc.ini

В [одном мануале](http://blog.mattwoodward.com/2012/08/freetds-quick-start.html) сказано про версию tds:

>The tds version setting is specific to the version of SQL Server (or Sybase) to which you're connecting.
>Use 7.0 for SQL Server 7, 7.1 for SQL 2000, and 7.2 for SQL 2005 or 2008 (full details about TDS versions).

##### Тестирование

Пробуем подключиться к серверу с помощью утилиты tsql.

    $ tsql -S mssql -U sa -P <pass> -D <database>

Notes about these flags and values:

The -S flag for the "server" is referring to the alias you created in the configuration file above.
-U is the user name and -P is the password for the database to which you wish to connect.
-D is the database name you wish to use after connecting to the server. If you don't provide a database name, it will
connect to the default database for the user.

Если в freetds.conf будет неправльно указана версия драйвера, то мы можем получить такую ошибку:

Error 100 (severity 11):
    unrecognized msgno

Если нам удалось подключиться с помощью команды tsql -S, значит базовая инсталяция FreeTDS прошла успешно.
Теперь можно перейти к настройке ODBC



##### Создание /etc/odbc.ini

Этот файл также изначально пустой. Он служит для создания соеденения с конкретным сервером SQL, и также
для создания DSN. Как видно из вывода команды ` odbcinst -j`, используются два таких файла. Они нужно для
разделения system-wide подключений (например, веб-сервер), и user-wide подключений (пользовательские приложения).
Выбрав нужный файл, настраиваем соедение:

    [MyOdbcApp]
    Driver = FreeTDS
    Description = My Test Server
    Trace = No
    ServerName = leshafolc
    Port = 1433
    Database = testDB
    TDS_Version = 4.2 (This version is the same as reported by tsql -C command)

где test - имя dsn, а mssql - имя для установки параметров сервера в freetds.conf


##### Тестирование подключения, утилита osql

Утилита проверяет конфигурационные файлы

    $ osql -S <dsn> -U sa -P <pass>
    checking shared odbc libraries linked to isql for default directories...
    strings: '': Нет такого файла
        trying /tmp/sql ... no
        trying /tmp/sql ... no
        trying /etc ... OK
    checking odbc.ini files
        reading /home/swasher/.odbc.ini
    [MyOdbcApp] not found in /home/swasher/.odbc.ini
        reading /etc/odbc.ini
    [MyOdbcApp] found in /etc/odbc.ini
    found this section:
        [MyOdbcApp]
        Driver = FreeTDS
        Description = My Test Server
        Trace = No
        # servername link to freetds.conf
        ServerName = leshafolc
        Port = 1433
        Database = MyOdbcApp
        TDS_Version = 7.1
        UID = sa
        PWD = revolution1917
    looking for driver for DSN [MyOdbcApp] in /etc/odbc.ini
      found driver line: "	Driver = FreeTDS"
      driver "FreeTDS" found for [MyOdbcApp] in odbc.ini
    found driver named "FreeTDS"
    "FreeTDS" is not an executable file
    looking for entry named [FreeTDS] in /etc/odbcinst.ini
      found driver line: "	Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so"
      found driver /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so for [FreeTDS] in odbcinst.ini
    /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so is an executable file
    Using ODBC-Combined strategy
    DSN [MyOdbcApp] has servername "" (from /etc/odbc.ini)

Сначала утилита выдавала такую ошибку:

    looking for entry named [FreeTDS] in /etc/odbcinst.ini
      found driver line: "	Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so"
      found driver /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so for [FreeTDS] in odbcinst.ini
    /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so is not an executable file
    osql: error: no driver found for MyOdbcApp

Пришлось исправить это, сделав

    ::console
    $ chmod 645 /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so

то есть дав права на выполнение "всем", так как я запускаю osql от непривелигированного пользователя

Примеры команд, которые можно выполнить при успешном подключении

    ::console
    $ sp_databases


##### Тестирование подключения, утилита isql

Try isql -v dsn username password

Тестирование, утилита odbcinst

Драйвер:

    ::console
    $ odbcinst -q -d

Data source:

    ::console
    $ odbcinst -q -s

3 - Нативные windows-драйверы под wine
===============================

[How to get Wine, Windows MySQL Connector/ODBC and Ubuntu 13.10 to all be friends](http://www.sanitarium.co.za/how-to-get-wine-windows-mysql-connectorodbc-and-ubuntu-13-10-to-all-be-friends/)

**Install Ubuntu X.X (and update if needed)**

Use the default options with “Download updates while installing” ticked. If you plan
on using this as a desktop solution, perhaps install the 3rd Party App Support as well,
as it would take away a few steps later on.

**Install Wine 1.7.1 and Winetricks**

    ::console
    $ sudo add-apt-repository ppa:joe-yasi/yasi
    $ sudo add-apt-repository ppa:ubuntu-wine/ppa
    $ sudo apt-get update
    $ sudo apt-get install wine1.7 winetricks

**Install all the extra’s and default fonts using Wintricks CLI**

    ::console
    $ winetricks corefonts eufonts lucida opensymbol tahoma cjkfonts

Although installing the fonts is not required, it is suggested as the windows apps you
plan on using with the ODBC install will most likely require these fonts. If the font’s
your app requires are not included in the above list, include them or install them
later via the Winetricks UI.

**Install visual basic runtime**

    ::console
    $ winetricks vb6run

**Install Microsoft Data Access Components**

    ::console
    $ winetricks mdac28

Follow instructions as per installer. The 32bit Ubuntu may require the addition install
of mdac27 which is a manual process. Just follow the terminal instructions

**Install something libs**
Microsoft XML Core Services, Microsoft Foundation Classes, Microsoft Jet 4.0

    ::console
    $ winetricks msxml4 mfc42 jet40 native_oleaut32

**To use Windows ODBC drivers, you’ll have to override Wine’s odbccp32, odbc32 and
oleaut32 with their native versions, since the Wine versions are currently wired
directly to Linux’s unixodbc.**

You can do this with winecfg under the Libraries tab.

    ::console
    $ winecfg

**Manually download and install the MySQL ODBC Connector**

For this example, I will be installing version 5.1.13 32bit.

Go to [http://dev.mysql.com/downloads/connector/odbc/5.1.html](http://dev.mysql.com/downloads/connector/odbc/5.1.html)
and download the appropriate Windows MSI Installer version and install it:

    ::console
    $ wine msiexec /i mysql-connector-odbc-5.1.13-win32.msi

**Configure the data sources.**

    ::console
    $ wine control

And that is it, your Windows MySQL Connector for ODBC should now be functional!

Source: [Sanitaruim](http://www.sanitarium.co.za/how-to-get-wine-windows-mysql-connectorodbc-and-ubuntu-13-10-to-all-be-friends/)