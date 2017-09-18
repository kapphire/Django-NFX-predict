import math
import numpy


class TypeCurveStatic(object):
	"""docstring for TypeCurveStatic"""
	def __init__(self, param):
		self.years = param['years']
		self.ticker_id = param['ticker_id']
		self.ticker = param['ticker']
		self.products = param['products']
		self.prices = param['prices']
		self.names = param['play_names']
		self.play_prods = param['play_prods']
		self.scraped_data = param['play_scraped_data']
		self.common_input_class = param['play_common_input_class']
		self.prod_date_choices = param['play_prod_date_choices']
		self.play_prod_declines = param['play_prod_declines']
		self.delta = 0.0001
		self.preprocess()

	def preprocess(self):
		# Align prices with prod
		price_align_prod = {}
		price_diff = {}
		for prod in self.play_prods:
			price_align_prod[prod.id] = []
			price_diff[prod.id] = prod.diff
		for ele in self.prices:
			for prod in self.play_prods:
				if ele.prod_id == prod.id:
					price_align_prod[prod.id].append(ele)
		# Product Price and Diff
		prod_price_diffs = []
		cell = {}
		for ele in price_align_prod:
			cell['prod_id'] = ele
			cell['price'] = price_align_prod[ele][1].price * price_diff[ele] / 100 + price_align_prod[ele][0].price
			cell['diff'] = price_align_prod[ele][1].price * price_diff[ele] / 100
			prod_price_diffs.append(cell.copy())
		self.prod_price_diffs = prod_price_diffs

		prod_price_diffs_1 = []
		cell = {}
		for ele in price_align_prod:
			cell['prod_id'] = ele
			cell['price'] = price_align_prod[ele][1].price * price_diff[ele] / 100 + price_align_prod[ele][1].price
			cell['diff'] = price_align_prod[ele][1].price * price_diff[ele] / 100
			prod_price_diffs_1.append(cell.copy())
		self.prod_price_diffs_1 = prod_price_diffs_1

		prod_price_diffs_2 = []
		cell = {}
		for ele in price_align_prod:
			cell['prod_id'] = ele
			cell['price'] = price_align_prod[ele][1].price * price_diff[ele] / 100 + price_align_prod[ele][2].price
			cell['diff'] = price_align_prod[ele][1].price * price_diff[ele] / 100
			prod_price_diffs_2.append(cell.copy())
		self.prod_price_diffs_2 = prod_price_diffs_2

		prod_price_diffs_3 = []
		cell = {}
		for ele in price_align_prod:
			cell['prod_id'] = ele
			cell['price'] = price_align_prod[ele][1].price * price_diff[ele] / 100 + price_align_prod[ele][3].price
			cell['diff'] = price_align_prod[ele][1].price * price_diff[ele] / 100
			prod_price_diffs_3.append(cell.copy())
		self.prod_price_diffs_3 = prod_price_diffs_3

		prod_price_diffs_4 = []
		cell = {}
		for ele in price_align_prod:
			cell['prod_id'] = ele
			cell['price'] = price_align_prod[ele][1].price * price_diff[ele] / 100 + price_align_prod[ele][4].price
			cell['diff'] = price_align_prod[ele][1].price * price_diff[ele] / 100
			prod_price_diffs_4.append(cell.copy())
		self.prod_price_diffs_4 = prod_price_diffs_4

		

		# Play product 12M, 24M...
		ip30 = 0
		eur_total = 0
		for individual in self.common_input_class:
			if individual.name == "IP30":
				ip30 = individual.value
				self.ip30 = ip30
			if individual.name == "EUR_total":
				eur_total = individual.value
				self.eur_total = eur_total
			if individual.name == "Royalty":
				royalty = individual.value
				self.royalty = royalty
			if individual.name == "Income Tax Rate":
				income_tax_rate = individual.value
				self.income_tax_rate = income_tax_rate
			if individual.name == "Well_Cost":
				well_cost = individual.value
				self.well_cost = well_cost
			if individual.name == "Inflation / Escalation":
				escalation = individual.value
				self.escalation = escalation

		for individual in self.scraped_data:
			if individual.name == "G&T":
				gt = individual.value
				self.gt = gt
			if individual.name == "LOE":
				loe = individual.value
				self.loe = loe

		prods_date = []
		drilling_f_d_pre = 0
		for ele in self.prod_date_choices:
			each_prod_date = {}
			if ele.prod_id is not 2:
				each_prod_date['prod_id'] = ele.prod_id
				each_prod_date['ip30'] = ele.ip30 * ip30 / 100
				each_prod_date['12m'] = each_prod_date['ip30'] * ele.m12 / 100 * ele.m12_decline / 100 / (ele.ip30 / 100)  
				each_prod_date['24m'] = each_prod_date['12m'] * ele.m24 / 100 * ele.m24_decline / 100 / (ele.m12 / 100)
				each_prod_date['eur'] = (ele.ip30 + ele.m12 + ele.m24) / 300 * eur_total
				prods_date.append(each_prod_date)
				drilling_f_d_pre += each_prod_date['eur']
			else:
				each_prod_date['prod_id'] = ele.prod_id
				each_prod_date['ip30'] = ele.ip30 * ip30 / 100 * 6 / 1000
				each_prod_date['12m'] = each_prod_date['ip30'] * ele.m12 / 100 * ele.m12_decline / 100 / (ele.ip30 / 100)  
				each_prod_date['24m'] = each_prod_date['12m'] * ele.m24 / 100 * ele.m24_decline / 100 / (ele.m12 / 100)
				each_prod_date['eur'] = (ele.ip30 + ele.m12 + ele.m24) / 300 * eur_total * 6 /1000
				prods_date.append(each_prod_date)
				drilling_f_d_pre_exc = each_prod_date['eur'] * 166.666666666667
		drilling_f_d = (well_cost * 1000) / (drilling_f_d_pre + drilling_f_d_pre_exc)
		self.drilling_f_d = drilling_f_d
		self.total_f_d = drilling_f_d + gt
		self.prods_date = prods_date
		self.pp_e = self.eur_total * self.total_f_d
		self.cash_flow = -self.pp_e
		return {'prod_price_diffs' : prod_price_diffs, 'prods_date' : prods_date, 'drilling_f_d' : drilling_f_d, 'total_f_d' : self.total_f_d}


	def get_original_sum(self, production, decline_rate, number_of_years, target):
		sum = 0.0
		for i in range(0, number_of_years - 1):
			sum += production * pow(decline_rate, i)
		numerator = sum - target

		return numerator


	def get_gradient_sum(self, production, decline_rate, number_of_years):
		sum = 0.0
		for i in range(0, number_of_years - 2):
			sum += production * (float(i) + 1.0) * pow(decline_rate, i)
		return sum


	def estimate_decline_rate(self, production, target, delta, decline_rate, number_of_years):
		self.timer += 1
		origin = self.get_original_sum(production, decline_rate, number_of_years, target)
		estimate = self.get_gradient_sum(production, decline_rate, number_of_years)

		pred_decline_rate = decline_rate - origin / estimate

		delta_val = self.get_original_sum(production, pred_decline_rate, number_of_years, target)

		if delta_val < delta or self.timer > 300:
			percent = (1.0 - pred_decline_rate) * 100
			return percent
		else:
			return self.estimate_decline_rate(production, target, delta, pred_decline_rate, number_of_years)
		

	def get_decline_rates(self):
		initial_productions = {}
		targets = {}
		self.timer = 0

		for predict in self.prods_date:
			prod_id = predict['prod_id']
			initial_productions[prod_id] = (predict['24m'] + predict['12m']) / 2 * 0.365
			targets[prod_id] = predict['eur'] - (predict['ip30'] + predict['12m']) / 2 * 0.365

		decline_rates = {}
		number_of_years = self.years

		for prod_id in initial_productions:
			decline_rates[prod_id] = self.estimate_decline_rate(float(initial_productions[prod_id]), float(targets[prod_id]), self.delta, 1, number_of_years)


		self.decline_rates = decline_rates
		return decline_rates



	def typeCurveTableData(self):
		table_data = []
		table_data_dict = []

		for year in range(1, self.years + 1):
			table_data_row = []
			table_data_row_dict = {}

			table_data_row_dict['year'] = year
			table_data_row.append(year)
			if year == 1:
				pred_total_pre = 0
				for ele in self.prods_date:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id] = {}

					table_data_row_dict[prod_id]['pred'] = (ele['ip30'] + ele['12m']) / 2 * 0.365
					table_data_row.append((ele['ip30'] + ele['12m']) / 2 * 0.365)
					if prod_id is not 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = ele['price']
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id != 2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + calc_prod
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = -self.loe
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-table_data_row_dict['net_price'] - table_data_row_dict['lifting_sec'], -self.pp_e)
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])
				# PP&E
				table_data_row_dict['pp_e'] = max(self.pp_e + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])

			elif year == 2:
				pred_total_pre = 0
				for ele in self.prods_date:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id] = {}					
					table_data_row_dict[prod_id]['pred'] = (ele['24m'] + ele['12m']) / 2 * 0.365
					table_data_row.append((ele['24m'] + ele['12m']) / 2 * 0.365)
					if prod_id != 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred	
					
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs_1:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = ele['price']
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id !=2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'])
						revenue_pre = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + revenue_pre
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = table_data_dict[year-2]['lifting'] * (1 + self.escalation / 100)
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-self.total_f_d * table_data_row_dict['pred_total'], -table_data_dict[year-2]['pp_e'])
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])

				# PP&E
				table_data_row_dict['pp_e'] = max(table_data_dict[year-2]['pp_e'] + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])	

			elif year == 3:
				pred_total_pre = 0
				for ele in self.play_prod_declines:
					prod_id = ele.prod_id
					table_data_row_dict[prod_id] = {}
					table_data_row_dict[prod_id]['pred'] = table_data_dict[year-2][prod_id]['pred'] * (1 - ele.decline / 100)
					table_data_row.append(table_data_row_dict[prod_id]['pred'])
					if prod_id != 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred	
					
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs_2:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = ele['price']
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id !=2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'])
						revenue_pre = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + revenue_pre
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = table_data_dict[year-2]['lifting'] * (1 + self.escalation / 100)
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-self.total_f_d * table_data_row_dict['pred_total'], -table_data_dict[year-2]['pp_e'])
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])

				# PP&E
				table_data_row_dict['pp_e'] = max(table_data_dict[year-2]['pp_e'] + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])

			elif year == 4:
				pred_total_pre = 0
				for ele in self.play_prod_declines:
					prod_id = ele.prod_id
					table_data_row_dict[prod_id] = {}
					table_data_row_dict[prod_id]['pred'] = table_data_dict[year-2][prod_id]['pred'] * (1 - ele.decline / 100)
					table_data_row.append(table_data_row_dict[prod_id]['pred'])
					if prod_id != 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred	
					
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs_3:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = ele['price']
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id !=2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'])
						revenue_pre = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + revenue_pre
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = table_data_dict[year-2]['lifting'] * (1 + self.escalation / 100)
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-self.total_f_d * table_data_row_dict['pred_total'], -table_data_dict[year-2]['pp_e'])
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])

				# PP&E
				table_data_row_dict['pp_e'] = max(table_data_dict[year-2]['pp_e'] + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])

			elif year == 5:
				pred_total_pre = 0
				for ele in self.play_prod_declines:
					prod_id = ele.prod_id
					table_data_row_dict[prod_id] = {}
					table_data_row_dict[prod_id]['pred'] = table_data_dict[year-2][prod_id]['pred'] * (1 - ele.decline / 100)
					table_data_row.append(table_data_row_dict[prod_id]['pred'])
					if prod_id != 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred	
					
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs_4:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = ele['price']
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id !=2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'])
						revenue_pre = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + revenue_pre
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = table_data_dict[year-2]['lifting'] * (1 + self.escalation / 100)
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-self.total_f_d * table_data_row_dict['pred_total'], -table_data_dict[year-2]['pp_e'])
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])

				# PP&E
				table_data_row_dict['pp_e'] = max(table_data_dict[year-2]['pp_e'] + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])
			else:
				pred_total_pre = 0
				for ele in self.play_prod_declines:
					prod_id = ele.prod_id
					table_data_row_dict[prod_id] = {}
					table_data_row_dict[prod_id]['pred'] = table_data_dict[year-2][prod_id]['pred'] * (1 - ele.decline / 100)
					table_data_row.append(table_data_row_dict[prod_id]['pred'])
					if prod_id != 2:
						pred_total_pre += table_data_row_dict[prod_id]['pred']
					else:
						calc_pred = table_data_row_dict[prod_id]['pred'] * 166.666666666667
				pred_total = pred_total_pre + calc_pred	
					
					# Proved products prices
				table_data_row.append(pred_total)	
				table_data_row_dict['pred_total'] = pred_total

				for ele in self.prod_price_diffs_4:
					prod_id = ele['prod_id']
					table_data_row_dict[prod_id]['prod'] = table_data_dict[year-2][prod_id]['prod'] * (1 + self.escalation / 100)
					table_data_row.append(table_data_row_dict[prod_id]['prod'])

				prod_total_pre = 0

				for ele in self.prods_date:
					prod_id = ele['prod_id']
					if prod_id !=2:
						prod_total_pre += table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod']
					else:
						calc_prod = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'])
						revenue_pre = (table_data_row_dict[prod_id]['pred'] * table_data_row_dict[prod_id]['prod'] * 1000)
				prod_total = (prod_total_pre + calc_prod) / table_data_row_dict['pred_total']
				revenue = prod_total_pre + revenue_pre
				table_data_row.append(prod_total)	
				table_data_row_dict['prod_total'] = prod_total

				# Royalty
				table_data_row_dict['royalty'] = -self.royalty * table_data_row_dict['prod_total'] / 100
				table_data_row.append(table_data_row_dict['royalty'])

				# Lifting
				table_data_row_dict['lifting'] = table_data_dict[year-2]['lifting'] * (1 + self.escalation / 100)
				table_data_row.append(table_data_row_dict['lifting'])

				# Revenue
				table_data_row_dict['revenue'] = revenue
				table_data_row.append(table_data_row_dict['revenue'])

				# Royalty_sec
				table_data_row_dict['royalty_sec'] = table_data_row_dict['royalty'] * table_data_row_dict['pred_total']
				table_data_row.append(table_data_row_dict['royalty_sec'])

				# Net Price
				table_data_row_dict['net_price'] = table_data_row_dict['revenue'] + table_data_row_dict['royalty_sec']
				table_data_row.append(table_data_row_dict['net_price'])

				# Lifting_sec
				table_data_row_dict['lifting_sec'] = table_data_row_dict['pred_total'] * table_data_row_dict['lifting']
				table_data_row.append(table_data_row_dict['lifting_sec'])

				# DD&A
				table_data_row_dict['dd_a'] = max(-self.total_f_d * table_data_row_dict['pred_total'], -table_data_dict[year-2]['pp_e'])
				table_data_row.append(table_data_row_dict['dd_a'])

				# Pre-tax Income
				table_data_row_dict['pre_tax_income'] = table_data_row_dict['net_price'] + table_data_row_dict['lifting_sec'] + table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['pre_tax_income'])

				# Tax
				table_data_row_dict['tax'] = -table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100
				table_data_row.append(table_data_row_dict['tax'])

				# NI
				table_data_row_dict['ni'] = table_data_row_dict['pre_tax_income'] + table_data_row_dict['tax']
				table_data_row.append(table_data_row_dict['ni'])

				# Cash Flow
				table_data_row_dict['cash_flow'] = table_data_row_dict['ni'] - table_data_row_dict['dd_a']
				table_data_row.append(table_data_row_dict['cash_flow'])

				# PP&E
				table_data_row_dict['pp_e'] = max(table_data_dict[year-2]['pp_e'] + table_data_row_dict['dd_a'] + (-table_data_row_dict['pre_tax_income'] * self.income_tax_rate / 100 - table_data_row_dict['tax']), 0)
				table_data_row.append(table_data_row_dict['pp_e'])

			table_data.append(table_data_row)
			table_data_dict.append(table_data_row_dict)	
		
		cash_flow_arr = [self.cash_flow]
		for idx, ele in enumerate(table_data_dict):
			cash_flow_arr.append(ele['cash_flow'])
		self.cash_flow_arr = cash_flow_arr

		return table_data


	def get_irr(self):
		irr = round(numpy.irr(self.cash_flow_arr), 5)
		npv = round(numpy.npv(0.1, self.cash_flow_arr), 5)
		pv_eur = npv / self.eur_total
		return {'irr' : irr, 'npv' : npv, 'pv_eur' : pv_eur}