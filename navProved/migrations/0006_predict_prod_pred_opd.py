# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0005_auto_20170907_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='predict',
            name='prod_pred_opd',
            field=models.FloatField(default=1),
        ),
    ]
