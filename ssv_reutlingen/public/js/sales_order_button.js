frappe.ui.form.on('Sales Order', {
    refresh: function(frm) {
        
        const has_valid_items = frm.doc.items.some(item => item.item_code);
        if (has_valid_items) {
            frm.add_custom_button(__('Create Delivery Notes and Send Emails'), function() {


                frappe.call({
                    method: "ssv_reutlingen.events.custom_sales_order.create_delivery_notes",
                    args: {
                        sales_order: frm.doc.name  // Pass the Sales Order name
                    },
                    callback: function(response) {
                        if (response.message) {
                            // Show a success message with the created Delivery Notes
                            frappe.msgprint(__('Delivery Notes created successfully.'));
                            // frappe.msgprint({
                            //     title: __('Success'),
                            //     message: __('Delivery Notes created: {0}', [response.message.join(', ')]),
                            //     indicator: 'green'
                            // });
                        }
                    }
                });

                
                // if (frm.cscript && frm.cscript.make_delivery_note_based_on_delivery_date) {
                //     frm.cscript.make_delivery_note_based_on_delivery_date();
                // } else {
                //     frappe.msgprint(__('The required function is not available.'));
                // }

                // if (frm.cscript && frm.cscript.make_delivery_note) {
                //     frm.cscript.make_delivery_note(['2024-12-18']);
                // } else {
                //     frappe.msgprint(__('The required function is not available.'));
                // }

                // let delivery_dates = ['2024-12-18']

                // frappe.call({

                //     method: "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
                //     frm: frm,
                //     args: {
                //         source_name: frm.doc.name,
                //         delivery_dates: delivery_dates
                //     },
                //     // method: "your_app.your_module.sales_order.create_delivery_notes_and_emails",
                //     // args: {
                //     //     sales_order: frm.doc.name
                //     // },
                //     callback: function(r) {
                //         if (r.message) {
                //             console.log(r.message)
                //             let delivery_note = frappe.model.sync(response.message)[0];
                            
                //             frappe.call({
                //                 method: "frappe.desk.form.save.savedocs",
                //                 args: {
                //                     doc: delivery_note
                //                 },
                //                 callback: function(save_response) {
                //                     if (!save_response.exc) {
                //                         frappe.msgprint(__("Document saved successfully!"));
                //                     }
                //                 }
                //             });

                //             // frappe.msgprint(__('Delivery Note created successfully'));
                //         }
                //         // if (!r.exc) {
                //         //     frappe.msgprint(__('Delivery Notes and Emails processed successfully'));
                //         // }
                //     }
                // });
            });
        }
    }
});
