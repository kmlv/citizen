# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-31 23:14
from __future__ import unicode_literals

import django.contrib.sessions.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False, verbose_name='session key')),
                ('session_data', models.TextField(verbose_name='session data')),
                ('expire_date', models.DateTimeField(db_index=True, verbose_name='expire date')),
            ],
            options={
                'verbose_name': 'session',
                'verbose_name_plural': 'sessions',
                'db_table': 'django_session',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.sessions.models.SessionManager()),
            ],
        ),
    ]
