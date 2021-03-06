from datetime import datetime
from dateutil.relativedelta import relativedelta
# import netsvc
import re
import logging
import frappe
import frappe.defaults
logger = logging.getLogger(__name__)

months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Setiembre', 'Octubre', 'Noviembre',
		  'Diciembre']

def get_url(url, values={}):
	"""Return a string of a get url query"""
	try:
		import urllib
		import urllib2
		from cookielib import CookieJar

		cj = CookieJar()
		erpnext = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		response = erpnext.open(url)
		rawfile = response.read()
		if values:
			data = urllib.urlencode(values)
			response = erpnext.open(url, data)
			rawfile = response.read()
		return rawfile
	except ImportError:
		raise Exception('Error: Unable to import urllib !')
	except IOError:
		raise Exception('Error: Web Service [%s] does not exist or it is non accesible !' % url)

def sunat_access_exception(Exception):
	pass


def get_sunat_rates(values={}):
	print "LLEGAAA!!!!"

	url = 'http://www.sunat.gob.pe/cl-at-ittipcam/tcS01Alias'

	data = get_url(url, values=values)
	if data:
		print "SUNAT sent a response"

	else:
		print  'Error retrieving info from SUNAT. No data retrieved from www.sunat.gob.pe - values', values
		return {}

	res_id = re.findall('<title>SUNAT - Tipo de Cambio Oficial</title>', data)
	if not (res_id and len(res_id) > 0):
		print 'Error retrieving info from SUNAT. Page data could not be recognized! - values: %s', values
		return {}

	res_id = re.findall('''<h3>(\S+) - (\d+)</h3>''', data)

	if not (res_id and len(res_id) > 0):
		print 'Error retrieving info from SUNAT. Page data could not be recognized! - values:', values

	month = res_id[0][0]
	year = int(res_id[0][1])
	today = values and datetime.strptime('%(anho)s-%(mes)s-01' % values, '%Y-%m-%d') or datetime.now()

	if (month not in months) or month != months[today.month - 1]:
		print 'Error retrieving info from SUNAT. Month is not recognized! - values: ', values
		return {}
	if year != today.year:
		print 'Error retrieving info from SUNAT. Year is not recognized! - values:', values
		return {}

	res_id = re.findall(
		'''<td width='4%' align='center' class="H3">\D+<strong>(\d+)</strong>\D+<td width='8%' align='center' class="tne10">\D+(\d+.\d+)\D+<td width='8%' align='center' class="tne10">\D+(\d+.\d+)''',
		data)

	if not (res_id and len(res_id) > 0):
		print 'Error retrieving info from SUNAT. Exchange rates not found! values:', values
		return {}

	days = {}
	for d in res_id:
		days[int(d[0])] = {
			'Sale': float(d[1]),
			'Purchase': float(d[2]),
		}
	res = {'days': days}
	day = today.day
	if day not in days:
		print 'Error retrieving info from SUNAT. Day number %s not found in data!', day
	else:
		res['current_sale_ratio'] = days[today.day]['Sale']
		res['current_purchase_ratio'] = days[today.day]['Purchase']

	val_purchase_here = res['current_purchase_ratio']
	val_sale_here = res['current_sale_ratio']
	exchange_rate_purchase = frappe.get_doc({
		"doctype": "Exchange Rate", "parent": 'USD-PEN', "parentfield": 'exchange_rates',
		"parenttype": 'Currency Exchange', 'idx': 1,
		"type": 'purchase',
		"date": '2015-03-31',
		"value": val_purchase_here
	})
	exchange_rate_purchase.ignore_permissions = True
	exchange_rate_purchase.ignore_mandatory = True
	exchange_rate_purchase.insert()
	exchange_rate_purchase.save()

	exchange_rate_sale = frappe.get_doc({
		"doctype": "Exchange Rate", "parent": 'USD-PEN', "parentfield": 'exchange_rates',
		"parenttype": 'Currency Exchange', 'idx': 1,
		"type": "sale",
		"date": '2015-03-31',
		"value": val_sale_here
	})
	exchange_rate_sale.ignore_permissions = True
	exchange_rate_sale.ignore_mandatory = True
	exchange_rate_sale.insert()
	exchange_rate_sale.save()
