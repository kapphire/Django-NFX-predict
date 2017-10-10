# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0022_auto_20171009_0832'),
        ('navTotal', '0020_totallandingresults'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalAddPlayConv',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lst_hc', models.FloatField()),
                ('flat', models.FloatField()),
                ('lst_prod', models.FloatField()),
                ('dev_cost', models.FloatField()),
                ('wl', models.FloatField()),
                ('operator', models.FloatField()),
                ('royalty', models.FloatField()),
                ('trap', models.FloatField()),
                ('reservoir', models.FloatField()),
                ('seal', models.FloatField()),
                ('timing', models.FloatField()),
                ('commercial', models.FloatField()),
                ('closure', models.FloatField()),
                ('drainage', models.FloatField()),
                ('mean', models.FloatField()),
                ('boe_feet', models.FloatField()),
                ('days_to', models.FloatField()),
                ('oil_conv', models.FloatField()),
                ('gas_conv', models.FloatField()),
                ('risk_conv', models.FloatField()),
                ('proved_book', models.FloatField()),
                ('play', models.ForeignKey(related_name='total_conv_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='total_conv_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
