# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('diff', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
            ],
            options={
                'ordering': ('-name',),
            },
        ),
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('esc', models.FloatField()),
                ('disc_factor', models.FloatField()),
                ('oil_diff', models.FloatField()),
                ('gas_diff', models.FloatField()),
                ('ngl_pers_wti', models.FloatField()),
                ('prod_taxes', models.FloatField()),
                ('tax_rate', models.FloatField()),
                ('deferred', models.FloatField()),
                ('op_cost_esc', models.FloatField()),
                ('dda', models.FloatField()),
                ('def_after_5yrs', models.FloatField()),
            ],
        ),
        migrations.AddField(
            model_name='price',
            name='prod',
            field=models.ForeignKey(related_name='prod_prices', to='navProved.Product'),
        ),
        migrations.AddField(
            model_name='price',
            name='ticker',
            field=models.ForeignKey(related_name='ticker_prices', to='navProved.Ticker'),
        ),
    ]
