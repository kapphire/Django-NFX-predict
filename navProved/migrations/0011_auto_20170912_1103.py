# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0010_auto_20170912_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='year',
            field=models.IntegerField(default=2016),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_initial_value',
            field=models.FloatField(),
        ),
    ]
