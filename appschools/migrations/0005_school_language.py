# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-10 22:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appschools', '0004_auto_20180424_1841'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='language',
            field=models.CharField(default='EN', max_length=2),
        ),
    ]