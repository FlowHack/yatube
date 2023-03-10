# YaTube

Простой сайт для ваших идей, мыслей и мечтаний

## ***Технологии***
```
Python 3.8.5
Django 2.2.6
Django REST Framework
Django REST Framework - simplejwt
```

## ***Запуск при помощи Python 3.8.5***
* Для начала создайте виртуальное окружение и установите зависимости
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

* Выполните миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

* Создайте суперпользователя
```bash
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
```
* Запустите сервер
```bash
python manage.py runserver
```
