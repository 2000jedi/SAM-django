# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-12-08 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0002_auto_20161208_1900'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalAssignment',
            fields=[
                ('id', models.IntegerField(auto_created=True, primary_key=True, serialize=False, unique=True)),
                ('assignment', models.ManyToManyField(to='assignment.Assignment')),
                ('student', models.ManyToManyField(to='assignment.Student')),
            ],
        ),
        migrations.AddField(
            model_name='class',
            name='assignments',
            field=models.ManyToManyField(to='assignment.Assignment'),
        ),
    ]
