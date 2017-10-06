# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0004_totalassetacqu_totalassetacquprod'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalassetacqu',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
