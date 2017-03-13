# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputeAmount(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputeAmount, self).setUp(*args, **kwargs)
        # Objects
        self.obj_payment_line = self.env['payment.line']
        self.obj_account_tax = self.env['account.tax']

        # Data
        self.partner = self.env.ref("base.res_partner_1")
        self.curr = self.env.ref("base.IDR")
        self.tax_positive = self._create_tax_positive()
        self.tax_negative = self._create_tax_negative()

    def _create_tax_positive(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Positive)Percent tax",
            type='percent',
            amount='0.1',
        ))

        return tax_id

    def _create_tax_negative(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Negative)Percent tax",
            type='percent',
            amount='-0.1',
        ))

        return tax_id

    def test_compute_case_1(self):
        new = self.obj_payment_line.new()
        new.tax_ids = [(
            6, 0, [
                self.tax_positive.id
            ]
        )]
        new.partner_id = self.partner.id
        new.currency = self.curr.id
        new.amount_currency = 500000

        self.assertEqual(50000, new.amount_tax_currency)

        self.assertEqual(550000, new.amount_total_currency)

    def test_compute_case_2(self):
        new = self.obj_payment_line.new()
        tax_id = self.obj_account_tax.create(dict(
            name="Percent tax include price",
            type='percent',
            amount='0.1',
            price_include=True
        ))

        new.tax_ids = [(6, 0, [tax_id.id])]
        new.partner_id = self.partner.id
        new.currency = self.curr.id
        new.amount_currency = 50000

        self.assertEqual(4545.45, new.amount_tax_currency)

        self.assertEqual(50000, new.amount_total_currency)

    def test_compute_case_3(self):
        new = self.obj_payment_line.new()
        new.tax_ids = [(
            6, 0, [
                self.tax_negative.id
            ]
        )]
        new.partner_id = self.partner.id
        new.currency = self.curr.id
        new.amount_currency = 500000

        self.assertEqual(-50000, new.amount_tax_currency)

        self.assertEqual(450000, new.amount_total_currency)

    def test_compute_case_4(self):
        new = self.obj_payment_line.new()
        tax_id = self.obj_account_tax.create(dict(
            name="Percent tax include price",
            type='percent',
            amount='-0.1',
            price_include=True
        ))

        new.tax_ids = [(6, 0, [tax_id.id])]
        new.partner_id = self.partner.id
        new.currency = self.curr.id
        new.amount_currency = 50000

        self.assertEqual(-5555.56, new.amount_tax_currency)

        self.assertEqual(50000, new.amount_total_currency)

    def test_compute_case_5(self):
        new = self.obj_payment_line.new()
        new.tax_ids = [(
            6, 0, [
                self.tax_positive.id,
                self.tax_negative.id
            ]
        )]
        new.partner_id = self.partner.id
        new.currency = self.curr.id
        new.amount_currency = 100000

        self.assertEqual(0, new.amount_tax_currency)

        self.assertEqual(100000, new.amount_total_currency)
