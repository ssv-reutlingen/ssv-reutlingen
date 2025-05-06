frappe.ui.form.on('Quotation', {
	refresh: function(frm) {
        const has_valid_items = frm.doc.items ? frm.doc.items.some(item => item.item_code) : false;

        if (!frm.doc.sponsoring) {
            if (has_valid_items) {
                frm.add_custom_button(
                    __('Sponsoring'), 
                    () => frm.events.make_sponsoring(frm),
                    __('Create'));

                // override the plus icon after sale order reference 
                const button = document.querySelector('button.btn-secondary[data-doctype="Sponsoring"]');
                if (button) {
                    button.replaceWith(button.cloneNode(true));
                    const newButton = document.querySelector('button.btn-secondary[data-doctype="Sponsoring"]');
                    newButton.addEventListener('click',
                        () => frm.events.make_sponsoring(frm)
                    );
                }
            }
        }
        else {
            const button = document.querySelector('button.btn-secondary[data-doctype="Sponsoring"]');
            if (button) {
                button.remove()
            }
        }
	},

    make_sponsoring: function(frm) {
        frappe.model.open_mapped_doc({
            method: 'ssv_reutlingen.api.custom_quotation.make_sponsoring',
            frm: frm
        });
    },
});