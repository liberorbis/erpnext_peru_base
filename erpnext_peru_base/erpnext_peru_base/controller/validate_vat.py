# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import frappe
import logging
import string
import datetime
import re
import json

from frappe import _
from frappe.model.document import Document

_logger = logging.getLogger(frappe.__name__)

#called father function to validate various numbers of documents by type
@frappe.whitelist(allow_guest=True)
def validate_vat_customer(doc, method):
    ret=True
    if isinstance(doc, basestring):
        doc = json.loads(doc)
    doc_number = doc.get('doc_number')
    type_document=doc.get('type_document')
    if type_document=='RUC':
        check_duple_vat(doc)
        if not check_vat_pe(doc_number):
            frappe.throw(_("RUC: {nif} invalid, please review...").format(doc_number=doc_number),frappe.DataError)
    if type_document=='DNI':
        check_duple_vat(doc)
        check_dni_pe(doc_number)
#called father function to validate various numbers of documents by type

@frappe.whitelist(allow_guest=True)
def validate_vat_supplier(doc, method):
    ret=True
    if isinstance(doc, basestring):
        doc = json.loads(doc)
    doc_number = doc.get('doc_number')
    type_document=doc.get('type_document')
    if type_document=='RUC':
        check_duple_vat_supplier(doc)
        if not check_vat_pe(doc_number):
            frappe.throw(_("RUC: {nif} invalid, please review...").format(doc_number=doc_number),frappe.DataError)
    if type_document=='DNI':
        check_duple_vat_supplier(doc)
        check_dni_pe(doc_number)
 #   after_install()
    return ret
#validate number RUC peruvian
def check_vat_pe(nif):
    nif = str(nif)
    if not nif.isdigit():
       frappe.throw(_("Number document: {nif} , only numbers").format(nif=nif),frappe.DataError)
       return False
    if len (nif) <> 11:
        frappe.throw(_("Number document: {nif},  11 dígits, please review...").format(nif=nif),frappe.DataError)
        return  False
    control = str(5432765432)
    n = 0
    for i, j in enumerate(nif[:-1]):
        n += int(control[i]) * int(j)
    r = 11 - n%11
    if r == 11:
        n = 1
    elif r == 10:
       n = 0
    else:
       n = r
    return n == int(nif[-1])

#validate number RUC peruvian
def check_dni_pe(dni):
    dni = str(dni)
    band=True
    if not dni.isdigit():
       frappe.throw(_("Number document: {dni} , only numbers").format(dni=dni),frappe.DataError)
       return False
    if len (dni) <> 8:
        frappe.throw(_("Number document: {dni},  8 dígits, please review...").format(dni=dni),frappe.DataError)
        return  False
    return band

#check duplicate number_doc
def check_duple_vat(doc):

    name_self= doc.get('name')
    nif = doc.get('doc_number')
    if not nif:#is possible nif to be null
        return

    _logger.info("doc is {0}".format(doc))

    customer = frappe.db.sql("""select customer_name, name from `tabCustomer` where (doc_number = %s) and (name <> %s)""" , (nif,name_self),as_dict=True)#only one must exist
    _logger.info("cursor for customer_name is {0}".format(customer))
    customer_name = customer[0].get('customer_name') if len(customer) > 0 else None
    cname = doc.get("customer_name")
    if(customer_name and customer_name == cname and name_self):#nif already exist but is for the same customer
        return
    elif(customer_name):#nif already exists but another customer already has it
        frappe.throw(_("Number {nif} exist in {name}").format(nif=nif, name=customer_name),frappe.DataError)
    else:#no customer exist with this nif. Save it
        return

def check_duple_vat_supplier(doc):

    name_self= doc.get('name')
    nif = doc.get('doc_number')
    if not nif:
        return

    _logger.info("doc is {0}".format(doc))

    supplier = frappe.db.sql("""select supplier_name, name from `tabSupplier` where (doc_number = %s) and (name <> %s)""" , (nif,name_self),as_dict=True)
    _logger.info("cursor for supplier_name is {0}".format(supplier))
    supplier_name = supplier[0].get('supplier_name') if len(supplier) > 0 else None
    cname = doc.get("supplier_name")
    if(supplier_name and supplier_name == cname and name_self):
        return
    elif(supplier_name):
        frappe.throw(_("Number Document {nif} exist in {name}").format(nif=nif, name=supplier_name),frappe.DataError)
    else:#no customer exist with this nif. Save it
        return
