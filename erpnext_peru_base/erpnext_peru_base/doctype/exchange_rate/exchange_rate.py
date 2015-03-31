# Copyright (c) 2013, dsdf and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

from frappe.celery_app import celery_task, task_logger


class ExchangeRate(Document):
    pass


@celery_task()
def fill_rate(site, exchangerate, event):
    # hack! pass event="bulk_long" to queue in longjob queue
    try:
        frappe.connect(site=site)
        doc = frappe.get_doc("Exchange Rate", exchangerate)
        doc.send_bulk()

    except:
        frappe.db.rollback()
        task_logger.warn(frappe.get_traceback())

        # wasn't able to send emails :(
        doc.db_set("email_sent", 0)
        frappe.db.commit()

        raise

    else:
        frappe.db.commit()

    finally:
        frappe.destroy()
