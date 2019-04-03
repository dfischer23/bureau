#!/bin/sh
set -e

/venv/bin/python manage.py makemigrations --noinput people
/venv/bin/python manage.py makemigrations --noinput schedule
/venv/bin/python manage.py migrate --noinput
/venv/bin/python manage.py collectstatic --noinput

exec "$@"
