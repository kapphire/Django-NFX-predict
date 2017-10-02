# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0021_product_nav_total_unit'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalAddPlayUnconv',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('acres', models.FloatField()),
                ('risk', models.FloatField()),
                ('spacing', models.FloatField()),
                ('zones', models.FloatField()),
                ('zone_pros', models.FloatField()),
                ('rigs', models.FloatField()),
                ('drill', models.FloatField()),
                ('wells', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_unconv_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_unconv_tickers', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='TotalInit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('net_asset_summary', models.FloatField()),
                ('inflation', models.FloatField()),
                ('rig_case', models.IntegerField()),
                ('m_a_case', models.IntegerField()),
                ('ngl_wti', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('r_calc', models.FloatField()),
                ('year', models.CharField(max_length=100)),
                ('boe_mcfe', models.IntegerField()),
                ('play', models.ForeignKey(related_name='total_init_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_init_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
