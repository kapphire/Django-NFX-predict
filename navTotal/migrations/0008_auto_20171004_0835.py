# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0007_remove_totalassetacqu_sources_share_cash'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalassetacqu',
            name='uses_prod',
            field=models.FloatField(default=1.4),
        ),
        migrations.AddField(
            model_name='totalassetacqu',
            name='uses_proved',
            field=models.FloatField(default=76),
        ),
    ]
