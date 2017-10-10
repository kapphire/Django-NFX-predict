from __future__ import division

class NavTotalStatic(object):
	def __init__(self, param):
		self.prods_date = param['prods_date']
		self.well_cost = param['well_cost']
		self.play_result = param['play_result']
		self.acre_unconv = param['acre_unconv']
		self.risk_unconv = param['risk_unconv']		
		self.spacing = param['spacing']
		self.zone = param['zone']
		self.zone_pros = param['zone_pros']
		self.rigs = param['rigs']
		self.days_to = param['days_to']
		self.drilled = param['drilled']
		self.total_init_variables = param['total_init_variables']
		self.shares_out = param['shares_out']

	def preprocess(self):
		unconv_fst_tbl_dict = {}
		unconv_fst_tbl = []
		unconv_sec_tbl_dict = {}
		
		acerage = self.risk_unconv * self.acre_unconv * self.zone * self.zone_pros / 100 / 100
		if self.spacing == 0:
			wells = 0
		else:
			wells = (acerage / self.spacing) - self.drilled

		unconv_fst_total = 0
		for product in self.prods_date:
			prod_id = product['prod_id']
			if product['prod_id'] != 2:
				unconv_sec_tbl_dict[prod_id] = product['eur'] * wells / 1000
				unconv_fst_tbl_dict[prod_id] = product['eur'] * wells / 1000
				unconv_fst_tbl.append(unconv_fst_tbl_dict[prod_id])
				unconv_fst_total_choice = unconv_fst_tbl_dict[prod_id]
				unconv_fst_total_choice_other = unconv_fst_tbl_dict[prod_id] * 6
			else:
				unconv_sec_tbl_dict[prod_id] = product['eur'] * wells
				unconv_fst_tbl_dict[prod_id] = product['eur'] * wells
				unconv_fst_tbl.append(unconv_fst_tbl_dict[prod_id])
				unconv_fst_total_choice = unconv_fst_tbl_dict[prod_id] / 6
				unconv_fst_total_choice_other = unconv_fst_tbl_dict[prod_id]
			if self.total_init_variables.boe_mcfe == 1:
				unconv_fst_total += unconv_fst_total_choice
			else:
				unconv_fst_total += unconv_fst_total_choice_other

		unconv_fst_tbl.append(unconv_fst_total)
		if (unconv_sec_tbl_dict[2] + unconv_sec_tbl_dict[1] * 6) == 0:
			gas_per = 'No Data'
		else:
			gas_per = (unconv_sec_tbl_dict[2] / (unconv_sec_tbl_dict[2] + unconv_sec_tbl_dict[1] * 6)) * 100
		unconv_fst_tbl.append(gas_per)

		if self.days_to == 0:
			wells_yr = 0
		else:
			wells_yr = self.rigs * (365 / self.days_to)
		if wells_yr = 0:
			years_unconv = 0
		else:
			years_unconv = wells / wells_yr

		unconv_sec_tbl_dict['total'] = unconv_fst_total
		unconv_sec_tbl_dict['gas_per'] = gas_per
		unconv_sec_tbl_dict['acerage'] = acerage
		unconv_sec_tbl_dict['wells'] = wells
		unconv_sec_tbl_dict['wells_yr'] = wells_yr
		unconv_sec_tbl_dict['years_unconv'] = years_unconv
		if years_unconv <= self.total_init_variables.duration:
			unconv_sec_tbl_dict['m_a'] = years_unconv
		else:
			unconv_sec_tbl_dict['m_a'] = self.total_init_variables.duration
		unconv_sec_tbl_dict['well_cost'] = self.well_cost
		unconv_sec_tbl_dict['well_pv_ten'] = self.play_result.pv_10
		unconv_sec_tbl_dict['well_pv_eur'] = self.play_result.pv_eur
		unconv_sec_tbl_dict['irr'] = self.play_result.irr

		if self.total_init_variables.rig_case == 1:
			denominator = years_unconv
		else:
			denominator = unconv_sec_tbl_dict['m_a']
		numerator = (1 + self.total_init_variables.inflation / 100) / (1 + self.total_init_variables.net_asset_summary / 100)


		unconv_sec_tbl_dict['boe'] = max(0, unconv_sec_tbl_dict['well_pv_eur'] * (1 - pow(numerator, (denominator - 1)))) / (1 - numerator) / denominator
		unconv_sec_tbl_dict['mm'] = unconv_sec_tbl_dict['boe'] * unconv_sec_tbl_dict['total']
		unconv_sec_tbl_dict['share'] = unconv_sec_tbl_dict['mm'] / self.shares_out
		unconv_sec_tbl_dict['acre'] = unconv_sec_tbl_dict['mm'] / self.acre_unconv * 1000000

		unconv_fst_tbl.append(unconv_sec_tbl_dict['boe'])
		unconv_fst_tbl.append(unconv_sec_tbl_dict['mm'])
		unconv_fst_tbl.append(unconv_sec_tbl_dict['share'])

		return {'array' : unconv_fst_tbl, 'dict' : unconv_sec_tbl_dict}
