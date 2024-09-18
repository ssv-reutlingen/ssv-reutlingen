// Copyright (c) 2024, phamos.eu and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sponsoring', {
	onload: function(frm) {
		if(frm.is_new()){
			// Get today's date
			const today = frappe.datetime.get_today();
			const today_date = new Date(today);
			const year = today_date.getFullYear();

			// Set the next 1st July
			const next_july = new Date(year, 6, 1);
			if (today_date > next_july) {
				next_july.setFullYear(year + 1);
			}
			frm.set_value('contract_start', next_july);
		}
	},

	contract_start: function(frm) {
		const contract_start_year = new Date(frm.doc.contract_start).getFullYear();

		// Set contract end date to 30th June of the next year
		const contract_end = new Date(contract_start_year + 1, 5, 30);
		frm.set_value('contract_end', contract_end);

		// Set the end of December
		const latest_notice_date = new Date(contract_start_year, 11, 31);
		frm.set_value('latest_notice_date', latest_notice_date);
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
