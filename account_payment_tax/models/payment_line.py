# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentLine(models.Model):
    _inherit = "payment.line"

    @api.multi
    @api.depends(
        "tax_ids",
        "amount_currency",
        "partner_id",
        "currency"
    )
    def _compute_amount(self):
        self.ensure_one()
        taxes = []
        taxes_total = 0.0
        total = 0.0
        for rec in self:
            rec.amount_tax_currency = 0.0
            rec.amount_total_currency = 0.0
            if rec.tax_ids:
                price = rec.amount_currency
                for tax in rec.tax_ids:
                    taxes = tax.compute_all(
                        price_unit=price,
                        quantity=1.0,
                        partner=rec.partner_id)
                    taxes_total += taxes['total']
                    for c in taxes['taxes']:
                        total += c.get('amount', 0.0)

            curr = rec.currency
            rec.amount_tax_currency =\
                curr.round(taxes_total)
            rec.amount_total_currency = taxes_total + total

    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name='account.tax',
        relation='payment_line_tax_rel',
        column1='line_id',
        column2='tax_id'
    )

    amount_tax_currency = fields.Float(
        string="Amount Untaxed",
        store=False,
        compute='_compute_amount'
    )

    amount_total_currency = fields.Float(
        string="Total",
        store=False,
        compute='_compute_amount'
    )
