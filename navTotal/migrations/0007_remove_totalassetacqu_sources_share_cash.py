# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0006_remove_totalassetacquprod_prod_mboepd_val'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalassetacqu',
            name='sources_share_cash',
        ),
    ]
