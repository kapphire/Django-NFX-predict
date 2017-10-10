import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import *
from navProved.models import *
from .common.typeCurve import TypeCurveStatic

# Create your views here.
def typeCurve(request):
	years = 0
	ticker_id = 1
	play_id = 1

	ticker = Ticker.objects.filter(id = ticker_id).get()
	products = Product.objects.filter(ticker = ticker_id).order_by('id')
	prices = Price.objects.filter(ticker = ticker_id).order_by('id').all()
	play_names = Play.objects.filter(ticker_id = ticker_id).get()
	play_prods = PlayProduction.objects.filter(play_id = play_id).order_by('id').all()
	play_scraped_data = PlayScrapedData.objects.filter(play_id = play_id).order_by('id').all()
	play_common_input_class = PlayCommonInputClass.objects.filter(play_id = play_id).order_by('id').all()
	play_prod_date_choices = PlayProductionDateChoice.objects.filter(ticker_id = ticker_id).order_by('id').all()
	play_prod_declines = PlayProdDecline.objects.filter(ticker_id = ticker_id, play_id = play_id).order_by('prod_id')

	typeCurveStatic = TypeCurveStatic({
			'years' : years,
			'ticker_id' : ticker_id,
			'ticker' : ticker,
			'products' : products,
			'prices' : prices,
			'play_names' : play_names,
			'play_prods' : play_prods,
			'play_scraped_data' : play_scraped_data,
			'play_common_input_class' : play_common_input_class,
			'play_prod_date_choices' : play_prod_date_choices,
			'play_prod_declines' : play_prod_declines
		})
	prod_price_diffs = typeCurveStatic.preprocess()['prod_price_diffs']
	prods_date = typeCurveStatic.preprocess()['prods_date']
	drilling_f_d = typeCurveStatic.preprocess()['drilling_f_d']
	total_f_d = typeCurveStatic.preprocess()['total_f_d']

	return render(request, 'type_curves_content.html', 
										{'ticker' : ticker,
										 'products' : products,
										 'prices' : prices, 
										 'play_names' : play_names,
										 'play_prods' : play_prods, 
										 'play_scraped_data' : play_scraped_data, 
										 'play_common_input_class' : play_common_input_class, 
										 'play_prod_date_choices' : play_prod_date_choices,
										 'prod_price_diffs' : prod_price_diffs,
										 'prods_date' : prods_date,
										 'drilling_f_d' : drilling_f_d,
										 'total_f_d' : total_f_d
										 })


def typeCurveAjax(request):
	if request.method == 'POST':
		years = json.loads(request.POST.get('val'))
		
		ticker_id = 1
		play_id = 1

		ticker = Ticker.objects.filter(id = ticker_id).get()
		products = Product.objects.filter(ticker = ticker_id).order_by('id')
		prices = Price.objects.filter(ticker = ticker_id).order_by('id').all()
		play_names = Play.objects.filter(ticker_id = ticker_id).get()
		play_prods = PlayProduction.objects.filter(play_id = play_id).all()
		play_scraped_data = PlayScrapedData.objects.filter(play_id = play_id).order_by('id').all()
		play_common_input_class = PlayCommonInputClass.objects.filter(play_id = play_id).order_by('id').all()
		play_prod_date_choices = PlayProductionDateChoice.objects.filter(ticker_id = ticker_id).order_by('prod_id').all()
		play_prod_declines = PlayProdDecline.objects.filter(ticker_id = ticker_id, play_id = play_id).order_by('prod_id')

		typeCurveAjax = TypeCurveStatic({
				'years' : years,
				'ticker_id' : ticker_id,
				'products' : products,
				'prices' : prices,
				'play_names' : play_names,
				'play_prods' : play_prods,
				'play_scraped_data' : play_scraped_data,
				'play_common_input_class' : play_common_input_class,
				'play_prod_date_choices' : play_prod_date_choices,
				'play_prod_declines' : play_prod_declines
			})

		decline_rates = typeCurveAjax.get_decline_rates()

		for prod_id in decline_rates:
			PlayProdDecline.objects.filter(prod_id = prod_id, ticker_id = ticker_id, play_id = play_id).update(decline = decline_rates[prod_id])

		result = typeCurveAjax.typeCurveTableData()
		irr_npv_pv = typeCurveAjax.get_irr()
		irr = irr_npv_pv['irr'] * 100
		npv = irr_npv_pv['npv']
		pv = irr_npv_pv['pv_eur']

		playResult = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).all()

		if playResult is None:
				insert_result = PlayResult(irr = irr, pv_10 = npv, pv_eur = pv)
				insert_result.save()
		else:
			playResult = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
			playResult.irr = irr
			
			playResult.pv_10 = npv
			playResult.pv_eur = pv
			playResult.save()
		
		return JsonResponse({
				'status' : True,
				'result' : result,
				'decline_rates' : decline_rates,
				'irr' : irr,
				'npv' : npv,
				'pv' : pv
			})


