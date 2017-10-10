from django.db import models
from navProved.models import *
import datetime

# Create your models here.
class Play(models.Model):
	name = models.CharField(max_length = 250)
	ticker = models.ForeignKey(Ticker, related_name = 'plays')


class PlayScrapedData(models.Model):
	play = models.ForeignKey(Play, related_name = 'playScrapedData')
	name = models.CharField(max_length = 100)
	unit = models.CharField(max_length = 250)
	value = models.FloatField()


class PlayProduction(models.Model):
	name = models.CharField(max_length = 250)
	play = models.ForeignKey(Play, related_name = 'playProductions')
	unit = models.CharField(max_length = 100)
	diff = models.FloatField()
	shortcut_name = models.CharField(max_length = 250)


class PlayCommonInputClass(models.Model):
	play = models.ForeignKey(Play, related_name = 'playCommonInputClasses')
	name = models.CharField(max_length = 250)
	unit = models.CharField(max_length = 250)
	value = models.FloatField()


class PlayProdDecline(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'playProdDeclines')
	play = models.ForeignKey(Play, related_name = 'playProdDeclines')
	prod = models.ForeignKey(PlayProduction, related_name = 'playProdDeclines')
	decline = models.FloatField()


class PlayProductionDateChoice(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'playProductionDateChoices')
	play = models.ForeignKey(Play, related_name = 'playProductionDateChoices')
	prod = models.ForeignKey(PlayProduction, related_name = 'playProductionDateChoices')
	ip30 = models.FloatField()
	m12 = models.FloatField()
	m24 = models.FloatField()
	m12_decline = models.FloatField()
	m24_decline = models.FloatField()
	eur_unit = models.CharField(max_length = 100)
	decline = models.ForeignKey(PlayProdDecline, related_name = 'playProductionDateChoices')


class PlayResult(models.Model):
	play = models.ForeignKey(Play, related_name = 'plays')
	ticker = models.ForeignKey(Ticker, related_name = 'tickers')
	irr = models.FloatField()
	pv_10 = models.FloatField()
	pv_eur = models.FloatField()