# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0006_predict_prod_pred_opd'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclineRate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('decline_rate', models.FloatField()),
                ('prod', models.ForeignKey(related_name='declineRates', to='navProved.Product')),
                ('ticker', models.ForeignKey(related_name='declineRates', to='navProved.Ticker')),
            ],
        ),
        migrations.CreateModel(
            name='NavProvedResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pv', models.FloatField()),
                ('pv_boe', models.FloatField()),
                ('pv_mcfe', models.FloatField()),
                ('ticker', models.ForeignKey(related_name='navProvedResults', to='navProved.Ticker')),
            ],
        ),
        migrations.RemoveField(
            model_name='predict',
            name='decline_rate',
        ),
        migrations.AlterField(
            model_name='predict',
            name='prod_pred_opd',
            field=models.FloatField(),
        ),
    ]
