# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0022_auto_20171010_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totaladdplayconv',
            name='proved_book',
            field=models.IntegerField(),
        ),
    ]
