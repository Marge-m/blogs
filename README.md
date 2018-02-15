# README #

Проект сделан с помощью:

* python==3.5.0
* psql==10.0
* virtualenv==15.1.0
* + requirements.txt (django==1.10.5, psycopg2)


### Функционал

Подписка/отписка на блоги - /allblogs/
Лента новостей - /feed/ (можно пометить сообщение прочитанным)
Все остальное - автоматически

### Создаем PostgreSQL базу:
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

### Устанавливаем окружение
```
virtualenv venv -p python3.5
source venv/bin/activate
git clone https://marge-m284@bitbucket.org/marge-m284/blogs.git
cd blogs
```

В blogs/settings.py при необходимости меняем имя ДБ и способ отправки сообщений (pp.129-137).

По дефолту настроен вывод писем в консоль.

Если нужна отправка действующей почтой, то снимаем комментирование gmail-настроек и вводим адрес действующей почты и пароль, а localhost настройки убираем.

```
pip install -r requirements.txt
```

### Миграции и запуск

```
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

### Тесты

```
./manage.py test
```
