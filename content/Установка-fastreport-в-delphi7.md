Title: Установка FastReport в Delphi7
Date: 2008-12-05 21:11
Category: IT
Tags: delphi
Author: Swasher

Используем FR_4_7_9.rar. Распаковываем. Запускаем recompile.exe  
  
Выбираем компилер, меняем язык на русский, Recompile all packages. Жмем
компилять. У нас должна образоваться папка LibD7.  
  
Копируем эту папку в `C:\Program Files\Borland\Delphi7\fastreport\LibD7` (например).
Добавляем путь к ней в `Tools->Environment Options -> Library -> Library Path`
  
Теперь надо проинсталлировать полученные BPL:  
Идем в эту папку, запускаем fs7.dpk, появляется диалог, жмем Compile.
  
Запускаем dclfrx7.dpk, в диалоге жмем Compile, потом Install.  
Повторяем процедуру (Compile-Install) для следующих Design-time пакетов:

dclfs\*.dpk  
dclfsDB\*.dpk  
dclfsBDE\*.dpk  
dclfsADO\*.dpk  
dclfsIBX\*.dpk  
dclfsTee\*.dpk  
dclfrx\*.dpk  
dclfrxDB\*.dpk  
dclfrxIBO\*.dpk  
dclfrxBDE\*.dpk  
dclfrxADO\*.dpk  
dclfrxIBX\*.dpk  
dclfrxDBX\*.dpk  
dclfrxTee\*.dpk  
dclfrxe\*.dpk  
  
При закрытии окна компиляции и инстала, спрашивают, надо ли сохранятся.
Тут я хз, наверное надо отвечать "да".
