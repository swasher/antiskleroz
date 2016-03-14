Title: Редактирование блога с помощью PyCharm
Date: 2014-06-05 15:17
Category: IT
Tags: blog, pycharm
Slug: pycharm-edit-blog
Author: Swasher


Долгое время я не мог найти удобную и продуктивную систему для редактирования своего блога. Перепробовав несколько способов, я вернулся
к динозаврам - заходил на сервер по ssh и редактировал текст в MidnightCommander, после чего давал команду `make html` для сборки и
смотрел получившийся результат в браузере.

Испробованы были и [Sublime][], с плагином ssh, и Notebook++, и web-редактор [Icecoder][], который устанавливается на сервер, а 
редактирование происходит в браузере. По тем или иным причинам никто из них у меня не прижился. Не буду устраивать тут обзор редакторов,
просто скажу, что редактировать файл, открытый по ssh, это ахтунг.

Я уже долгое время пользуюсь замечательной Python IDE PyCharm, для своих небольших хобби-проектов на питон. Она выпускается как в коммерческой
редакции, так и в бесплатной OpenSource Edition с некоторыми ограничениями. И однажны до меня дошло - ведь PyCharm можно использовать
и для редактирования любых документов! 10 минут настройки, и наступило счастье! :)

Принципиальное отличие Pycharm от других редакторов - это то, что он хранит файлы локально, и при необходимости аплоадит или синхронизирует
их с сервером через ssh. Тем, кто использует PyCharm в своей работе, статья будет не интересна, а для остальных - настройка в картинках.

Напомню, этот блог работает под двжком [Pelican][], а тексты статей хранянтся в формате [Markdown][].

Устанавливаем, запускаем, и создаем новый проект `blog`. Выбор интерпретатора питон не важен.

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946104/pycharm/pycharm-0001.png 750 %}

Далее идем в File->Settings, и настраиваем ssh

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946104/pycharm/pycharm-0002.png 750 %}

На вкладке Mappings путь устанавливаем так, чтобы root path + deployment path указывал на папку с нашими документами.

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946105/pycharm/pycharm-0004.png 750 %}

Опять идем в Settings, и устанавливаем плагин Markdown.

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946105/pycharm/pycharm-0005.png 750 %}

После этого у нас появится возможность видеть превью статей.

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946106/pycharm/pycharm-0006.png 750 %}

Настраиваем аплоад. Мне удобно, чтобы файл аплоадился каждый раз, когда я нажимаю Ctrl-S. Для этого включаем опцию

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946105/pycharm/pycharm-0008.png 750 %}

Установим шрифт с нормальными русскими буквами, они не в каждом шрифте есть

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946105/pycharm/pycharm-0009.png 750 %}

Создадим темплейт для новых записей блога (Settings -> File and code templates)

    ::jinja2
    Title: ${NAME}
    Date: ${YEAR}-${MONTH}-${DAY} ${TIME}
    Tags: tags
    Category: IT
    Author: Swasher

И последняя приятность. После внесения изменений в контент нужно пересобрать сайт, делается это командой `make html`
Раньше для этого нужно было логиниться по ssh и запускать процесс вручную. PyCharm имеет функцию выполнения команд через ssh, воспользуемся этим:

{% img lb-image http://res.cloudinary.com/swasher/image/upload/v1457946106/pycharm/pycharm-0011.png 750 %}
  
Теперь в меню Tools есть пункт Rebuild blog, а в вывод консоли мы увидим прямо в IDE.

Теперь для написания статьи или внесения изменений достаточно открыть pyCharm, внести правки, нажать Ctrl-S и Rebuild Blog и вуаля! И все это в прекрасном текстовом редакторе.



  [Sublime]: http://www.sublimetext.com/
  [Icecoder]: https://icecoder.net/
  [Pelican]: http://docs.getpelican.com/en/latest/
  [Markdown]: http://ru.wikipedia.org/wiki/Markdown