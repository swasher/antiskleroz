Title: Vue.js - основы
Date: 2019-05-05 08:12
Tags: vue
Category: IT
Author: Swasher

В этой памятке я запишу неочевидные факты про Vue.js


Структура
-----------------

-- Файл index.html содержит простую разметку HTML с единственным элементом “app” в body. Он будет заменён на 
DOM, сгенерированный vue.

-- В папке src лежит файл main.js, который содержит точку входа webpack. Компоненты Vue импортируются там же.

-- В этом же файле описан корневой экземпляр Vue, который пока что имеет два свойства. 
---- Свойство ‘el’ обеспечивает экземпляру Vue связь с указанным DOM элементом. 
---- Свойство ‘component’ обеспечивает связь с функцией отрисовки, генерирующая DOM из App.vue.

Ajax
-----------------

Компонент axios

    import axios from 'axios'
    export default {
      data () {
        return {
          posts: null,
          endpoint: 'https://jsonplaceholder.typicode.com/posts/',
        }
      },
    
      created() {
        this.getAllPosts();
      },
    
      methods: {
        getAllPosts() {
          axios.get(this.endpoint)
            .then(response => {
              this.posts = response.data;
            })
            .catch(error => {
              console.log('-----error-------');
              console.log(error);
            })
        }
      }
    } 
    
Метод getAllPosts обращается к серверу и возвращает данные. Хук `created` вызавается после создания экземпляра Vue.

Чем отличается export default от new Vue
------------------

Когда вы объявляете компонент:

    new Vue({
        el: '#app',
        data () {
          return {}
        }
    )}

Как правило, это ваш корневой экземпляр Vue, с которого происходит выход остальной части приложения. 
Это зависает от корневого элемента, объявленного в HTML-документе, например:

    <html>
      ...
      <body>
        <div id="app"></div>
      </body>
    </html>

Другой синтаксис объявляет компонент, который может быть зарегистрирован и повторно использован позже. 
Например, если вы создаете одинофайловый компонент, такой как:

    // my-component.js
    export default {
        name: 'my-component',
        data () {
          return {}
        }
    }

Вы можете позже импортировать это и использовать это как:

    // another-component.js
    <template>
      <my-component></my-component>
    </template>
    <script>
      import myComponent from 'my-component'
      export default {
        components: {
          myComponent
        }
        data () {
          return {}
        }
        ...
      }
    </script>

Кроме того, не забудьте объявить ваши свойство data как функции, иначе они не будут реактивными.

Корневой экземпляр
-------------------------------

Корневой экземпляр записывается в переменную `$vm0`. Набрав `$vm0` в консоле браузера, можно исследовать корневой инстанс.

@
-----------------------------------------
    
    // @ is an alias to /src (in a vue-cli generated project)
    import Child from '@/components/Child.vue'  

тег template и v-if
---------------------------------

Позволяет обернуть часть DOM, не используя теги div и подобные. Обертка может использовать v-if, а v-show - не поддерживается

    <template v-if="!message">
        <h1>Вы должны написать сообщение для получения помощи!</h1>
        <p>Немедленно отправьте посыльного!</p>
        <p>В соседнее королевство Сердец!</p>
    </template>

В директиве v-if происходит сравнение со строкой, если строка пустая, это false, иначе true.

this
------------------------------

this внутри методов указывает на ЧТО?!? Корневой экземпляр или компонент???

В любом случаем, мы можем обращаться к объявленным данным в секции data по имени: `this.param1`.
Это возможно потому, что внутри объекта Vue используется проксирование, т.е this.param1 => vm0._data.param1

Сокращения
-------------------------------

**v-on:click**
    
    <button type="button" v-on:click="upvote">
    <button type="button" @click="upvote">

**v-bind**

v-bind используется для динамического связывания одного или нескольких атрибутов, или свойств компонентов, к выражению.
Поскольку свойство `story` не строка, а объект JavaScript, вместо `story="..."` мы
используем `v-bind:story="..."` для привязывания свойства story к переданному
объекту. `:` — сокращение для v-bind, поэтому с этого момента мы воспользуемся этим `:story="..."` (напр., при передачи 
параметров в компонент):

    <Ingredients :ingredients=ingredients /> 


v-model
------------------

Используется для ПОЛЯ ВВОДА (text, textarea, number, radio, checkbox, select)

    <input v-model="something">
    
по сути то же самое, что и:

    <input
       v-bind:value="something"
       v-on:input="something = $event.target.value"
    >

или (сокращенный синтаксис):

    <input
       :value="something"
       @input="something = $event.target.value"
    >

Таким образом, v-model является **двусторонней связью для входных данных формы**. Он объединяет v-bind, 
который вносит значение js в разметку, и v-on:input для обновления значения js.

Или, совсем по простому, something помещается в текстовое поле, и при изменение текста обновляется something

v-bind
---------------------------

Привязывает данные к разметке, но НЕ ОБНОВЛЯЕТ переменную при пользовательском вводе (как это делает v-model)

    <input
      type='text'
      v-bind:value='data_source'
      placeholder='Если что-то набрать, data_source не изменится'
    />

функции в ES6
------------------------------

Некоторые свойсва, например, data в компоненте должно быть записано в виде функции. В ES5 синтаксис такой:

    data: function () { 
        //… 
    } 

что эквивалентно в ES6 

    data() { 
        //… 
    } 

обработка событий от дочернего компонента в родительском
-----------------------------------

Дочерний компонент

    <template>
        <button type="button" @click="vote">{{ name }}</button>
    </template>
    
    <script>
        export default {
            name: 'childComponent',
            methods: {
                vote: function (event) {
                    this.$emit('voted', event.target.textContent)
                }
            }
        }
    </script>

{% img  image  https://res.cloudinary.com/swasher/image/upload/v1560616067/blog/vue-child.png %}


Родительский компонент

    <template>
      <div>
        {{ votes }}
        <childComponent :somedata=somedata @voted="countVote" ></childComponent>
      </div>
    </template>
    
    <script>
        export default {
            name: 'parentComponent',
            data () {
                return {
                    somedata: '',
                    votes: 0
                }
            },
    
            methods: {
                countVote: function () {
                    this.votes++
                }
            }
        }
    </script>

{% img  image  https://res.cloudinary.com/swasher/image/upload/v1560616067/blog/vue-parent.png %}

