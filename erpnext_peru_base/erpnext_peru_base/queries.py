# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.widgets.reportview import get_match_cond
from frappe.model.db_query import DatabaseQuery

def get_document_type(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('user'):
		cond = '(`tabSerial Control`.user = "' + filters['user'] + '" or `tabSerial Control`.user ="" or `tabSerial Control`.user IS NULL) and'
	if filters.get('table'):
		cond += '(`tabElement Table`.parent = "' + filters['table'] + '" ) and'
	if filters.get('document'):
		cond += '(`tabSerial Control`.doc_type = "' + filters['document'] + '" ) and'

	return frappe.db.sql("""select `tabElement Table`.name from `tabSerial Control` inner join `tabElement Table`
		on `tabElement Table`.name = `tabSerial Control`.document_type
		where `tabSerial Control`.active = 1
			and %(cond)s (`tabElement Table`.name like "%(txt)s" or `tabElement Table`.description like "%(txt)s") %(mcond)s
		order by `tabElement Table`.name asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'mcond':get_match_cond(doctype),'start': start, 'page_len': page_len})

def get_document_type_basic(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('table'):
		cond += '(ET.parent = "' + filters['table'] + '" ) '

	return frappe.db.sql("""select ET.name, ET.description, ET.element_code from `tabElement Table` as ET
			where ET.active = 1 and (ET.name like "%(txt)s" or ET.description like "%(txt)s" or ET.element_code like "%(txt)s")
		and %(cond)s  order by ET.name asc
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

def get_province(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('department'):
		cond = 'and `tabAddress Province`.department = "' + filters['department'] + '"  '
	return frappe.db.sql("""select `tabAddress Province`.name, `tabAddress Province`.description from `tabAddress Province`
		where (`tabAddress Province`.description like "%(txt)s"  or
		`tabAddress Province`.name like "%(txt)s" ) %(cond)s
		order by `tabAddress Province`.description asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'start': start, 'page_len': page_len} )

def get_district(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('province'):
		cond = 'and `tabAddress District`.parent = "' + filters['province'] + '"  '
	return frappe.db.sql("""select `tabAddress District`.name, `tabAddress District`.description from `tabAddress District`
		where (`tabAddress District`.description like "%(txt)s" or `tabAddress District`.name like "%(txt)s")
		 %(cond)s order by `tabAddress District`.description asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'start': start, 'page_len': page_len} )

def get_purchase_invoice(doctype, txt, searchfield, start, page_len, filters):
	cond = ''
	if filters.get('supplier'):
		cond = '(pinv.supplier = "' + filters['supplier'] + '" ) and'
	if filters.get('documentdiff'):
		cond += '(pinv.document_type <> "' + filters['documentdiff'] + '" ) and'

	return frappe.db.sql("""select pinv.name, pinv.bill_no, pinv.posting_date,pinv.supplier,pinv.grand_total_import
		from `tabPurchase Invoice` as pinv
		where pinv.docstatus = 1
			and %(cond)s (pinv.name like "%(txt)s" or pinv.bill_no like "%(txt)s") %(mcond)s
		order by pinv.name asc
		limit %(start)s, %(page_len)s """ % {'cond': cond,'txt': "%%%s%%" % txt,
		'mcond':get_match_cond(doctype),'start': start, 'page_len': page_len})

