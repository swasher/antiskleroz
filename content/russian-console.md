Title: Русские буквы в консоли Debian/Ubuntu
Date: 2015-06-14 12:54
Tags: linux, font, console
Category: IT
Author: Swasher

Внимание!!! Никаких манипуляций с locale!!!

Все, что нужно сделать, чтобы в консоле отображались русские буквы:

##### Включить фреймбуффер:

    ::console
    $ sudo echo 'FRAMEBUFFER=Y' >> /etc/initramfs-tools/initramfs.conf
 
##### Настроить консоль

    ::console
    $ sudo dpkg-reconfigure console-setup
    
Выбираем:

- UTF-8
- Combined - Latin; Slavic and non-Slavic Cyrillic
- Fixed
- Размер по вкусу.
    
Шрифт нужно выбрать fixed, потому что Terminus у меня отображал русские буквы квадратами.

##### Обновить initrd

Обновить образ рамдиска периода инициализации ядра (initrd):

    ::console
    $ sudo update-initramfs -u
   
##### Автозагрузка изменений

После перезагрузки мы увидим опять старый шрифт. Чтобы применить настройки, нужно выполнить

    ::console
    $ setupcon -f

Для применения этой команды при загрузке, воспользуемся `/lib/systemd/system/systemd-vconsole-setup.service`:

    ::ini
    # shim unit to satisfy dependencies until Debian/Ubuntu enable systemd-vconsole
    [Unit]
    Description=Setup Virtual Console
    DefaultDependencies=no
    Conflicts=shutdown.target
    Requires=console-setup.service
    ConditionPathExists=/dev/tty0
    
    [Service]
    Type=oneshot
    RemainAfterExit=yes
    # ExecStart=/bin/true
    ExecStart=/bin/setupcon

Заменяем ExecStart с true на setupcon, и после перезагрузки видим, что выбранный шрифт на месте.

Не забываем проверить настройки в /etc/default/console-setup

Все! Теперь вывод русскими буквами будет отображаться нормально. Проверено на ubuntu 15.04.