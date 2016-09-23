# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('time_posted', models.DateTimeField(auto_now_add=True)),
                ('time_updated', models.DateTimeField(auto_now=True)),
                ('pick_up', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=2, default='FS', choices=[('OM', 'Off the market'), ('FS', 'For Sale'), ('N', 'Negotiating'), ('S', 'Sold'), ('E', 'Exchanged')])),
                ('condition', models.CharField(max_length=2, default='N', choices=[('N', 'New condition'), ('UG', 'Used and in good condition'), ('UO', 'Used and in okay condition'), ('UP', 'Used and in poor condition')])),
                ('category_id', models.ForeignKey(to='fafs_api.Category')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=75)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('rating', models.IntegerField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('school_id', models.ForeignKey(to='fafs_api.School')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(related_name='transaction_buyer', to='fafs_api.User'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='product_id',
            field=models.ForeignKey(to='fafs_api.Product'),
        ),
        migrations.AddField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(related_name='transaction_seller', to='fafs_api.User'),
        ),
        migrations.AddField(
            model_name='product',
            name='owner_id',
            field=models.ForeignKey(to='fafs_api.User'),
        ),
    ]
