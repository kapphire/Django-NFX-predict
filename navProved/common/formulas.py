from __future__ import division
import math


class NavProved(object):
	"""docstrings for NavProved"""
	def __init__(self, rawData, param):
		self.start = int(rawData[0])
		self.end = int(rawData[1])
		self.predicts = param['predicts']
		self.sum_param = param['sum_param']
		self.years = param['years']
		self.prices = param['prices']
		self.delta = 0.1
		self.early_stage_value = param['early_stage_value']


	def predict_params(self, predicts, decline_rates):
		prod_diff = {}
		prod_esc = {}
		pred_opd = {}

		for predict in predicts:
			if predict.prod_id not in prod_diff:
				prod_diff[predict.prod_id] = []

			if predict.prod_id not in prod_esc:
				prod_esc[predict.prod_id] = []

			if predict.prod_id not in pred_opd:
				pred_opd[predict.prod_id] = []

			prod_diff[predict.prod_id] = predict.prod_diff
			prod_esc[predict.prod_id] = predict.prod_esc
			pred_opd[predict.prod_id] = predict.prod_pred_opd

		self.prod_diff = prod_diff
		self.prod_esc = prod_esc
		# self.decline_rate = decline_rates_dict
		self.pred_opd = pred_opd

	def preprocess_prices(self, years, prices):
		self.sample_years = years
		self.ticker = prices[0].ticker

		price_samples = {}
		for item in prices:
			if item.prod_id not in price_samples:
				price_samples[item.prod_id] = []

			price_samples[item.prod_id].append(item.price)

		self.price_samples = price_samples
		return price_samples

	def get_original_sum(self, production, decline_rate, number_of_years, target):
		sum = 0.0
		for i in range(0, number_of_years):
			sum += production * pow(decline_rate, i)
		numerator = sum - target

		return numerator

	def get_gradient_sum(self, production, decline_rate, number_of_years):
		sum = 0.0
		for i in range(0, number_of_years - 1):
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

		for predict in self.predicts:
			initial_productions[predict.prod_id] = predict.prod_pred_opd
			targets[predict.prod_id] = predict.prod.prod_initial_value

		decline_rates = {}
		number_of_years = self.end - self.start + 1

		for prod_id in initial_productions:
			decline_rates[prod_id] = self.estimate_decline_rate(float(initial_productions[prod_id]), float(targets[prod_id]), self.delta, 1, number_of_years)


		self.decline_rates = decline_rates
		return decline_rates

	def initialize_prices(self, sum_params):
		self.preprocess_prices(self.years, self.prices)
		self.predict_params(self.predicts, self.decline_rates)

		diffs = self.prod_diff
		escs = self.prod_esc
		decline_rates = self.decline_rates
		pred_opds = self.pred_opd

		tbl_data = []
		tbl_sample_dict = []
		sample_len = len(self.price_samples[1])


		for idx_year, year in enumerate(range(self.start, self.end + 1)):
			table_row = []			
			tbl_sample_dict_row = {}

			table_row.append(year)

			# Calculating sample values - first 3 columns in sheet file.
			for prod_id in self.price_samples:				
				tbl_sample_dict_row[prod_id] = {}

				if idx_year < sample_len:
					tbl_sample_dict_row[prod_id]['price'] = self.price_samples[prod_id][idx_year] + diffs[prod_id]
				else:
					tbl_sample_dict_row[prod_id]['price'] = tbl_sample_dict[idx_year - 1][prod_id]['price'] * (1 + escs[prod_id] / 100)

				table_row.append(tbl_sample_dict_row[prod_id]['price'])

			# Calculating production values and total as well - net 4 columns in sheet file.
			total = 0
			net_revenue = 0
			for prod_id in self.price_samples:
				tbl_sample_dict_row[prod_id]['pred'] = pred_opds[prod_id] * pow((1.0 - decline_rates[prod_id] / 100.0), idx_year)

				table_row.append(tbl_sample_dict_row[prod_id]['pred'])
				total += sum_params[prod_id] * tbl_sample_dict_row[prod_id]['pred']
				
				# Calculating net revenue value	
				net_revenue += tbl_sample_dict_row[prod_id]['price'] * tbl_sample_dict_row[prod_id]['pred']

			tbl_sample_dict_row['total'] = total
			table_row.append(total)

			tbl_sample_dict_row['net_revenue'] = net_revenue
			table_row.append(net_revenue)

			# Calculating capex value
			capex_len = len(self.sample_years)
			if idx_year >= capex_len:
				tbl_sample_dict_row['capex'] = 0
			else:
				tbl_sample_dict_row['capex'] = self.ticker.capex / 5

			# Calculating Operating Costs value.
			if idx_year == 0:
				tbl_sample_dict_row['operating_costs_mcfe'] = self.ticker.op_cost

			elif idx_year in range(0, 8) :
				tbl_sample_dict_row['operating_costs_mcfe'] = tbl_sample_dict[idx_year - 1]['operating_costs_mcfe'] * (1 + self.ticker.op_cost_esc / 100)
			elif idx_year == 8:
				tbl_sample_dict_row['operating_costs_mcfe'] = 1.55
			else:
				tbl_sample_dict_row['operating_costs_mcfe'] = tbl_sample_dict[idx_year - 1]['operating_costs_mcfe'] * (1 + self.ticker.op_cost_esc / 100)

			tbl_sample_dict_row['operating_costs_mm'] = tbl_sample_dict_row['operating_costs_mcfe'] * tbl_sample_dict_row['total']

			# Calculating Prod_taxes
			tbl_sample_dict_row['prod_taxes'] = tbl_sample_dict_row['net_revenue'] * self.ticker.prod_taxes / 100

			# Calculating CFO
			tbl_sample_dict_row['cfo'] = tbl_sample_dict_row['net_revenue'] - tbl_sample_dict_row['operating_costs_mm'] - tbl_sample_dict_row['prod_taxes']

			# Calculating Less DD&A
			tbl_sample_dict_row['dda'] = tbl_sample_dict_row['total'] * self.ticker.dda

			# Calculating Operating Income
			tbl_sample_dict_row['operating_income'] = tbl_sample_dict_row['cfo'] - tbl_sample_dict_row['dda']

			# Calculating Tax
			if idx_year <= len(self.sample_years):
				tbl_sample_dict_row['tax'] = self.ticker.tax_rate / 100 * tbl_sample_dict_row['operating_income'] * (1 - self.ticker.deferred / 100)
			else:
				tbl_sample_dict_row['tax'] = self.ticker.tax_rate / 100 * tbl_sample_dict_row['operating_income'] * (1 - self.ticker.def_after_5yrs / 100)

			# Calculating FCF
			tbl_sample_dict_row['fcf'] = tbl_sample_dict_row['cfo'] - tbl_sample_dict_row['tax'] - tbl_sample_dict_row['capex']

			# Calculating Discount Factor
			if idx_year == 0:
				tbl_sample_dict_row['disc_factor'] = math.pow(1 / (1 + self.ticker.disc_factor / 100), 0.5)
			elif idx_year == 1:
				tbl_sample_dict_row['disc_factor'] = math.pow(1 / (1 + self.ticker.disc_factor / 100), 1)
			else:
				tbl_sample_dict_row['disc_factor'] = tbl_sample_dict[idx_year - 1]['disc_factor'] / (1 + self.ticker.disc_factor / 100)
			# Calculating PV
			tbl_sample_dict_row['pv'] = tbl_sample_dict_row['fcf'] * tbl_sample_dict_row['disc_factor']


			table_row.append(tbl_sample_dict_row['capex'])
			table_row.append(tbl_sample_dict_row['operating_costs_mcfe'])
			table_row.append(tbl_sample_dict_row['operating_costs_mm'])
			table_row.append(tbl_sample_dict_row['prod_taxes'])
			table_row.append(tbl_sample_dict_row['cfo'])
			table_row.append(tbl_sample_dict_row['dda'])
			table_row.append(tbl_sample_dict_row['operating_income'])
			table_row.append(tbl_sample_dict_row['tax'])
			table_row.append(tbl_sample_dict_row['fcf'])
			table_row.append(tbl_sample_dict_row['disc_factor'])
			table_row.append(tbl_sample_dict_row['pv'])


			tbl_sample_dict.append(tbl_sample_dict_row)
			tbl_data.append(table_row)
			self.tbl_sample_dict = tbl_sample_dict

		return tbl_data


	def get_sum_result(self):
		net_value = {}
		for individual in self.tbl_sample_dict:
			for key, value in individual.items():
				if type(value) is dict:
					if net_value.get(key) is None:
						net_value[key] = 0
					for prod_key, pred in value.items():
						if prod_key == 'pred':
							net_value[key] += pred
				else:
					if net_value.get(key) is None:
						net_value[key] = 0
					net_value[key] += value
		net_value['pv_boe'] = net_value['pv'] * 6 / net_value['total']
		net_value['pv_mcfe'] = net_value['pv'] / net_value['total']
		return net_value



if __name__ == "__main__":
	temp = NavProved()


# {'cfo': 7046.415350049809, 2: 1366.0000073877554, 3: 95.04998872337313, 'pv': 3203.171300359004, 1: 185.03291277957672, 'operating_income': -661.22311345599, 'capex': 1993.0, 'net_revenue': 14280.616640438278, 'tax': -2.5361469623997515, 'prod_taxes': 528.1651591057528, 'fcf': 5055.951497012208, 'disc_factor': 6.288388787148257, 'operating_costs_mm': 6706.036131282718, 'dda': 7707.638463505798, 'total': 3046.4974164054543, 'operating_costs_mcfe': 19.817419128038335}
