from __future__ import division

class InitVal(object):
	def __init__(self, params):
		self.net_asset_value = params['net_asset_value']
		self.inflation = params['inflation']
		self.wti = params['ngl_percent_wti']

	def preprocess(self):
		init_val_dict = {}
		init_val_dict['r'] = (1 + self.inflation / 100) / (1 + self.net_asset_value / 100)
		init_val_dict['wti'] = self.wti
		return init_val_dict