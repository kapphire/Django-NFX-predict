import math, datetime
import json
from django.shortcuts import render
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone

from navProved.models import *
from typeCurves.models import *
from navTotal.models import *

from navProved.common.formulas import NavProved
from typeCurves.common.typeCurve import TypeCurveStatic
from .common.navTotal import NavTotalStatic
from .common.equity_offering import EquityOffering
from .common.asset_acquisition import AssetAcquisition
from .common.asset_sale import AssetSale

# Create your views here.
def navTotal(request):
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
	total_add_play_unconv = TotalAddPlayUnconv.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	# total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

	if not total_add_play_unconv:
		acre_unconv = 0.01
		risk_unconv = 0.01
		spacing = 0.01
		zone = 0.01
		zone_pros = 0.01
		rigs = 0.01
		days_to = 0.01
		drilled = 0.01
	else:
		acre_unconv = total_add_play_unconv.acres
		risk_unconv = total_add_play_unconv.risk
		spacing = total_add_play_unconv.spacing
		zone = total_add_play_unconv.zones
		zone_pros = total_add_play_unconv.zone_pros
		rigs = total_add_play_unconv.rigs
		days_to = total_add_play_unconv.drill
		drilled = total_add_play_unconv.wells


	# navTotalStatic = NavTotalStatic({
	# 		'prods_date' : prods_date,
	# 		'well_cost' : well_cost,
	# 		'play_result' : playResult,
	# 		'acre_unconv' : acre_unconv,
	# 		'risk_unconv' : risk_unconv,
	# 		'spacing' : spacing,
	# 		'zone' : zone,
	# 		'zone_pros' : zone_pros,
	# 		'rigs' : rigs,
	# 		'days_to' : days_to,
	# 		'drilled' : drilled,
	# 		'total_init_variables' : total_init_variables,
	# 	})
	# result = navTotalStatic.preprocess()


	# Net Asset Value Summary Init Variables
	total_init_result = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	if not total_init_result:
		insert_result = TotalInit(
			net_asset_summary = 0,
			inflation = 0,
			rig_case = 0,
			duration = 0,
			year = 0,
			boe_mcfe = 0,
			date = timezone.now().today(),
			ticker_id = ticker_id,
			play_id = play_id,
		)
		insert_result.save()
		total_init_variables = None
	else:
		for element in total_init_result:
			total_init_variables = element

	# Equity Offering
	equity_offering_result = TotalEquityOffering.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	if not equity_offering_result:
		insert_result = TotalEquityOffering(
			choice = 0, 
			share_amount = 0, 
			shoe = 0, 
			last_price = 0, 
			gross_issue = 0, 
			net_issue = 0, 
			ticker_id = ticker_id, 
			play_id = play_id,
			date = timezone.now().today()
		)
		insert_result.save()
		equity_offering_dict = None
		equity_offering_variables = None
	else:
		for element in equity_offering_result:
			equity_offering_variables = element

		equity_offering_object = EquityOffering({
			'choice' : equity_offering_variables.choice,
			'share_amount' : equity_offering_variables.share_amount,	
			'shoe' : equity_offering_variables.shoe,
			'last_price' : equity_offering_variables.last_price,
			'gross_issue' : equity_offering_variables.gross_issue,
			'net_issue' : equity_offering_variables.net_issue
		})

		equity_offering_dict = equity_offering_object.get_values()

	# Asset Acquisition
	asset_acquisition_result = TotalAssetAcqu.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
	if not asset_acquisition_result:
		insert_result = TotalAssetAcqu(
				sources_share_fst = 0,
				sources_share_sec = 0,
				sources_share_total = 0,
				uses_acres = 0,
				uses_ip30 = 0,
				uses_cost = 0,
				uses_eur = 0,
				uses_f_d = 0,
				uses_pud = 0,
				uses_prod = 0,
				uses_proved = 0,
				choice = 0,
				play_id = play_id,
				ticker_id = ticker_id,
				date = timezone.now().today()
			)
		insert_result.save()
	else:
		for element in asset_acquisition_result:
			asset_acquisition_variables = element

	asset_acquisition_prod = TotalAssetAcquProd.objects.filter(play_id = play_id, ticker_id = ticker_id).all()

	if not asset_acquisition_prod:
		for product in products:
			insert_result = TotalAssetAcquProd(
					prod_id = product.id,
					ticker_id = ticker_id,
					play_id = play_id,
					eur_mix = 0,
					prod_mix = 0,
					proved_mix = 0
			)
			insert_result.save()
			asset_acqu_result = None
			asset_acquisition_variables = None
			asset_acquisition_prod = TotalAssetAcquProd.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
	else:
		asset_acquisition_prod = TotalAssetAcquProd.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
		asset_acquisition_variables = TotalAssetAcqu.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		acqu_date = asset_acquisition_variables.date
		acqu_uses_choice = asset_acquisition_variables.choice
		asset_acquisition_obj = AssetAcquisition({
			'acqu_date' : acqu_date,
			'acqu_uses_choice' : acqu_uses_choice,
			'asset_acquisition_variables' : asset_acquisition_variables,
			'asset_acquisition_prod' : asset_acquisition_prod,
		})

		asset_acqu_result = asset_acquisition_obj.preprocess()

	# Asset Sale
	asset_sale_result = TotalAssetSale.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
	if not asset_sale_result:
		insert_result = TotalAssetSale(
				sources_total = 0,
				sources_acres =0,
				sources_ip30 =0,
				sources_cost =0,
				sources_eur =0,
				sources_prod =0,
				sources_proved =0,
				sources_f_d =0,
				sources_pud =0,
				choice =0,
				play_id = play_id,
				ticker_id = ticker_id,
				date = timezone.now().today()
			)
		insert_result.save()
	else:
		for element in asset_sale_result:
			asset_sale_variables = element

	asset_sale_prod = TotalAssetSaleProd.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
	if 	not asset_sale_prod:
		for product in products:
			insert_result = TotalAssetSaleProd(
				prod_id = product.id,
				ticker_id = ticker_id,
				play_id = play_id,
				eur_mix = 0,
				prod_mix = 0,
				proved_mix = 0	
			)
			insert_result.save()
			asset_sale_calc_result = None
			asset_sale_variables = None
			asset_sale_prod = TotalAssetSaleProd.objects.filter(play_id = play_id, ticker_id = ticker_id).all()

	else:
		asset_sale_prod = TotalAssetSaleProd.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
		asset_sale_variables = TotalAssetSale.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		sale_date = asset_sale_variables.date
		sale_uses_choice = asset_sale_variables.choice

		asset_sale_obj = AssetSale({
			'sale_date' : sale_date,
			'sale_uses_choice' : sale_uses_choice,
			'asset_sale_variables' : asset_sale_variables,
			'asset_sale_prod' : asset_sale_prod,
		})
		asset_sale_calc_result = asset_sale_obj.preprocess()

	return render(request, 'nav_total_content.html', {
			'products' : products, 
			'prods_date' : prods_date,
			'play_result' : playResult,
			'equity_offering_dict' : equity_offering_dict,
			'equity_offering_variables' : equity_offering_variables,
			'asset_acquisition_variables' : asset_acquisition_variables,
			'asset_acquisition_prod' : asset_acquisition_prod,
			'asset_acqu_result' : asset_acqu_result,
			'asset_sale_prod' : asset_sale_prod,
			'asset_sale_variables' : asset_sale_variables,
			'asset_sale_calc_result' : asset_sale_calc_result,
			'total_init_variables' : total_init_variables,
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
		total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

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
				'total_init_variables' : total_init_variables,
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
		duration = json.loads(request.POST.get('total_duration'))
		year_define = request.POST.get('total_year_define')
		boe_mcfe = json.loads(request.POST.get('total_boe_mcfe'))
		date = request.POST.get('date')
		
		r_calc = (1 + inflation / 100) / (1 + net_asset_value / 100)

		total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

		total_init_variables.net_asset_summary = net_asset_value
		total_init_variables.inflation = inflation
		total_init_variables.rig_case = rig
		total_init_variables.duration = duration
		total_init_variables.year = year_define
		total_init_variables.boe_mcfe = boe_mcfe
		total_init_variables.date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

		total_init_variables.save()

		return JsonResponse({
			'status' : True,		
		})


def navTotalEquityOffering(request):
	ticker_id = 1
	play_id = 1
	if request.method == 'POST':
		choice = json.loads(request.POST.get('equity_choice'))
		share_amount = json.loads(request.POST.get('equity_share_amount'))		
		shoe = json.loads(request.POST.get('equity_shoe'))
		last_price = json.loads(request.POST.get('equity_last_price'))
		gross_issue = json.loads(request.POST.get('equity_gross_issue'))
		net_issue = json.loads(request.POST.get('equity_net_issue'))
		date = request.POST.get('date')

		equity_offering = TotalEquityOffering.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		equity_offering.choice = choice
		equity_offering.share_amount = share_amount
		equity_offering.shoe = shoe
		equity_offering.last_price = last_price
		equity_offering.gross_issue = gross_issue
		equity_offering.net_issue = net_issue
		equity_offering.date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

		equity_offering.save()

		equity_offering_object = EquityOffering({
			'choice' : choice,
			'share_amount' : share_amount,	
			'shoe' : shoe,
			'last_price' : last_price,
			'gross_issue' : gross_issue,
			'net_issue' : net_issue
		})

		result = equity_offering_object.get_values()

		return JsonResponse({
			'status' : True,
			'tbl_dict' : result	
		})


def navTotalAssetAcquisition(request):
	ticker_id = 1
	play_id = 1
	if request.method == 'POST':
		acqu_uses_eur_mix = json.loads(request.POST.get('acqu_uses_eur_mix'))
		acqu_uses_mix = json.loads(request.POST.get('acqu_uses_mix'))
		acqu_uses_proved_mix = json.loads(request.POST.get('acqu_uses_proved_mix'))
		acqu_date = request.POST.get('acqu_date')
		acqu_uses_choice = json.loads(request.POST.get('acqu_uses_choice'))
		acqu_src_shares_fst = json.loads(request.POST.get('acqu_src_shares_fst'))
		acqu_src_shares_sec = json.loads(request.POST.get('acqu_src_shares_sec'))
		acqu_src_total = json.loads(request.POST.get('acqu_src_total'))
		acqu_uses_acres = json.loads(request.POST.get('acqu_uses_acres'))
		acqu_uses_ip30 = json.loads(request.POST.get('acqu_uses_ip30'))
		acqu_uses_cost = json.loads(request.POST.get('acqu_uses_cost'))
		acqu_uses_eur = json.loads(request.POST.get('acqu_uses_eur'))
		acqu_uses_mboepd_total = json.loads(request.POST.get('acqu_uses_mboepd_total'))
		acqu_uses_proved_mmboe_total = json.loads(request.POST.get('acqu_uses_proved_mmboe_total'))
		acqu_uses_f_d = json.loads(request.POST.get('acqu_uses_f_d'))
		acqu_uses_pud = json.loads(request.POST.get('acqu_uses_pud'))

		asset_acquisition = TotalAssetAcqu.objects.filter(play_id = play_id, ticker_id = ticker_id).get()
		asset_acquisition.sources_share_fst = acqu_src_shares_fst
		asset_acquisition.sources_share_sec = acqu_src_shares_sec
		asset_acquisition.sources_share_total = acqu_src_total
		asset_acquisition.uses_acres = acqu_uses_acres
		asset_acquisition.uses_ip30 = acqu_uses_ip30
		asset_acquisition.uses_cost = acqu_uses_cost
		asset_acquisition.uses_eur = acqu_uses_eur
		asset_acquisition.uses_f_d = acqu_uses_f_d
		asset_acquisition.uses_pud = acqu_uses_pud
		asset_acquisition.choice = acqu_uses_choice
		asset_acquisition.uses_prod = acqu_uses_mboepd_total
		asset_acquisition.uses_proved = acqu_uses_proved_mmboe_total
		asset_acquisition.date = datetime.datetime.strptime(acqu_date, '%m/%d/%Y').date()
		asset_acquisition.save()

		asset_acquisition_prod_dict = {}
		for prod_id, prod_value in acqu_uses_eur_mix.items():
			asset_acquisition_prod_dict[prod_id] = {}
			asset_acquisition_prod_dict[prod_id]['eur_mix'] = json.loads(prod_value)

		for prod_id, prod_value in acqu_uses_mix.items():
			asset_acquisition_prod_dict[prod_id]['prod_mix'] = json.loads(prod_value)

		for prod_id, prod_value in acqu_uses_proved_mix.items():
			asset_acquisition_prod_dict[prod_id]['proved_mix'] = json.loads(prod_value)


		asset_acquisition_prod = TotalAssetAcquProd.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
		
		counter = 1
		other_eur_mix = 0
		other_prod_mix = 0
		other_proved_mix = 0
		for prod_id, value_set in asset_acquisition_prod_dict.items():
			counter += 1
			other_eur_mix += value_set['eur_mix']
			other_prod_mix += value_set['prod_mix']
			other_proved_mix += value_set['proved_mix']

			acquisition_uses_update = TotalAssetAcquProd.objects.filter(ticker_id = ticker_id, play_id = play_id, prod_id = prod_id).get()
			acquisition_uses_update.eur_mix = value_set['eur_mix']
			acquisition_uses_update.prod_mix = value_set['prod_mix']
			acquisition_uses_update.proved_mix = value_set['proved_mix']
			acquisition_uses_update.save()

		acquisition_uses_update = TotalAssetAcquProd.objects.filter(ticker_id = ticker_id, play_id = play_id, prod_id = counter).get()
		acquisition_uses_update.eur_mix = (100 - other_eur_mix)
		acquisition_uses_update.prod_mix = (100 - other_prod_mix)
		acquisition_uses_update.proved_mix = (100 - other_proved_mix)
		acquisition_uses_update.save()
		
		asset_acquisition_prod = TotalAssetAcquProd.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
		asset_acquisition_variables = TotalAssetAcqu.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		
		asset_acquisition_obj = AssetAcquisition({
			'acqu_date' : acqu_date,
			'acqu_uses_choice' : acqu_uses_choice,
			'asset_acquisition_variables' : asset_acquisition_variables,
			'asset_acquisition_prod' : asset_acquisition_prod,
		})

		result = asset_acquisition_obj.preprocess()

		return JsonResponse({
			'status' : True,
			'acqu_data' : result	
		})


def navTotalAssetSale(request):
	ticker_id = 1
	play_id = 1
	if request.method == 'POST':
		sale_date = request.POST.get('sale_date')
		sale_uses_choice = json.loads(request.POST.get('sale_uses_choice'))
		sale_sources_total = json.loads(request.POST.get('sale_sources_total'))
		sale_src_acres = json.loads(request.POST.get('sale_src_acres'))
		sale_src_ip30 = json.loads(request.POST.get('sale_src_ip30'))
		sale_src_cost = json.loads(request.POST.get('sale_src_cost'))
		sale_src_eur = json.loads(request.POST.get('sale_src_eur'))
		sale_src_mboepd_total = json.loads(request.POST.get('sale_src_mboepd_total'))
		sale_src_proved_mmboe_total = json.loads(request.POST.get('sale_src_proved_mmboe_total'))
		sale_src_f_d = json.loads(request.POST.get('sale_src_f_d'))
		sale_src_pud = json.loads(request.POST.get('sale_src_pud'))
		sale_src_eur_mix = json.loads(request.POST.get('sale_src_eur_mix'))
		sale_src_mix = json.loads(request.POST.get('sale_src_mix'))
		sale_src_proved_mix = json.loads(request.POST.get('sale_src_proved_mix'))
		
		
		asset_sale = TotalAssetSale.objects.filter(play_id = play_id, ticker_id = ticker_id).get()
		asset_sale.sources_total = sale_sources_total
		asset_sale.sources_acres = sale_src_acres
		asset_sale.sources_ip30 = sale_src_ip30
		asset_sale.sources_cost = sale_src_cost
		asset_sale.sources_eur = sale_src_eur
		asset_sale.sources_f_d = sale_src_f_d
		asset_sale.sources_pud = sale_src_pud
		asset_sale.choice = sale_uses_choice
		asset_sale.sources_prod = sale_src_mboepd_total
		asset_sale.sources_proved = sale_src_proved_mmboe_total
		asset_sale.date = datetime.datetime.strptime(sale_date, '%m/%d/%Y').date()

		asset_sale.save()

		asset_sale_prod_dict = {}
		for prod_id, prod_value in sale_src_eur_mix.items():
			asset_sale_prod_dict[prod_id] = {}
			asset_sale_prod_dict[prod_id]['eur_mix'] = json.loads(prod_value)

		for prod_id, prod_value in sale_src_mix.items():
			asset_sale_prod_dict[prod_id]['prod_mix'] = json.loads(prod_value)

		for prod_id, prod_value in sale_src_proved_mix.items():
			asset_sale_prod_dict[prod_id]['proved_mix'] = json.loads(prod_value)


		asset_sale_prod = TotalAssetSaleProd.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
		counter = 1
		other_eur_mix = 0
		other_prod_mix = 0
		other_proved_mix = 0
		for prod_id, value_set in asset_sale_prod_dict.items():
			counter += 1
			other_eur_mix += value_set['eur_mix']
			other_prod_mix += value_set['prod_mix']
			other_proved_mix += value_set['proved_mix']

			sale_src_update = TotalAssetSaleProd.objects.filter(ticker_id = ticker_id, play_id = play_id, prod_id = prod_id).get()
			sale_src_update.eur_mix = value_set['eur_mix']
			sale_src_update.prod_mix = value_set['prod_mix']
			sale_src_update.proved_mix = value_set['proved_mix']
			sale_src_update.save()

		sale_src_update = TotalAssetSaleProd.objects.filter(ticker_id = ticker_id, play_id = play_id, prod_id = counter).get()
		sale_src_update.eur_mix = (100 - other_eur_mix)
		sale_src_update.prod_mix = (100 - other_prod_mix)
		sale_src_update.proved_mix = (100 - other_proved_mix)
		sale_src_update.save()
		
		asset_sale_prod = TotalAssetSaleProd.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
		asset_sale_variables = TotalAssetSale.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		
		asset_sale_obj = AssetSale({
			'sale_date' : sale_date,
			'sale_uses_choice' : sale_uses_choice,
			'asset_sale_variables' : asset_sale_variables,
			'asset_sale_prod' : asset_sale_prod,
		})

		result = asset_sale_obj.preprocess()

		return JsonResponse({
			'status' : True,
			'sale_data' : result,
		})
