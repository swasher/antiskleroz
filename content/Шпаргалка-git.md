Title: Шпаргалка git
Date: 2012-04-02 20:50
Category: IT
Tags: git
Author: Swasher

##### Скопировать уже существующий с github

Создать копию репозитория на новой машине: Из каталога, выше, чем репозиторий:

    :::console
    $ git clone git@github.com:swasher/kinobox.git

Это создаст каталог kinobox и в нем полностью рабочий проект. Чтобы клонировать в отличный от kinobox каталог:

    :::console
    $ git clone git@github.com:swasher/kinobox.git moviebox

##### Создать с нуля новый репозиторий из проекта в текущей директории:

Сначала создаем репозиторий на github - назовем example. Чтобы не вводить логин-пароль, настраиваем доступ 
по ssh (см. ниже). Затем в нашей директории выполняем:

    ::console
    git init
    git add <files>
    git commit -m "first commit"
    git remote add origin https://github.com/<user>/<example>.git
    git push -u origin master

Добавить файл в версионный контроль

    :::console
    $ git add <filename>
    $ git add <dirname> - добавит рекурсивно

Удалить файл из контроля:

    :::console
    $ git rm --cached <filename>

Удалить файл из контроля и сам файл:

    :::console
    $ git rm --force <filename>

Для игнорирование определенных файлов добавляем шаблоны в exclude [http://help.github.com/ignore-files/][] После
добавления в exclude файлы не удалятся сами из соммита, их надо удалить вручную:

    :::console
    $ git rm --force <filename>

Коммит подготавливает данные для выполнения push

    :::console
    $ git commit -a -m "Комментарий"

Затем заливка на удаленный сервер `origin` в ветку `master`

    :::console
    $ git push origin master

Или просто

    :::console
    $ git push
    
Просто `git push` может ругаться как то так:
    
    ::text
    warning: push.default is unset; its implicit value is changing in
    Git 2.0 from 'matching' to 'simple'. To squelch this message
    and maintain the current behavior after the default changes, use:
    <сокращено>
    
Это говорит о том, что у нас не указано в явном виде, в какую ветку заливать. Подробно описано тут [prgmr.io][] 
Уставновим simple - это значит, push произойдет в текущую ветку, если ее не существует, она будет создана.
    
    ::console
    $ git config --global push.default simple

Даунлоад изменений(pull)

    :::console
    $ git pull

Чтобы посмотреть, какие удаленные репозитории настроены:

    :::console
    $ git remote -v
    origin  git@github.com:swasher/kinobox.git (fetch)
    origin  git@github.com:swasher/kinobox.git (push)

Инспекция удаленного репозитория

    :::console
    $ git remote show origin

Добавление удаленных репозиториев: Чтобы добавить новый удалённый Git-репозиторий под именем-сокращением, к 
которому будет проще обращаться, выполните git remote add [сокращение] [url]:

    :::console
    $ git remote add origin git@github.com:swasher/kinobox.git

### Как внести коммит в чужой репозиторий

- делаем форк
- скачиваем свой форк - git clone ...
- делаем в своем форке новую ветку, например feature:
 
        ::console
        # git checkout -b feature
        Switched to a new branch 'feature'
    
- вносим изменения

- делаем коммит

        # git commit -a -m "fix something"

- отправляем изменения на github в свой форк

        # git push origin feature

### SSH ключи

> ВНИМАНИЕ! Для того, чтобы при использовании ключа не запрашивался логин/пароль, нужно 
> обращаться к удаленному репозилорию по shh, а не по https. Для примера, это адрес https 
> `https://github.com/<Username>/<Project>.git`, а это ssh `git@github.com:<Username>/<Project>.git`

[Статья Github][] по ключам. Тезисно:

    ::console
    $ ssh-keygen -t rsa -C "your_email@example.com"
    $ clip < ~/.ssh/id_rsa.pub
    
На Github: Accout setting -> SSH Keys -> add -> paste -> Add key
Проверяем:

    ::console
    $ ssh -T git@github.com

Далее, нужно настроить url для использования доступа по ssh. Обычно они выглядят так

    ::console
    $ git remote -v
    origin  https://github.com/<user>/<repo>.git (fetch)
    origin  https://github.com/<user>/<repo>.git (push)

Нужно воспользоваться командой `set-url`

    ::console
    $ git remote set-url origin git@github.com:<user>/<repo>.git

Смотрим, что изменилось

    ::console
    $ git remote -v
    origin  git@github.com:<user>/<repo>.git (fetch)
    origin  git@github.com:<user>/<repo>.git (push)
 
Теперь команды типа push не будут запрашивать логин-пароль.

### Другое 
 
Предупреждение 

    warning: push.default is unset; its implicit value has changed in
    Git 2.0 from 'matching' to 'simple'.
    
Объяснение на [stackoverflow](http://stackoverflow.com/a/13148313/1334825)


  [http://help.github.com/ignore-files/]: http://help.github.com/ignore-files/
    "http://help.github.com/ignore-files/"
  [Статья Github]: https://help.github.com/articles/generating-ssh-keys
  [prgmr.io]: http://prgmr.io/coding/git-push-default/