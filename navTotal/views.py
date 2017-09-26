import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse

from navProved.models import *
from navProved.common.formulas import NavProved

# Create your views here.
def navTotal(request):
	year_range = 5
	ticker_id = 1
	years = []
	
	products = Product.objects.filter(ticker = ticker_id).order_by("id")
	ticker = Ticker.objects.get()
	decline_rates = DeclineRate.objects.filter(ticker = ticker_id).order_by("prod_id")
	predicts = Predict.objects.filter(ticker = ticker_id).order_by('prod_id').all()
	prod_total = ProductionTotal.objects.filter(ticker = ticker_id).get()


	cur_year = int(datetime.datetime.today().strftime("%Y"))
	for dev_life in range(0, year_range):
		years.append(cur_year + dev_life)
	prices = Price.objects.filter(ticker = ticker_id, year__in = years).order_by('prod_id').all()

	return render(request, 'nav_total_content.html', {'products' : products, 'prices' : prices, 'ticker' : ticker, "decline_rates" : decline_rates, "predicts" : predicts, "prod_total" : prod_total})