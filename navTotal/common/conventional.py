from __future__ import division

class Conventional(object):
	def __init__(self, params):
		self.variables = params['variables']
		self.init = params['init']
		self.shares_out = params['shares_out']

	def preprocess(self):
		conventional_dict = {}
		conventional_arr = []
		conventional_dict['lst_hc'] = self.variables.lst_hc
		conventional_dict['flat'] = self.variables.flat
		conventional_dict['lst_prod'] = self.variables.lst_prod
		conventional_dict['dev_cost'] = self.variables.dev_cost
		conventional_dict['wl'] = self.variables.wl
		conventional_dict['operator'] = self.variables.operator
		conventional_dict['royalty'] = self.variables.royalty
		conventional_dict['trap'] = self.variables.trap
		conventional_dict['reservoir'] = self.variables.reservoir
		conventional_dict['seal'] = self.variables.seal
		conventional_dict['timing'] = self.variables.timing
		conventional_dict['commercial'] = self.variables.commercial
		conventional_dict['closure'] = self.variables.closure
		conventional_dict['drainage'] = self.variables.drainage
		conventional_dict['mean'] = self.variables.mean
		conventional_dict['boe_feet'] = self.variables.boe_feet
		conventional_dict['oil_conv'] = self.variables.oil_conv
		conventional_dict['gas_conv'] = self.variables.gas_conv
		conventional_dict['risk_conv'] = self.variables.risk_conv
		conventional_dict['proved_book'] = self.variables.proved_book
		conventional_dict['ps'] = conventional_dict['trap'] * conventional_dict['reservoir'] * conventional_dict['seal'] * conventional_dict['timing'] * conventional_dict['commercial'] * 100
		conventional_dict['acre_feet'] = conventional_dict['drainage'] * conventional_dict['mean']
		conventional_dict['gross'] = conventional_dict['acre_feet'] * conventional_dict['boe_feet'] / 1000000
		conventional_dict['expected'] = conventional_dict['gross'] * conventional_dict['ps'] * conventional_dict['royalty'] * conventional_dict['wl'] / 1000000
		conventional_dict['ngl_conv'] = 100 - conventional_dict['oil_conv'] - conventional_dict['gas_conv']

		# ============================= Should be updated ===============================================
		conventional_dict['oil_data'] = conventional_dict['oil_conv'] / 100 * conventional_dict['expected'] * conventional_dict['risk_conv'] / 100
		conventional_dict['gas_data'] = conventional_dict['gas_conv'] / 100 * conventional_dict['expected'] * conventional_dict['risk_conv'] / 100 * 6
		conventional_dict['ngl_data'] = conventional_dict['ngl_conv'] / 100 * conventional_dict['expected'] * conventional_dict['risk_conv'] / 100
		if self.init.boe_mcfe == 0:
			conventional_dict['total'] = conventional_dict['gas_data'] + conventional_dict['oil_data'] * 6
		else:
			conventional_dict['total'] = conventional_dict['gas_data'] / 6 + conventional_dict['oil_data']
		if (conventional_dict['gas_data'] + conventional_dict['oil_data'] * 6) == 0:
			conventional_dict['per_gas'] = 'No data'
		else:
			conventional_dict['per_gas'] = conventional_dict['gas_data'] / (conventional_dict['gas_data'] + conventional_dict['oil_data'] * 6) * 100
		conventional_dict['asset_value'] = 10.39 # =================== Should be updated =====================
		conventional_dict['mm'] = max(0, conventional_dict['asset_value'] * conventional_dict['total']) * (1 - conventional_dict['proved_book'])
		conventional_dict['share'] = conventional_dict['mm'] / self.shares_out

		conventional_arr.append(conventional_dict['oil_data'])
		conventional_arr.append(conventional_dict['gas_data'])
		conventional_arr.append(conventional_dict['ngl_data'])
		conventional_arr.append(conventional_dict['total'])
		conventional_arr.append(conventional_dict['per_gas'])
		conventional_arr.append(conventional_dict['asset_value'])
		conventional_arr.append(conventional_dict['mm'])
		conventional_arr.append(conventional_dict['share'])

		result = {'dict' : conventional_dict, 'array' : conventional_arr}
		return result