# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0021_product_nav_total_unit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='navprovedresult',
            old_name='pv',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='navprovedresult',
            name='pv_boe',
        ),
        migrations.RemoveField(
            model_name='navprovedresult',
            name='pv_mcfe',
        ),
        migrations.AddField(
            model_name='navprovedresult',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
