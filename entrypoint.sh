#! /bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py super_ruby
# python manage.py runserver 0.0.0.0:8000
python manage.py collectstatic --noinput
gunicorn --workers 4 --bind 0.0.0.0:8000 splitwise.wsgi
