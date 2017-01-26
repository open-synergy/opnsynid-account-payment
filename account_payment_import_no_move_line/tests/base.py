# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase
from datetime import datetime


class BaseTest(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(BaseTest, self).setUp(*args, **kwargs)
        # Objects
        self.obj_account_invoice = self.env['account.invoice']
        self.obj_account_invoice_line = self.env['account.invoice.line']
        self.obj_bank_statement = self.env['account.bank.statement']
        self.obj_payment_order = self.env['payment.order']
        self.obj_payment_line = self.env['payment.line']
        self.obj_payment_mode = self.env['payment.mode']
        self.wiz = self.env['account.payment.populate.statement']
        self.obj_create_payment = self.env['payment.order.create']

        # Data
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.partner = self.env.ref("base.res_partner_1")
        self.product = self.env.ref('product.product_product_5')
        self.mode = self.env.ref('account_payment.payment_mode_1')
        self.curr = self.env.ref("base.IDR")
        self.account = self.env.ref('account.a_recv')
        self.journal = self.env.ref('account.bank_journal')
        self.invoice = self._create_invoice()
        self.payment_order = self._create_payment_order()
        self.data_payment = self.env.ref('account_payment.payment_order_1')

    def _create_invoice(self):
        vals = {
            'partner_id': self.partner.id,
            'reference_type': 'none',
            'currency_id': self.curr.id,
            'name': 'invoice to client',
            'account_id': self.account.id,
            'type': 'out_invoice',
            'date_invoice': self.date,
            'date_due': self.date
        }
        invoice_id = self.obj_account_invoice.create(vals)

        lines = {
            'product_id': self.product.id,
            'quantity': 1,
            'price_unit': 50000,
            'invoice_id': invoice_id.id,
            'name': 'Test Invoice'
        }
        self.obj_account_invoice_line.create(lines)

        return invoice_id

    def _create_payment_order(self):
        vals = {
            'reference': 'Test Payment',
            'mode': self.mode.id,
            'date_prefered': 'now'
        }

        order_id = self.obj_payment_order.create(vals)
        return order_id
