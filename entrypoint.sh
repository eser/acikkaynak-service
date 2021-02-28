#!/usr/bin/env sh

./manage.py migrate --noinput
./manage.py collectstatic --clear --noinput

gunicorn --workers 3 --bind 0.0.0.0:8000 --chdir /usr/src app.wsgi:application
