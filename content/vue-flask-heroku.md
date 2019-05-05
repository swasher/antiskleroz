Title: Создание темплейта Flask-Vue.js-Heroku
Date: 2019-05-05 08:12
Tags: vue, flask, heroku
Category: IT
Author: Swasher

Задача - написать минимальное, но хорошо структурированое приложение-темплейт, использующее в качестве
бекенда Flask, фронтэнд - Vue.js, в качестве хоста выберем SaaS платформу Heroku. База данных, конечно, Postges,
локально для девелопинга SQLite, в качестве ORM для Flask я выбрал Peewee вместо обычной SQLAlchemy.

Приложение минимальное - имеет модель Car с единственным полем name, по ссылке /admin можно добавлять записи, по
ссылке / эти записи выводятся на экран.

Эта статья не призвана учить азам vue или flask, больше упор делается на соеденение всех компонентов стека. 
Поэтому объяснений самого кода будет минимум.

Приступим, помолясь:

    $ mkdir flask-vue-heroku
    $ cd flask-vue-heroku
    $ python -m venv venv
    
> Pycharm notes: Mark `venv` directory as excluded in Settings:Project Structure. In Settings:Language turn on
> flask integration.

Создадим в корне `run.py`:

    from backend import app
    
    app.run(port=5000)
    
    # To Run:
    # python run.py
    # or
    # python -m flask run
    
А в директории `backend` у нас будет лежать серверная часть приложения (`__init__.py`):

    
    from flask import Flask
    app = Flask(__name__)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'
        
Нужно установить две переменных окружения (в винде вот так):

    > set FLASK_ENV=development
    > set FLASK_APP=backend
    
и проверить, запускается ли flask -`flask run` - смотрим, что у нас на 5000 порту.

Теперь добавим Vue.js. Пакет vue-cli устанавливаем глобально.

    $ npm install -g vue-cli
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
    
Чтобы это пофиксить, ставим библиотеку flask-cors: `pip install -U flask-cors` и добавим две строчки в `__init__.py`

    ::python
    from flask_cors import CORS
    
    # enable CORS
    CORS(app)

Смотрим теперь:

    Hello, Susana
    
На этом будем считать первую версию приложения законченной и перейдем к деплою на Heroku. После удачного деплоя 
попробуем усложнить приложиние, добавив работу с БД, web-компонентами и т.д.

#to be continued....