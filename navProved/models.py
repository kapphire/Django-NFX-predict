from django.db import models
import datetime

# Create your models here.

class Ticker(models.Model):
	name = models.CharField(max_length = 250)
	prod_taxes = models.FloatField()
	tax_rate = models.FloatField()
	deferred = models.FloatField()
	op_cost_esc = models.FloatField()
	dda = models.FloatField()	
	def_after_5yrs = models.FloatField()
	capex = models.FloatField()
	op_cost = models.FloatField()
	disc_factor = models.FloatField()
	year = models.IntegerField()

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length = 250)
	ticker = models.ForeignKey(Ticker, related_name = 'products')
	prod_initial_value = models.FloatField()
	sample_unit = models.CharField(max_length = 100, default = '$/bbl')
	prod_unit = models.CharField(max_length = 100, default = 'MMbbl')
	nav_total_unit = models.CharField(max_length = 100, default = 'Mmboe')
	class Meta:
		ordering = ('-name',)

	def __str__(self):
		return self.name


class Price(models.Model):
	prod = models.ForeignKey(Product, related_name = 'prices')
	ticker = models.ForeignKey(Ticker, related_name = 'prices')
	year = models.IntegerField()
	price = models.FloatField()


class Predict(models.Model):
	prod = models.ForeignKey(Product, related_name = 'predicts')
	ticker = models.ForeignKey(Ticker, related_name = 'predicts')
	prod_esc = models.FloatField()
	prod_diff = models.FloatField()
	prod_pred_opd = models.FloatField()


class DeclineRate(models.Model):
	prod = models.ForeignKey(Product, related_name = 'declineRates')
	ticker = models.ForeignKey(Ticker, related_name = 'declineRates')
	decline_rate = models.FloatField()


class NavProvedResult(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'navProvedResults')
	name = models.CharField(max_length = 100)
	value = models.FloatField()


class ProductionTotal(models.Model):
	ticker = models.ForeignKey(Ticker, related_name = 'productionTotals')
	prod_total_unit = models.CharField(max_length = 100)
	prod_total_value = models.FloatField()
