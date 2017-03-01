# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-28 21:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('riverdash', '0002_auto_20170228_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyDischarge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('river_profile', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('discharge', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('stage', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('month', models.IntegerField(default=0)),
                ('part', models.IntegerField(default=0)),
            ],
        ),
    ]
