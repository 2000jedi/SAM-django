# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-08 12:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0010_auto_20161208_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]