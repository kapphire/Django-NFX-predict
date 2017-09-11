# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0002_auto_20170907_0826'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticker',
            name='op_cost',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ticker',
            name='prod_gas',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ticker',
            name='prod_ngl',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='ticker',
            name='prod_oil',
            field=models.FloatField(default=0),
        ),
    ]
