# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appschools', '0008_auto_20180625_2039'),
    ]

    operations = [
        migrations.AddField(
            model_name='schoolclass',
            name='shift',
            field=models.IntegerField(default=1),
        ),
    ]
