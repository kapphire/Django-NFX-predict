from __future__ import division

class SharesOut(object):
	def __init__(self, params):
		self.acquisition = params['acquisition']
		self.equity = params['equity']

	def get_shares_out(self):
		shares_out = (self.equity.share_amount + self.equity.share_amount * self.equity.shoe / 100) * self.equity.choice + self.acquisition.choice * self.acquisition.sources_share_fst + 163.6
		return shares_out