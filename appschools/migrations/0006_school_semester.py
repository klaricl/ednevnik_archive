# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-12 12:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appschools', '0005_school_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='school',
            name='semester',
            field=models.IntegerField(default=1),
        ),
    ]