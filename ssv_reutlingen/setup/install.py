import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

def after_migrate():
	create_custom_fields(get_custom_fields())
	
def before_uninstall():
	delete_custom_fields(get_custom_fields())

def delete_custom_fields(custom_fields):
	for doctype, fields in custom_fields.items():
		for field in fields:
			custom_field_name = frappe.db.get_value(
				"Custom Field", dict(dt=doctype, fieldname=field.get("fieldname"))
			)
			if custom_field_name:
				frappe.delete_doc("Custom Field", custom_field_name)

		frappe.clear_cache(doctype=doctype)

def get_custom_fields():
	custom_fields_sales_order = [
		{
			"label": "SSV Section",
			"fieldname": "ssv_section",
			"fieldtype": "Section Break",
			"hidden": 1
		},
        {
            "fieldname": "processed",
            "fieldtype": "Check",
			"label": "Processed",
            "default": "0",
            "print_hide": 1,
			"allow_on_submit": 1,
            "insert_after": "ssv_section"
        },
		{
			"fieldname": "ssv_last_section",
			"fieldtype": "Section Break",
			"insert_after": "processed"
		}
	]

	return {
		"Sales Order": custom_fields_sales_order
	}