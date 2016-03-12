Title: Установка ZeosDBO в Delphi7
Date: 2008-12-04 21:23
Category: IT
Tags: delphi, mysql
Author: Swasher
Slug: ustanoka-zeosdbo

На примере версии ZEOSDBO-6.6.4-stable  

1. Распаковываем архив **целиком** в корневую папку дельфи, у меня `C:\Program Files\Borland\Delphi7\zeos`

2. Запускаем Дельфи, жмем `Tools -> Environment Option -> Library -> Library Path` (жмем кнопочку справа от списка путей)  

3. Добавляем путь `$(DELPHI)\zeos\packages\delphi7\build`, жмем ок, ок, закрываем Дельфи, не сохраняем проект.

4. Идем в `$(DELPHI)\zeos\packages\delphi7\`, жмем даблклик на ZeosDbo.bpg. Должна запуститься оболочка дельфи. Вызываем Project
Manager (Ctrl-Alt-F11)
  
5. Жмемь правой кнопкой и выбираем Compile для следующих файлов, в том порядке как перечислено:

    * ZCore.bpl
    * ZParseSql.bpl
    * ZPlain.bpl 
    * ZDbc.bpl
    * ZComponent.bpl  
  
6. Если все откомпилилось без ошибок, жмем правой кнопкой на `ZComponentDesign.bpl` и выбираем Install  
  
7. Закрываем Дельфи, жмем Yes

Zeos готов, можно юзать.

>Важно! Архив нужно распаковывать весь, иначе он не найдеть сорцы (по условным путям)
