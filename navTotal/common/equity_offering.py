from __future__ import division

class EquityOffering(object):
	def __init__(self, param):
		self.choice = param['choice']
		self.share_amount = param['share_amount']	
		self.shoe = param['shoe']
		self.last_price = param['last_price']
		self.gross_issue = param['gross_issue']
		self.net_issue = param['net_issue']

	def get_values(self):
		equity_offering_dict = {}
		equity_offering_dict['shoe'] = self.share_amount * self.shoe / 100
		equity_offering_dict['total_shares_issued'] = equity_offering_dict['shoe'] + self.share_amount
		equity_offering_dict['gross_issue_price'] = self.last_price * (1 + self.gross_issue / 100)
		equity_offering_dict['net_issue_price'] = equity_offering_dict['gross_issue_price'] * (1 + self.net_issue / 100)
		equity_offering_dict['gross_proceeds'] = equity_offering_dict['total_shares_issued'] * equity_offering_dict['gross_issue_price']
		equity_offering_dict['net_proceeds'] = equity_offering_dict['total_shares_issued'] * equity_offering_dict['net_issue_price']

		return equity_offering_dict 
