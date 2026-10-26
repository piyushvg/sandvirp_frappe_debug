// Copyright (c) 2026, Sandvirp and contributors
// For license information, please see license.txt

frappe.ui.form.on("API Failure Log", {
	refresh(frm) {
		frm.add_custom_button(__("Copy Export JSON"), () => {
			frappe
				.call("sandvirp_debug.api_failure_log.export", { name: frm.doc.name })
				.then((r) => frappe.utils.copy_to_clipboard(JSON.stringify(r.message, null, 1)));
		});
		frm.add_custom_button(__("Copy as cURL"), () => {
			frappe
				.call("sandvirp_debug.api_failure_log.as_curl", { name: frm.doc.name })
				.then((r) => frappe.utils.copy_to_clipboard(r.message));
		});
	},
});
