# Django_stripe
Интернет магазин на Django с Stripe SDK
>
Организован интернет магазин, с переходом и оплатой через Stripe
>
https://g1lza.pythonanywhere.com/
```
Админ зона:

login: adminsite
password: adminsite

Тестовый Юзер:

login: Test
password: zxcv0987
```
## Установка:
### После клонирования репрозитория:
* Установаите виртуальное окружение
```python -m venv venv / python3 -m venv venv```
>
* Активируйте виртуальное окружение
```source venv/Scripts/activate / source venv/bin/activate```
>
* Установите requirements
```pip install -r requirements.txt```
>
* Выполните миграции
```python manage.py migrate```
>
* Запуск сервера
```python manage.py runserver```
>
