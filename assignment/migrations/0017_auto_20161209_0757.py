# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-12-08 23:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assignment', '0016_auto_20161208_2232'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='assignments',
            new_name='attachments',
        ),
    ]
