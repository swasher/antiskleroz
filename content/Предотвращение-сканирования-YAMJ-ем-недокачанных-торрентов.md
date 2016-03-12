Title: Предотвращение сканирования YAMJ-ем недокачанных торрентов
Date: 2012-01-11 10:44
Category: Popcorn
Tags: rtorrent, yamj
Author: Swasher

Скрипт предназначен для того, чтобы запущенный YAMj не сканировал недокачанные торренты. В противном случае, он не можен нормально выполнить
`mediainfo`, и техническая информация о фильме остается в дальнейшем незаполненной.

Модифицируем rtorrent.rc:

    #создание директории закачки+создание mjbignore
    system.method.set_key=event.download.inserted_new,create_struct,"d.open= ; f.multicall=,\"execute={sh,/home/swasher/creator.sh,$f.get_frozen_path=,$f.get_path=}\""

    #окончание закачки, удаление mjbignore
    system.method.set_key = event.download.finished,remove_mjbignore,"execute=sh,/home/swasher/remove_mjbignore.sh,$d.get_directory="


Тут я использую скрипт, предназначенный для прозрачного создания целевой
директории для закачки. В него передается еще одна переменная `f.get_path`. Он создает директорию, и потом в ней файл-метку .mjbignore.

*creator.sh*

    ::::bash
    #!/bin/sh

    dir=`dirname "${1}"`
    mkdir -p "${dir}"

    #берем снова 1-полный путь 2-файл
    fdir="${1}"
    filez="${2}"

    # удаляем из полного пути имя файла, получаем директорию скачивания
    target=${fdir%$filez}

    touch "${target}""/.mjbignore"


Скрипт для удаление метки после завершения закачки:

*remove_mjbignore.sh*

    ::::bash
    #!/bin/sh
    # script name: remove_mjbignore.sh
    rm "${1}""/.mjbignore"
