import math


class NavProved(object):
	"""docstrings for NavProved"""
	def __init__(self, rawData, param):
		self.start = int(rawData[0])
		self.end = int(rawData[1])

		self.preprocess_prices(param['years'], param['prices'])
		self.predict_params(param['predicts'], param['decline_rates'])
		self.initialize_prices(param['sum_param'])

	def predict_params(self, predicts, decline_rates):
		prod_diff = {}
		prod_esc = {}
		decline_rate = {}
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

		for rate in decline_rates:
			if rate.prod_id not in decline_rate:
				decline_rate[rate.prod_id] = []

			decline_rate[rate.prod_id] = rate.decline_rate

		self.prod_diff = prod_diff
		self.prod_esc = prod_esc
		self.decline_rate = decline_rate
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

	def initialize_prices(self, sum_params):
		diffs = self.prod_diff
		escs = self.prod_esc
		decline_rates = self.decline_rate
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
				if idx_year == 0:
					tbl_sample_dict_row[prod_id]['pred'] = pred_opds[prod_id]
				else:
					tbl_sample_dict_row[prod_id]['pred'] = tbl_sample_dict[idx_year - 1][prod_id]['pred'] * (1 - decline_rates[prod_id] / 100)

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


		return tbl_data

if __name__ == "__main__":
	temp = NavProved()