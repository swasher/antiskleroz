Title: Памятка South Quick Start
Date: 2014-06-25 14:12
Category: IT
Tags: django, south
Author: Swasher

Памятка South Quick Start

Устанавливаем South

    ::console
    pip install South

Добавляем его в INSTALLED_APPS

    ::py
    INSTALLED_APPS = (
        'django.contrib.auth',
        '...'
        'south',
    )

Синхронизируем базу, при этом South создает миграционные таблицы

    ::console
    # ./manage.py syncdb

Включаем отслеживание измнений для нашего приложения, создание первонональной "миграции"

    ::console
    # python manage.py convert_to_south <our_app>

Теперь, после изменения модели, создаем новую "миграцию"

    ::console
    # python manage.py schemamigration  <app_name> <migration_name> --auto

И применяем ее

    ::console
    # python manage.py migrate nfoapp