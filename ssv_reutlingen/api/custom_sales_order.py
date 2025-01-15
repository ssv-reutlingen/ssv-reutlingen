import frappe
import json
from frappe import _

@frappe.whitelist()
def create_delivery_notes(sales_order, dialog_data, items):

    sales_order_doc = frappe.get_doc("Sales Order", sales_order)
    dialog_data = json.loads(dialog_data)
    items = json.loads(items)
    
    total_steps = len(items)
    current_step = 0

    for idx, item in enumerate(items):
        current_step += 1
        progress = (current_step / total_steps) * 100
        frappe.publish_progress(
            progress,
            title=_("Creating Delivery Notes and Sending Emails"),
            description=_("Creating delivery note and sending email for item {}/{}").format(current_step, total_steps)
        )

        delivery_note_doc = frappe.new_doc("Delivery Note")
        delivery_note_doc.customer = sales_order_doc.customer
        delivery_note_doc.posting_date = frappe.utils.nowdate()
        delivery_note_doc.set("items", [])
        email = sales_order_doc.contact_email
        template = dialog_data[item.get('item_code')]

        item_data = {
            "item_code": item.get('item_code'),
            "qty": item.get('qty'),
            "rate": item.get('rate'),
            "warehouse": item.get('warehouse'),
            "uom": item.get('uom'),
        }
        
        delivery_note_doc.append("items", item_data)

        delivery_note_doc.save()
        delivery_note_doc.submit()
        frappe.db.commit()

        send_csv_via_email(email, delivery_note_doc, template)

    sales_order_doc.db_set("processed", 1)

    return {"message": "Delivery Notes created successfully!"}


def send_csv_via_email(recipient_email, doc, template):
    try:
        doc = frappe.as_json(doc.as_dict(), indent=2)

        template = frappe.get_doc(
		"Email Template", template
	    )

        subject = template.subject
        message = template.response

        attachments = [{
            "fname": "delivery_note",
            "fcontent": doc,
        }]
        
        frappe.sendmail(
			recipients=recipient_email,
			subject=subject,
			message=message,
            attachments=attachments,
            delayed=False,
            retry=3
		)

        return {"status": "success", "message": _("Email sent successfully.")}
    except Exception as e:
        return {"status": "error", "message": str(e)}