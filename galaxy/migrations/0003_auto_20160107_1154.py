# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-07 11:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0002_action_log_actuin_info_galaxy_image_graph_info'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Actuin_Info',
            new_name='Action_Info',
        ),
    ]
