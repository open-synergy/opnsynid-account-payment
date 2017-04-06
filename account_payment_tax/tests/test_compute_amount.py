# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp.tests.common import TransactionCase


class TestComputeAmount(TransactionCase):
    def setUp(self, *args, **kwargs):
        super(TestComputeAmount, self).setUp(*args, **kwargs)
        # Objects
        self.obj_payment_order = self.env['payment.order']
        self.obj_payment_line = self.env['payment.line']
        self.obj_order_tax = self.env['payment.order.tax']
        self.obj_account_tax = self.env['account.tax']

        # Data
        self.partner = self.env.ref("base.res_partner_1")
        self.partner_2 = self.env.ref("base.res_partner_2")
        self.partner_3 = self.env.ref("base.res_partner_3")
        self.curr = self.env.ref("base.IDR")
        self.mode = self.env.ref('account_payment.payment_mode_1')
        self.acc_1 = self.env.ref('account.conf_ova')
        self.acc_2 = self.env.ref('account.conf_iva')
        self.tax_positive_1 = self._create_tax_positive_1()
        self.tax_positive_2 = self._create_tax_positive_2()
        self.tax_negative_1 = self._create_tax_negative_1()
        self.tax_negative_2 = self._create_tax_negative_2()
        self.tax_without_acc_1 = self._create_tax_without_acc_1()
        self.tax_without_acc_2 = self._create_tax_without_acc_2()

    def _create_tax_without_acc_1(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(No Acc)Percent tax - 1",
            type='percent',
            amount='0.1'
        ))

        return tax_id

    def _create_tax_without_acc_2(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(No Acc)Percent tax - 2",
            type='percent',
            amount='0.2'
        ))

        return tax_id

    def _create_tax_positive_1(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Positive)Percent tax - 1",
            type='percent',
            amount='0.1',
            account_collected_id=self.acc_1.id
        ))

        return tax_id

    def _create_tax_positive_2(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Positive)Percent tax - 2",
            type='percent',
            amount='0.2',
            account_collected_id=self.acc_2.id
        ))

        return tax_id

    def _create_tax_negative_1(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Negative)Percent tax - 1",
            type='percent',
            amount='-0.3',
            account_collected_id=self.acc_1.id
        ))

        return tax_id

    def _create_tax_negative_2(self):
        tax_id = self.obj_account_tax.create(dict(
            name="(Negative)Percent tax - 2",
            type='percent',
            amount='-0.4',
            account_collected_id=self.acc_2.id
        ))

        return tax_id

    def test_compute_case(self):
        payment_order = self.obj_payment_order.create({
            'reference': 'Test Payment',
            'mode': self.mode.id,
            'date_prefered': 'now'
        })

        # Create Payment Line 1
        payment_line_1 = self.obj_payment_line.create({
            'order_id': payment_order.id,
            'partner_id': self.partner.id,
            'currency': self.curr.id,
            'amount_currency': 500000,
            'tax_ids': [(
                6, 0, [
                    self.tax_positive_1.id,
                    self.tax_positive_2.id
                ]
            )],
            'communication': '-'
        })

        payment_line_1.button_reset_taxes()

        # Check Amount Tax
        self.assertEqual(150000, payment_line_1.amount_tax_currency)

        # Check Amount Total
        self.assertEqual(650000, payment_line_1.amount_total_currency)

        # Check Tax
        criteria_1 = [
            ('payment_line_id', '=', payment_line_1.id),
            ('account_id', '=', self.acc_1.id)
        ]
        tax_1 = self.obj_order_tax.search(criteria_1)
        self.assertEqual(50000, tax_1.amount)

        criteria_2 = [
            ('payment_line_id', '=', payment_line_1.id),
            ('account_id', '=', self.acc_2.id)
        ]
        tax_2 = self.obj_order_tax.search(criteria_2)
        self.assertEqual(100000, tax_2.amount)

        # Create Payment Line 2
        payment_line_2 = self.obj_payment_line.create({
            'order_id': payment_order.id,
            'partner_id': self.partner_2.id,
            'currency': self.curr.id,
            'amount_currency': 750000,
            'tax_ids': [(
                6, 0, [
                    self.tax_negative_1.id,
                    self.tax_negative_2.id
                ]
            )],
            'communication': '-'
        })

        payment_line_2.button_reset_taxes()

        # Check Amount Tax
        self.assertEqual(-525000, payment_line_2.amount_tax_currency)

        # Check Amount Total
        self.assertEqual(225000, payment_line_2.amount_total_currency)

        # Check Tax
        criteria_3 = [
            ('payment_line_id', '=', payment_line_2.id),
            ('account_id', '=', self.acc_1.id)
        ]
        tax_3 = self.obj_order_tax.search(criteria_3)
        self.assertEqual(-225000, tax_3.amount)

        criteria_4 = [
            ('payment_line_id', '=', payment_line_2.id),
            ('account_id', '=', self.acc_2.id)
        ]
        tax_4 = self.obj_order_tax.search(criteria_4)
        self.assertEqual(-300000, tax_4.amount)

        # Create Payment Line 3
        payment_line_3 = self.obj_payment_line.create({
            'order_id': payment_order.id,
            'partner_id': self.partner_3.id,
            'currency': self.curr.id,
            'amount_currency': 350000,
            'tax_ids': [(
                6, 0, [
                    self.tax_without_acc_1.id,
                    self.tax_without_acc_2.id
                ]
            )],
            'communication': '-'
        })

        payment_line_3.button_reset_taxes()

        # Check Amount Tax
        self.assertEqual(105000, payment_line_3.amount_tax_currency)

        # Check Amount Total
        self.assertEqual(455000, payment_line_3.amount_total_currency)

        # Check Tax
        criteria_5 = [
            ('payment_line_id', '=', payment_line_3.id)
        ]
        tax_5 = self.obj_order_tax.search(criteria_5)
        self.assertEqual(105000, tax_5.amount)

        # Check Factor Base
        self.assertEqual(
            (tax_5.base_amount/tax_5.base),
            tax_5.factor_base
        )

        # Check Factor Tax
        self.assertEqual(
            (tax_5.tax_amount/tax_5.amount),
            tax_5.factor_tax
        )

        # Check Factor Tax
        self.assertEqual(
            (tax_5.tax_amount/tax_5.amount),
            tax_5.factor_tax
        )

        # Check Total Payment Order
        self.assertEqual(1330000, payment_order.total)
