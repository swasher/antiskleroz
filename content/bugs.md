Title: Записки о багах
Date: 2015-07-06 17:26
Tags: tags
Category: IT
Author: Swasher

### Samba mount: can not access a needed shared library

Ubuntu 15.04. При попытке монтирование через fstab выдает такую ошибку

    ::log
    mount error(79):can not access a needed shared library

При этом в syslog можно увидеть

    ::log
    kernel: [59206.574829] CIFS VFS: CIFS mount error: iocharset utf8 not found
    
Лечится установкой пакета 'linux-generic'
 
    ::bash
    $ apt-get install  linux-generic

Найдено [тут](http://askubuntu.com/a/618187/335705)

### Samba не монитирует шары при загрузке

При установленном systemd нужно добавить в fstab параметр `x-systemd.automount`:

    ::ini
    //192.168.1.101/mediaserver2/ /mnt/mediaserver/ cifs user=*****, \
    password=*********, iocharset=utf8,file_mode=0777,dir_mode=0777, \
    uid=1000,gid=1000,nounix,x-systemd.automount 0 0

### Ошибка bower, которой уже 4 года

    ::console
    $ bower
    /usr/bin/env: node: No such file or directory

Обсуждение [на github](https://github.com/nodejs/node-v0.x-archive/issues/3911)

Лечится просто:

    $ sudo ln -s /usr/bin/nodejs /usr/bin/node