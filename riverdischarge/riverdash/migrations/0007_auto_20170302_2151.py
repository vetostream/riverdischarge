# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 21:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riverdash', '0006_auto_20170228_2304'),
    ]

    operations = [
        migrations.AddField(
            model_name='devicereading',
            name='devread_discharge',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
        migrations.AddField(
            model_name='devicereading',
            name='devread_quarter',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='devicereading',
            name='devread_stage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]