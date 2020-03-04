# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentLine(models.Model):
    _inherit = "payment.line"

    @api.multi
    @api.depends(
        "amount_currency",
        "tax_line.amount"
    )
    def _compute_amount(self):
        for rec in self:
            rec.amount_tax_currency = sum(line.amount for line in rec.tax_line)
            rec.amount_total_currency =\
                rec.amount_currency + rec.amount_tax_currency

    amount_tax_currency = fields.Float(
        string="Amount Tax",
        store=False,
        compute='_compute_amount'
    )

    amount_total_currency = fields.Float(
        string="Amount Total",
        store=False,
        compute='_compute_amount'
    )

    tax_ids = fields.Many2many(
        string="Taxes",
        comodel_name='account.tax',
        relation='payment_line_tax_rel',
        column1='line_id',
        column2='tax_id'
    )

    tax_line = fields.One2many(
        comodel_name='payment.order.tax',
        inverse_name='payment_line_id',
        string='Tax Lines',
        readonly=True,
        copy=True
    )

    @api.multi
    def button_reset_taxes(self):
        payment_order_tax = self.env['payment.order.tax']
        for rec in self:
            self._cr.execute(
                "DELETE FROM payment_order_tax "
                "WHERE payment_line_id=%s AND manual is False", (rec.id,)
            )
            self.invalidate_cache()
            for tax in payment_order_tax.compute(rec).values():
                payment_order_tax.create(tax)
        return True
