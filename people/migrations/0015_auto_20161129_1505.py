# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0014_auto_20161125_1604'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='guardians',
            field=models.ManyToManyField(blank=True, related_name='students', to='people.Contact'),
        ),
    ]
