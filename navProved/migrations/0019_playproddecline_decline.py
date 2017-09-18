# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0018_auto_20170914_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='playproddecline',
            name='decline',
            field=models.FloatField(default=1),
        ),
    ]
