Title: Миграция модели между приложениями
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

    project
      |_ oldapp
        |_ Car
      |_ newapp
    
Должно получиться:

    project
      |_ oldapp
      |_ newapp
        |_ Car
        
Забегая вперед. У нас всего должно получится 4 файла миграции. После makemigration на 
шаге 3 будет 1 автомиграция в newapp и 1 автомиграция в oldapp, и еще вручную 
добавим 2 миграции в oldapp. На шаге 5 ручную миграцию в oldapp поставим *перед* 
авто-миграцией, и у нас в итоге получится такая картина:

    project
      |_ oldapp
      |  |_ migrations
      |      |-0005_auto_20170406_1300.py  <- старая миграция до наших действий
      |      |-0006_auto_20170617_1922.py  <- пустая миграция [database_operations изменяем имя таблицы на новую модель]
      |      |-0007_auto_20170617_1808.py  <- автомиграция
      |      |_0008_auto_20170617_1908.py  <- пустая миграция [state_operations удаление старой таблицы]
      |_ newapp
        |_ migrations
        |    |_0001_initial.py             <- [state_operations - создание новой таблицы]
        |                                  # Это может быть не стартовая миграция, а просто следующая в модели newapp
        |_ Model Car
        
Зависимости миграция, для наглядности, выглядят так:

[](http://res.cloudinary.com/swasher/image/upload/v1497880974/blog/migration_dependencies.png)
        
#### 1. Переносим модель из старой app в новую

cut'n'paste

#### 2. Исправляем импорты и внешние ключи

Проверяем все места, где импортировалась наша модель, и где на нее были внешние ключи, 
исправляем на новое `newapp`. Проверить можно, выполнив `manage.py check`

#### 3. Создаем миграции

    $ manage.py makemigrations

Если сейчас запустить `migrate`, получим ошибку `django.db.utils.IntegrityError: 
insert or update on table "oldapp_dependedtable" violates foreign key constraint...`,
потому что мы удалили таблицу, которая содержит данные, на которые указывают ключи из
другой таблицы.

Так как авто-миграции не работают, на нужно создать свои файлы миграций. Начнем с
исходного приложения:

#### 3a. Fix errors

В реальном приложении перемещаемая модель Employee имела one-to-one отношение к можели User, и я получил такую ошибку:

    $ python manage.py makemigrations
    SystemCheckError: System check identified some issues:
    
    ERRORS:
    core.Employee.user: (fields.E304) Reverse accessor for 'Employee.user' clashes with reverse accessor for 'Employee.user'.
            HINT: Add or change a related_name argument to the definition for 'Employee.user' or 'Employee.user'.
    core.Employee.user: (fields.E305) Reverse query name for 'Employee.user' clashes with reverse query name for 'Employee.user'.
            HINT: Add or change a related_name argument to the definition for 'Employee.user' or 'Employee.user'.
    workflow.Employee.user: (fields.E304) Reverse accessor for 'Employee.user' clashes with reverse accessor for 'Employee.user'.
            HINT: Add or change a related_name argument to the definition for 'Employee.user' or 'Employee.user'.
    workflow.Employee.user: (fields.E305) Reverse query name for 'Employee.user' clashes with reverse query name for 'Employee.user'.
            HINT: Add or change a related_name argument to the definition for 'Employee.user' or 'Employee.user'.

Если добавить `related_name` в старом приложении, это фиксит проблему:

    class Employee(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='+')


#### 4. Создаем пустую миграцию в старом `app`

    $ python manage.py makemigrations old_app --empty
    
#### 5. Меням последовательность миграций

Эта созанная нами миграция должна выполнится ДО удаления модели, то есть ей нужно 
присвоить номер, меньший на 1, чем последняя автомиграция, и соответствующим образом
исправить `dependencies `. Например, было

    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1808.py  <- миграция с шага 3

Послое makemigrations имеем

    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1808.py  <- миграция с шага 3
    0007_auto_20170617_1922.py  <- новая пустая миграция  

Переименовываем файлы следуюшим образом

    0001_initial.py                 
    0002_auto_20150807_1307.py      
    0003_auto_20150807_1341.py
    0004_auto_20160714_1151.py
    0005_auto_20170406_1300.py
    0006_auto_20170617_1922.py  <- новая пустая миграция 
    0007_auto_20170617_1808.py  <- миграция с шага 3

и меняем в двух последних миграциях зависимости:

0006_auto_20170617_1922.py:

    dependencies = [
        # не забываем изменить зависимость на предыщую миграцию
        ('oldapp', '0005_auto_xxx'), 
    ]

0007_auto_20170617_1808.py:

    dependencies = [
        ('oldapp', '0006_auto_20170617_1922'),    # Меняем последовательность миграций
                                                  # в зависимостях
        ('newapp', '0001_initial'), # Добавляем зависимость от миграции в newapp
    ]

#### 6. Редактируем нашу пустую миграцию [1 of 3 in oldapp, 006]

Здесь мы разделяем операции `state` и `database`. Цель этого шага - изменить название 
таблицы, не трогая состояние.

    class Migration(migrations.Migration):
    
        dependencies = [
            # не забываем изменить зависимость на предыщую миграцию
            ('oldapp', '0005_auto_xxx'),
        ]
    
        database_operations = [
            # здесь указываем исходное имя модели ('Car') и конечное (newapp_Car'), 
            # обычно в формате app_model. Внимание! Case sensetive!
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
  
    class Migration(migrations.Migration):
    
        dependencies = [
            # Установить эту зависимость на ПЕРВУЮ кастомную миграцию в oldapp, 
            # в которой мы изменили database без изменения state
            # Если в django создал тут еще и другие зависимости - оставляем их
            ('oldapp', '0006_auto_20170617_1922'),
        ]
    
        # Измняем "operations" на "state_operations" (операция выполнится только для 
        # state, но не database)
        state_operations = [
            # Эти операции были сгенерированы автоматически функцией makemigrations.
            migrations.CreateModel(
                name='Car',
                fields=[
                    ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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

    class Migration(migrations.Migration):
    
        dependencies = [
            ('oldapp', '0007_auto_20170617_1841'), # Меняем название файла на авто-
                                                    сгенерированную миграцию
            
                                                    # auto-generated migration would be
                                                 # after the custom one.
            ('newapp', '0001_initial'), # Указываем миграцию из нового app.
        ]
    
        # This migration was auto-generated when I changed the model FK references.
        # We need to remove the DeleteModel operation because that model exists in 
        # state only. 
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


    class Migration(migrations.Migration):
    
        dependencies = [
            ('oldapp', '0007_auto_20170617_1922'),
        ]
    
        # This needs to be a state-only operation because the database model was
        # renamed, and no longer exists according to Django.
        state_operations = [
            # Pasted from auto-generated operations in previous step:
            migrations.DeleteModel(
                name='Tires',
            ),
        ]
    
        operations = [
            # After this state operation, the Django DB state should match the 
            # actual database structure.
            migrations.SeparateDatabaseAndState(state_operations=state_operations)
        ]
        
#### Finally

    $ manage.py migrate
    

        
================================================

Вариант номер 2

1. Копируем модель Car из oldapp в newapp

2. Добавляем в newapp.Car класс Meta:

    Class Meta:
        db_table = 'oldapp_Car'
        
3. Создаем миграцию

    $ python manage.py makemigrations newapp
    
4. В этой только что созданной миграции ищем операцию CreateModel, и копируем ее
в newapp/migrations/0001_initial.py, как будто эта модель тут была с самого начала.
Затем удаляем только-что созданную миграцию

PS - Если это первая миграция в newapp, то этот шаг нужно пропустить.

5. Теперь в старом oldapp комментируем создание модели в 0001_initial, и далее во всех
миграциях комментируем все действия с этой моделью.

6. Исправляем во всем проекте все импорты, все внешние ключи нашей модели на newapp.
Also, don't forget that all possible foreign keys to app1.YourModel in migrations have to be changed to app2.YourModel
Так же, не забудьте исправить все внешние ключи в миграция с oldapp.Car на newapp.Car

7. В этот момент, если мы сделаем `manage.py migrate`, - ничего не смигрируется, и если
мы сделаем `manage.py makemigration --dry-run` - никаких новых миграций не создастся.

На этом месте я получил ошибку 
The '... ' was declared with a lazy reference to '...', but app 'app' doesn't provide model 'Car'.

Дальше дело не продвинулось.

Потом я уже догадался, что вероятно дело в последовательнсти миграций... 

 
