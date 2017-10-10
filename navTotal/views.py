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
from .common.init_val import InitVal
from .common.shares_out import SharesOut
from .common.net_landing import NetLanding
from .common.proved_reserves import ProvedReserves
from .common.conventional import Conventional


# Create your views here.
def get_all_variables(play_id, ticker_id):
	equity = TotalEquityOffering.objects.filter(play_id = play_id, ticker_id = ticker_id).get()
	acquisition = TotalAssetAcqu.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	sale = TotalAssetSale.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	init = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	return {
				'equity' : equity, 
				'acquisition' : acquisition,
				'sale' : sale,
				'init' : init,
			}


def sharesOut(play_id, ticker_id):
	all_variables = get_all_variables(play_id, ticker_id)
	shares_out_obj = SharesOut({
			'acquisition' : all_variables['acquisition'],
			'equity' : all_variables['equity'], 
		})
	shares_out = shares_out_obj.get_shares_out()
	return shares_out


def netLanding(play_id, ticker_id):
	all_variables = get_all_variables(play_id, ticker_id)
	net_landing_variables = TotalNetLandingChange.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

	net_landing_obj = NetLanding({
			'acquisition' : all_variables['acquisition'],
			'equity' : all_variables['equity'],
			'sale' : all_variables['sale'],
			'init' : all_variables['init'],
			'net_landing' : net_landing_variables,
		})
	net_landing = net_landing_obj.get_net_landing()
	return net_landing


def provedReserves(ticker_id, play_id):
	nav_proved = NavProvedResult.objects.filter(ticker_id = ticker_id).all()
	total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	shares_out = sharesOut(play_id, ticker_id)
	proved_reserves_obj = ProvedReserves({
			'shares_out' : shares_out,
			'nav_proved' : nav_proved,
			'total_init_variables' : total_init_variables,
		})
	proved_reserves = proved_reserves_obj.get_proved_reserves()
	return proved_reserves


def otherAssets(play_id, ticker_id):
	net_landing = netLanding(play_id, ticker_id)
	shares_out = sharesOut(play_id, ticker_id)
	other_asset_mm = round(net_landing['sale_net'] - net_landing['purchase_net'], 2)
	share = round(other_asset_mm / shares_out, 2)
	other_asset_arr = ['TBA Transactional S&U'] # ======== Should be updated ==========
	other_asset_arr.append(other_asset_mm)
	other_asset_arr.append(share)
	other_asset_dict = {}
	other_asset_dict['name'] = 'TBA Transactional S&U'
	other_asset_dict['mm'] = other_asset_mm
	other_asset_dict['share'] = share
	return {'array' : other_asset_arr, 'dict' : other_asset_dict}


def landingResults(play_id, ticker_id):
	landing_results = TotalLandingResults.objects.filter(play_id = play_id, ticker_id = ticker_id).get()
	shares_out = sharesOut(play_id, ticker_id)
	get_mm = NavProvedResult.objects.filter(ticker_id = ticker_id).all()
	for individual in get_mm:
		if individual.name == 'pv':
			mm = individual.value
	calc_results = {}
	calc_results['debt'] = landing_results.debt / shares_out
	calc_results['equivalents'] = landing_results.equivalents / shares_out
	calc_results['deficit'] = landing_results.deficit / shares_out
	calc_results['hedge'] = landing_results.hedge / shares_out
	calc_results['total_share_liabilities'] = round(calc_results['debt'] + calc_results['equivalents'] + calc_results['deficit'] + calc_results['hedge'], 2)
	calc_results['total_mm_liabilities'] = landing_results.debt + landing_results.equivalents + landing_results.deficit + landing_results.hedge
	other_assets = otherAssets(play_id, ticker_id)['dict']
	calc_results['proven_net_mm'] = other_assets['mm'] + mm - calc_results['total_mm_liabilities']
	calc_results['proven_net_share'] = round(calc_results['proven_net_mm'] / shares_out)
	return calc_results


