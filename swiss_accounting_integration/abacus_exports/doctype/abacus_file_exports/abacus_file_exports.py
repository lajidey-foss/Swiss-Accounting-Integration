# -*- coding: utf-8 -*-
# Copyright (c) 2021, Grynn and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
# import frappe
from frappe.model.document import Document


class AbacusFileExports(Document):
    def submitd(self):
        '''
        On Submit Hook
        Check out 
        https://frappeframework.com/docs/user/en/basics/doctypes/controllers#controller-hooks
        '''
        self.get_transactions()
        return

    def get_transactions(self):
        """
        What are Transactions ?

        - Sales Invoice
        - Purchase Invoice
        - Payment Entry
        - Journal Entry
        """
        # Get Sales Invoice
        sales_invoices = frappe.db.get_list('Sales Invoice',
                                            filters={
                                                'posting_date': self.start_date,
                                                'posting_date': self.end_date,
                                                'docstatus': 1,
                                                'exported_to_abacus': 0,
                                                'company': self.Company

                                            })

        # Get Purchase Invoice
        purchase_invoice = frappe.db.get_list('Purchase Invoice',
                                              filters={
                                                  'posting_date': self.start_date,
                                                  'posting_date': self.end_date,
                                                  'docstatus': 1,
                                                  'exported_to_abacus': 0,
                                                  'company': self.Company
                                              })
        # Get Payment Entry
        payment_entry = frappe.db.get_list('Payment Entry',
                                           filters={
                                               'posting_date': self.start_date,
                                               'posting_date': self.end_date,
                                               'docstatus': 1,
                                               'exported_to_abacus': 0,
                                               'company': self.Company
                                           })
        # Get Journal Entry
        journal_entry = frappe.db.get_list('Journal Entry',
                                           filters={
                                               'posting_date': self.start_date,
                                               'posting_date': self.end_date,
                                               'docstatus': 1,
                                               'exported_to_abacus': 0,
                                               'company': self.Company
                                           })

        # Combining Entry
        docs = sales_invoices + purchase_invoice + payment_entry + journal_entry

        # clear all children
        self.references = []

        # add to child table
        for doc in docs:
            self.append('references', {'dt': doc['dt'], 'dn': doc['dn']})
        self.save()

        # mark as exported
        sinvs = self.get_docs(docs, "Sales Invoice")
        pinvs = self.get_docs(docs, "Purchase Invoice")
        pes = self.get_docs(docs, "Payment Entry")
        jvs = self.get_docs(docs, "Journal Entry")

        # Aggregated
        all_docs = sinvs + pinvs + pes + jvs

        # TODO
        # Update
        all_docs['exported_to_abacus'] = 1

        # TODO: implement Save
        # Save
        all_docs.save()

    def get_docs_d(self, references, dt):
        """
        Getting Docs Where
            dt == 'Sales Invoice'
        """
        docs = []
        for d in references:
            if d['dt'] == dt:
                docs.append(d['dn'])
        return docs

    def reset_export_flags_d(self):
        """
        Reset Flags to exported_to_abacus = 0
        Used From Frontend As a Service
        """
        sinvs = frappe.db.get_list('Sales Invoice')
        purchase_invoice = frappe.db.get_list('Sales Invoice')
        payment_entry = frappe.db.get_list('Payment Invoice')
        journal_entry = frappe.db.get_list('Journal Invoice')

        # Updating
        docs = sinvs + purchase_invoice + payment_entry + journal_entry

        docs.update({
            'exported_to_abacus': 0
        })
        pass
