# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('navProved', '0014_play_playcommoninputclass_playproduction_playproductiondatechoice_playresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayScrapedData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('unit', models.CharField(max_length=250)),
                ('value', models.FloatField()),
                ('play', models.ForeignKey(related_name='playScrapedData', to='navProved.Play')),
            ],
        ),
    ]
