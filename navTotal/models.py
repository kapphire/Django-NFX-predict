from django.db import models
from navProved.models import *
from typeCurves.models import *

# Create your models here.
class TotalInit(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_init_tickers')
	play = models.ForeignKey(Play, related_name = 'total_init_plays')
	net_asset_summary = models.FloatField()
	inflation = models.FloatField()
	rig_case = models.IntegerField()
	m_a_case = models.IntegerField()
	ngl_wti = models.IntegerField()
	duration = models.IntegerField()
	r_calc = models.FloatField()
	year = models.CharField(max_length = 100)
	boe_mcfe = models.IntegerField()


class TotalAddPlayUnconv(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_unconv_tickers')
	play = models.ForeignKey(Play, related_name = 'total_unconv_plays')
	acres = models.FloatField()
	risk = models.FloatField()
	spacing = models.FloatField()
	zones = models.FloatField()
	zone_pros = models.FloatField()
	rigs = models.FloatField()
	drill = models.FloatField()
	wells = models.FloatField()