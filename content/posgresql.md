Title: Settings up postgresql
Date: 2015-06-27 13:34
Tags: tags
Category: IT
Author: Swasher
Status: draft

Note about postgresql setup for django run.

postgresql.conf
------------------------------------

In postgresql.conf uncoment 

    include_dir = 'conf.d'

create in /etc/postgresql/9.4/main directory conf.d
create in /etc/postgresql/9.4/main/conf.d file mysetup.conf
in /etc/postgresql/9.4/main/conf.d/mysetup.conf write `listen_addresses = '192.168.0.203'`

listen_addresses определяет, какие интерфейсы слушают входяшие соеденения.

- '*' - любые интерфейсы
- '0.0.0.0 '- любые IPv4
- '::' - любые IPv6
- 'ip' - если есть несколько интерфейсов, то можно выбрать один конкретный.

По умолчанию - localhost, но у меня не завелось, пока я не поставил * или IP-адрес машины,
на которой работает Postgresql.


pg_hba.conf
------------------------------------

Next, pg_hba.conf describe which remote connection will be accepted.

Format:
TYPE  DATABASE        USER      ADDRESS                     METHOD
host  pdfuploaddb     swasher   192.168.0.0/24              md5
host  all             all       192.168.0.0 255.255.255.0   trust

=====================================

Step # 4: Test your setup
Use psql command from client system as follows:
psql -h PostgreSQL-IP-ADDRESS -U USERNAME -d DATABASENAME

Connect to remote server by IP address 192.168.1.5 and login using vivek user to connect to sales database, use:
$ psql -h 192.168.1.5 -U vivek -d sales

Where,

-h 192.168.1.5 : Specifies the host name of the machine or IP address (192.168.1.5) on which the server is running.
-U vivek : Connect to the database as the vivek username instead of the default. You must have account and permission to connect as vivek user.
-d sales : Specifies the name of the database (sales) to connect to.


