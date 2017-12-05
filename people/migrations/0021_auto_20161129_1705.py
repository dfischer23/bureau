# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-29 17:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0020_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'verbose_name': 'Notiz', 'verbose_name_plural': 'Notizen'},
        ),
        migrations.AlterField(
            model_name='note',
            name='archived',
            field=models.BooleanField(default=False, verbose_name='Archiviert'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(verbose_name='Inhalt'),
        ),
        migrations.AlterField(
            model_name='note',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Datum'),
        ),
    ]