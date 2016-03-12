Title: Установка свежего nginx в ubuntu 14.04
Date: 2014-10-07 14:02
Tags: nginx, ubuntu
Category: IT
Author: Swasher

В ubuntu 14.04 в репах nginx довольно старый, 1.4, при том что stable уже 1.6. Свежий nginx можно установить из ppa.

Если при установке ppa вываливается такая ошибка 

    ::console
    $ add-apt-repository ppa:nginx/stable
    The program 'add-apt-repository' can be found in the following packages:
     * python-software-properties
     * software-properties-common
    Try: apt-get install <selected package>

то нужно установить пакет

    ::console
    $ sudo apt-get install software-properties-common

Затем
    
    ::console
    $ add-apt-repository ppa:nginx/stable
    $ apt-get update
    $ apt-get install nginx
    
Окей, 

    ::console
    $ nginx -v
    nginx version: nginx/1.6.0
    
 