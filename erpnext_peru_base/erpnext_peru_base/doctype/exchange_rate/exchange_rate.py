# Copyright (c) 2013, dsdf and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.celery_app import celery_task, task_logger


class ExchangeRate(Document):
    pass
