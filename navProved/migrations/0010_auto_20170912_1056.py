# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0009_auto_20170912_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_initial_value',
            field=models.FloatField(default=10),
        ),
        migrations.AlterField(
            model_name='product',
            name='ticker',
            field=models.ForeignKey(related_name='products', to='navProved.Ticker'),
        ),
    ]
