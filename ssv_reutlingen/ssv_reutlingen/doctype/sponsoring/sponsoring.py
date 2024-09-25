# Copyright (c) 2024, phamos.eu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe import _

class Sponsoring(Document):
	def validate(self):
		self.validate_contribution_type()

	def validate_contribution_type(self):
		total_contribution_amount = 0
		for ct in self.contribution_type:
			total_contribution_amount += ct.amount
		
		if total_contribution_amount != self.net_total:
			frappe.throw(_("The sum of Contribution Type amounts must equal with Net Total"))

	@frappe.whitelist()
	def calculate_net_total(self):
		total_net_amount = 0
		for item in self.sponsoring_items:
			total_net_amount += item.net_amount
		return total_net_amount

@frappe.whitelist()
def calculate_grand_total(net_total):
	settings = frappe.get_single("SSV Reutlingen Settings")
	tax_rate = settings.tax_rate or 0
	grand_total = float(net_total) * (1 + tax_rate / 100)
	return grand_total