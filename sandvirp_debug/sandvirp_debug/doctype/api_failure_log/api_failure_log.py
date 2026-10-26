# Copyright (c) 2026, Sandvirp and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.query_builder import Interval
from frappe.query_builder.functions import Now


class APIFailureLog(Document):
	def onload(self):
		if not self.error_log:
			from sandvirp_debug.api_failure_log import find_error_log

			if error_log := find_error_log(self):
				self.db_set("error_log", error_log, update_modified=False)

	@staticmethod
	def clear_old_logs(days=30):
		table = frappe.qb.DocType("API Failure Log")
		frappe.db.delete(table, filters=(table.creation < (Now() - Interval(days=days))))
