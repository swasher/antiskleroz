Title: Создание темплейта Flask-Vue.js-Heroku
Date: 2019-05-05 08:12
Tags: vue, flask, heroku
Category: IT
Author: Swasher
Status: draft

Задача - написать минимальное, но хорошо структурированое приложение-темплейт, использующее в качестве
бекенда Flask, фронтэнд - Vue.js, в качестве хоста выберем SaaS платформу Heroku. База данных, конечно, Postges,
локально для девелопинга SQLite, в качестве ORM для Flask я выбрал Peewee вместо обычной SQLAlchemy.

Приложение минимальное - имеет модель Car с единственным полем name, по ссылке /admin можно добавлять записи, по
ссылке / эти записи выводятся на экран.

Эта статья не призвана учить азам vue или flask, больше упор делается на соеденение всех компонентов стека. 
Поэтому объяснений самого кода будет минимум.

Первая, неудачная попытка была создать структуру проекта с папками frontend и backend:
    
    doc/
    ├── backend/
    ├── frontend/
    │   └── package.json
    ├ Procfile
    ├ requirements.txt
    └ run.py

То есть flask и vue были отделены от корневого каталога. В таком виде оно хорошо работает, но для деплоя на heroku
нужно наличие в корне package.json. Это можно побороть скриптами, но я решил попробовать flatten-структуру.

Итак, приступим:


Vue.js
==============================================

Установим Vue.js, используя опцию `-g` для глобальной установки. 

    $ npm install -g @vue/cli
    
Следующая команда создаст корневую директорию для нашего проекта. 
    
    $ cd /home/all_my_projects
    $ vue create flask-vue-heroku --no-git

> Pycharm notes: In `Settings:Language` turn on flask integration.

Выбираем кастомную установку, пресет линтинга Airbnb, хранение настроек в одном файле. Переходим в папку проекта, и в
отдельном терминале запускаем dev-сервер:

    $ cd flask-vue-heroku
    $ npm run serve
    
Открываем в браузере `http://localhost:8080/`.

Теперь создадим свой простейший компонент во vue.js. Наш компонент будет показывать версию операционной системы
бекенда. Пока что у нас бекенда нет, мы будем просто писать "Unknown". Компоненты хранятся в папке `src\components`. 
Удалим оттуда дефолтный `HelloWorld.vue` и создадим свой `Server_os.vue` с таким содержимым:   

    ::html
    <template>
        <p>Server working on: {{ os }}</p>
    </template>
    
    <script>
    export default {
      name: 'Server_os',
      data() {
        return {
          os: 'Unknown',
        };
      },
    };
    </script>

и в файле `src\App.vue` исправим пути и имена:

    <template>
      <div id="app">
        <img alt="Vue logo" src="./assets/logo.png">
        <Os/>
      </div>
    </template>
    
    <script>
    import Os from './components/Server_os.vue';
    
    export default {
      name: 'App',
      components: {
        Os,
      },
    };
    </script>

Мы должны увидеть `Server working on: Unknown`: 

