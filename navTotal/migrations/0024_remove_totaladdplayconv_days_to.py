# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0023_auto_20171010_1612'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totaladdplayconv',
            name='days_to',
        ),
    ]
