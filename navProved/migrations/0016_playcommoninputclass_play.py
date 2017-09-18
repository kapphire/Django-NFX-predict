# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0015_playscrapeddata'),
    ]

    operations = [
        migrations.AddField(
            model_name='playcommoninputclass',
            name='play',
            field=models.ForeignKey(related_name='playCommonInputClasses', default=1, to='navProved.Play'),
        ),
    ]
