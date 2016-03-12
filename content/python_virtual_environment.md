Title: Python и виртуальное окружение
Date: 01.02.2015 16:47
Category: IT
Tags: pip, python, virtualenv
Author: Swasher

Тут постараюсь свести до кучи использование python 2 и 3, pip, virtualenv, vitrualenvwrapper и 
PyCharm. 

Для определенности версии пакетов:

- Ubuntu  - 14.10 Utopic Unicorn
- Python2 - 2.7.8
- Python3 - 3.4.2
- Django  - 1.7.4
- PyCharm - 4.0.4 (windows)

Чтобы узнать, какая версия питона стоит в системе по-умолчанию, можно воспользоваться утилитой `pyversions`:

    ::console
    $ pyversions -d
    python2.7
   
Установка pip
---------------------------

В версии питона 3.4 pip уже устанавливается вместе с питоном. В другом случае, нужно установить его самостоятельно.

- Скачиваем [get-pip.py]
- Запускаем `python get-pip.py`. Это установит или обновит pip.

Создание виртуального окружения
---------------------------

##### Новый способ - pyvenv (только python3)

Python3 имеет встроенную утилиту для создания виртуального окружения - [pyvenv][]. 

pyvenv устанавливается вместе с python3. Вызывается командой `pyvenv-3.4`.
Если установть пакет `python3-venv` (`sudo apt-get install python3-venv`), то можно использовать сокращенную
запись: `pyvenv`

> Внимание! пакет python3-venv появляется только в Ubuntu 14.10! В 14.04 утилита `pyvenv` имеет баги.

Создаем виртуальное окружние, затем активируем его:

    ::console
    $ pyvenv myvirt
    $ source myvirt/bin/activate

Можно убедится, что pip и python работают в контейнере

    ::console
    (myvirt) $ which pip
    /home/swasher/myvirt/bin/pip
    (myvirt) $ which python
    /home/swasher/myvirt/bin/python
    (myvirt) $ python -V
    Python 3.4.2

Все, можно начинать устанавливать джанго

    ::console
    (yourenv)root@test:~# pip install django
    
    (myvirt) $ pip freeze         # check our environment is clean (no output)
    (myvirt) $ pip install django django-extensions # install django dependencies
    (myvirt) $ pip freeze         # see our installed dependencies
    Django==1.7.4
    django-extensions==1.5.0
    six==1.9.0
    (myvirt) $ django-admin.py startproject newproject  # create new django project
    (myvirt) $ pip freeze > newproject/requirements.txt # save dependencies into project
 
Выйти из контейнера можно командой  

    ::console
    (myvirt)root@test:~# deactivate

##### Старый способ - virtualenv (python2 и 3)

Для сравнения приведу старый метод, с помощью virtualenv. Этот способ хоть и совместим с новыми версиями питона, 
но не рекомендуется использовать с ними.

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
Так как проект обернут, сам проект джанго мы назовем просто project, а приложение (app) - slova.

    ::console
    $ pyvenv uchislova
    $ source uchislova/bin/activate
    (uchislova) $ pip3 install django
    (uchislova) $ cd uchislova/
    (uchislova) $ django-admin startproject project
    (uchislova) $ cd project/
    (uchislova) $ ./manage.py startapp uchislova
    (uchislova) $ ./manage.py migrate
    (uchislova) $ deactivete
    
Так, проект мы создали, теперь посмотрим, как будет работать PyCharm с виртуальным окружением.

PyCharm
--------------------------------------------

Создаем в PyCharm новый проект, интерпретатор выбираем из нашего виртуального окружения:

{% img lb-image /images/pip/1.png 770 %}

Далее нужно сделать следующее, я не буду подробно расписывать:

- настроить deployment и path mapping
- выбрать Project Interpreter, который создали чуть выше (он у нас python 3.4.0)
- выполнить синхронизацию
- включить поддержу django
- настраиваем конфигурацию запуска dev-сервера из PyCharm, как на картинке:

{% img lb-image /images/pip/2.png 770 %}

Не забываем указать наш интерпретатор. Хост `0.0.0.0` нужен для того, чтобы сервер был доступен с любого
внешнего адреса, иначе только с localhost.

Дополнение
-----------

##### Как установить python3-версию пакета через pip?

Взято [отсюда][].

На новых системах использовать только новый способ! Старый для сравнения приведен.

НОВЫЙ СПОСОБ (начиная с ubutnu 13.10)

    ::console
    $ sudo apt-get install python3-pip
    $ sudo pip3 install MODULE_NAME

СТАРЫЙ СПОСОБ (не рекомендуется использовать):

    ::console
    $ sudo apt-get install curl
    $ curl http://python-distribute.org/distribute_setup.py | sudo python3
    $ curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py | sudo python3
    $ sudo pip-3.2 install MODULE_NAME

----------------------------

Так же можно использовать не system-wide установку, а пользовательскую, с ключем `--user`:

    ::console
    $ pip install --user SomePackage
    
Для некоторых пакетов нужно установка dev:

    ::console
    $ sudo apt-get install python3-dev

  [get-pip.py]: https://raw.github.com/pypa/pip/master/contrib/get-pip.py
  [отсюда]: http://stackoverflow.com/questions/10763440/how-to-install-python3-version-of-package-via-pip
  [pyvenv]: https://docs.python.org/3/library/venv.html
  [баг]: https://bugs.launchpad.net/ubuntu/+source/python3.4/+bug/1290847
  [пример]: https://docs.python.org/3/library/venv.html#an-example-of-extending-envbuilder
  [статья]: http://fgimian.github.io/blog/2014/04/20/better-python-version-and-environment-management-with-pyenv/