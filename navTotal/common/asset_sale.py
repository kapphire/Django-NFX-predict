from __future__ import division

class AssetSale(object):
	def __init__(self, params):
		self.date = params['sale_date']
		self.uses_choice = params['sale_uses_choice']
		self.sale_prod = params['asset_sale_prod']
		self.sale_vals = params['asset_sale_variables']

	def preprocess(self):
		asset_sale_dict = {}
		asset_sale_dict['prod_mix'] = {}
		asset_sale_dict['proved_mix'] = {}

		for prod_value in self.sale_prod:
			asset_sale_dict['prod_mix'][prod_value.prod_id] = prod_value.prod_mix * self.sale_vals.sources_prod / 100
			asset_sale_dict['proved_mix'][prod_value.prod_id] = prod_value.proved_mix * self.sale_vals.sources_proved / 100
			
		asset_sale_dict['total'] = self.sale_vals.sources_total
		asset_sale_dict['other_eur_mix'] = prod_value.eur_mix
		asset_sale_dict['other_prod_mix'] = prod_value.prod_mix
		asset_sale_dict['other_proved_mix'] = prod_value.proved_mix
		
		return asset_sale_dict