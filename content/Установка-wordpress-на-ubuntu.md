Title: Установка wordpress на Ubuntu
Date: 2009-04-29 00:32
Category: IT
Tags: Wordpress
Author: Swasher
Slug: install-wordpress

Испоьзуемая операционая система - Ubuntu 9.04. Обновляемся и устанавливаем

    apt-get install wordpress  
  
Устанавливается вордпресс в `/usr/share/wordpress`
Некоторые полезные файлы в `/usr/share/doc/wordpress/examples`
Так же создает `/etc/wordpress`
  
Способы привязки вордпресса к апачу описаны в `/usr/share/doc/wordpress/examples/apache.conf`, их три:

- мягкой ссылкой в /var/www
- виртуалным хостом  
- алиасом  
  
Используем виртуальный хост, получаем доступ к вордпрессу по swasher.moryak.com.ua  
  
Создаем базу и юзера MySql с помощью прилагаемого скрипта.

    sudo sh /usr/share/doc/wordpress/examples/setup-mysql -n (your mysql user) localhost
  
Подходящее имя юзера - wordpress
  
Руками это можно сделать как описано, например, [здесь][], в разделе **Работа с MySQL клиентом**
  
Рестартим апач

    sudo /etc/init.d/apache2 restart  

Заходим в http://wordpress.domen.com/wp-admin/install.php, или куда
привязали, сразу меняем пароль юзера admin.  
  
Тут оно мне начало ругаться, что не может найти конфиги. Незнаю почему,
но скрипт setup-mysql создал конфиг config-localhost.php, а инсталяция
хочет config-swasher.moryak.com.ua.php. Так что переименовываем один в
другой.  
  
В итоге получаем английский вордпресс.

  [здесь]: http://codex.wordpress.org/%D0%A3%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0_WordPress
