import frappe

def set_sales_order(doc, method=None):
    if doc.sponsoring:
        sponsoring = frappe.get_doc("Sponsoring", doc.sponsoring)
        sponsoring.sales_order = doc.name
        sponsoring.save()
        frappe.db.commit()