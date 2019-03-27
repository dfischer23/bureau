
# For now, just some notes

## starting server

`# python manage.py runserver`

## change passwords manually

```
# python manage.py shell
from django.contrib.auth.models import User
users = User.objects.all()
print(users)
user = users[0]
user.set_password('_new_password_')
user.save()
```


## setup pi

https://mikesmithers.wordpress.com/2017/02/21/configuring-django-with-apache-on-a-raspberry-pi/


https://docs.djangoproject.com/en/1.11/ref/contrib/staticfiles/#django-admin-collectstatic

kleinundalleszusammen

### in the venv:
./manage.py collectstatic
./manage.py createsuperuser
./manage.py compilemessages
./manage.py migrate


./manage.py import /tmp/in.csv 



## TODO

elternpostliste: (gefiltert) schüler, jeder erziehungsberechtigter, dann nach postadresse kombinieren ("Daniel und Sylvia Fischer") -> ist das wirklich notwendig?
mailliste: einfach alle erziehungsberechtigten aller (gefiltert) schüler
pip install django-multiselectfield
