# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0008_auto_20171004_0835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalassetacqu',
            name='uses_prod',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='totalassetacqu',
            name='uses_proved',
            field=models.FloatField(),
        ),
    ]
