# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-08 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0004_auto_20161208_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='passwd',
        ),
        migrations.AlterField(
            model_name='user',
            name='ChineseName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='EnglishName',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
