# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.widgets.reportview import get_match_cond
from frappe.model.db_query import DatabaseQuery

def get_document_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('user'):
		cond = '(`tabSerial Control`.user = "' + filters['user'] + '" ) and'
	if filters.get('table'):
		cond += '(`tabElement Table`.parent = "' + filters['table'] + '" ) and'
	if filters.get('document'):
		cond += '(`tabSerial Control`.doc_type = "' + filters['document'] + '" ) and'

	return frappe.db.sql("""select `tabElement Table`.name from `tabSerial Control` inner join `tabElement Table`
		on `tabElement Table`.name = `tabSerial Control`.document_type
		where `tabSerial Control`.active = 1
			and %(cond)s `tabSerial Control`.name like "%(txt)s" %(mcond)s
		order by `tabSerial Control`.name asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'mcond':get_match_cond(doctype),'start': start, 'page_len': page_len})

