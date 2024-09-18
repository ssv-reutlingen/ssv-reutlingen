# Copyright (c) 2024, phamos.eu and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Sponsoring(Document):
	pass

@frappe.whitelist()
def calculate_grand_total(net_total):
	settings = frappe.get_single("SSV Reutlingen Settings")
	tax_rate = settings.tax_rate or 0
	grand_total = float(net_total) * (1 + tax_rate / 100)
	return grand_total