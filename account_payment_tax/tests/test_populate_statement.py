# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import datetime

from openerp.tests.common import TransactionCase


class TestPopulateStatement(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestPopulateStatement, self).setUp(*args, **kwargs)
        # Objects
        self.obj_payment_order = self.env["payment.order"]
        self.obj_account_invoice = self.env["account.invoice"]
        self.obj_account_invoice_line = self.env["account.invoice.line"]
        self.obj_bank_statement = self.env["account.bank.statement"]
        self.obj_account_tax = self.env["account.tax"]
        self.wiz = self.env["account.payment.populate.statement"]
        self.obj_create_payment = self.env["payment.order.create"]
        self.obj_res_user = self.env["res.users"]

        # Data
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.product = self.env.ref("product.product_product_4")
        self.account = self.env.ref("account.a_recv")
        self.mode = self.env.ref("account_payment.payment_mode_1")
        self.partner = self.env.ref("base.res_partner_1")
        self.curr = self.env.ref("base.IDR")
        self.journal = self.env.ref("account.bank_journal")
        self.invoice = self._create_invoice()
        self.tax = self._create_tax()
        self.payment_order = self._create_payment_order()

    def _create_invoice(self):
        vals = {
            "partner_id": self.partner.id,
            "reference_type": "none",
            "currency_id": self.curr.id,
            "name": "invoice to client",
            "account_id": self.account.id,
            "type": "out_invoice",
            "date_invoice": self.date,
            "date_due": self.date,
        }
        invoice_id = self.obj_account_invoice.create(vals)

        lines = {
            "product_id": self.product.id,
            "quantity": 1,
            "price_unit": 50000,
            "invoice_id": invoice_id.id,
            "name": "Test Invoice",
        }
        self.obj_account_invoice_line.create(lines)

        return invoice_id

    def _create_tax(self):
        tax_id = self.obj_account_tax.create(
            dict(
                name="Percent tax",
                type="percent",
                amount="0.1",
            )
        )
        return tax_id

    def _create_payment_order(self):
        vals = {
            "reference": "Test Payment",
            "mode": self.mode.id,
            "date_prefered": "now",
        }

        order_id = self.obj_payment_order.create(vals)
        return order_id

    def test_populate_statement_1(self):
        company = self.env.user.company_id
        company.write({"currency_id": self.curr.id})

        self.invoice.signal_workflow("invoice_open")
        move_line = self.invoice.move_id.line_id[0]

        create_payment = self.obj_create_payment.with_context(
            active_model="payment.order", active_id=self.payment_order.id
        )
        create_payment.create({"entries": [(6, 0, [move_line.id])]}).create_payment()

        vals = {
            "name": "Test Statement",
            "journal_id": self.journal.id,
            "date": self.date,
            "balance_end_real": 0.0,
            "balance_start": 0.0,
            "currency": self.curr.id,
        }
        bank_stmt = self.obj_bank_statement.create(vals)

        line = self.payment_order.line_ids[0]

        wiz = self.wiz.with_context(active_id=bank_stmt.id)
        wiz.create({"lines": []}).populate_statement()

        self.assertFalse(bank_stmt.line_ids.id)

        wiz = self.wiz.with_context(active_id=bank_stmt.id)
        wiz.create({"lines": [(6, 0, [line.id])]}).populate_statement()

        self.assertEqual(-line.amount_currency, bank_stmt.line_ids.amount)

    def test_populate_statement_2(self):
        company = self.env.user.company_id
        company.write({"currency_id": self.curr.id})

        self.invoice.signal_workflow("invoice_open")
        move_line = self.invoice.move_id.line_id[0]

        create_payment = self.obj_create_payment.with_context(
            active_model="payment.order", active_id=self.payment_order.id
        )
        create_payment.create({"entries": [(6, 0, [move_line.id])]}).create_payment()

        vals = {
            "name": "Test Statement",
            "journal_id": self.journal.id,
            "date": self.date,
            "balance_end_real": 0.0,
            "balance_start": 0.0,
            "currency": self.curr.id,
        }
        bank_stmt = self.obj_bank_statement.create(vals)

        line = self.payment_order.line_ids[0]
        line.tax_ids = [(6, 0, [self.tax.id])]

        wiz = self.wiz.with_context(active_id=bank_stmt.id)
        wiz.create({"lines": []}).populate_statement()

        self.assertFalse(bank_stmt.line_ids.id)

        wiz = self.wiz.with_context(active_id=bank_stmt.id)
        wiz.create({"lines": [(6, 0, [line.id])]}).populate_statement()

        self.assertEqual(-line.amount_total_currency, bank_stmt.line_ids.amount)