{% img image https://res.cloudinary.com/swasher/image/upload/v1557519436/blog/flask-vue-1.png %}

Вкратце, что происходит в коде:

- `public/index.html` - точка входа. Главное в этом файле - строка `<div id="app"></div>`, этот id='app' фреймворк vue.js заменит на 
сгенерированный им html-код.
- `src/main.js` - в этом файле загружается и инициализируется vue. Тут же мы указываем, что сгенерированный код будет помещен
в контейнер с id=app. Во второй строке подгружается 'главный' компонент 'App.vue', в который, в свою очередь, будут подгружаться
все созданные нами компоненты.
- `src/App.vue` - 'главный' (root) компонент. Как и любой компонент, состоит из раздела `template` - это html-темплейт наподобие Jinja,  
раздела `script`, который этот темплейт преобразует в собственно html и возвращает как результат работы компонента, и раздел
`style`, который содержит CSS-стили для этого компонента.
- `src/components/Server_os.vue` - это наш рабочий компонент, который подключается в главный `App.vue`. Содержит те же разделы.
В разделе `script` немного другой синтаксис - компонент объявляется как `export default` и указывается свойство `name` ('Server_os'). Под этим именем
он может импортироваться в другие компоненты (переиспользоваться). Свойство `data` содержит функцию - она возвращает некие данные для
использования в темплейте. У нас она пока-что возвращает просто переменную `os` со значением 'Unknown'.

Фронт-энд часть у нас работает, займемся бекэнд. Сделаем так, чтобы серверный код передавал на фронтэнд название операционной системы сервера.

Flask
=======================================

    $ mkdir flask-vue-heroku
    $ cd flask-vue-heroku
    $ pipenv install flask
    
> Pycharm notes: Mark `venv` directory as excluded in `Settings:Project Structure`. 

Создадим в корне `app.py`:
    
    ::python
    from flask import Flask, jsonify
    import platform
    app = Flask(__name__)
    
    
    @app.route('/')
    def get_os_name():
        p = platform.platform()
        return jsonify({'platform': p})
        
Нужно установить переменную окружения (в винде вот так):

    > set FLASK_ENV=development
    
Запускаем flask -`flask run` и смотрим, что у нас на 5000 порту:

    {
      "platform": "Windows-7-6.1.7601-SP1"
    }

Сейчас мы можем запустить одновременно обе части приложения - в одной консоле flask, в другой vue.js 

{% img image https://res.cloudinary.com/swasher/image/upload/v1557565280/blog/flask-vue-2.png %}


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~






Теперь попробуем получить какую-то информацию с бекенда. Для ajax
используем библиотеку axios. 

    $ cd frontend
    $ npm install axios --save  
    
Добавим пару строк, чтобы flask по ссылке `/` отдавал какие-то данные в формате json:

    from flask import Flask
    from flask import jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        firstname = 'Susana'
        return jsonify({'firstname': firstname})

Теперь напишем "принимающую" сторону - яваскрипт, который из браузера будет обращаться к серверу и получать оттуда данные.
Для этого модифицируем Hello.vue следующим образом 

    <script>
    import axios from 'axios';
    
    export default {
      name: 'getname',
      data() {
        return {
          firstname: '',
        };
      },
      methods: {
        getName() {
          const path = 'http://localhost:5000/';
          axios.get(path)
            .then((response) => {
              this.firstname = response.data.firstname;
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
            });
        },
      },
      created() {
        this.getName();
      },
    };
    </script>
    
Что здесь происходит:
- имя компонента - 'getname', оно будет видно в отладчике Vue в хроме
- date() - указываем, что компонент будет возвращать `firstname`
- далее создаем метод `getName`, который делает ajax запрос по пути `path`
- ajax возвращает объект response
- из этого объекта берем данные по ключу firsname (`response.data.firstname`)
- и возвращаем их через this.firstname
- хук created запуская метод при инициализации экземпляра Vue






DEPRECATED
=====================================

Flask
=======================================

    $ mkdir flask-vue-heroku
    $ cd flask-vue-heroku
    $ python -m venv venv
    $ pipenv install flask
    
> Pycharm notes: Mark `venv` directory as excluded in Settings:Project Structure. In Settings:Language turn on
> flask integration.

Создадим в корне `run.py`:

    from backend import app
    
    app.run(port=5000)
    
    # To Run:
    # python run.py
    # or
    # python -m flask run
    
А в директории `app` у нас будет лежать серверная часть приложения (`__init__.py`):

    
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
        
Нужно установить две переменных окружения (в винде вот так):

    > set FLASK_ENV=development
    > set FLASK_APP=app
    
и проверить, запускается ли flask -`flask run` - смотрим, что у нас на 5000 порту.

Vue.js
==============================================

Теперь добавим Vue.js. Пакет vue-cli устанавливаем глобально.

    $ npm install -g @vue/cli
    $ vue init webpack frontend
    
Я на вопросы отвечал вот так

    ? Project name frontend
    ? Project description A Vue.js project
    ? Author swasher <mr.swasher@gmail.com>
    ? Vue build standalone
    ? Install vue-router? No
    ? Use ESLint to lint your code? Yes
    ? Pick an ESLint preset Airbnb
    ? Set up unit tests No
    ? Setup e2e tests with Nightwatch? No
    ? Should we run `npm install` for you after the project has been created? (recommended) npm
    
Попробуем запустить vue:

    $ cd frontend
    $ npm run dev
    |  Your application is running here: http://localhost:8080
    
У нас есть работающие по-отдельности бекенд и фронтенд. Теперь создадим свой простейший компонент во vue.js, а затем 
попробуем передать что-то из серверной части в клиентскую.

Компоненты хранятся в папке `frontend\src\components`. Удалим оттуда дефолтный `HelloWorld.vue` и создадим свой `Hello.vue`
с таким содержимым:   

    ::html
    <template>
      <div>
        <p>Hello, {{ msg }}</p>
      </div>
    </template>
    
    <script>
    export default {
      name: 'Hello',
      data() {
        return {
          msg: 'Alex',
        };
      },
    };
    </script>
    
и в файле `frontend\src\App.vue` исправим пути и имена:

    <script>
    import Hello from './components/Hello';
    
    export default {
      name: 'App',
      components: {
        Hello,
      },
    };
    </script>

Теперь мы должны увидеть `Hello, Alex`. Теперь попробуем получить какую-то информацию с бекенда. Для ajax
используем библиотеку axios. 

    $ cd frontend
    $ npm install axios --save  
    
Добавим пару строк, чтобы flask по ссылке `/` отдавал какие-то данные в формате json:

    from flask import Flask
    from flask import jsonify
    
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        firstname = 'Susana'
        return jsonify({'firstname': firstname})

Теперь напишем "принимающую" сторону - яваскрипт, который из браузера будет обращаться к серверу и получать оттуда данные.
Для этого модифицируем Hello.vue следующим образом 

    <script>
    import axios from 'axios';
    
    export default {
      name: 'getname',
      data() {
        return {
          firstname: '',
        };
      },
      methods: {
        getName() {
          const path = 'http://localhost:5000/';
          axios.get(path)
            .then((response) => {
              this.firstname = response.data.firstname;
            })
            .catch((error) => {
              // eslint-disable-next-line
              console.error(error);
            });
        },
      },
      created() {
        this.getName();
      },
    };
    </script>
    
Что здесь происходит:
- имя компонента - 'getname', оно будет видно в отладчике Vue в хроме
- date() - указываем, что компонент будет возвращать `firstname`
- далее создаем метод `getName`, который делает ajax запрос по пути `path`
- ajax возвращает объект response
- из этого объекта берем данные по ключу firsname (`response.data.firstname`)
- и возвращаем их через this.firstname
- хук created запуская метод при инициализации экземпляра Vue

-----------------

Пробуем запустить нашу связку. Для этого в двух разных терминалах запускем vue и flask командами `npm run dev` в 
директории `frontend` и `pyton run.py` из корня. Смотрим, что отдает flask по адресу http://127.0.0.1:5000/:

    {
        "firstname": "Susana"
    }
    
это мы и ожидали. Теперь смотрим, что отдаем vue (http://localhost:8080/):

    Hello,
    
Имени нет. Это потому, что у нас не проходят кросс-доменные запросы. Смотрим в дебаггер хрома (F12), и видим что-то вроде

    Access to XMLHttpRequest at 'http://localhost:5000/' from origin 'http://localhost:8080' has been blocked 
    by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
    
Чтобы это пофиксить, ставим библиотеку flask-cors: `pipenv install -U flask-cors` и добавим две строчки в `__init__.py`

    ::python
    from flask_cors import CORS
    
    # enable CORS
    CORS(app)

Смотрим теперь:

    Hello, Susana
    
Все работает, фронтэнд принимает данные от бекенда. На этом будем считать первую версию приложения законченной и перейдем к деплою на Heroku. После удачного деплоя 
попробуем усложнить приложиние, добавив работу с БД, web-компонентами и т.д.

##to be continued....

Heroku
===================================

Нам понадобится установленные [Heroku Toolbelt](https://blog.heroku.com/the_heroku_toolbelt).

Так как мы пилим темплейт для автоматического деплоя, настроим проект таким образом, чтобы он разворачивался на
Heroku путем [нажатия одной кнопки](https://devcenter.heroku.com/articles/heroku-button) в репозитории Github. Создадим
в корне файл `app.json`:

    {
      "name": "Flask VueJs Heroku Template",
      "description": "template for automatic deploy flask-vue application",
      "repository": "https://github.com/gtalarico/flask-vuejs-template",
      "logo": "https://github.com/gtalarico/flask-vuejs-template/raw/master/docs/project-logo.png",
      "keywords": ["flask", "vue", "heroku"],
      "env": {
        "FLASK_ENV": {
          "description": "Flask Enviroment",
          "value": "production"
        },
        "SECRET": {
          "description": "Flask Secret Key",
          "value": "SecretKey"
        }
       },
      "addons": [
       ],
      "buildpacks": [
        {
          "url": "heroku/nodejs"
        },
        {
          "url": "heroku/python"
        }
      ]
    } 

Запилим красивую кнопку в файле README.md:

    |One button Installer | [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy) |
    |---------------------|-------------------------------------------------------------------------------------|


Создадим [Procfile](https://devcenter.heroku.com/articles/procfile):

    echo web: gunicorn backend:app --log-file - > Procfile 
    
