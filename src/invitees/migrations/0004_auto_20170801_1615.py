# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-08-01 16:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invitees', '0003_auto_20170722_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='choice',
            field=models.CharField(blank=True, choices=[('yes', 'yes'), ('no', 'no')], max_length=4, null=True),
        ),
    ]
