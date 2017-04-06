# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class PaymentOrder(models.Model):
    _inherit = "payment.order"

    @api.multi
    @api.depends(
        "line_ids.amount_currency",
        "line_ids.tax_line.amount"
    )
    def _compute_amount(self):
        for payment in self:
            amount_untaxed = 0
            amount_tax = 0
            amount_untaxed =\
                sum(line.amount_currency for line in payment.line_ids)
            for line in payment.line_ids:
                amount_tax += sum(tax.amount for tax in line.tax_line)
            payment.total = amount_untaxed + amount_tax

    total = fields.Float(
        string='Total',
        digits=dp.get_precision('Account'),
        store=True,
        readonly=True,
        compute='_compute_amount'
    )
