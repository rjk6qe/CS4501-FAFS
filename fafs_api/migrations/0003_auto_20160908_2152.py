# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fafs_api', '0002_auto_20160908_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
