# Copyright (c) 2013, Web Notes Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, msgprint
from frappe.utils import flt, rounded, cint

from erpnext.setup.utils import get_company_currency
from erpnext.accounts.party import get_party_details

from erpnext.controllers.stock_controller import StockController

def determine_exclusive_rate(self):
	if not any((cint(tax.included_in_print_rate) for tax in self.tax_doclist)):
		# no inclusive tax
		return

	for item in self.item_doclist:
		item_tax_map = self._load_item_tax_rate(item.item_tax_rate)
		cumulated_tax_fraction = 0
		for i, tax in enumerate(self.tax_doclist):
			tax.tax_fraction_for_current_item = self.get_current_tax_fraction(tax, item_tax_map)

			if i==0:
				tax.grand_total_fraction_for_current_item = 1 + tax.tax_fraction_for_current_item
			else:
				tax.grand_total_fraction_for_current_item = \
					self.tax_doclist[i-1].grand_total_fraction_for_current_item \
					+ tax.tax_fraction_for_current_item

			cumulated_tax_fraction += tax.tax_fraction_for_current_item

		if cumulated_tax_fraction and not self.discount_amount_applied and item.qty:
			item.base_amount = flt((item.amount * self.conversion_rate) /
				(1 + cumulated_tax_fraction), self.precision("base_amount", item))

			item.base_rate = flt(item.base_amount / item.qty, self.precision("base_rate", item))
			item.discount_percentage = flt(item.discount_percentage, self.precision("discount_percentage", item))

			if item.discount_percentage == 100:
				item.base_price_list_rate = item.base_rate
				item.base_rate = 0.0
			else:
				item.base_price_list_rate = flt(item.base_rate / (1 - (item.discount_percentage / 100.0)),
					self.precision("base_price_list_rate", item))

def get_current_tax_fraction(self, tax, item_tax_map):
	"""
		Get tax fraction for calculating tax exclusive amount
		from tax inclusive amount
	"""
	current_tax_fraction = 0

	if cint(tax.included_in_print_rate):
		tax_rate = self._get_tax_rate(tax, item_tax_map)

		if tax.charge_type == "On Net Total":
			current_tax_fraction = tax_rate / 100.0

		elif tax.charge_type == "On Previous Row Amount":
			current_tax_fraction = (tax_rate / 100.0) * \
				self.tax_doclist[cint(tax.row_id) - 1].tax_fraction_for_current_item

		elif tax.charge_type == "On Previous Row Total":
			current_tax_fraction = (tax_rate / 100.0) * \
				self.tax_doclist[cint(tax.row_id) - 1].grand_total_fraction_for_current_item

	return current_tax_fraction