def unconventional(play_id, ticker_id):
	years = 0

	products = Product.objects.filter(ticker = ticker_id).order_by("id")
	prices = Price.objects.filter(ticker = ticker_id).order_by('id').all()
	play_names = Play.objects.filter(ticker_id = ticker_id).get()
	play_prods = PlayProduction.objects.filter(play_id = play_id).order_by('id').all()
	play_scraped_data = PlayScrapedData.objects.filter(play_id = play_id).order_by('id').all()
	play_common_input_class = PlayCommonInputClass.objects.filter(play_id = play_id).order_by('id').all()
	play_prod_date_choices = PlayProductionDateChoice.objects.filter(ticker_id = ticker_id).order_by('id').all()
	play_prod_declines = PlayProdDecline.objects.filter(ticker_id = ticker_id, play_id = play_id).order_by('prod_id')
	play_result = PlayResult.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

	navTotal = TypeCurveStatic({
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
	prods_date = navTotal.preprocess()['prods_date']
	well_cost = navTotal.preprocess()['well_cost']
	return {
			'prods_date' : prods_date, 
			'well_cost' : well_cost, 
			'play_result' : play_result,
			'total_init_variables' : total_init_variables
		}


def conventional(play_id, ticker_id):
	variables = TotalAddPlayConv.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
	shares_out = sharesOut(play_id = play_id, ticker_id = ticker_id)
	conventional_obj = Conventional({
			'variables' : variables,
			'init' : total_init_variables,
			'shares_out' : shares_out,
		})
	result = conventional_obj.preprocess()
	return result



def navTotal(request):
	ticker_id = 1
	play_id = 1

	products = Product.objects.filter(ticker = ticker_id).order_by("id")
	ticker = Ticker.objects.filter(id = ticker_id).get()

	# ========================= Net Asset Value Summary Init Variables ==================================
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
		init_val_dict = None
	else:
		for element in total_init_result:
			total_init_variables = element

		ngl_percent_wti = 30	# ============= Should comes from NAV Proved =================

		init_val = InitVal({
			'net_asset_value' : total_init_variables.net_asset_summary,
			'inflation' : total_init_variables.inflation,
			'ngl_percent_wti' : ngl_percent_wti,
		})
		init_val_dict = init_val.preprocess()


	# ============================ Equity Offering =========================================================
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

	# ========================================== Asset Acquisition =========================================
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

	# ==================================== Asset Sale ====================================================
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

	# ====================================== Net Landing ================================================== 
	
	net_landing_change = TotalNetLandingChange.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	if not  net_landing_change:
		insert_result = TotalNetLandingChange(
				play_id = play_id,
				ticker_id = ticker_id,
				sale_proceeds_s = 0,
				sale_carries_s = 0,
				equity_s = 0,
				monies_s = 0,
				carries_s = 0,
			)
		insert_result.save()
		net_landing = None
		net_landing_change_variables = None
	else:
		for element in net_landing_change:
			net_landing_change_variables = element

		net_landing = netLanding(play_id = play_id, ticker_id = ticker_id)

	# ==================================== Shares Out ====================================================
	shares_out = sharesOut(play_id = play_id, ticker_id = ticker_id)

	# =================================== Landing Proved Reserves ==========================================
	result = provedReserves(ticker_id = ticker_id, play_id = play_id)
	if not shares_out:
		proved_reserves == None
	else:
		proved_reserves = result['dict']

	if not shares_out:
		other_asset = None
	else:
		other_asset = otherAssets(play_id, ticker_id)['dict']

	# =================================== Landing Resutls ==================================================
	landing_result = TotalLandingResults.objects.filter(play_id = play_id, ticker_id = ticker_id).all()
	if not landing_result:
		insert_table = TotalLandingResults(
				ticker_id = ticker_id,
				play_id = play_id,
				debt = 0,
				equivalents = 0,
				deficit = 0,
				hedge = 0
			)
		insert_table.save()
		landing_results = None
		landing_results_variables = None
	else:
		landing_results = landingResults(play_id, ticker_id)
		landing_results_variables = TotalLandingResults.objects.filter(play_id = play_id, ticker_id = ticker_id).get()


	# ================================ Unconventional =====================================================
	total_add_play_unconv = TotalAddPlayUnconv.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	if not total_add_play_unconv:
		insert_result = TotalAddPlayUnconv(
				ticker_id = ticker_id,
				play_id = play_id,
				acres = 0,
				risk = 0,
				spacing = 0,
				zones = 0,
				zone_pros = 0,
				rigs = 0,
				drill = 0,
				wells = 0
			)
		insert_result.save()
		prods_date = None
		total_add_play_unconv = None
		calc_result = None
	else:
		prods_date = unconventional(play_id, ticker_id)['prods_date']
		total_add_play_unconv = TotalAddPlayUnconv.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		result = unconventional(play_id, ticker_id)
		unconventional_result = NavTotalStatic({
			'prods_date' : result['prods_date'],
			'well_cost' : result['well_cost'],
			'play_result' : result['play_result'],
			'acre_unconv' : total_add_play_unconv.acres,
			'risk_unconv' : total_add_play_unconv.risk,
			'spacing' : total_add_play_unconv.spacing,
			'zone' : total_add_play_unconv.zones,
			'zone_pros' : total_add_play_unconv.zone_pros,
			'rigs' : total_add_play_unconv.rigs,
			'days_to' : total_add_play_unconv.drill,
			'drilled' : total_add_play_unconv.wells,
			'total_init_variables' : result['total_init_variables'],
			'shares_out' : shares_out,
		})
		calc_result = unconventional_result.preprocess()['dict']

	# ================================ Conventional ===================================================
	total_add_play_conv = TotalAddPlayConv.objects.filter(ticker_id = ticker_id, play_id = play_id).all()
	if not total_add_play_conv:
		insert_result = TotalAddPlayConv(
				ticker_id = ticker_id,
				play_id = play_id,
				lst_hc = 0,
				flat = 0,
				lst_prod = 0,
				dev_cost = 0,
				wl = 0,
				operator = 0,
				royalty = 0,
				trap = 0,
				reservoir = 0,
				seal = 0,
				timing = 0,
				commercial = 0,
				closure = 0,
				drainage = 0,
				mean = 0,
				boe_feet = 0,
				days_to = 0,
				oil_conv = 0,
				gas_conv = 0,
				risk_conv = 0,
				proved_book = 0
			)
		insert_result.save()
		conventional_variables = None
		conventional_dict = None
	else:
		conventional_variables = TotalAddPlayConv.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		conventional_dict = conventional(play_id, ticker_id)['dict']

	return render(request, 'nav_total_content.html', {
			'products' : products, 
			'prods_date' : prods_date,
			'equity_offering_dict' : equity_offering_dict,
			'equity_offering_variables' : equity_offering_variables,
			'asset_acquisition_variables' : asset_acquisition_variables,
			'asset_acquisition_prod' : asset_acquisition_prod,
			'asset_acqu_result' : asset_acqu_result,
			'asset_sale_prod' : asset_sale_prod,
			'asset_sale_variables' : asset_sale_variables,
			'asset_sale_calc_result' : asset_sale_calc_result,
			'total_init_variables' : total_init_variables,
			'init_val_dict' : init_val_dict,
			'shares_out' : shares_out,
			'net_landing' : net_landing,
			'net_landing_change_variables' : net_landing_change_variables,
			'proved_reserves' : proved_reserves,
			'other_asset' : other_asset,
			'landing_results': landing_results,
			'landing_results_variables' : landing_results_variables,
			'total_add_play_unconv' : total_add_play_unconv,
			'calc_result' : calc_result,
			'conv_dict' : conventional_dict,
			'conv_variables' : conventional_variables,
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

		total_init_variables = TotalInit.objects.filter(ticker_id = ticker_id, play_id = play_id).get()

		total_init_variables.net_asset_summary = net_asset_value
		total_init_variables.inflation = inflation
		total_init_variables.rig_case = rig
		total_init_variables.duration = duration
		total_init_variables.year = year_define
		total_init_variables.boe_mcfe = boe_mcfe
		total_init_variables.date = datetime.datetime.strptime(date, '%m/%d/%Y').date()

		total_init_variables.save()

		ngl_percent_wti = 30	# ============= Should comes from NAV Proved =================
		init_val = InitVal({
			'net_asset_value' : net_asset_value,
			'inflation' : inflation,
			'ngl_percent_wti' : ngl_percent_wti,
		})
		result = init_val.preprocess()

		return JsonResponse({
			'status' : True,
			'init_data' : result,		
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

		shares_out = sharesOut(play_id = play_id, ticker_id = ticker_id)

		proved_reserves = provedReserves(ticker_id = ticker_id, play_id = play_id)['array']

		return JsonResponse({
			'status' : True,
			'tbl_dict' : result,
			'shares_out' : shares_out,
			'proved_reserves' : proved_reserves,
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

		shares_out = sharesOut(play_id = play_id, ticker_id = ticker_id)

		proved_reserves = provedReserves(ticker_id = ticker_id, play_id = play_id)['array']

		return JsonResponse({
			'status' : True,
			'acqu_data' : result,
			'shares_out' : shares_out,
			'proved_reserves' : proved_reserves,
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


def navTotalNetLanding(request):
	ticker_id = 1
	play_id = 1
	if request.method == "POST":
		sale_proceeds_s = json.loads(request.POST.get('sale_proceeds_s'))
		sale_carries_s = json.loads(request.POST.get('sale_carries_s'))
		equity_s = json.loads(request.POST.get('equity_s'))
		monies_s = json.loads(request.POST.get('monies_s'))
		carries_s = json.loads(request.POST.get('carries_s'))

		net_landing_update = TotalNetLandingChange.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		net_landing_update.sale_proceeds_s = sale_proceeds_s
		net_landing_update.sale_carries_s = sale_carries_s
		net_landing_update.equity_s = equity_s
		net_landing_update.monies_s = monies_s
		net_landing_update.carries_s = carries_s
		net_landing_update.save()

		net_landing = netLanding(play_id = play_id, ticker_id = ticker_id)

		other_asset = otherAssets(play_id, ticker_id)['array']

		return JsonResponse({
				'status' : True,
				'net_landing' : net_landing,
				'other_asset' : other_asset,
			})


def navTotalLandingResults(request):
	ticker_id = 1
	play_id = 1
	if request.method == "POST":
		debt = json.loads(request.POST.get('debt'))
		equivalents = json.loads(request.POST.get('equivalents'))
		deficit = json.loads(request.POST.get('deficit'))
		hedge = float(request.POST.get('hedge'))   # ====== Should be updated =======
		
		landing_results = TotalLandingResults.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		landing_results.debt = debt
		landing_results.equivalents = equivalents
		landing_results.deficit = deficit
		landing_results.hedge = hedge
		landing_results.save()

		landing_calc_results = landingResults(play_id, ticker_id)
		return JsonResponse({
				'status' : True,
				'calc_results' : landing_calc_results,
			})


def navTotalUnconventional(request):
	ticker_id = 1
	play_id = 1
	if request.method == "POST":
		acre_unconv = json.loads(request.POST.get('acre_unconv'))
		risk_unconv = json.loads(request.POST.get('risk_unconv'))
		spacing = json.loads(request.POST.get('spacing'))
		zone = json.loads(request.POST.get('zone'))
		zone_pros = json.loads(request.POST.get('zone_pros'))
		rigs = json.loads(request.POST.get('rigs'))
		days_to = json.loads(request.POST.get('days_to'))
		drilled = json.loads(request.POST.get('drilled'))

		unconventional_update = TotalAddPlayUnconv.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		unconventional_update.acres = acre_unconv
		unconventional_update.risk = risk_unconv
		unconventional_update.spacing = spacing
		unconventional_update.zones = zone
		unconventional_update.zone_pros = zone_pros
		unconventional_update.rigs = rigs
		unconventional_update.drill = days_to
		unconventional_update.wells = drilled
		unconventional_update.save()

		result = unconventional(play_id, ticker_id)
		shares_out = sharesOut(play_id = play_id, ticker_id = ticker_id)

		unconventional_result = NavTotalStatic({
			'prods_date' : result['prods_date'],
			'well_cost' : result['well_cost'],
			'play_result' : result['play_result'],
			'acre_unconv' : acre_unconv,
			'risk_unconv' : risk_unconv,
			'spacing' : spacing,
			'zone' : zone,
			'zone_pros' : zone_pros,
			'rigs' : rigs,
			'days_to' : days_to,
			'drilled' : drilled,
			'total_init_variables' : result['total_init_variables'],
			'shares_out' : shares_out,
		})
		calc_result = unconventional_result.preprocess()
		return JsonResponse({
				'status' : True,
				'calc_result' : calc_result,
			})


def navTotalConventional(request):
	ticker_id = 1
	play_id = 1
	if request.method == 'POST':
		lst_hc = json.loads(request.POST.get('lst_hc'))
		flat = json.loads(request.POST.get('flat'))
		lst_prod = json.loads(request.POST.get('lst_prod'))
		dev_cost = json.loads(request.POST.get('dev_cost'))
		wl = json.loads(request.POST.get('wl'))
		operator = request.POST.get('operator')
		royalty = json.loads(request.POST.get('royalty'))
		trap = json.loads(request.POST.get('trap'))
		reservoir = json.loads(request.POST.get('reservoir'))
		seal = json.loads(request.POST.get('seal'))
		timing = json.loads(request.POST.get('timing'))
		commercial = json.loads(request.POST.get('commercial'))
		closure = json.loads(request.POST.get('closure'))
		drainage = json.loads(request.POST.get('drainage'))
		mean = json.loads(request.POST.get('mean'))
		boe_feet = json.loads(request.POST.get('boe_feet'))
		oil_conv = json.loads(request.POST.get('oil_conv'))
		gas_conv = json.loads(request.POST.get('gas_conv'))
		risk_conv = json.loads(request.POST.get('risk_conv'))
		proved_book = json.loads(request.POST.get('proved_book'))

		conventional_update = TotalAddPlayConv.objects.filter(ticker_id = ticker_id, play_id = play_id).get()
		
		conventional_update.lst_hc = lst_hc
		conventional_update.flat = flat
		conventional_update.lst_prod = lst_prod
		conventional_update.dev_cost = dev_cost
		conventional_update.wl = wl
		conventional_update.operator = operator
		conventional_update.royalty = royalty
		conventional_update.trap = trap
		conventional_update.reservoir = reservoir
		conventional_update.seal = seal
		conventional_update.timing = timing
		conventional_update.commercial = commercial
		conventional_update.closure = closure
		conventional_update.drainage = drainage
		conventional_update.mean = mean
		conventional_update.boe_feet = boe_feet
		conventional_update.oil_conv = oil_conv
		conventional_update.gas_conv = gas_conv
		conventional_update.risk_conv = risk_conv
		conventional_update.proved_book = proved_book
		conventional_update.save()

		calc_result = conventional(play_id, ticker_id)

		return JsonResponse({
				'status' : True,
				'calc_result' : calc_result,
			})