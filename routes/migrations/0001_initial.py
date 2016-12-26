# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 20:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Drone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=200)),
                ('weight', models.FloatField()),
                ('add_weight', models.FloatField()),
                ('speed', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=500)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('load_title', models.CharField(max_length=200)),
                ('load_weight', models.FloatField()),
                ('time', models.DateTimeField()),
                ('distance', models.FloatField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('drone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='routes.Drone')),
                ('end_point', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='end_point', to='routes.Location')),
                ('start_point', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='start_point', to='routes.Location')),
            ],
        ),
    ]
