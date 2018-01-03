# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2018-01-03 21:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('email', models.EmailField(blank=True, max_length=200)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='core.Comment')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='ShipCoordinates',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.FloatField(null=True)),
                ('longitude', models.FloatField(null=True)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ShipDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('remarks', models.CharField(blank=True, max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='ShipImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('title', models.CharField(max_length=200)),
                ('image_description', models.TextField(blank=True)),
                ('artist', models.CharField(max_length=200)),
                ('created', models.CharField(max_length=200)),
                ('source_url', models.URLField()),
                ('usage_terms', models.CharField(max_length=250)),
                ('license_url', models.URLField()),
                ('license_short_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='ShipList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ship', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('region', models.CharField(blank=True, max_length=250)),
                ('city', models.CharField(blank=True, max_length=250)),
                ('from_country', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=20)),
                ('ship_class', models.CharField(blank=True, max_length=200)),
                ('ship_type', models.CharField(blank=True, max_length=200)),
                ('remarks', models.CharField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.AddField(
            model_name='shipimage',
            name='ship',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='ship_image', to='core.ShipList'),
        ),
        migrations.AddField(
            model_name='shipdetails',
            name='ship',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='core.ShipList'),
        ),
        migrations.AddField(
            model_name='shipcoordinates',
            name='ship',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='coordinates', to='core.ShipList'),
        ),
        migrations.AddField(
            model_name='comment',
            name='ship',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='core.ShipList'),
        ),
    ]
