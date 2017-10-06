# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0012_remove_totalassetsale_uses_cash'),
    ]

    operations = [
        migrations.AddField(
            model_name='totalassetsale',
            name='uses_cash',
            field=models.FloatField(default=800),
        ),
    ]
