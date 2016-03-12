Title: Программное управление crontab из bash
Date: 2012-11-18 22:53
Category: IT
Tags: linux, shell
Author: Swasher


Иногда возникает необходимость остановить или запустить выполнение задач
cron из shell-скриптов. Для этого были разработаны два скрипта, для
удаления задачи и для ее добавления в crontab. **cron\_add.sh**

    #!/bin/bash
    CRON="1 2 3 4 5 /root/bin/backup.sh"

    if fgrep -i "$CRON" <(crontab -l)
    then
        echo "Задача уже присутствует в crontab"
    else
        cat <(crontab -l) <(echo "${CRON}") | crontab -
    fi


**cron\_remove.sh**

    #!/bin/bash

    CRON="1 2 3 4 5 /root/bin/backup.sh"

    if fgrep -i "$CRON" <(crontab -l)
    then
        echo "Задача присутствует в crontab, удаляем"
        cat <(fgrep -i -v "$CRON" <(crontab -l)) | crontab -
    else
        echo "Задачи нет в crontab"
    fi


В переменной CRON содержится необходимая строка. Ньюанс - скрипты
почему-то не совместимы с оболочкой sh, а в bash отрабатывают нормально.

