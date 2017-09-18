# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0013_productiontotal'),
    ]

    operations = [
        migrations.CreateModel(
            name='Play',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('ticker', models.ForeignKey(related_name='plays', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='PlayCommonInputClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('unit', models.CharField(max_length=250)),
                ('value', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='PlayProduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('unit', models.CharField(max_length=100)),
                ('diff', models.FloatField()),
                ('decline', models.FloatField()),
                ('play', models.ForeignKey(related_name='playProductions', to='navProved.Play')),
            ],
        ),
        migrations.CreateModel(
            name='PlayProductionDateChoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip30', models.FloatField()),
                ('m12', models.FloatField()),
                ('m24', models.FloatField()),
                ('m12_decline', models.FloatField()),
                ('m24_decline', models.FloatField()),
                ('eur_unit', models.CharField(max_length=100)),
                ('production', models.ForeignKey(related_name='playProductionDateChoices', to='navProved.PlayProduction')),
                ('ticker', models.ForeignKey(related_name='playProductionDateChoices', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='PlayResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('irr', models.FloatField()),
                ('pv_10', models.FloatField()),
                ('pv_eur', models.FloatField()),
                ('play', models.ForeignKey(related_name='plays', to='navProved.Play')),
                ('ticker', models.ForeignKey(related_name='tickers', to='navProved.Ticker')),
            ],
        ),
    ]
