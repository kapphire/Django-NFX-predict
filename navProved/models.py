from django.db import models
import datetime

# Create your models here.
class Product(models.Model):
	name = models.CharField(max_length = 250)

	class Meta:
		ordering = ('-name',)

	def __str__(self):
		return self.name


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
	pv = models.FloatField()
	pv_boe = models.FloatField()
	pv_mcfe = models.FloatField()
