# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0012_auto_20170912_1108'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionTotal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_total_unit', models.CharField(max_length=100)),
                ('prod_total_value', models.FloatField()),
                ('ticker', models.ForeignKey(related_name='productionTotals', to='navProved.Ticker')),
            ],
        ),
    ]
