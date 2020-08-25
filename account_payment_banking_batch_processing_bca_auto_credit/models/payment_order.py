# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from openerp import models, fields


class PaymentOrder(models.Model):
    _inherit = "payment.order"

    report_bca_auto_credit_ids = fields.One2many(
        string="BCA Auto-Credit",
        comodel_name="payment.report_bca_auto_credit",
        inverse_name="order_id",
        readonly=True,
    )
