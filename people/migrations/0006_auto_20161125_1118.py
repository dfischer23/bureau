# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_auto_20161125_1107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='contact',
        ),
        migrations.AddField(
            model_name='contact',
            name='address',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='people.Address'),
            preserve_default=False,
        ),
    ]
