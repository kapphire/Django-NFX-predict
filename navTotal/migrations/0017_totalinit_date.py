# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0016_remove_totalinit_r_calc'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalinit',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
