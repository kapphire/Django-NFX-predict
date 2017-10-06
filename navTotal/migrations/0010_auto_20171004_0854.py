# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navTotal', '0009_auto_20171004_0836'),
    ]

    operations = [
        migrations.RenameField(
            model_name='totalassetacquprod',
            old_name='eur_mix_val',
            new_name='eur_mix',
        ),
        migrations.RenameField(
            model_name='totalassetacquprod',
            old_name='prod_mix_val',
            new_name='prod_mix',
        ),
        migrations.RenameField(
            model_name='totalassetacquprod',
            old_name='proved_mix_val',
            new_name='proved_mix',
        ),
    ]
