import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse

from navProved.models import *
from typeCurves.models import *
from navTotal.models import *

from navProved.common.formulas import NavProved
from typeCurves.common.typeCurve import TypeCurveStatic
from .common.navTotal import NavTotalStatic

# Create your views here.
def navTotal(request):
	years = 0
	ticker_id = 1
	play_id = 1
	undefined = 1

	products = Product.objects.filter(ticker = ticker_id).order_by("id")
	ticker = Ticker.objects.filter(id = ticker_id).get()
	
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

	prods_date = typeCurveStatic.preprocess()['prods_date']
	well_cost = typeCurveStatic.preprocess()['well_cost']
	playResult = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

	navTotalStatic = NavTotalStatic({
			'prods_date' : prods_date,
			'well_cost' : well_cost,
			'play_result' : playResult,
			'acre_unconv' : undefined,
			'risk_unconv' : undefined,
			'spacing' : undefined,
			'zone' : undefined,
			'zone_pros' : undefined,
			'rigs' : undefined,
			'days_to' : undefined,
			'drilled' : undefined,
		})
	result = navTotalStatic.preprocess()

	return render(request, 'nav_total_content.html', {
														'products' : products, 
														'prods_date' : prods_date,
														'play_result' : playResult,
													})


def navTotalAjax(request):
	if request.method == "POST":

		acre_unconv = json.loads(request.POST.get('acre_unconv'))
		risk_unconv = json.loads(request.POST.get('risk_unconv'))		
		spacing = json.loads(request.POST.get('spacing'))
		zone = json.loads(request.POST.get('zone'))
		zone_pros = json.loads(request.POST.get('zone_pros'))
		rigs = json.loads(request.POST.get('rigs'))
		days_to = json.loads(request.POST.get('days_to'))
		drilled = json.loads(request.POST.get('drilled'))
		
		years = 0
		ticker_id = 1
		play_id = 1

		products = Product.objects.filter(ticker = ticker_id).order_by("id")
		ticker = Ticker.objects.filter(id = ticker_id).get()
		
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

		prods_date = typeCurveStatic.preprocess()['prods_date']
		well_cost = typeCurveStatic.preprocess()['well_cost']
		playResult = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

		navTotalStatic = NavTotalStatic({
				'prods_date' : prods_date,
				'well_cost' : well_cost,
				'play_result' : playResult,
				'acre_unconv' : acre_unconv,
				'risk_unconv' : risk_unconv,
				'spacing' : spacing,
				'zone' : zone,
				'zone_pros' : zone_pros,
				'rigs' : rigs,
				'days_to' : days_to,
				'drilled' : drilled,
			})
		result = navTotalStatic.preprocess()		
		
		return JsonResponse({
			'status' : True,
		})


def navTotalInitVariables(request):
	ticker_id = 1
	play_id = 1
	if request.method == 'POST':
		net_asset_value = json.loads(request.POST.get('total_net_asset_value'))
		inflation = json.loads(request.POST.get('total_inflation'))		
		rig = json.loads(request.POST.get('total_rig'))
		m_a = json.loads(request.POST.get('total_m_a'))
		ngl_percent = json.loads(request.POST.get('total_ngl_percent'))
		duration = json.loads(request.POST.get('total_duration'))
		year_define = request.POST.get('total_year_define')
		boe_mcfe = json.loads(request.POST.get('total_boe_mcfe'))
		
		print(year_define)

		r_calc = (1 + inflation / 100) / (1 + net_asset_value / 100)

		total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).all()

		if not total_init_variables:
			insert_result = TotalInit(net_asset_summary = net_asset_value, inflation = inflation, rig_case = rig, m_a_case = m_a, ngl_wti = ngl_percent, duration = duration, year = year_define, boe_mcfe = boe_mcfe, ticker_id = ticker_id, play_id = play_id, r_calc = r_calc)
			insert_result.save()
		else:
			total_init_variables_update = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
			total_init_variables_update.net_asset_summary = net_asset_value
			total_init_variables_update.inflation = net_asset_value
			total_init_variables_update.rig_case = rig
			total_init_variables_update.m_a_case = m_a
			total_init_variables_update.ngl_wti = ngl_percent
			total_init_variables_update.duration = duration
			total_init_variables_update.year = year_define
			total_init_variables_update.boe_mcfe = boe_mcfe
			total_init_variables_update.r_calc = r_calc

			total_init_variables_update.save()

		return JsonResponse({
			'status' : True,		
		})