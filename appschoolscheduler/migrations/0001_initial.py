# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 19:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('appschoolsubjects', '0004_auto_20180603_1056'),
        ('appschools', '0009_schoolclass_shift'),
    ]

    operations = [
        migrations.CreateModel(
            name='SchoolScheduler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('order', models.IntegerField()),
                ('shift', models.IntegerField()),
                ('razred', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appschools.SchoolClass')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appschoolsubjects.SchoolSubject')),
            ],
        ),
    ]