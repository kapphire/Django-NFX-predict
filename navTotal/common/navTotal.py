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

	def preprocess(self):
		unconv_fst_tbl_dict = {}
		unconv_fst_tbl = []
		unconv_sec_tbl_dict = {}
		
		acerage = self.risk_unconv * self.acre_unconv * self.zone * self.zone_pros / 100 / 100
		wells = (acerage / self.spacing) - self.drilled
		print((acerage / self.spacing))

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
			if self.total_init_variables.boe_mcfe == 0:
				unconv_fst_total += unconv_fst_total_choice
			else:
				unconv_fst_total += unconv_fst_total_choice_other

		unconv_fst_tbl.append(unconv_fst_total)	
		gas_per = (unconv_sec_tbl_dict[2] / (unconv_sec_tbl_dict[2] + unconv_sec_tbl_dict[1] * 6)) * 100
		unconv_fst_tbl.append(gas_per)	
		wells_yr = self.rigs * (365 / self.days_to)
		years_unconv = wells / wells_yr



		unconv_sec_tbl_dict['acerage'] = acerage
		unconv_sec_tbl_dict['wells'] = wells
		unconv_sec_tbl_dict['wells_yr'] = wells_yr
		unconv_sec_tbl_dict['years_unconv'] = years_unconv
		unconv_sec_tbl_dict['m_a'] = years_unconv

		return unconv_fst_tbl
