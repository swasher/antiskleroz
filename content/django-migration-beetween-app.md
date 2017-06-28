Title: Django: Миграция модели между приложениями
Date: 2017-06-17 18:56
Tags: django, migrations
Category: IT
Author: Swasher

Предположим, мы хотим перенсти модель Car в другое приложение. Стандартными средствами
Django этого делать не позволяет.

> ВНИМАНИЕ!!! Бекап базы обязателен! Скорее всего, понадобится не одна попытка, чтобы 
> выполнить этот квест по перемещению модели.

> ВНИМАНИЕ!!! Внимательно читаем комментарии в коде, там описаны критически важные действия

Было:

    ::bash
    project
      |_ oldapp
        |_ model Car
      |_ newapp
    
Должно получиться:

    ::bash
    project
      |_ oldapp
      |_ newapp
        |_ model Car
        
Забегая немного вперед. У нас всего должно получится 4 файла миграции. После makemigration на 
шаге 3 будет 1 автомиграция в newapp и 1 автомиграция в oldapp, и еще вручную 
добавим 2 миграции в oldapp. На шаге 5 ручную миграцию в oldapp поставим *перед* 
авто-миграцией, и у нас в итоге получится такая картина:

    ::bash
    project
      |_ oldapp
      |  |_ migrations
      |      |-0005_auto_20170406_1300.py  <- старая миграция, еще до наших действий
      |      |-0006_auto_20170617_1922.py  <- пустая миграция [database_operations изменяем имя 
      |      |                                таблицы на новую модель: newapp_car]
      |      |-0007_auto_20170617_1808.py  <- автомиграция
      |      |_0008_auto_20170617_1908.py  <- пустая миграция [state_operations удаление старой
      |                                       таблицы]
      |_ newapp
        |_ migrations
        |    |_0001_initial.py             <- [state_operations - создание новой таблицы]
        |                                     Это может быть не стартовая миграция, а просто 
        |                                     следующая в модели newapp
        |_ Model Car
        
Зависимости миграций, для наглядности, выглядят так:

![](http://res.cloudinary.com/swasher/image/upload/v1497880974/blog/migration_dependencies.png)
        
#### 1. Переносим модель из старой app в новую

cut'n'paste

#### 2. Исправляем импорты и внешние ключи

Проверяем все места, где импортировалась наша модель, и где на нее были внешние ключи, 
исправляем на новое `newapp`. Проверить можно, выполнив `manage.py check`

#### 3. Создаем миграции

    ::bash
    $ manage.py makemigrations
    
    Migrations for 'newapp':
      newapp/migrations/0001_initial.py
        - Create model Car
    Migrations for 'oldapp':
      oldapp/migrations/0006_auto_20170617_1808.py
        - Alter field customer on rental
        - Delete model Car

Строка `Alter field customer on rental` означает, что у нас есть таблица Rental, которая
имеет внешний ключ на нашу модель Car:

    ::python
    # in oldapp
    class Rental(models.Model):
        customer = models.ForeignKey(Car)
        
Миграция изменила этот ключ в соответсвии с новой таблицей newapp.Car.

Если сейчас запустить `migrate`, получим ошибку `django.db.utils.IntegrityError: 
insert or update on table "oldapp_dependedtable" violates foreign key constraint...`,
потому что мы удалили таблицу, которая содержит данные, на которые указывают ключи из
другой таблицы.

#### 3.1. Fix errors

У меня в реальном приложении перемещаемая модель Employee имела one-to-one отношение к 
модели User, и я получил такую ошибку:

    ::bash
    $ python manage.py makemigrations
    SystemCheckError: System check identified some issues:
    
    ERRORS:
    core.Employee.user: (fields.E304) Reverse accessor for 'Employee.user' clashes with \
    reverse accessor for 'Employee.user'.
        HINT: Add or change a related_name argument to the definition for 
        'Employee.user' or 'Employee.user'.
    core.Employee.user: (fields.E305) Reverse query name for 'Employee.user' clashes with 
    reverse query name for 'Employee.user'.
        HINT: Add or change a related_name argument to the definition for 
        'Employee.user' or 'Employee.user'.
    workflow.Employee.user: (fields.E304) Reverse accessor for 'Employee.user' clashes with \
    reverse accessor for 'Employee.user'.
        HINT: Add or change a related_name argument to the definition for 
        'Employee.user' or 'Employee.user'.
    workflow.Employee.user: (fields.E305) Reverse query name for 'Employee.user' clashes with \
    reverse query name for 'Employee.user'.
        HINT: Add or change a related_name argument to the definition for 
        'Employee.user' or 'Employee.user'.

Если добавить `related_name` в старом приложении, это фиксит проблему:

    ::python
    class Employee(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')


#### 4. Создаем пустую миграцию в старом `app`

теперь созданим свои custom-миграции. Начнем с исходного приложения.

    ::bash
    $ python manage.py makemigrations old_app --empty
    
#### 5. Меням последовательность миграций

Эта созанная нами миграция должна выполнится ДО удаления модели, то есть ей нужно 
присвоить номер, меньший на 1, чем последняя автомиграция, и соответствующим образом
исправить `dependencies `. Например, было

    ::text
    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1808.py  <- миграция с шага 3

Послое makemigrations имеем

    ::text
    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1808.py  <- миграция с шага 3
    0007_auto_20170617_1922.py  <- пустая миграция с шага 4

Переименовываем файлы следуюшим образом

    ::text
    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1922.py  <- пустая миграция с шага 4
    0007_auto_20170617_1808.py  <- миграция с шага 3

и меняем в двух последних миграциях зависимости:

0006_auto_20170617_1922.py:

    ::python
    dependencies = [
        # не забываем изменить зависимость на предыщую миграцию
        ('oldapp', '0005_auto_xxx'), 
    ]

0007_auto_20170617_1808.py:

    ::python
    dependencies = [
        ('oldapp', '0006_auto_20170617_1922'),    # Меняем последовательность миграций
                                                  # в зависимостях
        ('newapp', '0001_initial'), # Добавляем зависимость от миграции в newapp
    ]

#### 6. Редактируем нашу пустую миграцию [1 of 3 in oldapp, 006]

Здесь мы разделяем операции `state` и `database`. Цель этого шага - изменить название 
таблицы, не трогая состояние.

    ::python
    class Migration(migrations.Migration):
    
        dependencies = [
            # не забываем изменить зависимость на предыщую миграцию
            ('oldapp', '0005_auto_xxx'),
        ]
    
        database_operations = [
            # здесь указываем исходное имя модели ('Car') и конечное (newapp_Car'), 
            # обычно в формате app_model, в нижнем регистре
            migrations.AlterModelTable('Car', 'newapp_Car')  
        ]
        
        # Состояние пока-что не изменяем
        state_operations = [
        ]
    
        operations = [
            migrations.SeparateDatabaseAndState(
                database_operations=database_operations,
                state_operations=state_operations)
        ]
 
#### 7. Переходим к миграции для нового приложения (newapp)

Операции в порядке, но мы хотим изменить только «состояние», а не базу данных. 
Зачем? Потому что мы фактически сохраняем таблицы базы данных из старого приложения. 
Кроме того, мы должны убедиться, что изменение database произойдет ДО выполнения этой
миграции (указывает первую из трех соданных миграций в oldapp в качестве зависимости)

В моем случае это 0001_initial.py. Обратите внимаение, в шаге 5 эта миграция
используется как зависимость.
  
    ::python
    class Migration(migrations.Migration):
    
        dependencies = [
            # Установить эту зависимость на ПЕРВУЮ кастомную миграцию в oldapp, 
            # в которой мы изменили database без изменения state
            # Если django создал тут еще и другие зависимости - оставляем их
            ('oldapp', '0006_auto_20170617_1922'),
        ]
    
        # Измняем "operations" на "state_operations" (операция выполнится только для 
        # state, но не database)
        state_operations = [
            # Эти операции были сгенерированы автоматически функцией makemigrations.
            migrations.CreateModel(
                name='Car',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, \
                        auto_created=True, primary_key=True)),
                    ('name', models.CharField(max_length=40, verbose_name=b'Brand Name')),
                    ('color', models.CharField(max_length=40, verbose_name=b'Color')),
                ],
                options={
                    'verbose_name_plural': 'Cars',
                },
            ),
        ]
    
        operations = [
            # Запуская только "state operations", мы засталяем Django думать, что он
            # применяем миграции к базе данных. В действительности, мы уже переименовали
            # таблицу "oldapp_cars" в "newapp_cars" ранее.
            migrations.SeparateDatabaseAndState(state_operations=state_operations)
        ]
        
