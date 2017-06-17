Title: Миграция модели между приложениями
Date: 2017-06-17 18:56
Tags: django, migrations
Category: IT
Author: Swasher

Предположим, мы хотим перенсти модель Car в другое приложение. Стандартными средствами
Django этого делать не позволяет.

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
        
#### 1. Переносим модель из старой app в новую

cut'n'paste

#### 2. Исправляем импорты и внешние ключи

Проверяем все места, где импортировалась наша модель, и где на нее были внешние ключи, 
исправляем на новое `newapp`. Проверить поможет команда `manage.py check`

#### 3. Создаем миграции

    $ manage.py makemigrations

Если сейчас запустить `migrate`, получим ошибку `django.db.utils.IntegrityError: 
insert or update on table "oldapp_dependedtable" violates foreign key constraint...`,
потому что мы удалили таблицу, которая содержит данные, на которые указывают ключи из
другой таблицы.

Так как авто-миграции не работают, на нужно создать свои файлы миграций. Начнем с
исходного приложения:

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
        ('oldapp', '0005_auto_20170406_1300'), # Change dependency to NOT use last auto-migration
    ]

0007_auto_20170617_1808.py:

    dependencies = [
        ('oldapp', '0006_auto_20170617_1922'), # I changed the number so this 
                                                  # auto-generated migration would be
                                                  # after the custom one.
        ('newapp', '0001_initial'), # Make certain the tires db state is setup
    ]

#### 6. Редактируем нашу пустую миграцию

Здеась мы разделяем операции `state` и `database`. Название таблицы меням на новое
приложение, а состояние - удалено.

    class Migration(migrations.Migration):
    
        dependencies = [
            ('oldapp', '0005_auto_20170406_1300'),
        ]
    
        database_operations = [
            migrations.AlterModelTable('Car', 'newapp_Car')  
            # здесь указываем исходное имя модели ('Car') и конечное (newapp_Car'), 
            # обычно в формате app_model
        ]
    
        state_operations = [
            migrations.DeleteModel('Car')
        ]
    
        operations = [
            migrations.SeparateDatabaseAndState(
                database_operations=database_operations,
                state_operations=state_operations)
        ]
 
#### 7. Переходим к миграции для нового приложения (newapp)

В моем случае это 0001_initial.py. Обратите внимаение, в шаге 5 эта миграция
используется как зависимость.
  
    class Migration(migrations.Migration):
    
        dependencies = [
            # Установить эту зависимость на ПЕРВУЮ кастомную миграцию в oldapp
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
        
#### Возвращаемся к oldapp и редактируем авто-сгенерированную миграцию

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
        
#### At last...

И последнее, но не менее важное: вам нужно сделать окончательную custom-миграцию в старом приложении.
Здесь мы сделаем операцию «state» только для удаления модели oldapp.Car.
Выполняется state-only  потому, что таблица базы данных для oldapp.Car уже переименована. 
Эта последняя миграция очищает оставшееся состояние Django.


    class Migration(migrations.Migration):
    
        dependencies = [
            ('cars', '0003_auto_20150603_0630'),
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