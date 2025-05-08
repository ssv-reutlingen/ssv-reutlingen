// Copyright (c) 2024, phamos.eu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sponsoring', {
	refresh: function(frm) {
		const has_valid_items = frm.doc.sponsoring_items ? frm.doc.sponsoring_items.some(item => item.item_code) : false;
        const button = document.querySelector('button.btn-secondary[data-doctype="Quotation"]');
        if (button) {
            button.remove()
        }

        if (has_valid_items){
            frm.add_custom_button(
                __('Sales Order'), 
                () => frm.events.make_sales_order(frm),
                __('Create'));
            
            // override the plus icon after sale order reference 
            const button = document.querySelector('button.btn-secondary[data-doctype="Sales Order"]');
            if (button) {
                button.replaceWith(button.cloneNode(true));
                const newButton = document.querySelector('button.btn-secondary[data-doctype="Sales Order"]');
                newButton.addEventListener('click',
                    () => frm.events.make_sales_order(frm)
                );
            }
        }
	},
    
    make_sales_order: function(frm) {
        frappe.model.open_mapped_doc({
            method: 'ssv_reutlingen.ssv_reutlingen.doctype.sponsoring.sponsoring.create_sales_order',
            frm: frm
        });
    },

	onload: function(frm) {
        if(frm.is_new()){
            frappe.call({
                method: 'get_contract_start',
                doc: frm.doc,
                callback: function(res) {
                    if (res.message) {
                        frm.set_value('contract_start', res.message);
                    }
                }
            });
        }
	},

    contract_start: function(frm) {
        frappe.call({
            method: 'get_contract_end_and_notice_dates',
            doc: frm.doc,
            callback: function(res) {
                if (res.message) {
                    frm.set_value('contract_end', res.message[0]);
                    frm.set_value('latest_notice_date', res.message[1]);
                }
            }
        });
	},

    customer: function(frm) {
        frappe.call({
            method: "frappe.client.get",
            args: {
                doctype: "Contact",
                name: frm.doc.customer_primary_contact,
            },
            callback: function (response) {
                if (response.message) {
                    const contact = response.message;
                    frm.set_value('contact_email', contact.email_id)   
                }
            },
        });
        
    },
	
	net_total: function(frm) {
		// Set grand total
		frappe.call({
            method: 'ssv_reutlingen.ssv_reutlingen.doctype.sponsoring.sponsoring.calculate_grand_total',
            args: {
                net_total: frm.doc.net_total
            },
            callback: function(res) {
                if (res.message) {
                    frm.set_value('grand_total', res.message);
                }
            }
        });
	}
});

frappe.ui.form.on('Sponsoring Items', {
    item_code: function(frm, cdt, cdn){
        let row = locals[cdt][cdn];
                
        frappe.call({
            method: 'ssv_reutlingen.ssv_reutlingen.doctype.sponsoring.sponsoring.get_item_details',
            args: {
                item_code: row.item_code,
                company: frm.doc.company
            },
            callback: function(res) {
                if (res.message) {
                    row.warehouse = res.message
                }
            }
        });
        
    },

	net_rate: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		row.net_amount = calculate_amount(row.net_rate, row.qty)
		refresh_field("net_amount", cdn, "sponsoring_items");
		calculate_net_total(frm)
	},

	qty: function(frm,cdt,cdn) {
		let row = locals[cdt][cdn];
		row.net_amount = calculate_amount(row.net_rate, row.qty)
		refresh_field("net_amount", cdn, "sponsoring_items");
		calculate_net_total(frm)
	},

	sponsoring_items_remove: function(frm,cdt,cdn){
		calculate_net_total(frm)
	}
});

function calculate_amount (net_rate, qty) {
	return net_rate * qty
}

function calculate_net_total (frm) {
	frappe.call({
		method: 'calculate_net_total',
		doc: frm.doc,
		callback: function(res) {
			if (res.message) {
				frm.set_value('net_total', res.message);
			}
		}
	});
}