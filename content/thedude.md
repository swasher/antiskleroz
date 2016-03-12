Title: The Dude на headless сервере
Date: 19.07.2014 22:09
Category: IT
Tags: the dude, server
Author: Swasher

# В РАЗРАБОТКЕ

Тезисное изложение установки системы мониторинга The dude на сервер под линуксом. Эта 
конфигурация имеет существенную проблему безопастности - Thedude должен запускается под wine c 
правами рута. Вследствии чего приходится использовать автоматический логин в рута.

Поехали. 

##### Устанавливаем [minimal ubuntu]()

Дистрибутив весит всего 30 метров. Только самые необходимые пакеты. Я использовал 32-битную 
версию, так как жрет меньше памяти. 
 
##### Устанавливаем минималистичный оконный менеджер fluxbox и сопуствующие пакеты

    ::console
    $ apt-get install fluxbox
    $ apt-get install xinit
    
##### Устанавливаем wine    

    ::console
    $ apt-get install pulseaudio #чтобы wine не ругался на отсутствие звука
    $ apt-get install wine
    $ cp /usr/share/fonts/truetype/msttcorefonts/* ~/.wine/drive_c/windows/Fonts/


>ЭТО НЕ НУЖНО УЖЕ
>apt-get install gksu (чтобы запускать dude под рутом)
>apt-get install slim (для автологина)

Редактируем конфиг /etc/slim.conf

    # default_user        root
    # auto_login          no

Через apt pinning устанавливаем последнюю версию slim, в ней есть slimlock

Download The Dude installer, at the time of writing, the latest version is 4.0 Beta 3:

    $ wget http://download.mikrotik.com/dude/4.0beta3/dude-install-4.0beta3.exe

Перезапускаем систему, должен произойти автологин под рут. Устанавливаем dude
wine dude-install-4.0beta3.exe

Запускаем

wine ~/.wine/drive_c/Program\ Files/Dude/dude.exe &
Устанавливаем галучку на secure подключение, порт изменится на 2211. Логин и пароль нужно будет изменить позже - пока это Admin с пустым паролем.

Пробрасываем порт наружу.


Добавляем строки запуска в `/root/.fluxbox/startup` после 
строки `Application you want to run with fluxbox`

    wine ~/.wine/drive_c/Program\ Files/Dude/dude.exe &
    slimlock

Подключаемся с удаленного компьютера, не забываем установить пароль, также хорошая идея сменить логин.
 
## UPDATE 
Переделываем как описано тут [Setting up the Dude Service](http://wiki.mikrotik.com/wiki/The_Dude/Dude_as_a_Linux_Service#Setting_up_the_Dude_Service)

Запускаем dude как сервис.

##### Устанвливаем Xvfb (X virtual framebuffer)

As you can imagine, we are going to need a GUI to install Dude. However, we usually don 't have
one in server environments, unless you have a desktop manager installed like Gnome, KDE, etc. I 
sometimes install fluxbox (a very small desktop environment) for this purposes. Well, this 
program will allow us to create a virtual (fake) X Server used to install Dude.

    ::console
    $ apt-get install xvfb
 
##### Ставим vnc

    ::console
    $ apt-get install x11vnc
    
##### Создаем виртуальный дисплей с помощью Xvfb 
    
    ::console
    $ Xvfb :1 -screen 0 800x600x16 &
    
##### Разрешаем vnc коннектится к виртульному дисплею
    
    ::console
    $ x11vnc -display :1  -bg -forever
    
##### Запускаем установку dude
    
    ::console
    $ export DISPLAY=:1
    $ export WINEPREFIX=/srv/dude
    $ wine dude-installer-xxx.exe
    
##### Подключаемся к виртуальному дисплею с vnc-клиента (напр. openvnc)
    
    Завершая инсталляцию в обычном режиме.
    
##### Запускаем Thedude как демон
    
Создаем файл `/etc/init.d/dude` со следующим содержимым
    
    ::bash
    #!/bin/bash
    
    ### BEGIN INIT INFO
    # Provides: dude
    # Required-Start: $remote_fs $syslog
    # Required-Stop: $remote_fs $syslog
    # Default-Start: 2 3 4 5
    # Default-Stop:
    # Short-Description: Dude Server
    ### END INIT INFO
    
    action=${1}
    
    # ----------------------------------------------
    # User Options
    # ----------------------------------------------
    xvfb_pidfile='/var/run/dude-xvfb.pid'
    wine_pidfile='/var/run/dude-wine.pid'
    virtual_display=':1'
    dude_path='/srv/dude'
    # ----------------------------------------------
    
    export DISPLAY=$virtual_display
    export WINEPREFIX=$dude_path
    
    start ()
    {
     echo -n 'Starting Dude virtual display: '
     Xvfb $virtual_display &> /dev/null &
     echo $! > $xvfb_pidfile
     echo 'ok'
     echo -n 'Starting Dude Server: '
     sleep 5
     wine 'c:\Program Files (x86)\Dude\dude.exe' --server &> /dev/null &
     echo $! > $wine_pidfile
     echo 'ok'
    }
    
    stop ()
    {
     echo -n 'Stopping Dude Server: '
     kill $(cat $wine_pidfile)
     rm -f $wine_pidfile
     sleep 5
     echo 'ok'
     echo -n 'Stopping Dude virtual display: '
     kill $(cat $xvfb_pidfile)
     rm -f $xvfb_pidfile
     echo 'ok'
    }
    
    case "$action" in
     start)
      start
     ;;
    
     stop)
      stop
     ;;
    
     *)
      echo "Usage: $0 {start|stop}"
     ;;
    esac
    
    # -----------------------------------------------------------------------
    
В скрипте путь к dude.exe может варьироваться, - `Program Files (x86)` или просто `Program Files` 
 
Устанавливаем права

    ::console
    $ chown root:root /etc/init.d/dude
    $ chmod 755 /etc/init.d/dude
 
 [minimal ubuntu]: https://help.ubuntu.com/community/Installation/MinimalCD