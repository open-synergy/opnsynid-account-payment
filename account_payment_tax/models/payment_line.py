# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api

class PaymentLine(models.Model):
    _inherit = "payment.line"

    payment_line_tax_id = fields.Many2many(
        comodel_name='account.tax',
        relation='payment_order_line_tax_rel',
        column1='payment_line_id',
        column2='tax_id',
        string='Taxes',
        domain=[('parent_id', '=', False)]
    )
