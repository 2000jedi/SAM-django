# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-09 05:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0020_auto_20161209_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='class',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assignment.User'),
        ),
    ]