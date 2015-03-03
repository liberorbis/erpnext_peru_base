# Copyright (c) 2013, LiberOrbis SAC and Contributors
# See license.txt

import frappe
import unittest

test_records = frappe.get_test_records('element_table')

class Testelement_table(unittest.TestCase):
	pass
