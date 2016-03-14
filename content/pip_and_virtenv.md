Title: Использование pip и virtualenv
Date: 08.10.2014 5:08
Category: IT
Tags: pip, python, virtualenv
Author: Swasher

[НОВАЯ ВЕРСИЯ СТАТЬИ](|filename|python_virtual_environment.md)

Тут постараюсь свести до кучи использование python 2 и 3, pip, virtualenv, vitrualenvwrapper и 
PyCharm.

Для определенности версии пакетов:

- Ubuntu  - 14.04 trusty
- Python2 - 2.7.6
- Python3 - 3.4.0
- Django  - 1.7 
- PyCharm - 3.4.1 (windows)

Есть два способа использовать изолированное окружение - либо один virtualenv для всех проектов, либо
для каждого проекта свой virtualenv. Так как раньше изолирование не использовал, я пойду по второму пути.

Чтобы узнать, какая версия питона стоит в системе по-умолчанию, можно воспользоваться утилитой `pyversions`:

    ::console
    $ pyversions -d
    python2.7
   

Создание виртуального окружения
---------------------------

##### Новый способ - pyvenv (только python3)

Python3 имеет встроенную утилиту для создания виртуального окружения - [pyvenv][]. К сожалению,
на Ubuntu 14.04 она имеет [баг][], создание окружения аварийно завершается ошибкой:

    ::console
    $ pyvenv-3.4 myvirt
    Error: Command '['/home/swasher/django_test/myvirt/bin/python3.4', '-Im', 'ensurepip', \
    '--upgrade', '--default-pip']' returned non-zero exit status 1

Разработчики вроде бы пофиксили, но в апстрим фикс попадет только в 14.10. Но не беда, эта утилита 
основана на питоновском классе EnvBuilder, который появился в 3.3. На сайте python есть 
[пример][] скрипта. Его работа заключается в создании окружения и установке туда 
setuptools и pip. Скачиваем скрипт и запускаем:
 
    ::console
    $ python3 pyvenvex.py yourenv
    
Aктивируем

    ::console
    $ source yourenv/bin/activate

Можно убедится, что pip и python работают в контейнере

    ::console
    (yourenv)root@test:~# which pip
    /home/swasher/yourenv/bin/pip
    (yourenv)root@test:~# which python
    /home/swasher/yourenv/bin/python
    (yourenv)root@test:~# python -V
    Python 3.4.0

Все, можно начинать устанавливать джанго

    ::console
    (yourenv)root@test:~# pip install django
 
Выйти из контейнера можно командой  

    ::console
    (yourenv)root@test:~# deactivate

##### Старый способ - virtualenv (python2 и 3)

Для сравнения приведу старый метод, с помощью virtualenv:

    ::console
    # for python2
    $ virtualenv yourenv
    # for python3
    $ virtualenv -p /usr/bin/python3 yourenv 
    $ source yourenv/bin/activate
    $ pip install package-name
    
Aктивируем

    ::console
    $ source yourenv/bin/activate

Можно убедится, что pip и python в контейнере

    ::console
    (yourenv)root@test:~# which pip
    /home/swasher/yourenv/bin/pip
    (yourenv)root@test:~# which python
    /home/swasher/yourenv/bin/python
    (yourenv)root@test:~# python -V
    Python 3.4.0

##### pyenv

> TODO: Существует также утилита pyvenv с плагинами pyenv-virtualenv и pyenv-virtualenvwrapper,
> которая предлагает очень элегантное управление версиями питона и виртуальными окружениями.
> [статья][]

Создание нового проекта
---------------------------------------------

Предполагается, что у нас есть несколько django-проектов, некоторые под python2, другие под python3.
Новый проект будем создавать под python3.

Создаем новое окружение, ставим джанго и стартуем новый проект. Проект у меня называется uchislova.
Так как проект обернут, сам проект джанго мы назовем просто project, а вот приложение (app) - uchislova.

    ::console
    $ python3 pyvenvex.py newproject
    $ source uchislova/bin/activate
    (uchislova) $ pip3 install django
    (uchislova) $ django-admin startproject project
    (uchislova) $ cd project/
    (uchislova) $ ./manage.py startapp uchislova
    (uchislova) $ ./manage.py migrate
    (uchislova) $ deactivete
    
Так, проект мы создали, теперь посмотрим, как будет работать PyCharm с виртуальным окружением.

PyCharm
--------------------------------------------

Создаем в PyCharm новый проект, интерпретатор выбираем из нашего виртуального окружения:

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457945825/pycharm/pip1.png 770 %}

Далее нужно сделать следующее, я не буду подробно расписывать:

- настроить deployment и path mapping
- выбрать Project Interpreter, который создали чуть выше (он у нас python 3.4.0)
- выполнить синхронизацию
- включить поддержу django
- настраиваем конфигурацию запуска dev-сервера из PyCharm, как на картинке:

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457945826/pycharm/pip2.png 770 %}

Не забываем указать наш интерпретатор. Хост `0.0.0.0` нужен для того, чтобы сервер был доступен с любого
внешнего адреса, иначе только с localhost.

Дополнение
-----------

##### Как установить python3-версию пакета через pip?

Взято [отсюда][].

На новых системах использовать только новый способ! Старый для сравнения приведен.

НОВЫЙ СПОСОБ (начиная с ubutnu 13.10)

    ::console
    sudo apt-get install python3-pip
    sudo pip3 install MODULE_NAME

СТАРЫЙ СПОСОБ (не рекомендуется использовать):

    ::console
    sudo apt-get install curl
    curl http://python-distribute.org/distribute_setup.py | sudo python3
    curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3
    sudo pip-3.2 install MODULE_NAME

----------------------------

Так же можно использовать не system-wide установку, а пользовательскую, с ключем `--user`:

    ::console
    $ pip install --user SomePackage
    
Для некоторых пакетов нужно установка dev:

    ::console
    sudo apt-get install python3-dev

  [отсюда]: http://stackoverflow.com/questions/10763440/how-to-install-python3-version-of-package-via-pip
  [pyvenv]: https://docs.python.org/3/library/venv.html
  [баг]: https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847
  [пример]: https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder
  [статья]: http://fgimian.github.io/blog/2014/04/20/better-python-version-and-environment-management-with-pyenv/