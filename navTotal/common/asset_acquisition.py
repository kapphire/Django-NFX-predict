from __future__ import division

class AssetAcquisition(object):
	def __init__(self, params):
		self.date = params['acqu_date']
		self.uses_choice = params['acqu_uses_choice']
		self.acqu_prod = params['asset_acquisition_prod']
		self.acqu_vals = params['asset_acquisition_variables']

	def preprocess(self):
		asset_acqu_dict = {}
		asset_acqu_dict['shares'] = self.acqu_vals.sources_share_fst * self.acqu_vals.sources_share_sec
		asset_acqu_dict['cash'] = self.acqu_vals.sources_share_total - asset_acqu_dict['shares']

		asset_acqu_dict['prod_mix'] = {}
		asset_acqu_dict['proved_mix'] = {}
		for prod_value in self.acqu_prod:
			asset_acqu_dict['prod_mix'][prod_value.prod_id] = prod_value.prod_mix * self.acqu_vals.uses_prod / 100
			asset_acqu_dict['proved_mix'][prod_value.prod_id] = prod_value.proved_mix * self.acqu_vals.uses_proved / 100
		asset_acqu_dict['total'] = self.acqu_vals.sources_share_total
		asset_acqu_dict['other_eur_mix'] = prod_value.eur_mix
		asset_acqu_dict['other_prod_mix'] = prod_value.prod_mix
		asset_acqu_dict['other_proved_mix'] = prod_value.proved_mix
		
		return asset_acqu_dict