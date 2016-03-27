Title: Деплой приложения Django на сервис Heroku
Date: 2016-03-19 23:23
Tags: tags
Category: IT
Author: Swasher


Мой первый опыт деплоя на heroku. Сервис предоставляет бесплатные инстансы с разумными ограничениями, чем я и воспользуюсь.

Официальный документ [тут](https://devcenter.heroku.com/articles/django-app-configuration), а это вольный перевод,
который делался вместе с запуском моего приложения на heroku.

[Deploying Python and Django Apps on Heroku](https://devcenter.heroku.com/articles/deploying-python)

Задача: запустить уже имеющийся джанго-проект на сервисе heroku.

Окружение:

- host Windows 7 x64
- guest Ubuntu wily 15.10
- under Vagrant 1.8.1
- python 3.4.3
- django 1.9.2
- db backend sqlite3

Все команды выполняются внутри Vagrant-контейнера. Деплой на heroku из-под Windows тоже возможен, но там есть ряд
несовместимостей, все подробно описаны с соотв. разделах статей на [сайте](devcenter.heroku.com) Heroku.

Toolbelt
--------------------

Первое, что нужно сделать, это установить в систему "тулбелт" - приложение, которое позволяет
управдять инстансами heroku из командной строки. Для debian/ubuntu команда будет такая

    ::console
    $ wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh

для других систем смотрим на [toolbelt.heroku.com](https://toolbelt.heroku.com/debian)

Procfile
--------------------

Каждый проект должен иметь Procfile. Он определяет тип процессов приложения и точку входа. Должен располагаться
в корне проекта.

    ::ruby
    web: gunicorn myproject.wsgi --log-file -

Эта строка определяет одиночный тип процесса, `web`, и команду для его запуска. Имя `web` здесь важно.
Оно означает, что этот процесс будет приаттачен к [стеку HTTP](https://devcenter.heroku.com/articles/http-routing)
роутинга сервиса Heroku, и получать веб траффик после деплоя.
Запуск приложения будет осуществляться с помощью `Gunicorn`, веб-сервера приложений, рекомендуемого Heroku.

Установим `Gunicorn` прямо сейчас:

    ::bash
    $ pip install gunicorn
    ...
    $ pip freeze > requirements.txt


runtime.txt
---------------------------------

Heroku должен правильно определить, что приложение у нас написано на Python. Происходит это очень просто -
по наличию файла `requirements.txt` в корне проекта. Даже если нет зависимых пакетов, `requirements.txt` должен
присутствовать.

Когда происходит деплой, heroku сообщает о найденном приложении python:

    ::console
    $ git push heroku master
    ...
    remote: -----> Python app detected
    remote: -----> Installing python-2.7.11

Это означает, что heroku будет разворачивать наше приложение, используя питон версии `2.7.11`. Причем не имеет значения,
какую версию питона мы используем при разработке.

Чтобы изменить версию питона на продакшене, нужно указать ее в файле `runtime.txt`:

    ::console
    $ echo "python-3.5.1" >> runtime.txt
    $ git add runtime.txt
    $ git commit -am "add runtime.txt"
    $ git push heroku master
    remote: -----> Python app detected
    remote: -----> Installing python-3.5.1

Не все версии питона одинаково поддерживаются. На момент написания статьи это были `python-2.7.11` и `python-3.5.1`.
Можно указать и другие версии, однако heroku одобряет и поддерживает именно эти.
Подробнее - [Supported python runtimes](https://devcenter.heroku.com/articles/python-support#supported-python-runtimes).


settings.py и среда выполнения
---------------------------------

Настройки Django для среды разработки и для heroku будут разнится, поэтому нужно позаботиться о том, чтобы
наше приложение знало, где оно выполняется. Я делаю это через переменные окружения. На ubuntu/debian это делается так:

    $ sudo echo 'SERVER=development' >> /etc/environment

а на heroku так:

    $ heroku config:set SERVER=production

Или можно через интерфейс, в секции Settingы -> Config Variables. Проверить установленные переменные можно или там же в интерфейсе,
или командой

    $ heroku config

но обязательно из директории проекта (или понадобится явно указать `--app APP`)

Далее в settings.py делаем такую конструкцию:

    SERVER = os.getenv('SERVER')
    if SERVER == 'production':
        # heroku specific settings
    if SERVER == 'develoment':
        # develoment specific settings


Sqlite или Postgres
----------------------------------

Sqlite не подходит для использования на heroku. На heroku используется так
называемая [ephemeral filesystem](https://devcenter.heroku.com/articles/dynos#ephemeral-filesystem)
Каждый `dyno` обладает такой файловой системой. На нее можно писать, с нее можно читать, но она время от времени сбрасывается.
Так же она очищается при деплое. Поэтому нельзя использовать файловую систему для хранения перманентных данных.

Поэтому в качестве базы данных нужно использовать Postgres. Heroku предоставляет бесплатный инстанс базы данных
PostgreSQL с ограницением в 10k строк. Это ограничение нужно учитывать при выборе Heroku как бесплатного сервиса.

Однако если приложение не использует каких-то особенностей Postgres, то можно оставить среду разработки на sqlite,
чтобы не устанавливать Postgres локально.

Heroku Postgres работает как адд-он к приложению. Аддон можно установить командой

    $ heroku addons:create heroku-postgresql:<PLANNAME>

где <PLANNAME> - название тарифного плана, для free плана это `hobby-dev`.

Про ограничения этого плана можно почитать [здесь](https://devcenter.heroku.com/articles/heroku-postgres-plans#hobby-tier)

После этого в нашем приложении появится переменная окружения `DATABASE_URL` для подключения к инстансу Postgres.

Следующее, что нам нужно сделать, это установить psycopg2 для использования Python совместно с Postgres.

    ::console
    $ sudo apt-get install python3-dev # для нужной версии питона
    $ sudo apt-get install libpq-dev
    $ pip install psycopg2



Конфигурация базы данных
----------------------------------

На Heroku есть такое понятие, как `Config Vars`. Это, по сути, набор констант. Хранятся они вместе с контейнером, и
передаются в среду выполнения как переменные окружения. В них рекомендуется хранить приватные настройки, такие
как логины и пароли.

Там же Heroku хранит и настройки подключения к ДБ Posgres, в переменной `DATABASE_URL`.

Чтобы внедрить эти параметры в наш `settings.py`, на помощь приходит
пакет [dj-database-url](https://warehouse.python.org/project/dj-database-url/). Он парсит `DATABASE_URL` и
подставляет данные подключения в `DATABASES['default']` в нашем проекте джанго.

    ::console
    $ pip install dj-database-url
    $ pip freeze > requirements.txt

В `settings.py` добавляем (убирать ничего не нужно) настройки подключения к ДБ в соответствии с `$DATABASE_URL`:

    ::python
    import dj_database_url
    db_from_env = dj_database_url.config()
    DATABASES['default'].update(db_from_env)

Database connection persistence
-----------------------------------------

По умолчанию, Django будет создавать постоянное подключение к базе данных только для
каждого [цикла запроса](http://stackoverflow.com/questions/4814514/http-request-life-cycle) приложения.

> Постоянные соединения представляют собой связи с базами данных, которые не закрываются при завершении скрипта.
> При получении запроса на постоянное соединение сервер вначале проверяет, имеется ли идентичное постоянное соединение
> (которое было открыто при предыдущих обращениях) и, если таковое было найдено, использует его.

Это весьма накладное поведение, которое может замедлить выполение Django приложения.

К счастью, Django может обеспечивать постоянные соеденения, которые дают значительное улучшение производительности приложения.

settings.py:

    ::python
    # Update database configuration with $DATABASE_URL.
    import dj_database_url
    db_from_env = dj_database_url.config(conn_max_age=500)
    DATABASES['default'].update(db_from_env)

Подробнее: [Concurrency and Database Connections in Django](https://devcenter.heroku.com/articles/python-concurrency-and-database-connections)


Обслуживание статики
----------------------------------------

> TODO перевести

Django settings for static assets can be a bit difficult to configure and debug.
However, if you just add the following settings to your settings.py, everything should work exactly as expected:

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.9/howto/static-files/

    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
    STATIC_URL = '/static/'

    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = (
        os.path.join(PROJECT_ROOT, 'static'),
    )

Для дополнительной информации см. [Django and Static Assets](https://devcenter.heroku.com/articles/django-assets).


Whitenoise
----------------------------------

По умолчанию, Django не поддерживает обслуживание статики в продакшене.
Heroku рекомендует использовать проект WhiteNoise для наилучшего обслуживания статики на продакшене.

Installing Whitenoise

    ::console
    $ pip install whitenoise
    ...
    $ pip freeze > requirements.txt

settings.py (добавить)

    ::python
    # Simplified static file serving.
    # https://warehouse.python.org/project/whitenoise/

    STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

wsgi.py (целиком)

    ::python
    import os
    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "<project>.settings")

    application = get_wsgi_application()
    application = DjangoWhiteNoise(application)


Bower
--------------------------------------

Так как мы используем bower для установки зависимостей, нужно научить делать то же самое heroku. Для этой цели служат buildpack'и.
Каждый buildpack устанавливает в контейнер heroku какой-то набор окружения. Есть [официальные](https://devcenter.heroku.com/articles/buildpacks)
buildpack'и и [неофициальные](https://devcenter.heroku.com/articles/third-party-buildpacks). У нас приложение на python, поэтому
у нас автоматически установится buildpack `heroku/python`.

Нам нужно установть три buildpack'а, но, важно! - именно в такой последовательности - nodejs, bower, python:

    ::console
    $ heroku buildpacks:clear
    $ heroku buildpacks:set heroku/nodejs
    $ heroku buildpacks:add https://github.com/ejholmes/heroku-buildpack-bower
    $ heroku buildpacks:add heroku/python

На этом все, bower должен установиться и установать зависимости, наблюдаем так ли это в логе, во время деплоя.


Запуск приложения локально
-----------------------------------------

Используем команду [heroku local](https://devcenter.heroku.com/articles/heroku-local):

    $ heroku local
    [WARN] No ENV file found
    [OKAY] Trimming display Output to 210 Columns
    4:17:32 PM web.1 |  [2016-03-27 16:17:32 +0000] [16437] [INFO] Starting gunicorn 19.4.5
    4:17:32 PM web.1 |  [2016-03-27 16:17:32 +0000] [16437] [INFO] Listening at: http://0.0.0.0:5000 (16437)
    4:17:32 PM web.1 |  [2016-03-27 16:17:32 +0000] [16437] [INFO] Using worker: sync
    4:17:32 PM web.1 |  [2016-03-27 16:17:32 +0000] [16440] [INFO] Booting worker with pid: 16440

Конечно, команда должна выполняться при включенном виртуальном окружении. `heroku local` запустит сервер на 5000 порту.
Если все прошло удачно, двигаемся дальше, если нет - анализируем вывод команды.


Деплой на Heroku
---------------------------------------

Добавляем новые файлы и делаем коммит

    ::console
    $ git add Procfile
    $ git commit -m "Added a Procfile."

Логинемся на heroku

    ::console
    $ heroku login
    Enter your Heroku credentials.
    Email: mr.swasher@gmail.com
    Password (typing will be hidden):
    Logged in as mr.swasher@gmail.com

Создаем инстанс

    ::console
    $ heroku create <name_of_project>
    Creating intense-falls-9163... done, stack is cedar-14
    https://*-*-*-*-springs-13087.herokuapp.com/ | https://git.heroku.com/*-*-*-*-springs-13087.git
    http://intense-falls-9163.herokuapp.com/ | https://git.heroku.com/intense-falls-9163.git
    Git remote heroku added

Если инстанс уже был создан и привязан к приложению, а теперь нужно задеплоить на другой инстанс, проделываем следующее:

    ::console
    $ git remote rm heroku
    $ heroku git:remote -a <new_instance_name>

Если мы хотим просто переименовать инстанс, то выполняем такую команду

    ::console
    $ heroku apps:rename <new_instance_name>

Теперь можно делать деплой:

    ::console
    $ git push heroku master

Если во время деплоя что-то пошло не так, исправляем ошибки, делаем коммит, затем снова деплой

    ::console
    $ git commit -am "error fixed"
    $ git push heroku master

После этого увидим красивый отчет об установке:

    ::console
    $ git push heroku master
    Counting objects: 4, done.
    Compressing objects: 100% (4/4), done.
    Writing objects: 100% (4/4), 373 bytes | 0 bytes/s, done.
    Total 4 (delta 2), reused 0 (delta 0)
    remote: Compressing source files... done.
    remote: Building source:
    remote:
    remote: -----> Using set buildpack heroku/nodejs
    remote: -----> Node.js app detected
    remote:
    remote: -----> Creating runtime environment
    remote:
    remote:        NPM_CONFIG_LOGLEVEL=error
    remote:        NPM_CONFIG_PRODUCTION=true
    remote:        NODE_ENV=production
    remote:        NODE_MODULES_CACHE=true
    remote:
    remote: -----> Installing binaries
    remote:        engines.node (package.json):  unspecified
    remote:        engines.npm (package.json):   unspecified (use default)
    remote:
    remote:        Resolving node version (latest stable) via semver.io...
    remote:        Downloading and installing node 5.9.1...
    remote:        Using default npm version: 3.7.3
    remote:
    remote: -----> Restoring cache
    remote:        Skipping cache restore (new runtime signature)
    remote:
    remote: -----> Building dependencies
    remote:        Pruning any extraneous modules
    remote:        Installing node modules (package.json)
    remote:        /tmp/build_1a000d4aee253f7d34cb042fdda8292e
    remote:        └── bower@1.7.7
    remote:
    remote:
    remote: -----> Caching build
    remote:        Clearing previous node cache
    remote:        Saving 2 cacheDirectories (default):
    remote:        - node_modules
    remote:        - bower_components (nothing to cache)
    remote:
    remote: -----> Build succeeded!
    remote:        └── bower@1.7.7
    remote:
    remote: -----> Fetching set buildpack https://github.com/ejholmes/heroku-buildpack-bower... done
    remote: -----> Bower buildpack app detected
    remote: bower jquery#^2.2.1         not-cached git://github.com/jquery/jquery-dist.git#^2.2.1
    remote: bower jquery#^2.2.1            resolve git://github.com/jquery/jquery-dist.git#^2.2.1
    remote: bower bootstrap#^3.3.6      not-cached git://github.com/twbs/bootstrap.git#^3.3.6
    remote: bower bootstrap#^3.3.6         resolve git://github.com/twbs/bootstrap.git#^3.3.6
    remote: bower jquery#^2.2.1           download https://github.com/jquery/jquery-dist/archive/2.2.2.tar.gz
    remote: bower bootstrap#^3.3.6        download https://github.com/twbs/bootstrap/archive/v3.3.6.tar.gz
    remote: bower jquery#^2.2.1            extract archive.tar.gz
    remote: bower bootstrap#^3.3.6         extract archive.tar.gz
    remote: bower jquery#^2.2.1           resolved git://github.com/jquery/jquery-dist.git#2.2.2
    remote: bower bootstrap#^3.3.6        resolved git://github.com/twbs/bootstrap.git#3.3.6
    remote: bower jquery#^2.2.1            install jquery#2.2.2
    remote: bower bootstrap#^3.3.6         install bootstrap#3.3.6
    remote:
    remote: jquery#2.2.2 bower_components/jquery
    remote:
    remote: bootstrap#3.3.6 bower_components/bootstrap
    remote: └── jquery#2.2.2
    remote: -----> Using set buildpack heroku/python
    remote: -----> Python app detected
    remote: -----> Installing python-3.5.1
    remote:      $ pip install -r requirements.txt
    remote:        Collecting Django==1.9.4 (from -r requirements.txt (line 1))
    remote:          Downloading Django-1.9.4-py2.py3-none-any.whl (6.6MB)
    remote:        Collecting dj-database-url==0.4.0 (from -r requirements.txt (line 2))
    remote:          Downloading dj-database-url-0.4.0.tar.gz
    remote:        Collecting gunicorn==19.4.5 (from -r requirements.txt (line 3))
    remote:          Downloading gunicorn-19.4.5-py2.py3-none-any.whl (112kB)
    remote:        Collecting whitenoise==2.0.6 (from -r requirements.txt (line 4))
    remote:          Downloading whitenoise-2.0.6-py2.py3-none-any.whl
    remote:        Installing collected packages: Django, dj-database-url, gunicorn, whitenoise
    remote:          Running setup.py install for dj-database-url: started
    remote:            Running setup.py install for dj-database-url: finished with status 'done'
    remote:        Successfully installed Django-1.9.4 dj-database-url-0.4.0 gunicorn-19.4.5 whitenoise-2.0.6
    remote:
    remote:      $ python manage.py collectstatic --noinput
    remote:        299 static files copied to '/app/staticfiles', 299 post-processed.
    remote:
    remote:
    remote: -----> Discovering process types
    remote:        Procfile declares types -> web
    remote:
    remote: -----> Compressing...
    remote:        Done: 75.1M
    remote: -----> Launching...
    remote:        Released v6
    remote:        https://fathomless-springs-13087.herokuapp.com/ deployed to Heroku
    remote:
    remote: Verifying deploy... done.
    To https://git.heroku.com/fathomless-springs-13087.git
       82caeec..7bb8761  master -> master

После этого остается лишь посмотреть адрес нашего приложения в админке сервиса и скопировать его в браузер :)

Custom domain
------------------------

Бесплатный тир heroku так же поддерживает custom domain для нашего приложения. Использовать Custom domain достаточно
просто: сначла нужно подключить домен к приложению

    ::console
    $ heroku domains:add www.example.com
    $ heroku domains
    === fathomless-springs-13087 Heroku Domain
    fathomless-springs-11111.herokuapp.com

    === fathomless-springs-13087 Custom Domains
    Domain Name       DNS Target
    ────────────────  ──────────────────────────────────────
    www.example.com   fathomless-springs-11111.herokuapp.com

Затем добавить запись CNAME у доменного провайдера, ссылающуюся на DNS Target из таблички, примерно так

Имя  | Тип    | Данные
-----|------- | -------------
 @   | CNAME  | fathomless-springs-13087.herokuapp.com.

Точка в конце DNS Target может присутствовать, а может и нет, в зависмости от требований DNS провайдера.