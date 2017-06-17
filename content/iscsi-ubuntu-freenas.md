Title: iSCSI: Подключаем СХД Nas4Free к Ubuntu Server
Date: 2013-05-31 11:11
Tags: ubuntu, freenas, iscsi
Category: IT
Slug: iscsi
Author: Swasher

Заметка о подключении iscsi target'а к Ubuntu Server. Предполагается, что сам сервер Nas4Free уже настроен и работает.

Таргеты а планирую настроить как устройства, то есть отдавать их целыми "винчестерами". Альтернативно, можно создать разделы и отдавать разделами.

## Настройка таргета на Nas4Free 

Сборка NAS4Free имеет версию 9.1.0.1 (531). Переходим на вкладку "Services|iSCSI Target|Target". Вот что написано на самой страничке конфигурации:

>To configure the target, you must add at least Portal Group and Initiator Group and Extent.
>Portal Group which is identified by tag number defines IP addresses and listening TCP ports.
>Initiator Group which is identified by tag number defines authorised initiator names and networks.
>Auth Group which is identified by tag number and is optional if the target does not use CHAP authentication defines authorised users and secrets for additional security.
>Extent defines the storage area of the target.

Пройдусь по всем вкладкам, начиная с последней:

#### Services|iSCSI Target|Media

не настраиваем

#### Services|iSCSI Target|Auth Group

не настраиваем

#### Services|iSCSI Target|Initiator Group

- Tag number - 1
- Initiators - ALL
- Authorised network - ALL
- Comment - My Initiators Descriptions

#### Services|iSCSI Target|Portal Group

- Tag number - 1
- Portals - 0.0.0.0:3260
- Comment - myportal

#### Services|iSCSI Target|Extent|Add

- Extent Name - extent0
- Type - Device
- Device - ada4 -> тут выбираем нужный нам винт
- Comment - RED 3TB SLOT 4

#### Services|iSCSI Target|Target|Add

- Target Name - disk0
- Target Alias - baculafiles
- Type - Disk
- Flags - r/w
- Portal Group (Primary) - Tag1(myportal)
- Initiator Group (Primary) - Tag1(My Initiators Descriptions)

LUN0 -> Storage - extent0(/dev/ada4) (The storage area mapped to LUN0.)

Настройки Advanced settings не трогал.

Все, теперь из сети у нас должена быть видна лунка iqn.2012.nas4free:disk0

## Настройка инициатора на Ubuntu 

Используется Ubuntu server x64 13.04 raring. Устанавливаем iscsi

    ::console
    $ apt-get install open-iscsi

На этом этапе мы должны увидеть наш таргет, пробуем:

    ::console
    $ sudo iscsiadm -m discovery -t st -p 192.168.0.60
    192.168.0.60:3260,1 iqn.2012.nas4free:disk0

Теперь пробуем подключиться

    ::console
    $ sudo iscsiadm -m node --login
    Logging in to [iface: default, target: iqn.2012.nas4free:disk0, portal: 192.168.0.60,3260] (multiple)
    Login to [iface: default, target: iqn.2012.nas4free:disk0, portal: 192.168.0.60,3260] successful.

Чтобы подключение выполнялось автоматически при загрузке, редактируем конфиг `/etc/iscsi/iscsid.conf`:

    ::text
    node.startup = automatic

Смотрим вывод dmesg:

    ::text
    [2678585.588790] Loading iSCSI transport class v2.0-870.
    [2678586.568851] iscsi: registered transport (tcp)
    [2678978.204955] scsi3 : iSCSI Initiator over TCP/IP
    [2678979.465243] scsi 3:0:0:0: Direct-Access     FreeBSD  iSCSI DISK       0001 PQ: 0 ANSI: 5
    [2678979.470864] sd 3:0:0:0: Attached scsi generic sg2 type 0
    [2678979.475169] sd 3:0:0:0: [sdb] 5860533168 512-byte logical blocks: (3.00 TB/2.72 TiB)
    [2678979.476596] sd 3:0:0:0: [sdb] Write Protect is off
    [2678979.476609] sd 3:0:0:0: [sdb] Mode Sense: 83 00 00 08
    [2678979.477145] sd 3:0:0:0: [sdb] Write cache: enabled, read cache: enabled, doesn't support DPO or FUA
    [2678979.488842]  sdb: sdb1
    [2678979.493134] sd 3:0:0:0: [sdb] Attached SCSI disk

Наш таргет успешно подключился как /dev/sdb. Последнее, что я сделал - это перезагрузил сервер и убедился, что таргет
успешно и автоматически подключается при загрузке.

