# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-18 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0024_auto_20171205_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='short_name',
            field=models.CharField(default='', max_length=100, verbose_name='Short Name'),
            preserve_default=False,
        ),
    ]
