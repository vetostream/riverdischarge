# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riverdash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_battery',
            field=models.DecimalField(decimal_places=6, max_digits=11, null=True),
        ),
    ]
