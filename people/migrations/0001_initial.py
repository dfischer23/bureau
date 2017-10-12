# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-25 10:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(blank=True, max_length=200, verbose_name='Street Address')),
                ('postal_code', models.CharField(blank=True, max_length=200, verbose_name='Postal Code')),
                ('city', models.CharField(blank=True, max_length=200, verbose_name='City')),
                ('alternative', models.CharField(blank=True, max_length=1000, verbose_name='Alternative')),
                ('country', models.CharField(blank=True, max_length=200, verbose_name='Country')),
            ],
            options={
                'verbose_name_plural': 'Postal Addresses',
                'verbose_name': 'Postal Address',
            },
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('kind', models.CharField(choices=[('oth', 'Other'), ('fam', 'Family'), ('com', 'Company'), ('org', 'Organization')], max_length=3, verbose_name='Kind')),
            ],
            options={
                'verbose_name_plural': 'Contacts',
                'verbose_name': 'Contact',
            },
        ),
        migrations.CreateModel(
            name='EMailAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=200, verbose_name='Address')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Description')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Contact', verbose_name='Contact')),
            ],
            options={
                'verbose_name_plural': 'EMailAddresses',
                'verbose_name': 'EMail Address',
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=200, verbose_name='Phone Number')),
                ('description', models.CharField(blank=True, max_length=200, verbose_name='Description')),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Contact', verbose_name='Contact')),
            ],
            options={
                'verbose_name_plural': 'Phone Numbers',
                'verbose_name': 'Phone Number',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=200, verbose_name='Last Name')),
                ('family', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Contact', verbose_name='Family')),
            ],
            options={
                'verbose_name_plural': 'Students',
                'verbose_name': 'Student',
            },
        ),
    ]
