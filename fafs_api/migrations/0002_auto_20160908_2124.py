# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fafs_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(blank=True),
        ),
    ]
