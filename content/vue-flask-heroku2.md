Title: Создание темплейта Flask-Vue.js-Heroku (2 часть)
Date: 2019-05-13 00:27
Tags: vue, flask, heroku
Category: IT
Author: Swasher
Status: draft

Продолжение [первой части]({filename}vue-flask-heroku.md)

Попробуем навести феншуй в нашем простейшем приложении. Создадим отдельное приложение flask, уберем хардкод,
установим базу данных и орм и так далее.

 Flask
===============================

###### package `app`

Перемести логику фласк из корня в пакет. Подробнее про организацию проекта написано [Organizing your project
](http://exploreflask.com/en/latest/organizing.html). Для этого пересестим файл app.py в директорию `app` и 
переименуем его в `__init__.py` - он будет выполняться при инициализации пакета `app`. А в корень поместим `run.py`:


    from app import app
    app.run(port=5000)


###### handling env

Удобно управлять переменнымы окружения, записав их в файл `.env` в корне и установив пакет `python-dotenv`.
При запуске через `flask run` переменные из этого файла будут автоматически загружены. При запуске же на 
продакшене они загружены не будут. Так можно разделить dev и prod среды исполнения. [Подробнее](
http://flask.pocoo.org/docs/dev/cli/#environment-variables-from-dotenv).

В коде можно так обртиться к переменны:

    ::python
    s = os.getenv("SECRET_KEY")
    
В корне проекта разместим два файла - `.env` и `.flaskenv`. Первый файл у нас с секретными настройками, а второй 
дублирует эти настройки с фейковыми данными, в качестве примера, и находится в репозитории. Настройки читаются 
сначала из `.flaskenv`, затем перезаписываются имеющимися в `.env`.

###### config.py

Добавим в корень сайта файл `config.py` с объектом конфигурации.
 
    import os
    from app import app
        
    class Config(object):
        APP_DIR = os.path.dirname(__file__)
        ROOT_DIR = os.path.dirname(APP_DIR)
        DIST_DIR = os.path.join(ROOT_DIR, 'dist')
    
        FLASK_ENV = os.getenv('FLASK_ENV')
        FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH')
        SECRET_KEY = os.getenv('SECRET_KEY')
        DATABASE_URL = os.getenv('DATABASE_URL')
    
        if not os.path.exists(DIST_DIR):
            raise Exception(
                f'DIST_DIR not found: {DIST_DIR}')
    
    app.config.from_object('app.config.Config')

Далее этот объект загрущим в `app/__init.py` командой

    from .config import Config


###### peewee

    $ pipenv install peewee

создаем models.py. В нем описывам модели и подключение к БД. В моем конфиге при работе в dev окружении
мы работаем с SQLite, а в prod - подключаемся к Postgres. Это реализовано через проксирование БД, подробно тут: 
[Dynamically defining a database](http://docs.peewee-orm.com/en/latest/peewee/database.html#dynamically-defining-a-database)
В функции initialize_db мы создаем таблицы в базе. Под heroku все это требует допиливания.

    import os
    from peewee import *
    
    FLASK_ENV = os.getenv("FLASK_ENV")
    
    
    database_proxy = DatabaseProxy()
    
    
    class Effect(Model):
        name = CharField(unique=True)
    
        def __str__(self):
            return self.name
    
        class Meta:
            database = database_proxy  # This model uses the "people.db" database.
    
    
    class Ingredient(Model):
        name = CharField(unique=True)
        effect1 = ForeignKeyField(Effect)
        effect2 = ForeignKeyField(Effect)
        effect3 = ForeignKeyField(Effect)
        effect4 = ForeignKeyField(Effect)
    
        class Meta:
            database = database_proxy  # This model uses the "people.db" database.
    
    
    # Based on configuration, use a different database.
    if FLASK_ENV == 'development':
        database = SqliteDatabase('base.db')
    elif FLASK_ENV == 'production':
        database = PostgresqlDatabase('my_app', user='postgres', password='secret', host='10.1.0.9', port=5432)
    else:
        raise Exception('No FLASK_ENV environment during db init.')
    
    
    # Configure our proxy to use the db we specified in config.
    database_proxy.initialize(database)
    
    
    def initialize_db():
        database_proxy.connect()
        database_proxy.create_tables([Effect], safe=True)
        database_proxy.create_tables([Ingredient], safe=True)
        database_proxy.close()
    initialize_db()

или можно использовать враппер из библиотеки `playhouse`, что дает еще более элегантный код. В `config.py` добавим 
конфигурацию БД:

    class Config(object):
        if FLASK_ENV == 'development':
            app.config['DATABASE'] = 'sqlite:///base.db'
        # else using heroku DATABASE_URL
   
и упростим `models.py`:

    from app import app
    from peewee import *
    from playhouse.flask_utils import FlaskDB
    
    db_wrapper = FlaskDB(app)
    
    class Effect(db_wrapper.Model):
        ...
    
    class Ingredient(db_wrapper.Model):
        ...    
    
    def initialize_db():
        with db_wrapper.database as db:
            db.create_tables([Effect, Ingredient], safe=True)
    initialize_db()

`FlaskDB` работает следующим образом - он создает соеденение с базой данных, используя `app.config['DATABASE']`, а если
не находит его, то тогда использует `app.config['DATABASE_URL']`. Таким образом, в `dev` мы определяем 'DATABASE' в 
`config.py`, а в `prod` на heroku у нас автоматически существует `DATABASE_URL`.
   
   
###### abstraction

Добавим немного абстракции для феншуя. Отдавать входную точку (`/`) будем так:

    def index():
        dist_dir = current_app.config['DIST_DIR']
        entry = os.path.join(dist_dir, 'index.html')
        return send_file(entry)


###### admin

    pipenv install Flask-admin
    pipenv install wtf-peewee - необходимо для Flask-admin
    
Добавьте в __init__.py

    from flask_admin import Admin
    from flask_admin.contrib.peewee import ModelView
    from .models import Effect, Ingredient
    
    # admin -----------------------
    app.config['FLASK_ADMIN_SWATCH'] = os.getenv("FLASK_ADMIN_SWATCH")
    admin = Admin(app, name='Skyrim Alchemy', template_mode='bootstrap3')
    admin.add_view(ModelView(Effect))
    admin.add_view(ModelView(Ingredient))
    
Чтобы использовать тему, укажите ее в .flaskenv:

    FLASK_ADMIN_SWATCH = darkly

###### bootstrap

Для использования компонентов бутстрап достаточно установить пакет плагин и классы бутстрап начнут отображаться:

    $ vue add bootstrap-vue



###### heroku

Подключаем репозиторий к heroku, тут подробно останавливаться не буду, нам главное, чтобы по команде `git push heroku`
запускался деплой.

Убеждаемся, что мы установили buildpack для питона и ноды (первый питон, это важно!):

    $ heroku buildpacks:set heroku/python
    $ heroku buildpacks:add --index 1 heroku/nodejs
    
Устанавливаем аддон для постгреса:

    $ heroku addons:create heroku-postgresql:hobby-dev --app:<our-app-name>

Вносим изменения в models.py, чтобы мы в окружении dev подключались к heroku-postgresql. Настройки для подключения
хранятся на heroku в переменной `DATABASE_URL`, она создается автоматически после запуска предыдущей команды.

    ....
    elif FLASK_ENV == 'production':
        # connect to heroku POSTGRES
        DATABASE_URL = os.environ['DATABASE_URL']
        database = connect(DATABASE_URL)

Не забываем создать на heroku нужные переменные, типа `SECRET_KEY`.
