# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('typeCurves', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='playproduction',
            name='shortcut_name',
            field=models.CharField(default=b'a', max_length=250),
        ),
    ]
