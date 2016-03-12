Title: Заметки Django
Date: 2014-05-16 11:27
Category: IT
Tags: ubuntu
Author: Swasher

## Сортировка: поле сортировки жестко задано в моделе

    ::python
    class Publisher(models.Model):
        name = models.CharField(max_length=30)
        address = models.CharField(max_length=50)
        city = models.CharField(max_length=60)
        state_province = models.CharField(max_length=30)
        country = models.CharField(max_length=50)
        website = models.URLField()

        def __unicode__(self):
            return self.name

        class Meta:
            ordering = ["name"]

Пока не будет использован явный вызов метода order_by(), все объекты Publisher будут выдаваться отсортированными по полю name.
Полный список полей мета гуглим "django available meta options"

## Передача в шаблон списка или кортежа

    ::python
    *view.py*
    from django.template import RequestContext
    dic=['red', 'gree', 'white']
    OR
    dic=('red', 'gree', 'white')
    return render_to_response('kinopoisk.html', \
      context_instance=RequestContext(request, {'data':dic}))

    *template.html*
    {% for value in data %}
         {{ value }}
    {% endfor %}
    
## Пути для статики

`STATIC_URL` - '/static/' is usually fine, it's just a prefix for static files.

`MEDIA_ROOT` - место, где хранятся залитые пользователем файлы для полей FileField.  

> Absolute filesystem path to the directory that will hold [user-uploaded files].

`STATIC_ROOT` - абсолютный путь к директории, куда метод `manage.py collectstatic` соберет всю статику.  
Обычно это путь на деплойменте. Collectstatic собирает в него, в т.ч., скрипты и стили от используемых приложений, например, grappelli или admin.
Ручками сюда ничего ложить нельзя!

> The absolute path to the directory where collectstatic will collect static files for deployment.

> If the staticfiles contrib app is enabled (default) the collectstatic management command will collect static files into this directory. 
> See the howto on managing static files for more details about usage.

`STATICFILES_DIRS` - это список(list) директорий, в которых Джанго будет искать статику, в дополнение к каждой директории `static` каждого app.

> This setting defines the additional locations the staticfiles app will traverse if the FileSystemFinder finder is enabled, e.g. if you use the collectstatic or findstatic management command or use the static file serving view.

  [user-uploaded files]: https://docs.djangoproject.com/en/dev/topics/files/
  
  
## Выполнить скрипт в командной строке в окружении Django

    ::python
    #!/usr/bin/env python

    import sys, os
    from pprint import pprint
    
    sys.path.append('/home/swasher/pdfupload')
    os.environ['DJANGO_SETTINGS_MODULE'] = 'pdfupload.settings'
    from django.conf import settings
    
    pprint(settings.DATABASES)

## Как сделать редирект на текущий домен, но на другой порт

Например, я хочу перейти на порт 9181, на котором работает rq-dashbord. Можно прибить в темплейте ссылку гвоздями, 
но тогда не будет нормально работать на продакшене/тестинге/девелопменте. Сделать ссылку на текущий домен можно
следующим образом.

Во первых, нужно знать, что в Django 1.8 [изменили формат настройки темплейтов](https://docs.djangoproject.com/en/1.8/ref/templates/upgrading/#upgrading-templates-to-django-1-8)
в `settings.py`: убрали все настройки, связанные с темплейтами (в частности, TEMPLATE_CONTEXT_PROCESSORS), и 
ввели только одну, для всего -  TEMPLATES.

По умолчанию там не содержится ['django.template.context_processors.request'](https://docs.djangoproject.com/en/1.8/ref/templates/api/#django-template-context-processors-request), поэтому надо добавить в наш
`settings.py` шаблон настройки TEMPLATES (по ссылке выше), и в раздел `'context_processors'` добавить обработчик request.
  
Теперь у нас в каждом шаблоне будет доступна переменная request. Ссылку теперь можно сформировать так:

    ::jinja2
    <a href="{{ request.get_host }}:9181">

## Установка Pillow

[Tip on Decoder JPEG not available (addition to docs ?)](https://github.com/python-pillow/Pillow/issues/1275) 

## Set Django's FileField to an existing file

[Set Django's FileField to an existing file](http://stackoverflow.com/questions/8332443/set-djangos-filefield-to-an-existing-file)

## Прикол с MEDIA_URL и STATIC_URL

Если url начинается со слеша (MEDIA_URL = "/media/"), то при обращении к полю базы в темплейте, например
`{{ gallery.image.url }}`, суффикс будет добавлен к домену:

    www.mygallery.com/media
    
Если же слеша нет, то суффикс будет добавлен к текущему адресу:

    www.mygallery.com/photo/media

## Организация структуры каталогов

Называйте ваш проект project (django-admin.py startproject project) — ну или другим, но одинаковым именем для всех проектов. 
Раньше я называл проекты соответственно домену, но при повторном использовании приложений в других проектах приходилось 
менять пути импорта — то from supersite import utils, то from newsite import utils. Это путает и отвлекает. Если расширить 
этот совет — зафиксируйте (унифицируйте) для себя структуру каталогов всех ваших проектов и строго её придерживайтесь.

Живой пример:
--site.ua
  |--static
  |--media
  |--project (папка с проектом)
     |--manage.py
     |--project (папка с основным приложением)
     |  |--settings.py
     |  |--urls.py
     |  |-- ...
     |--app1
     |--app2
     |--...
