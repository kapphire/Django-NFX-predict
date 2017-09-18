# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0020_auto_20170914_1723'),
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
                ('play', models.ForeignKey(related_name='playCommonInputClasses', to='typeCurves.Play')),
            ],
        ),
        migrations.CreateModel(
            name='PlayProdDecline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('decline', models.FloatField()),
                ('play', models.ForeignKey(related_name='playProdDeclines', to='typeCurves.Play')),
            ],
        ),
        migrations.CreateModel(
            name='PlayProduction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('unit', models.CharField(max_length=100)),
                ('diff', models.FloatField()),
                ('play', models.ForeignKey(related_name='playProductions', to='typeCurves.Play')),
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
                ('prod', models.ForeignKey(related_name='playProductionDateChoices', to='typeCurves.PlayProduction')),
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
                ('play', models.ForeignKey(related_name='plays', to='typeCurves.Play')),
                ('ticker', models.ForeignKey(related_name='tickers', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='PlayScrapedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=250)),
                ('value', models.FloatField()),
                ('play', models.ForeignKey(related_name='playScrapedData', to='typeCurves.Play')),
            ],
        ),
        migrations.AddField(
            model_name='playproddecline',
            name='prod',
            field=models.ForeignKey(related_name='playProdDeclines', to='typeCurves.PlayProduction'),
        ),
        migrations.AddField(
            model_name='playproddecline',
            name='ticker',
            field=models.ForeignKey(related_name='playProdDeclines', to='navProved.Ticker'),
        ),
    ]
