 Title: Bash completions
Date: 2015-03-23 12:32
Tags: bash, completions
Category: IT
Author: Swasher

Difference between bashrc, bash_profile, profile
--------------------------------------------------

[Understanding](http://stackoverflow.com/questions/415403/whats-the-difference-between-bashrc-bash-profile-and-environment)

    ::console
    /bin/bash
           The bash executable
    /etc/profile
           The systemwide initialization file, executed for login shells
    ~/.bash_profile
           The personal initialization file, executed for login shells
    ~/.bashrc
           The individual per-interactive-shell startup file
    ~/.bash_logout
           The individual login shell cleanup file, executed when a login shell exits
    ~/.inputrc
           Individual readline initialization file

Когда пользователь заходит в систему (в терминал, или по ssh), сначала выполняются ЛОГИН-скрипты
(.login или .profile или .zlogin)

Затем, должен запуститься какой-то шелл. И тогда уже выполняются скрипты от шелла (.bashrc, .tcshrc, .zshrc, etc.)

.profile is simply the login script filename originally used by /bin/sh. 
bash, being generally backwards-compatible with /bin/sh, will read .profile if one exists.


pip
----------------------

`pip` поставляется с поддержкой автодополнения командной строки в Bash и Zsh и позволяет дополнять все команды и опции. 
Чтобы включить этот функционал, нужно просто скопировать необходимый скрипт в файл оболочки (например, .profile или .zprofile), 
выполнив команду, например, для Bash:

    ::console
    $ pip completion --bash >> ~/.profile

[ссылка](http://pip.readthedocs.org/en/0.6.1/#command-line-completion)
    
django
-------------------------

Чтобы активировать режим автодополнения для django, нужно в `~/.bashrc` скопировать содержимое файла
`https://github.com/django/django/blob/master/extras/django_bash_completion`

[ссылка](https://docs.djangoproject.com/en/dev/ref/django-admin/#bash-completion)

fabric
---------------------------

Скрипт взят из обсуждения на гитхабе. Как обычно, копируем в `~/.profile` или `~/.bashrc` 

    ::bash
    #!/bin/sh

    _fabric()
    {
        local cur prev split=false
     
        COMPREPLY=()
        cur=`_get_cword`
        prev=${COMP_WORDS[COMP_CWORD-1]}
        _split_longopt && split=true
     
        case "$prev" in
            -@(f|-fabfile))
                _filedir
                return 0
                ;;
        esac
     
        $split && return 0
     
        if [[ "$cur" == -* ]]; then
            COMPREPLY=( $( compgen -W '-h --help -V --version -l --list -d \
                --display= -r --reject-unknown-hosts -D --disable-known-hosts \
                -u --user= -p --password= -H --hosts= -R --roles= -i -f --fabfile= \
                -w --warn-only -s --shell= -c --config= --hide= --show=' \
                -- "$cur" ) )
        else
            CUSTOM_TASKS=`fab -l 2> /dev/null | awk 'NR>2{ print $1 }'`
            COMPREPLY=( $( compgen -W '$CUSTOM_TASKS' -- "$cur" ) )
        fi
    } &&
    complete -F _fabric fab

[ссылка](https://github.com/fabric/fabric/issues/6)


heroku
----------------------------

Плагин для автокомплита здесь [https://github.com/stefansundin/heroku-bash-completion](https://github.com/stefansundin/heroku-bash-completion)

    $ heroku plugins:install git://github.com/stefansundin/heroku-bash-completion.git
    $ heroku completion:init

Последняя строка должна добавить команду в `.bash_profile`, обычно

    source '$HOME/.heroku/plugins/heroku-bash-completion/heroku-completion.bash'

У меня `.bash_profile` отсутствует, поэтому я добавил ручками:

    echo "source '$HOME/.heroku/plugins/heroku-bash-completion/heroku-completion.bash'" >> .bashrc