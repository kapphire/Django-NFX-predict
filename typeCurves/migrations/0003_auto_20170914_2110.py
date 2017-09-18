# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0002_playproduction_shortcut_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playproddecline',
            old_name='prod',
            new_name='prod_decline',
        ),
        migrations.AlterField(
            model_name='playproduction',
            name='shortcut_name',
            field=models.CharField(max_length=250),
        ),
    ]