> TODO - продумать действия в ситуации, когда инициатор загружается, а таргет в этот момент не доступен.

## Форматирование

Смотрим, что скажет fdisk:

    ::console
    $ sudo fdisk -l /dev/sdb

    WARNING: GPT (GUID Partition Table) detected on '/dev/sdb'! The util fdisk doesn't support GPT. Use GNU Parted.


    Disk /dev/sdb: 3000.6 GB, 3000592982016 bytes
    256 heads, 63 sectors/track, 363376 cylinders, total 5860533168 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 4096 bytes / 1048576 bytes
    Disk identifier: 0x00000000

	Device Boot      Start         End      Blocks   Id  System
    /dev/sdb1   *           1  4294967295  2147483647+  ee  GPT
    Partition 1 does not start on physical sector boundary.

fdisk честно нас предупреждает, что для 3TB диска лучше использовать parted, что мы и сделаем, отформатировав наше устройство как ext4
Тут я комментировать код не буду, ибо и так все очевидно

    ::console
    $ sudo parted /dev/sdb

    (parted) mklabel gpt
    (parted) unit %
    (parted) mkpart primary 0 100
    (parted) unit TB
    (parted) print

    Model: FreeBSD iSCSI DISK (scsi)
    Disk /dev/sdb: 3.00TB
    Sector size (logical/physical): 512B/512B
    Partition Table: gpt

    Number  Start   End     Size    File system  Name     Flags
     1      0.00TB  0.00TB  0.00TB               primary

    (parted) quit

Раздел создали, теперь его нужно отформатировать, указываем размер блока 4к:

    ::console
    $ sudo mkfs.ext4 -b 4096 /dev/sdb

    mke2fs 1.42.13 (17-May-2015)
    Found a gpt partition table in /dev/sdb
    Proceed anyway? (y,n) y
    Creating filesystem with 976754646 4k blocks and 244195328 inodes
    Filesystem UUID: 6626a138-c076-46a9-8414-29ffd68c72a1
    Superblock backups stored on blocks:
            32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
            4096000, 7962624, 11239424, 20480000, 23887872, 71663616, 78675968,
            102400000, 214990848, 512000000, 550731776, 644972544

    Allocating group tables: done
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done


Пробуем примонтировать

    ::console
    $ mkdir /mnt/bacula
    $ mount /dev/sdb1 /mnt/bacula
    $ df -H

    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sda1        52G  1.7G   48G   4% /
    /dev/sdb1       3.0T   77M  2.9T   1% /mnt/bacula

Ок, том готов к работе. Осталось внести изменения в fstab и еще раз прогнать ребут. Строчка в fstab:


    /dev/sdb1   /mnt/bacula    ext4   defaults,_netdev   0 0


>Про опцию '_netdev':
>The filesystem resides on a device that requires network access (used to prevent the system from attempting  to  mount  these  filesystems
>until the network has been enabled on the system).


Прикидываем, что мы получили по пропускной способности:

    ::console
    $ dd if=/dev/sdb of=/dev/null bs=128K count=20000
    20000+0 records in
    20000+0 records out
    2621440000 bytes (2.6 GB) copied, 233.209 s, 11.2 MB/s
    
    $ dd if=/dev/zero of=/mnt/bacula/000.dd bs=128K count=100000
    100000+0 records in
    100000+0 records out
    13107200000 bytes (13 GB) copied, 1147.12 s, 11.4 MB/s

Около 11MB/s - не густо, надо будет что-то думать, хотя для моей задачи резевного копирования хватит.

Полезные команды
-----------------

сначала мы находим нужные нам target, для этого мы должны знать IP/dns-имя инициатора: 
iscsiadm -m discovery -t st -p 192.168.0.1 -t st — это команда send targets.

iscsiadm -m node (список найденного для логина)
iscsiadm -m node -l -T iqn.2011-09.example:data (залогиниться, то есть подключиться и создать блочное устройство).
iscsiadm -m session (вывести список того, к чему подключились)
iscsiadm -m session -P3 (вывести его же, но подробнее — в самом конце вывода будет указание на то, какое блочное устройство какому target'у принадлежит).
iscsiadm -m session -u -T iqn.2011-09.example:data (вылогиниться из конкретной )
iscsiadm -m node -l (залогиниться во все обнаруженные target'ы)
iscsiadm -m node -u (вылогиниться из всех target'ов)
iscsiadm -m node --op delete -T iqn.2011-09.example:data (удалить target из обнаруженных).


Полезные ссылки
----------------

[Хабрахабр - Настройка ISCSI initiator в linux](http://habrahabr.ru/post/97529/)
