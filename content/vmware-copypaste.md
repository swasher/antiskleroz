Title: ESXi - Как включить copy-paste в виртуальной машине
Date: 2013-09-29 11:20
Tags: esxi, vmware
Category: IT
Author: Swasher


По умолчанию в гипервизоре VmWare ESXi выключена возможность копировать текст через буфер обмена в виртуальную машину. Сделано это по соображениям безопасности.
Однако это бывает часто необходимым и очень полезным.
Есть два способа включить эту возможность - для каждой VM через ее настройки, и через редактирование конфигов гипервизора для всех машин.

Способ I
---------

Включение возможности copy-paste для конкретной машины.

1. Логинимся в vSphere Client и выключаем нужную машину.
2. Заходим в свойства машины (Edit Settings)
3. Редактируем параметры (Options > Advanced > General -> кнопка Configuration Parameters)
4. Нажимаем Add Row.
5. Вводим два ключа со значениями:

        ::text
        isolation.tools.copy.disable    false
        isolation.tools.paste.disable   false

>Замечание: эти настройки имеют больший вес, чем настройки, сделанные в VmWare Tools в операционной системе.

Закрываем окошко настроек и включаем виртуальную машину.

Способ II
---------

Для включение возможности copy-paste на всем хосте ESXi, требуется отредактировать файлы на гипервизоре. 
Для этого нам необходимо получить доступ по ssh. Включаем эту возможность:

1. В VSphere Client выбираем хост и заходим во вкладку Configuration
2. В панеле Software жмем Security Profile
3. В секции Services жмем Properties
4. Находим строчку SSH и жмем Options
5. Запускаем сервис SSH кнопкой Start
6. Для автоматического запуска сервиса вместе с гипервизором выбираем "Start and stop with host"
7. Жмем ок и закрываем окна.

Теперь, когда сервис ssh запущен, с помощью любого ssh-клиента подключаемся в шелл гипервизора как root.

Следующий шаг - редактирование файлов. Так как в стандартной оболочке, кроме vi, нам ничего не доступно, прийдется пользоваться именно им.
Не владея этим редактором, использовать его невозможно, поэтому по ходу дела указаны команды vi.

Делаем бекап конфига

    ::console
    $ cp /etc/vmware/config /etc/vmware/config.backup

Откраваем в текстовом редакторе

    ::console
    $ vi /etc/vmware/config

В появившемся окне, двигаем курсор в конец послеждней строчки и жмем кнопку `i`. Этим мы переводим vi в режим редактирования. 
Жмем enter - переходим на новую строку, и вставляем следующие три строки:

    ::plain
    vmx.fullpath = "/bin/vmx"
    isolation.tools.copy.disable="FALSE"
    isolation.tools.paste.disable="FALSE"

Чтобы сохранить и выйти, жмем такие кнопки `Esc` (выйти из режима редактирования), `:`(режим ввода команды), `w`(записать), `q`(выйти), и затем `Enter`. Если нужно выйти без сохрания, используем команду `quit!`.

Для того, чтобы изменения вступили в силу, необходимо полностью выключить гостевую систему со стороны хоста, и потом снова ее включить. 


Материалы
---------

[Editing files on an ESX host using vi or nano (1020302)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1020302)  
[Enabling root SSH login on an ESX host (8375637)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=8375637)  
[Clipboard Copy and Paste does not work in vSphere Client 4.1 and later (1026437)](http://kb.vmware.com/selfservice/microsites/search.do?language=en_US&cmd=displayKC&externalId=1026437)