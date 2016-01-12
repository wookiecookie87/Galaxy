# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-11 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('galaxy', '0003_auto_20160111_0742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action_info',
            name='point_1_x',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='action_info',
            name='point_1_y',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='action_info',
            name='point_2_x',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
        migrations.AlterField(
            model_name='action_info',
            name='point_2_y',
            field=models.DecimalField(decimal_places=4, max_digits=8),
        ),
    ]