Устанавливаем окружение

virtualenv vblogs -p python3.5
source vblogs/bin/activate
git clone https://marge-m284@bitbucket.org/marge-m284/blogs.git
cd blogs
pip install -r requirements.txt

Создаем PostgreSQL базу:
```
psql
create user blogs_user with password 'password';
alter role blogs_user set client_encoding to 'utf8';
alter role blogs_user set default_transaction_isolation to 'read committed';
alter role blogs_user set timezone to 'UTC';
ALTER USER blogs_user CREATEDB;
create database blogs_test owner blogs_user;
\q
```


Миграции и запуск:
```
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```
