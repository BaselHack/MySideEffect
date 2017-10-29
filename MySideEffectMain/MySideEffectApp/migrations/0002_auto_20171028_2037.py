# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 20:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('MySideEffectApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Occurence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('adverse_effects', models.TextField(blank=True, null=True)),
                ('drug_names', models.TextField(blank=True, null=True)),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=30, null=True)),
                ('continent', models.CharField(blank=True, max_length=30, null=True)),
                ('literature_reference', models.CharField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('gender', models.CharField(blank=True, max_length=30, null=True)),
                ('continent', models.CharField(blank=True, max_length=30, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Drug',
        ),
    ]
