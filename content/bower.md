Title: Quickstart with bower (and Django project)
Date: 2015-02-18 14:36
Tags: bower, django
Category: IT
Author: Swasher

Quick start
----------------

Установка менеджера пакетов `npm` (System wide).  
Флаг `-g` (или `--global`) устанавливает Node Package Manager (NPM) глобально, он становится доступен из любой директории, не только из текущего проекта.

    ::console
    $ sudo apt-get install npm
    $ sudo npm intall -g bower

В директории с проектом django.
Создаем конфиг `.bowerrc`, в котором указываем, куда bower будет ставить пакеты.
А ставить нам надо в `settigs.STATIC_URL`:

    ::bash
    $ touch .bowerrc
    {
      "directory": "myapp/static"
    }

Следующая команда создаст в текущей директории файл `bower.json`. В дальнейшем в него будут записываться все наши установленные пакеты.
    
    ::bash
    $ bower init
    
На все вопросы отвечаем по-умолчанию, просто жмем Enter. 

> Единственное, на вопрос «would you like to mark this package as private which prevents it from being accidentally published to the registry?» — можно ответить «Yes» — это предотвратит случайную регистрацию пакета в реестре Бовер.

Далее ставим необходимые для нашего проекта пакеты, обязательно с ключем `--save`:

    ::bash
    $ bower install jquery --save
    $ bower install eonasdan-bootstrap-datetimepicker#latest --save
    
Все скачается и установится в папку `myapp/static`. Список зависимостей хранится в `bower.json`. Проверим, что у нас поставилось:
 
    ::bash
    $ bower list

В будущем, чтобы развернуть зависимости, нужно иметь в текущей директории наши bower.json и .bowerrc, и выполнить команду
    
    ::bash
    $ bower install

Полезные ссылки:

[Официальный сафт bower](http://bower.io/)
[Хорошая статья про использование bower](http://nano.sapegin.ru/all/bower)
[Еще статья про воркфлов django+bower](http://axiacore.com/blog/effective-dependency-management-django-using-bower/)
