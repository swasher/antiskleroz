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