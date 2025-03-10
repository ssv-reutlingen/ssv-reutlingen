from frappe import _


def get_data():
	return {
		"fieldname": "sponsoring",
		
		"transactions": [
			{"label": _("Sales Order"), "items": ["Sales Order"]},
		],
	}