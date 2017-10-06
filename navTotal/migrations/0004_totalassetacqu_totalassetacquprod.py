# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0021_product_nav_total_unit'),
        ('navTotal', '0003_auto_20171002_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalAssetAcqu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sources_share_fst', models.FloatField()),
                ('sources_share_sec', models.FloatField()),
                ('sources_share_cash', models.FloatField()),
                ('sources_share_total', models.FloatField()),
                ('uses_acres', models.FloatField()),
                ('uses_ip30', models.FloatField()),
                ('uses_cost', models.FloatField()),
                ('uses_eur', models.FloatField()),
                ('uses_f_d', models.FloatField()),
                ('uses_pud', models.FloatField()),
                ('choice', models.IntegerField()),
                ('play', models.ForeignKey(related_name='total_acquisition_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_acquisition_tickers', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='TotalAssetAcquProd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eur_mix_val', models.FloatField()),
                ('prod_mix_val', models.FloatField()),
                ('prod_mboepd_val', models.FloatField()),
                ('proved_mix_val', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_acquisition_prod_plays', to='typeCurves.Play')),
                ('prod', models.ForeignKey(related_name='total_acquisition_prod_products', to='navProved.Product')),
                ('ticker', models.ForeignKey(related_name='total_acquisition_prod_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
