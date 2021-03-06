# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-05 19:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appschoolsubjects', '0004_auto_20180603_1056'),
        ('appschoolscheduler', '0007_presenceofstudent_semester'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonplan',
            name='subject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appschoolsubjects.SchoolSubject'),
        ),
        migrations.AlterField(
            model_name='presenceofstudent',
            name='semester',
            field=models.IntegerField(),
        ),
    ]
