import frappe
import json
from frappe import _
from frappe.core.doctype.communication.email import _make as make_communication


def _parse_json_param(value):
    if isinstance(value, str):
        return json.loads(value)
    return value


@frappe.whitelist()
def create_delivery_notes(doctype, name, dialog_data, items):

    doc = frappe.get_doc(doctype, name)
    items = _parse_json_param(items)
    dialog_data = _parse_json_param(dialog_data)
    
    total_steps = len(items)
    current_step = 0
    created_delivery_notes = []

    for idx, item in enumerate(items):
        current_step += 1
        progress = (current_step / total_steps) * 100
        frappe.publish_progress(
            progress,
            title=_("Creating Delivery Notes and Sending Emails"),
            description=_("Creating delivery note and sending email for item {}/{}").format(current_step, total_steps)
        )

        delivery_note_doc = frappe.new_doc("Delivery Note")
        delivery_note_doc.customer = doc.customer
        delivery_note_doc.posting_date = frappe.utils.nowdate()
        delivery_note_doc.set("items", [])
        email = doc.contact_email
        template = _get_template_for_item(dialog_data, item.get("item_code"))


        item_data = {
            "item_code": item.get('item_code'),
            "qty": item.get('qty'),
            "rate": item.get('rate') if doctype == "Sales Order" else item.get('net_rate'),
            "warehouse": item.get('warehouse'),
            "uom": item.get('uom'),
        }
        
        delivery_note_doc.append("items", item_data)

        delivery_note_doc.save()
        delivery_note_doc.submit()
        frappe.db.commit()

        communication = send_csv_via_email(email, delivery_note_doc, template)
        frappe.db.commit()

        created_delivery_notes.append({
            "delivery_note": delivery_note_doc.name,
            "communication": communication,
        })

    doc.db_set("processed", 1)
    if doctype == "Sales Order":
        doc.db_set("status", "To Bill")
        doc.db_set("delivery_status", "Fully Delivered")
        doc.db_set("per_delivered", 100)

    return {
        "message": "Delivery Notes created successfully!",
        "delivery_notes": created_delivery_notes,
    }


def _get_template_for_item(dialog_data, item_code):
    item_code = (item_code or "").strip()
    for row in dialog_data:
        if (row.get("item_code") or "").strip() == item_code:
            return row
    return None


def send_csv_via_email(recipient_email, delivery_note_doc, template):
    if not recipient_email:
        frappe.throw(
            _("No contact email found on {0} {1}. Cannot send delivery note email.").format(
                delivery_note_doc.doctype, delivery_note_doc.name
            )
        )

    if not template:
        frappe.throw(
            _("No email template found for delivery note {0}.").format(delivery_note_doc.name)
        )

    subject = template.get("subject") or ""
    message = template.get("response") or ""
    doc_json = frappe.as_json(delivery_note_doc.as_dict(), indent=2)

    attachments = [{
        "fname": f"{delivery_note_doc.name}.json",
        "fcontent": doc_json,
    }]

    # Same path as the desk "New Email" button (frappe.core.doctype.communication.email.make).
    result = make_communication(
        doctype=delivery_note_doc.doctype,
        name=delivery_note_doc.name,
        content=message,
        subject=subject,
        recipients=recipient_email,
        communication_medium="Email",
        send_email=True,
        attachments=attachments,
        communication_type="Communication",
        add_signature=False,
        now=True,
    )
    return result.get("name")


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