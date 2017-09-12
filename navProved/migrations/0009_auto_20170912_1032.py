# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0008_ticker_disc_factor'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ticker',
            field=models.ForeignKey(related_name='products', default=1, to='navProved.Ticker'),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='disc_factor',
            field=models.FloatField(),
        ),
    ]
