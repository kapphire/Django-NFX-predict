# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0021_product_nav_total_unit'),
        ('navTotal', '0018_auto_20171006_0729'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalNetLandingChange',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sale_proceeds_s', models.FloatField()),
                ('sale_carries_s', models.FloatField()),
                ('equity_s', models.FloatField()),
                ('monies_s', models.FloatField()),
                ('carries_s', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_net_landing_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_net_landing_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
