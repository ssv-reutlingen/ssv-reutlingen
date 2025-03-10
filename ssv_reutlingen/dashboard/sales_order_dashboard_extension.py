from frappe import _

def get_data(data):
    
    custom_section = {
        "label": _("Sponsoring"),
        "items": ["Sponsoring"]
    }

    data.get("transactions", []).append(custom_section)

    return data
