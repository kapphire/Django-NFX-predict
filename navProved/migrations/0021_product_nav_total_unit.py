# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0020_auto_20170914_1723'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='nav_total_unit',
            field=models.CharField(default=b'Mmboe', max_length=100),
        ),
    ]
