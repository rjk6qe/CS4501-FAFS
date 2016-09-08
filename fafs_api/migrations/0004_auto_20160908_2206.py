# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fafs_api', '0003_auto_20160908_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='school_id',
            field=models.ForeignKey(to='fafs_api.School'),
        ),
    ]
