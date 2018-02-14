# README #

Проект сделан с помощью:

* python==3.5.0
* psql==10.0
* virtualenv==15.1.0
* + requirements.txt (django==1.10.5, psycopg2)

### Создаем PostgreSQL базу:

sudo -u postgres psql postgres

create user USER_NAME with password 'password';

alter role USER_NAME set client_encoding to 'utf8';

alter role USER_NAME set default_transaction_isolation to 'read committed';

alter role USER_NAME set timezone to 'UTC';

ALTER USER USER_NAME CREATEDB;

create database blog owner USER_NAME;

\q

### Устанавливаем окружение
virtualenv venv -p python3.5

source venv/bin/activate

git clone https://marge-m284@bitbucket.org/marge-m284/blogs.git

cd blogs

В blogs/settings.py при необходимости меняем имя ДБ и способ отправки сообщений (pp.129-137).

По дефолту настроен вывод писем в консоль.

Если нужна отправка действующей почтой, то git checkout mail и вводим логин-пароль почты в pp.131-132

pip install -r requirements.txt

### Миграции и запуск

./manage.py migrate

./manage.py createsuperuser

./manage.py runserver