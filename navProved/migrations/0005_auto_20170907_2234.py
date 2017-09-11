# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0004_auto_20170907_0857'),
    ]

    operations = [
        migrations.CreateModel(
            name='Predict',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prod_esc', models.FloatField()),
                ('prod_diff', models.FloatField()),
                ('decline_rate', models.FloatField()),
                ('prod', models.ForeignKey(related_name='predicts', to='navProved.Product')),
            ],
        ),
        migrations.RenameField(
            model_name='ticker',
            old_name='disc_factor',
            new_name='capex',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='esc',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='gas_diff',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='ngl_pers_wti',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='oil_diff',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='prod_gas',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='prod_ngl',
        ),
        migrations.RemoveField(
            model_name='ticker',
            name='prod_oil',
        ),
        migrations.AlterField(
            model_name='price',
            name='prod',
            field=models.ForeignKey(related_name='prices', to='navProved.Product'),
        ),
        migrations.AlterField(
            model_name='price',
            name='ticker',
            field=models.ForeignKey(related_name='prices', to='navProved.Ticker'),
        ),
        migrations.AddField(
            model_name='predict',
            name='ticker',
            field=models.ForeignKey(related_name='predicts', to='navProved.Ticker'),
        ),
    ]
