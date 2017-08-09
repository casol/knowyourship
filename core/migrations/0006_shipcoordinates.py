# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-09 17:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20170728_1140'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShipCoordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('country', models.CharField(max_length=50)),
                ('ship', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='core.ShipList')),
            ],
        ),
    ]
