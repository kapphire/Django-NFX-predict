# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0011_totalassetsale_totalassetsaleprod'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalassetsale',
            name='uses_cash',
        ),
    ]
