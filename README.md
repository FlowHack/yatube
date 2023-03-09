# YaTube

Простой сайт для ваших идей, мыслей и мечтаний

___Для запуска на данном этапе понадобится Python версии 3.8.___


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
