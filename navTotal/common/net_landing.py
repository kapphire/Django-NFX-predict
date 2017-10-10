from __future__ import division

class NetLanding(object):
	def __init__(self, params):
		self.equity = params['equity']
		self.acqu = params['acquisition']
		self.sale = params['sale']
		self.init = params['init']
		self.net_landing = params['net_landing']

	def get_net_landing(self):
		net_landing_dict = {}
		
		if self.init.date > self.sale.date:
			date_compared = 0
		else:
			date_compared = 1
		net_landing_dict['sale_proceeds_p'] = self.sale.choice * self.sale.sources_total * date_compared
		net_landing_dict['sale_proceeds_xp'] = net_landing_dict['sale_proceeds_p'] * self.net_landing.sale_proceeds_s / 100
		sale_carries_p = 0 # ================= Guess it will be changed (None) ==========================
		net_landing_dict['sale_carries_xp'] = sale_carries_p * self.net_landing.sale_carries_s / 100

		if self.init.date > self.equity.date:
			date_compared = 0
		else:
			date_compared = 1
		equity_net_proceed = (self.equity.share_amount + self.equity.share_amount * self.equity.shoe / 100) * (self.equity.last_price * (1 + self.equity.net_issue * 100))
		net_landing_dict['equity_p'] = (self.acqu.sources_share_fst * self.acqu.sources_share_sec) + date_compared * self.equity.choice * equity_net_proceed
		net_landing_dict['equity_xp'] = net_landing_dict['equity_p'] * self.net_landing.equity_s / 100
		net_landing_dict['sale_net'] = net_landing_dict['sale_proceeds_xp'] + net_landing_dict['sale_carries_xp'] + net_landing_dict['equity_xp']

		if self.init.date > self.acqu.date:
			date_compared = 0
		else:
			date_compared = 1
		net_landing_dict['monies_p'] = self.acqu.sources_share_total
		net_landing_dict['monies_xp'] = net_landing_dict['monies_p'] * self.net_landing.monies_s / 100
		carries_p = 0 # ================= Guess it will be changed (None) ==========================
		net_landing_dict['carries_xp'] = carries_p * self.net_landing.carries_s
		net_landing_dict['purchase_net'] = net_landing_dict['monies_xp'] + net_landing_dict['carries_xp']
		
		return net_landing_dict