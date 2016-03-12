Title: Установка vmware-tools на гостевую Ubuntu 9.04
Date: 2009-04-27 23:53
Category: IT
Tags: ubuntu, vmware
Author: Swasher

Использовалась 9.04 десктоп, VmWare Workstation версии 6.5.2  
  
Инфа взята [отсюда][], а оффициальный документ лежит [здесь][].  
  
Прописываем репозитарий:  

    ::console  
    $ apt-key adv --fetch-keys http://packages.vmware.com/tools/VMWARE-PACKAGING-GPG-KEY.pub
    $ echo "deb http://packages.vmware.com/tools/esx/3.5u4/ubuntu intrepid main restricted" >\
      /etc/apt/sources.list.d/vmware-tools.list
  
и обновляемся  

    ::console
    $ apt-get update  

Устанавливаем модули ядра
--------------------------------

This section describes how to build a customized Ubuntu binary kernel and how to install VMware Tools OSPs.  
To build customized kernels for Ubuntu

1. Install the kernel source packages, type:

        ::console
        $ apt-get install open-vm-tools-kmod-source vmware-tools-kmod-source  

2. Prepare for the build, type:  

        ::console
        $ module-assistant prepare  

3. Build the kernel modules for each package, type:  

        ::console
        $ module-assistant build open-vm-tools-kmod vmware-tools-kmod  

    This produces two .deb files in /usr/src by default.  

4. Install the produced binary packages, type:

        ::console
        $ module-assistant install open-vm-tools-kmod vmware-tools-kmod  

See the module-assistant manpage.  
  
  
1. Устанавливаем версию ядра для нашей Убунты, например, такой командой:  

        ::console
        $ uname -r

    Команда возвращает тип ядра и версию ядра. Тип может быть таким:  

    - generic  
    - server  
    - virtual  
  
    У меня получилось так:

        ::console
        $ uname -r
        2.6.28-11-generic
  
2. Устанавливаем модули ядра для нашего типа и версии, например:  


        ::console
        $ apt-get install open-vm-tools-kmod-<type>
        $ vmware-tools-kmod-</type><type>  

    Должно получится  

        ::console
        $ apt-get install open-vm-tools-kmod-2.6.28-11-generic
        $ vmware-tools-kmod-2.6.28-11-generic  
  
    > Мне написало в этом месте, что самые новые версии пакетов уже установлены, это непорядок... ((
  
3. Установка остальных компонентов  

        ::console
        $ apt-get install vmware-tools  

    When this command is run, all the other packages are automatically installed in the correct order.
  
    Мне эта команда ругается на (отсутствие) зависимости от open-vm-tools:

        ::text
        Пакеты, имеющие неудовлетворённые зависимости:  
        vmware-tools: Зависит: open-vm-tools (= 7.4.6-0.153875.157734) но
        2008.11.18-130226-1lenny1 будет установлен  
        E: Сломанные пакеты  
  
    Но вроде все работает, если сделать руками:  


        ::console    
        $ apt-get install vmware-tools-common  
        $ apt-get install vmware-toolbox  
        $ apt-get install vmware-user  

    и вроде все заработало  
  

Что на выходе
-------------

Что должно появиться в результате этих манипуляций:

- **мышь** - свободно выходит за границы виртуальной машины  
- **эзернет** - идем в Система-Администрирование-Драйверы устройств - должен появиться VmWare Virtual Ethernet Driver  
- **экран** - подстраивает разрешение под изменение размеров окна машины

  [отсюда]: http://gitterdimmerung.blogspot.com/2009/04/2.html
  [здесь]: http://www.vmware.com/pdf/osp_install_guide.pdf
