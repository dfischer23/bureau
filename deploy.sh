#!/bin/bash

APP="people"
DBNAME="db.sqlite3"

python3 manage.py migrate
python3 manage.py compilemessages
sudo systemctl restart apache2

