# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0005_auto_20170929_0742'),
        ('navProved', '0022_auto_20171009_0832'),
        ('navTotal', '0019_totalnetlandingchange'),
    ]

    operations = [
        migrations.CreateModel(
            name='TotalLandingResults',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('debt', models.FloatField()),
                ('equivalents', models.FloatField()),
                ('deficit', models.FloatField()),
                ('hedge', models.FloatField()),
                ('play', models.ForeignKey(related_name='results_plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='results_tickers', to='navProved.Ticker')),
            ],
        ),
    ]
