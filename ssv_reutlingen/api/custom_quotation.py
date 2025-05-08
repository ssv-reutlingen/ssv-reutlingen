import frappe
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def make_sponsoring(source_name, target_doc=None):
    return _make_sponsoring(source_name, target_doc)


def _make_sponsoring(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.customer = source.party_name
        target.company = source.company
        target.quotation = source.name
        target.prevdoc_docname = source.name

    doc = get_mapped_doc("Quotation", source_name, {
        "Quotation": {
            "doctype": "Sponsoring",
            "field_map": {
                "party_name": "customer",
                "company": "company",
            }
        },
        "Quotation Item": {
            "doctype": "Sponsoring Items",
            "field_map": {
                "item_code": "item_code",
                "description": "item_description",
                "uom": "uom",
                "qty": "qty",
                "rate": "net_rate",
            }
        }
    }, target_doc, set_missing_values)
    
    frappe.db.set_value("Quotation", source_name, "sponsoring", doc.name)

    return doc