#### Возвращаемся к oldapp и редактируем авто-сгенерированную миграцию [2 of 3 in oldapp, 007]

Редактируем `0007_auto_20170617_1808.py`, которая сгенерировалась еще на шаге 3.

    ::python
    class Migration(migrations.Migration):
    
        dependencies = [
            ('oldapp', '0006_auto_20170617_1922'), # Меняем название файла на авто-
                                                   # сгенерированную миграцию
            
                                                    # auto-generated migration would be
                                                 # after the custom one.
            ('newapp', '0001_initial'), # Указываем миграцию из нового app.
        ]
    
        # Эта миграция была авто-сгенерирована для изменения ForeignKey, которые
        # указываюn на нашу таблицу.
        # Нам нужно только удалить операцию DeleteModel, потому что эта модель в данный 
        # момент существует state-only
        operations = [
            migrations.AlterField(
                model_name='car',
                name='tires',
                field=models.ForeignKey(to='newapp.Car'),
            ),
            migrations.AlterField(
                model_name='car',
                name='year',
                field=models.IntegerField(default=2015, verbose_name='Year'),
            ),
            
            # Внизу удаляем DeleteModel. Удалять будем в следующей миграции.
        ]
        
#### At last... [3 of 3 in oldapp, 008]

И последнее, но не менее важное: вам нужно сделать окончательную custom-миграцию в старом приложении.
Здесь мы сделаем операцию «state» только для удаления модели oldapp.Car.
Выполняется state-only  потому, что таблица базы данных для oldapp.Car уже переименована. 
Эта последняя миграция очищает оставшееся состояние Django. Создаем еще одну миграцию `008`
в oldapp (`makemigration oldapp --empty`):


    ::python
    class Migration(migrations.Migration):
    
        dependencies = [
            ('oldapp', '0007_auto_20170617_1922'),
        ]
    
        # Здесь нужно изменить operations на state_operations, потому что модель в ДБ 
        # была переименована, и она более не существует для Django
        state_operations = [
            # Copy-paste из из авто-сгенерированной операции на предыдущем шаге 
            migrations.DeleteModel(
                name='Tires',
            ),
        ]
    
        operations = [
            # После этой state-операции, состояние Django будет соответсвовать 
            # реальной структуре в базе данных.
            migrations.SeparateDatabaseAndState(state_operations=state_operations)
        ]
        
#### Finally

    ::bash
    $ manage.py migrate