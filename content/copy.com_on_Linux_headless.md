Title: How to install Copy.com on a headless linux
Date: 2016-01-17 20:48
Tags: copy.com
Category: IT
Author: Swasher


На форуме copy.com есть интересные [топик](https://community.barracudanetworks.com/forum/index.php?/topic/27350-copycom-command-line-interface/). На вопрос о том, где же документация по command-line
 интерфейсу, Barracuda Team Members по имени Michael Potter недвусмысленно ответил:
 
> We do not have documentation for this but you can refer ti this [link](https://nowhere.dk/articles/installing-and-running-copy-com-agent-on-a-headless-ubuntudebian-linux
)

Ну что ж, как послали, так послали...

В этой заметке мы посмотрим, как установить клиент `copy.com` на безголовый линукс сервер, а именно Ubuntu 15.10 Wily x64.

Установка из ppa
----------------

Для ubuntu поддерживается [ppa-репозиторий](http://paolorotolo.github.io/copy/), но ничего не мешает скачать архив с 
офф. сайта и использовать его.
Я все же предпочитаю установку из пакетов:

    ::console
    $ sudo apt-add-repository ppa:paolorotolo/copy 
    $ sudo apt-get update 
    $ sudo apt-get install copy
    

Первый запуск
---------------------

Идем в `/opt/copy-client` и наблюдаем там пачку файлов, в числе которых есть три исполняемых, и вот 
для чего они нужны (текст, найденый в скачанном с copy.com тарболе):

    To use Copy in Linux, install this tarball wherever you like. There are three
    binaries available for use, described below.
    
    1.  CopyAgent – This is a QT based UI application for the Linux GUI; it acts
        as a tray application, just like the Mac and Windows versions.
    1.a     You can install overlays on certain version of Nautilus, by
            running as root ./CopyAgent –installOverlay.
    
    2.  CopyConsole – This is a headless version of the Copy app. It can run
        in a terminal or as a background process.
    2.a     This version won't have a login prompt, so if you haven't logged
            in before you'll need to provide at minimum a username and Copy
            folder location. If a password isn't provided at the command line,
            it will be prompted for. Example:
            CopyConsole -username=<email> -root=/home/<user>/Copy
    2.b     If you have previously logged in, either with CopyAgent or
            CopyConsole, then no special arguments are required.
    2.c     For more options, run: CopyCommand -help
    
    3.  CopyCmd – This is a tool that provides commandline APIs into various
        aspects of the Copy app. You can do cool things like create a link
        URL to a file in your account or upload a file directly into
        the cloud.
    3.a     For a full list of commands, run: CopyCmd -help
    3.b     Several commands require a [path] as an argument. All such paths
            must begin with / and are relative to your Copy folder. For
            example, if your Copy folder contains a subdirectory called Foo,
            and inside that is a file called Bar, then the [path] argument
            needed to refer to file Bar would be /Foo/Bar.

То есть, CopyAgent - gui утилита, это не про нас. CopyCmd - выполняет различные команды, например, можно залить файл в облако,
или скачать его, установить или убрать оверлейную иконку, обозначающую синхронизированные файлы, а так же фунции
отладки и аутентификации.

Нас же интересует команда CopyConsole.  

Посмотрим, какую информацию даст хелп от CopyConsole:

    $ ./CopyConsole -h
    Error: The specified option is not supported
    
    CopyConsole - Run a console-only Copy agent
    usage: CopyConsole [ -appdata | -daemonize | -debugOutput | -debugToConsole
                       | -password | -root | -username ]
    
    Options: 
        -[ appdata | data ]  Location of Copy application data directory
        -[ daemonize | daemon ]  Daemon mode
        -[ debugOutput | debug ]  Enable debug message masks
        -[ debugToConsole | consoleOutput | console ]  Logs debug to output
        -[ password | pass | p ]  Password for the login
        -[ root | r ]  Location of Copy root directory
        -[ username | user | u ]  Login to the cloud as this user

Странно, что утилита не имеет никаких help ключей, но введя неправильный ключ, можно увидеть справку.

Попробуем запустить клиент, указав логин (почту), пароль, и корневую директорию для синхронизации: 

    ::console
    $ /opt/copy-client/CopyConsole \
        -u=the_mail_you_signed_up_with \
        -r=/home/your_linux_username/copy \
        -p=the_password_you_signed_up_with
    Failed to write status file: Exception - Description: File not \
        found (/home/swasher/.copy/status.txt) Original: 25 Mapped: 25 Location: \
        Open:/home/jenkins/workspace/Copy_Agent_Linux-1.4/libbrt/Brt/File/YFile.cpp:48
    Using profile /home/swasher/.copy/config.ini
    User from cmdline <the_mail>
    Root from cmdline /home/swasher/Music
    Password from cmdline
    Starting copy...success
    Logged in as user: <the_mail> Copy folder is: '/home/swasher/Сopy'
    Press enter to exit
    Syncing
    Scanning for changes
    All files up to date
    
Отлично! В папке ~/.copy у нас появились разные служебные файлы - настройки, сокет и др., а в папке Copy - 
синхронизировались файлы из аккаунта Copy. Теперь синхронизация будет продолжаться, пока мы не нажмем Ctrl-C, прервав синхронизацию.
 
Демон
---------------------

Осталость сделать так, чтобы наша синхронизация запускалась и работала как демон.

Параметры входа в аккаунт, которые мы указали, сохранятся для текущего юзера в ~/.copy, и будут использованы при следующем запуске.
Так демон сможет автоматически логинится.

Утилита `CopyConsole` имеет ключ для запуска как демон:

    ::console
    /opt/copy-client/CopyConsole -daemon

и, в принципе, можно запускать ее с этим ключем в каком-нибудь rc.local, но мы пойдем другим путем
и создадим сервис Systemd.

Для этого создадим файл `/etc/systemd/system/copy-console.service`:

    ::ini
    [Unit]
    Description=CopyConsole
    After=local-fs.target network.target
    
    [Service]
    Type=simple
    ExecStart=/opt/copy-client/CopyConsole
    ExecReload=/bin/kill -HUP $MAINPID
    KillMode=process
    Restart=always
    User=swasher
    
    [Install]
    WantedBy=multi-user.target

Включаем и запускаем сервис

    ::console
    $ sudo systemctl enable copy-console.service
    
А затем проверяем его работу
    
    ::console
    $ sudo systemctl status copy-console.service 
    ● copy-console.service - CopyConsole
       Loaded: loaded (/etc/systemd/system/copy-console.service; enabled; vendor preset: enabled)
       Active: active (running) since Mon 2016-01-18 10:28:00 EET; 2min 17s ago
     Main PID: 8470 (CopyConsole)
       CGroup: /system.slice/copy-console.service
               └─8470 /opt/copy-client/CopyConsole
    
    Jan 18 10:28:00 nas systemd[1]: Started CopyConsole.
    Jan 18 10:28:01 nas CopyConsole[8470]: Using profile /home/swasher/.copy/config.ini
    Jan 18 10:28:01 nas CopyConsole[8470]: User from database mr.swasher@gmail.com
    Jan 18 10:28:01 nas CopyConsole[8470]: Root from database /home/swasher/Music
    Jan 18 10:28:01 nas CopyConsole[8470]: Token from database ATC-cad2e4be7dee80d95eb7e97c13f6bdafc6b5e2ad
    Jan 18 10:28:03 nas CopyConsole[8470]: Starting copy...success
    Jan 18 10:28:03 nas CopyConsole[8470]: Logged in as user: '<the_mail>' Copy folder is: '/home/swasher/Music'
    Jan 18 10:28:03 nas CopyConsole[8470]: Press enter to exit    
    
Если пишет зеленеым `Active: active (running)` - все окей, сервис запущен, а если красным `Active: failed`,
то танцуем с бубном.