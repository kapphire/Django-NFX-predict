# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0021_product_nav_total_unit'),
        ('navTotal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalEquityOffering',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('chocie', models.IntegerField()),
                ('share_amount', models.FloatField()),
                ('shoe', models.FloatField()),
                ('last_price', models.FloatField()),
                ('gross_issue', models.FloatField()),
                ('net_issue', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_equity_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_equity_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
