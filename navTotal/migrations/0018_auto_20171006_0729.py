# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0017_totalinit_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='totalinit',
            name='m_a_case',
        ),
        migrations.RemoveField(
            model_name='totalinit',
            name='ngl_wti',
        ),
    ]
