import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Product, Ticker, Price, Predict, DeclineRate
from common.formulas import *


# Create your views here.
def navProved(request):
	year_range = 5
	ticker_id = 1
	years = []
	
	products = Product.objects.all().order_by("id")
	ticker = Ticker.objects.get()
	decline_rates = DeclineRate.objects.all()
	predicts = Predict.objects.filter(ticker = ticker_id).order_by('prod_id').all()

	cur_year = int(datetime.datetime.today().strftime("%Y"))
	for dev_life in range(0, year_range):
		years.append(cur_year + dev_life)
	prices = Price.objects.filter(ticker = ticker_id, year__in = years).order_by('prod_id').all()

	return render(request, 'nav_proved_content.html', {'products' : products, 'prices' : prices, 'ticker' : ticker, "decline_rates" : decline_rates, "predicts" : predicts})


def navProvedAjax(request):
	if request.method == "POST":
		# Should be updated.
		year_range = 5
		ticker_id = 1

		ajaxData = request.POST.get('val')
		ajaxData = json.loads(ajaxData)
		cur_year = int(datetime.datetime.today().strftime("%Y"))
		years = []
		for dev_life in range(0, year_range):
			years.append(cur_year + dev_life)

		prices = Price.objects.filter(ticker = ticker_id, year__in = years).order_by('prod_id').all()
		predicts = Predict.objects.filter(ticker = ticker_id).order_by('prod_id').all()
		decline_rates = DeclineRate.objects.all()
		ticker = Ticker.objects.get()
		sum_param = {1 : 6, 2 : 1, 3 : 6}

		navProved = NavProved(ajaxData, {"years" : years, "prices" : prices, "predicts" : predicts, "decline_rates" : decline_rates, "ticker" : ticker, "sum_param" : sum_param})
		table_data = navProved.initialize_prices(sum_param)
		
		return JsonResponse({'status' : True, 'table_data' : table_data})
		
