# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0021_product_nav_total_unit'),
        ('navTotal', '0010_auto_20171004_0854'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalAssetSale',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uses_cash', models.FloatField()),
                ('sources_acres', models.FloatField()),
                ('sources_ip30', models.FloatField()),
                ('sources_cost', models.FloatField()),
                ('sources_eur', models.FloatField()),
                ('sources_prod', models.FloatField()),
                ('sources_proved', models.FloatField()),
                ('sources_f_d', models.FloatField()),
                ('sources_pud', models.FloatField()),
                ('choice', models.IntegerField()),
                ('date', models.DateField(default=datetime.date.today)),
                ('play', models.ForeignKey(related_name='total_sale_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_sale_tickers', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='TotalAssetSaleProd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('eur_mix', models.FloatField()),
                ('prod_mix', models.FloatField()),
                ('proved_mix', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_sale_prod_plays', to='typeCurves.Play')),
                ('prod', models.ForeignKey(related_name='total_sale_prod_products', to='navProved.Product')),
                ('ticker', models.ForeignKey(related_name='total_sale_prod_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
