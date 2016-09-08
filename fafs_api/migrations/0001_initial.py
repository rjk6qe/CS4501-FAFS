# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, blank=True, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('rating', models.IntegerField()),
                ('phone_number', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=75)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='school_id',
            field=models.OneToOneField(to='fafs_api.School'),
        ),
    ]
