# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0007_auto_20170908_1007'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='disc_factor',
            field=models.FloatField(default=10),
        ),
    ]
