# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0024_remove_totaladdplayconv_days_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totaladdplayconv',
            name='lst_hc',
            field=models.IntegerField(),
        ),
    ]
