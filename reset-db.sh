#!/bin/bash

read -p "This will delete the active DB and reset all migrations. Are you sure you want to do that? (y/n) " -n 1 -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
	echo -e "\nNot doing anything."
	exit
fi

echo -e "\nOk, resetting..."

APP="people"
DBNAME="db.sqlite3"
MIGRATIONS="$APP/migrations/0*.py"

rm $DBNAME
rm $MIGRATIONS
python manage.py makemigrations $APP
python manage.py migrate
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'fischer@interaktiva.de', 's3cr3t')"
