# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0021_totaladdplayconv'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totaladdplayconv',
            name='operator',
            field=models.CharField(max_length=100),
        ),
    ]
