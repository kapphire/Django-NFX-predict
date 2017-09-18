# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0019_playproddecline_decline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='play',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='playcommoninputclass',
            name='play',
        ),
        migrations.RemoveField(
            model_name='playproddecline',
            name='play',
        ),
        migrations.RemoveField(
            model_name='playproddecline',
            name='prod',
        ),
        migrations.RemoveField(
            model_name='playproddecline',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='playproduction',
            name='play',
        ),
        migrations.RemoveField(
            model_name='playproductiondatechoice',
            name='prod',
        ),
        migrations.RemoveField(
            model_name='playproductiondatechoice',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='playresult',
            name='play',
        ),
        migrations.RemoveField(
            model_name='playresult',
            name='ticker',
        ),
        migrations.RemoveField(
            model_name='playscrapeddata',
            name='play',
        ),
        migrations.DeleteModel(
            name='Play',
        ),
        migrations.DeleteModel(
            name='PlayCommonInputClass',
        ),
        migrations.DeleteModel(
            name='PlayProdDecline',
        ),
        migrations.DeleteModel(
            name='PlayProduction',
        ),
        migrations.DeleteModel(
            name='PlayProductionDateChoice',
        ),
        migrations.DeleteModel(
            name='PlayResult',
        ),
        migrations.DeleteModel(
            name='PlayScrapedData',
        ),
    ]
