# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class PaymentOrder(models.Model):
    _inherit = "payment.order"

    @api.multi
    @api.depends(
        'line_ids.amount_currency',
        'tax_line.amount'
    )
    def _compute_amount(self):
        for payment in self:
            payment.amount_untaxed = sum(line.amount_currency for line in payment.line_ids)
            payment.amount_tax = sum(line.amount for line in payment.tax_line)
            payment.total = payment.amount_untaxed + payment.amount_tax

    amount_untaxed = fields.Float(
        string='Subtotal',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount',
        track_visibility='always'
    )
    amount_tax = fields.Float(
        string='Tax',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    total = fields.Float(
        string='Total',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
    tax_line = fields.One2many(
        comodel_name='payment.order.tax',
        inverse_name='payment_id',
        string='Tax Lines',
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=True
    )

    @api.multi
    def button_reset_taxes(self):
        payment_order_tax = self.env['payment.order.tax']
        for payment in self:
            self._cr.execute("DELETE FROM payment_order_tax WHERE payment_id=%s AND manual is False", (payment.id,))
            self.invalidate_cache()
            for tax in payment_order_tax.compute(payment).values():
                payment_order_tax.create(tax)
        return self.write({'line_ids': []})