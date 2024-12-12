// Copyright (c) 2024, phamos.eu and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Customer Details"] = {
	"filters": [
		{
            fieldname: "customer_group",
            label: __("Customer Group"),
            fieldtype: "Link",
            options: "Customer Group"
        }
	]
};
