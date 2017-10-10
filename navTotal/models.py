from django.db import models
from navProved.models import *
from typeCurves.models import *
from datetime import date

# Create your models here.
class TotalInit(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_init_tickers')
	play = models.ForeignKey(Play, related_name = 'total_init_plays')
	net_asset_summary = models.FloatField()
	inflation = models.FloatField()
	rig_case = models.IntegerField()
	duration = models.IntegerField()
	year = models.CharField(max_length = 100)
	boe_mcfe = models.IntegerField()
	date = models.DateField(default = date.today)


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


class TotalAddPlayConv(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_conv_tickers')
	play = models.ForeignKey(Play, related_name = 'total_conv_plays')
	lst_hc = models.IntegerField()
	flat = models.FloatField()
	lst_prod = models.FloatField()
	dev_cost = models.FloatField()
	wl = models.FloatField()
	operator = models.CharField(max_length = 100)
	royalty = models.FloatField()
	trap = models.FloatField()
	reservoir = models.FloatField()
	seal = models.FloatField()
	timing = models.FloatField()
	commercial = models.FloatField()
	closure = models.FloatField()
	drainage = models.FloatField()
	mean = models.FloatField()
	boe_feet = models.FloatField()
	oil_conv = models.FloatField()
	gas_conv = models.FloatField()
	risk_conv = models.FloatField()
	proved_book = models.IntegerField()


class TotalEquityOffering(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_equity_tickers')
	play = models.ForeignKey(Play, related_name = 'total_equity_plays')
	choice = models.IntegerField()
	share_amount = models.FloatField()
	shoe = models.FloatField()
	last_price = models.FloatField()
	gross_issue = models.FloatField()
	net_issue = models.FloatField()
	date = models.DateField(default = date.today)


class TotalAssetAcquProd(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_acquisition_prod_tickers')
	play = models.ForeignKey(Play, related_name = 'total_acquisition_prod_plays')
	prod = models.ForeignKey(Product, related_name = 'total_acquisition_prod_products')
	eur_mix = models.FloatField()
	prod_mix = models.FloatField()
	proved_mix = models.FloatField()
	

class TotalAssetAcqu(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_acquisition_tickers')
	play = models.ForeignKey(Play, related_name = 'total_acquisition_plays')
	sources_share_fst = models.FloatField()
	sources_share_sec = models.FloatField()
	sources_share_total = models.FloatField()
	uses_acres = models.FloatField()
	uses_ip30 = models.FloatField()
	uses_cost = models.FloatField()
	uses_eur = models.FloatField()
	uses_prod = models.FloatField()
	uses_proved = models.FloatField()
	uses_f_d = models.FloatField()
	uses_pud = models.FloatField()
	choice = models.IntegerField()
	date = models.DateField(default = date.today)


class TotalAssetSaleProd(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_sale_prod_tickers')
	play = models.ForeignKey(Play, related_name = 'total_sale_prod_plays')
	prod = models.ForeignKey(Product, related_name = 'total_sale_prod_products')
	eur_mix = models.FloatField()
	prod_mix = models.FloatField()
	proved_mix = models.FloatField()


class TotalAssetSale(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_sale_tickers')
	play = models.ForeignKey(Play, related_name = 'total_sale_plays')
	sources_total = models.FloatField()
	sources_acres = models.FloatField()
	sources_ip30 = models.FloatField()
	sources_cost = models.FloatField()
	sources_eur = models.FloatField()
	sources_prod = models.FloatField()
	sources_proved = models.FloatField()
	sources_f_d = models.FloatField()
	sources_pud = models.FloatField()
	choice = models.IntegerField()
	date = models.DateField(default = date.today)


class TotalNetLandingChange(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'total_net_landing_tickers')
	play = models.ForeignKey(Play, related_name = 'total_net_landing_plays')
	sale_proceeds_s = models.FloatField()
	sale_carries_s = models.FloatField()
	equity_s = models.FloatField()
	monies_s = models.FloatField()
	carries_s = models.FloatField()


class TotalLandingResults(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'results_tickers')
	play = models.ForeignKey(Play, related_name = 'results_plays')
	debt = models.FloatField()
	equivalents = models.FloatField()
	deficit = models.FloatField()
	hedge = models.FloatField()