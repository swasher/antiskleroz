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

Get DB owner's name in PostgreSql
====================================

You can use the combination of pg_database, pg_users system tables and current_database() function in this way:

    ::sql
    SELECT u.usename
    FROM pg_database d
        JOIN pg_user u ON (d.datdba = u.usesysid)
    WHERE d.datname = (SELECT current_database());

Drop DB
====================================

Login (-h localhost is important)

    $ psql -h localhost -U postgres

Dropdb

    postgres=# DROP DATABASE mydbname;

May be this line in pg_hba.conf will help:

    local   mydbname     postgres                             trust

Create DB
====================================

    $ createdb --username=postgres --owner=swasher --host=localhost mydbname

OR

    postgres=# CREATE DATABASE mydbname;

After create DB, if we want work from another as `postgres` user, we need grant permission to our user:

    $ psql -U postgres mydbname -c "GRANT ALL ON ALL TABLES IN SCHEMA public to user;"
    $ psql -U postgres mydbname -c "GRANT ALL ON ALL SEQUENCES IN SCHEMA public to user;"
    $ psql -U postgres mydbname -c "GRANT ALL ON ALL FUNCTIONS IN SCHEMA public to user;"

Create extension
====================================

    $ psql -U postgres -d mydbname -c 'create extension hstore;'

OR in sql console

    postgres=# \connect mydbname;
    postgres=# CREATE EXTENSION hstore;



