# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-08 18:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0003_auto_20160107_1154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='graph_info',
            old_name='graph_num',
            new_name='graph_count',
        ),
    ]
