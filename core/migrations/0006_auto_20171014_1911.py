# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-14 19:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20171014_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipimage',
            name='ship',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_image', to='core.ShipList'),
        ),
    ]
