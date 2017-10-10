import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import *
from .common.formulas import NavProved


# Create your views here.
def navProved(request):
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

	return render(request, 'nav_proved_content.html', {'products' : products, 'prices' : prices, 'ticker' : ticker, "decline_rates" : decline_rates, "predicts" : predicts, "prod_total" : prod_total})


def getNavProvedTableData(start, end, ticker_id = 1):
	year_range = 5

	cur_year = int(datetime.datetime.today().strftime("%Y"))
	years = []
	for dev_life in range(0, year_range):
		years.append(cur_year + dev_life)

	prices = Price.objects.filter(ticker = ticker_id, year__in = years).order_by('prod_id').all()
	predicts = Predict.objects.filter(ticker = ticker_id).order_by('prod_id').all()
	ticker = Ticker.objects.filter(id = ticker_id).get()

	sum_param = {1 : 6, 2 : 1, 3 : 6}
	early_stage_value = 0.5

	navProved = NavProved([start, end], {
		"years" : years, 
		"prices" : prices, 
		"predicts" : predicts, 
		"ticker" : ticker, 
		"sum_param" : sum_param, 
		"early_stage_value" : early_stage_value
	})

	decline_rates = navProved.get_decline_rates()

	for prod_id in decline_rates:
		DeclineRate.objects.filter(prod_id = prod_id, ticker_id = ticker.id).update(decline_rate = decline_rates[prod_id])

	table_data = navProved.initialize_prices(sum_param)

	sum_result = navProved.get_sum_result()

	sum_result_tbl = NavProvedResult.objects.filter(ticker_id = ticker_id).all()
	
	if not sum_result_tbl:
		for key, value in sum_result.items():
			insert_table = NavProvedResult(name = key, value = value, ticker_id = ticker_id)
			insert_table.save()
	else:
		for key, value in sum_result.items():
			sum_result_update = NavProvedResult.objects.filter(ticker_id = ticker_id, name = key).get()
			sum_result_update.value = value
			sum_result_update.save()

	return {
		'table_data': table_data,
		'decline_rates': decline_rates
	}

def navProvedAjax(request):
	if request.method == "POST":
		years = json.loads(request.POST.get('val'))
		result = getNavProvedTableData(years[0], years[1])
		
		
		return JsonResponse({
			'status' : True, 
			'table_data' : result['table_data'],
			'decline_rates': result['decline_rates']
		})
		

def changeInitProduct(request):
	if request.method == "POST":
		# Should be updated.
		ticker_id = 1
		id = json.loads(request.POST.get('id'))
		value = json.loads(request.POST.get('value'))
		flag = json.loads(request.POST.get('table_data_flag'))

		Predict.objects.filter(prod_id = id, ticker_id = ticker_id).update(prod_pred_opd = value)

		if flag:
			start = json.loads(request.POST.get('start'))
			end = json.loads(request.POST.get('end'))
			result = getNavProvedTableData(start, end)
			
			return JsonResponse({
				'status' : True, 
				'table_data' : result['table_data'],
				'decline_rates': result['decline_rates']
			})
		else:			
			return JsonResponse({
				'status' : True,
			})