#!/bin/sh
set -e

DBFILE=/data/db.sqlite3

if [ ! -e $DBFILE ]; then
	echo "Bureau: Initializing database."
	/venv/bin/python manage.py makemigrations --noinput
	/venv/bin/python manage.py migrate --noinput
	/venv/bin/python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@foo.com', 's3cr3t')"
else 
	echo "Bureau: Migrating database."
	/venv/bin/python manage.py makemigrations --noinput
	/venv/bin/python manage.py migrate --noinput
fi


/venv/bin/python manage.py collectstatic --noinput

echo "Bureau: Done, starting."

exec "$@"
