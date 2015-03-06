# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
import frappe.defaults
from frappe.utils import cint, cstr, flt
from frappe import _, msgprint, throw
from erpnext.accounts.party import get_party_account, get_due_date
from erpnext.controllers.stock_controller import update_gl_entries_after
from frappe.model.mapper import get_mapped_doc


def autoname(sales_invoice, method):
	from frappe.model.naming import make_autoname
	import frappe
	type = frappe.db.get_value("Element Table",sales_invoice.document_type, "element_code2")
	if not type:
		type=sales_invoice.document_type
	sales_invoice.name = make_autoname(type +sales_invoice.serie_nr+'-.######')
	sales_invoice.document_nr = sales_invoice.name.split("-")[1]
	#self.name = str(self.document_type) + ' - ' + str(self.document_nr)

def autoname_code(doc, method):
	doc.name = doc.code
