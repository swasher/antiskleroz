Title: Установка последнего mc
Date: 2012-03-10 15:21
Category: IT
Tags: mc, ubuntu
Slug: install-latest-mc

Если в офф. репозитории находится устаревший mc, можно устновить свежий с офф. сайта.
Для этого идем на [сайт Midnight Commander][], ищем свой дистр, копируем нужные строчки в
/etc/apt/sources.list. Желающие могут установить ночную сборку (Nightly)

    deb http://www.tataranovich.com/debian oneiric main
    deb-src http://www.tataranovich.com/debian oneiric main

Ищем на указанной страничке строчку с ключем: `Repository signed with key PGP key ID: 2EE7EF82`
Добавляем этот ключ в локальный кейринг:

    gpg --keyserver keyserver.ubuntu.com --recv-keys 2EE7EF82

Экспортируем ключ из pgp и добавляем его в список авторизованных ключей apt с помощью apt-key: 

    gpg --armor --export 2EE7EF82 | apt-key add -

Обновляем мс:

    apt-get update && apt-get upgrade


  [сайт Midnight Commander]: https://www.midnight-commander.org/wiki/Binaries
    "Midnight Commander"
