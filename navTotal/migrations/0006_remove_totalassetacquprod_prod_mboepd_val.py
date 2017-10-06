# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0005_totalassetacqu_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalassetacquprod',
            name='prod_mboepd_val',
        ),
    ]
