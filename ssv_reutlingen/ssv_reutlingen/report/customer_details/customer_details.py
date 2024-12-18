# Copyright (c) 2024, phamos.eu and contributors
# For license information, please see license.txt

import frappe
from frappe import _

def execute(filters=None):
	columns, data = [], []
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
    return [
        {
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data", 
			"width": 200
		},
        {
			"label": _("Customer Group"),
			"fieldname": "customer_group",
			"fieldtype": "Link",
			"options": "Customer Group",
			"width": 150
		},
        {
			"label": _("Salutation"),
			"fieldname": "salutation",
			"fieldtype": "Data",
			"width": 100
		},
        {
			"label": _("First Name"),
			"fieldname": "first_name",
			"fieldtype": "Data",
			"width": 150
		},
        {
			"label": _("Last Name"),
			"fieldname": "last_name",
			"fieldtype": "Data",
			"width": 150
		},
        {
			"label": _("Email Address"),
			"fieldname": "email",
			"fieldtype": "Data",
			"width": 200
		},
        {
			"label": _("Address"),
			"fieldname": "address",
			"fieldtype": "Data",
			"width": 300
		},
    ]

def get_data(filters):
	conditions = ""
	if filters.get("customer_group"):
		conditions += " AND c.customer_group = %(customer_group)s"

	data = frappe.db.sql("""
        SELECT
            c.customer_name,
            c.customer_group,
            con.salutation,
            con.first_name,
            con.last_name,
            con.email_id AS email,
            CONCAT_WS(
                ", ",
                addr.address_line1,
                addr.address_line2,
                addr.pincode,
                addr.country
            ) AS address
        FROM
            `tabCustomer` AS c
        LEFT JOIN
            `tabContact` AS con ON con.name = c.customer_primary_contact
        LEFT JOIN
            `tabAddress` AS addr ON addr.name = c.customer_primary_address
        WHERE
            c.disabled = 0 {conditions}
    """.format(conditions=conditions), filters, as_dict=True)

	return data