def changeInitProduct(request):
	if request.method == "POST":
		# Should be updated.
		play_id = 1
		id = json.loads(request.POST.get('id'))
		value = json.loads(request.POST.get('value'))
		flag = json.loads(request.POST.get('table_data_flag'))

		PlayCommonInputClass.objects.filter(id = id, play_id = play_id).update(value = value)

		if flag:
			years = json.loads(request.POST.get('start'))
			ticker_id = 1

			ticker = Ticker.objects.filter(id = ticker_id).get()
			products = Product.objects.filter(ticker = ticker_id).order_by('id')
			prices = Price.objects.filter(ticker = ticker_id).order_by('id').all()
			play_names = Play.objects.filter(ticker_id = ticker_id).get()
			play_prods = PlayProduction.objects.filter(play_id = play_id).all()
			play_scraped_data = PlayScrapedData.objects.filter(play_id = play_id).order_by('id').all()
			play_common_input_class = PlayCommonInputClass.objects.filter(play_id = play_id).order_by('id').all()
			play_prod_date_choices = PlayProductionDateChoice.objects.filter(ticker_id = ticker_id).order_by('prod_id').all()
			play_prod_declines = PlayProdDecline.objects.filter(ticker_id = ticker_id, play_id = play_id).order_by('prod_id')

			typeCurveAjax = TypeCurveStatic({
					'years' : years,
					'ticker_id' : ticker_id,
					'ticker' : ticker,
					'products' : products,
					'prices' : prices,
					'play_names' : play_names,
					'play_prods' : play_prods,
					'play_scraped_data' : play_scraped_data,
					'play_common_input_class' : play_common_input_class,
					'play_prod_date_choices' : play_prod_date_choices,
					'play_prod_declines' : play_prod_declines
				})

			decline_rates = typeCurveAjax.get_decline_rates()

			for prod_id in decline_rates:
				PlayProdDecline.objects.filter(prod_id = prod_id, ticker_id = ticker_id, play_id = play_id).update(decline = decline_rates[prod_id])

			result = typeCurveAjax.typeCurveTableData()
			
			result = typeCurveAjax.typeCurveTableData()
			irr_npv_pv = typeCurveAjax.get_irr()
			irr = irr_npv_pv['irr'] * 100
			npv = irr_npv_pv['npv']
			pv = irr_npv_pv['pv_eur']

			playResult = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

			if playResult is None:
				insert_result = PlayResult(irr = irr, pv_10 = npv, pv_eur = pv)
				insert_result.save()
			else:
				playResult.irr = irr
				playResult.pv_10 = npv
				playResult.pv_eur = pv
				playResult.save()
			
			return JsonResponse({
					'status' : True,
					'result' : result,
					'decline_rates' : decline_rates,
					'irr' : irr,
					'npv' : npv,
					'pv' : pv
				})
		else:			
			return JsonResponse({
				'status' : True,
			})
