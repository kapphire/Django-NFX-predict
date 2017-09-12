# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0011_auto_20170912_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prod_unit',
            field=models.CharField(default=b'MMbbl', max_length=100),
        ),
        migrations.AddField(
            model_name='product',
            name='sample_unit',
            field=models.CharField(default=b'$/bbl', max_length=100),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='year',
            field=models.IntegerField(),
        ),
    ]
