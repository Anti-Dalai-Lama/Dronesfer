# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-26 12:44
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20161225_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='price',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
