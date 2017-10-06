# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0013_totalassetsale_uses_cash'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalassetsale',
            name='uses_cash',
        ),
        migrations.AddField(
            model_name='totalassetsale',
            name='sources_total',
            field=models.FloatField(default=800),
            preserve_default=False,
        ),
    ]
