import frappe
import json
from frappe import _

@frappe.whitelist()
def create_delivery_notes(sales_order, dialog_data, items):

    sales_order_doc = frappe.get_doc("Sales Order", sales_order)
    items = json.loads(items)
    dialog_data = json.loads(dialog_data)
    
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
        template = next((it for it in dialog_data if it["item_code"] == item.get('item_code')), None)


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
    sales_order_doc.db_set("status", "To Bill")
    sales_order_doc.db_set("delivery_status", "Fully Delivered")
    sales_order_doc.db_set("per_delivered", 100)

    return {"message": "Delivery Notes created successfully!"}


def send_csv_via_email(recipient_email, doc, template):
    try:
        doc = frappe.as_json(doc.as_dict(), indent=2)

        subject = template['subject']
        message = template['response']

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


@frappe.whitelist()
def get_email_template(item_code):

    Item = frappe.qb.DocType("Item")
    EmailTemplate = frappe.qb.DocType("Email Template")

    email_template_name = (
        frappe.qb.from_(Item)
        .select(Item.email_template)
        .where(Item.item_code == item_code)
    ).run(as_dict=True)

    if not email_template_name or not email_template_name[0].get("email_template"):
        return {
            "email_template": "",
            "subject": "",
            "response": ""
        }

    email_template_name = email_template_name[0]["email_template"]
   
    email_template_details = (
        frappe.qb.from_(EmailTemplate)
        .select(EmailTemplate.subject, EmailTemplate.response)
        .where(EmailTemplate.name == email_template_name)
    ).run(as_dict=True)

    return {
        "email_template": email_template_name,
        "subject": email_template_details[0].get("subject", ""),
        "response": email_template_details[0].get("response", "")
    }