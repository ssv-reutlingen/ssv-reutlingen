frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        
        const has_valid_items = frm.doc.items.some(item => item.item_code);
        if (!frm.doc.processed && has_valid_items) {
            frm.add_custom_button(__('Create Delivery Notes and Send Emails'), function() {
                const dialog = new frappe.ui.Dialog({
                    title: __("Create Delivery Notes and Send Emails"),
                    fields: [
                        {
                            fieldtype: "Table",
                            fieldname: "items_with_templates",
                            label: __("Items and Email Templates"),
                            fields: [
                                {
                                    fieldtype: "Link",
                                    fieldname: "item_code",
                                    label: __("Item Code"),
                                    options: 'Item',
                                    in_list_view: 1,
                                },
                                {
                                    fieldtype: "Link",
                                    fieldname: "email_template",
                                    label: __("Email Template"),
                                    options: "Email Template",
                                    in_list_view: 1,
                                },
                            ],
                            data: frm.doc.items.map(item => ({
                                item_code: item.item_code,
                                email_template: "",
                                edit_option: 0,
                            })),
                            get_data: () => {
                                return dialog.get_value("items_with_templates");
                            },
                        },
                    ],
                    primary_action_label: __("Create Delivery Notes"),
                    primary_action: function() {
                        let dialog_data = dialog.get_value("items_with_templates");

                        if (!dialog_data || !dialog_data.length) {
                            frappe.msgprint(__("Please map at least one Email Template to proceed."));
                            return;
                        }

                        dialog_data = dialog_data.reduce((acc, item) => {
                            acc[item.item_code] = item.email_template;
                            return acc;
                        }, {});

                        dialog.hide();
                        
                        frappe.call({
                            method: "ssv_reutlingen.api.custom_sales_order.create_delivery_notes",
                            args: {
                                sales_order: frm.doc.name,
                                dialog_data: dialog_data,
                                items: frm.doc.items
                            },
                            callback: function(response) {
                                if (response.message) {
                                    frm.reload_doc();
                                    frappe.msgprint(__("Delivery Notes created and emails sent successfully!"));
                                    
                                }
                            }
                        });
                    },
                });

                dialog.show();

            });
        }
    }
});