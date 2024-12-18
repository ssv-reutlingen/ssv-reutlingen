import frappe

# @frappe.whitelist()
# def create_delivery_notes(sales_order):
#     from erpnext.selling.doctype.sales_order.sales_order import make_delivery_note

#     sales_order_doc = frappe.get_doc("Sales Order", sales_order)
#     delivery_note_names = []

#     # Iterate through each item in the Sales Order items table
#     for item in sales_order_doc.items:
#         print(item)
#         # Create a Delivery Note for this item
#         delivery_note_doc = make_delivery_note(sales_order)
        
#         # # Modify the Delivery Note for a single item
#         delivery_note_doc.set("items", [])
#         delivery_note_doc.items = [item]  # Only include this item
#         # delivery_note_doc.flags.ignore_permissions = True  # Optional: Ignore user permissions

#         # # Save the Delivery Note
#         delivery_note_doc.save()

#         # # Append the Delivery Note name to the list
#         # delivery_note_names.append(delivery_note_doc.name)

#     return delivery_note_names


@frappe.whitelist()
def create_delivery_notes(sales_order):
    # Fetch the Sales Order
    sales_order_doc = frappe.get_doc("Sales Order", sales_order)
    
    # Loop through each item in the Sales Order
    for item in sales_order_doc.items:
        # Create a new Delivery Note document
        delivery_note_doc = frappe.new_doc("Delivery Note")
        delivery_note_doc.customer = sales_order_doc.customer
        delivery_note_doc.posting_date = frappe.utils.nowdate()
        delivery_note_doc.set("items", [])

        # Prepare item data
        item_data = {
            "item_code": item.item_code,
            "qty": item.qty,
            "rate": item.rate,
            "warehouse": item.warehouse,
            "uom": item.uom,
        }
        
        # Append the item to the Delivery Note
        delivery_note_doc.append("items", item_data)

        # Save the Delivery Note
        delivery_note_doc.save()
        frappe.db.commit()

    return {"message": "Delivery Notes created successfully!"}
