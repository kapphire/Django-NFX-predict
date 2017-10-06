# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0015_totalequityoffering_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalinit',
            name='r_calc',
        ),
    ]
