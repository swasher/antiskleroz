Title: Краткая шпаргалка: Апгрейд ESXi с 5.1 до 5.5
Date: 2014-07-04 16:07
Tags: esxi
Category: IT
Author: Swasher
Slug: esxi-upgrading

Включаем сервис ssh:

`Хост` -> `configuration` -> `Security Profile` -> `Properties (of Services)` -> `SSH` -> `Options` -> `Start`
 
Заходим по ssh.

Открываем файрволл для http

    ::console
    $ esxcli network firewall ruleset set -e true -r httpClient

Смотрим список доступных апдейтов. Список большой, фильтруем через grep

    ::console
    $ esxcli software sources profile list \
    -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml |\
     grep 5.5 | grep standard

Выбираем нужный апдейт, устанавливаем 

    ::console
    $ esxcli software profile update \
    -d https://hostupdate.vmware.com/software/VUM/PRODUCTION/main/vmw-depot-index.xml \
    -p ESXi-5.5.0-20131204001-standard

Пока апдейт (около 300+ метров) скачивается из инета, на экране ничего не происходит - терпеливо ждем. Если апдейт установился удачно, появится сообщение

    ::console
    Update Result
    Message: The update completed successfully, but the system
    needs to be rebooted for the changes to be effective.
    
    Reboot Required: true
    
    VIBs Installed: VMware_bootbank_ata-pata-amd_0.3.10-3vmw.550.0.0.1331820, 
    VMware_bootbank_ata-pata-atiixp_0.4.6-4vmw.550.0.0.1331820, <...>

Закрываем http 

    ::console
    $ esxcli network firewall ruleset set -e false -r httpClient