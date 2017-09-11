# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0003_auto_20170907_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticker',
            name='op_cost',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='prod_gas',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='prod_ngl',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='prod_oil',
            field=models.FloatField(),
        ),
    ]
