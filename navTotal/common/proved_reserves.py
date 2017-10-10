from __future__ import division
import collections

class ProvedReserves(object):
	def __init__(self, params):
		self.nav_proved = params['nav_proved']
		self.shares_out = params['shares_out']
		self.total_init_variables = params['total_init_variables']

	def get_proved_reserves(self):
		proved_reserves_arr = ['United States', '']  # ======= Should be updated ===========
		proved_reserves_dict = {}
		ordered = {}
		for individual in self.nav_proved:
			if individual.name in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
				proved_reserves_dict[int(individual.name)] = individual.value
				ordered = collections.OrderedDict(sorted(proved_reserves_dict.items()))
			if individual.name == 'pv':
				pv = individual.value

		for key, value in ordered.items():
			proved_reserves_arr.append(round(value, 1))

		if self.total_init_variables.boe_mcfe == 0:
			total = proved_reserves_dict[1] + proved_reserves_dict[2] * 6
		else:
			total = proved_reserves_dict[1] + proved_reserves_dict[2] / 6
		if (proved_reserves_dict[1] + proved_reserves_dict[2] * 6) == 0:
			percent = 'No Data'
		else:
			percent = proved_reserves_dict[2] / (proved_reserves_dict[2] + proved_reserves_dict[1] * 6)
		if total == 0:
			asset_value = 'No Data'
		else:
			asset_value = pv / total



		proved_reserves_dict['total'] = total
		proved_reserves_dict['percent'] = percent
		proved_reserves_dict['asset_value'] = asset_value
		proved_reserves_dict['mm'] = pv
		proved_reserves_dict['share'] = round(pv / self.shares_out, 1)

		proved_reserves_arr.append(round(total, 1))
		proved_reserves_arr.append(round(percent, 1))
		proved_reserves_arr.append(round(asset_value, 1))
		proved_reserves_arr.append(round(pv, 1))
		proved_reserves_arr.append(round(proved_reserves_dict['share'], 1))

		result = {'array' : proved_reserves_arr, 'dict' : proved_reserves_dict}

		return result