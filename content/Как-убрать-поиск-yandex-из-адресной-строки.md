Title: Как убрать поиск Yandex из адресной строки Firefox?
Date: 2009-09-11 23:43
Category: IT
Author: Swasher
Slug: remove-yandex

Для этого Набираем в адресной строке браузера `about:config`
  
Для смены поисковой системы поменять значение параметра `keyword.URL` на соответствующее другой поисковой системе;

-   для отключения функции поиска из адресной строки нужно поменять значение параметра `keyword.enabled` на **false**.
-   Для того чтобы вернуть режим поиска через Google (как в версии 3.0.*) значение ключа `keyword.URL` должно быть таким:
   `http://www.google.com/search?ie=UTF-8&oe;=UTF-8&sourceid;=navclient&gfns;=1&q;=`
