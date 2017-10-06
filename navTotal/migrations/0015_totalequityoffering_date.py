# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0014_auto_20171005_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalequityoffering',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
