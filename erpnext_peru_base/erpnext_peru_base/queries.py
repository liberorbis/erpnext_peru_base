# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.widgets.reportview import get_match_cond
from frappe.model.db_query import DatabaseQuery

def get_document_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('user'):
		cond = '(`tabSerial Control`.user = "' + filters['user'] + '" or `tabSerial Control`.user IS NULL) and'
	if filters.get('table'):
		cond += '(`tabElement Table`.parent = "' + filters['table'] + '" ) and'
	if filters.get('document'):
		cond += '(`tabSerial Control`.doc_type = "' + filters['document'] + '" ) and'

	return frappe.db.sql("""select `tabElement Table`.name from `tabSerial Control` inner join `tabElement Table`
		on `tabElement Table`.name = `tabSerial Control`.document_type
		where `tabSerial Control`.active = 1
			and %(cond)s `tabSerial Control`.name like "%(txt)s" %(mcond)s
		order by `tabElement Table`.name asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'mcond':get_match_cond(doctype),'start': start, 'page_len': page_len})

def get_serie_nr(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('user'):
		cond = '(`tabSerial Control`.user = "' + filters['user'] + '" or `tabSerial Control`.user IS NULL) and'
	if filters.get('document'):
		cond += '(`tabSerial Control`.doc_type = "' + filters['document'] + '" ) and'

	return frappe.db.sql("""select `tabSerial Control`.serie_nr from `tabSerial Control`
		where `tabSerial Control`.active = 1
		limit 1 """ )

def get_location(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('department'):
		cond = '`tabAddress Province`.department = "' + filters['department'] + '"  '
	aa = """select `tabAddress Province`.name from `tabAddress Province`
		where `tabAddress Province`.description like "%(txt)s and %(cond)s "
		order by `tabAddress Province`.description asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'start': start, 'page_len': page_len}
	print aa
	return frappe.db.sql(aa)


