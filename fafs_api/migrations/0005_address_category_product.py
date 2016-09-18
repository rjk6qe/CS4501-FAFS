# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('fafs_api', '0004_auto_20160908_2206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.IntegerField()),
                ('street_name', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.IntegerField()),
                ('description', models.CharField(max_length=300)),
                ('address_2', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('picture', models.ImageField(upload_to='')),
                ('time_posted', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('pick_up', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=2, default='FS', choices=[('OM', 'Off the market'), ('FS', 'For Sale'), ('N', 'Negotiating'), ('S', 'Sold'), ('E', 'Exchanged')])),
                ('condition', models.CharField(max_length=2, default='N', choices=[('N', 'New condition'), ('UG', 'Used and in good condition'), ('UO', 'Used and in okay condition'), ('UP', 'Used and in poor condition')])),
                ('category', models.ForeignKey(to='fafs_api.Category')),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
