# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0016_playcommoninputclass_play'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playproduction',
            name='decline',
        ),
        migrations.AlterField(
            model_name='playcommoninputclass',
            name='play',
            field=models.ForeignKey(related_name='playCommonInputClasses', to='navProved.Play'),
        ),
    ]
