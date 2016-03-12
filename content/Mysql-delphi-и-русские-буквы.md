Title: MySQL, Delphi и русские буквы
Date: 2008-12-04 21:51
Category: IT
Tags: delphi, mysql
Author: Swasher
Slug: delphi-mysql-and-ruusian-fonts

Что нужно сделать, чтобы в связке КЛИЕНТ(WindowsXP+Delphi) и
СЕРВЕР(Linux+MySQL) корректно отображались русские буквы?

Перепробовав кучу настроек в разных местах и прочитав много форумов,
мануалов и хау-ту, выяснил, что ларчик просто открывался.

Добавляем в конфиг мускуля строчки в секцию mysqld:

   [mysqld]
   skip-character-set-client-handshake
   default_character_set=cp1251

При создании таблиц нужно использовать кодировку cp1251_general_ci. Вот и все!

Использовалось:

- Windows XP SP3 русский
- Delphi 7
- Ubuntu server 8.10
- MySQL 5.0 из репозитариев
