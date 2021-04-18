#!/bin/sh

set -e

python manage.py collectstatic -noinput
python manage.py migrate
python manage.py createsu
python manage.py fixtures dropdowns

uwsgi --socket :8000 --master --enable-threads --module cst8333.wsgi