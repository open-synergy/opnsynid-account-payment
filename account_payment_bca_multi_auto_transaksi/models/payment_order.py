# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PaymentOrder(models.Model):
    _name = "payment.order"
    _inherit = "payment.order"

    bca_multi_auto_transfer_ids = fields.One2many(
        string="BCA Multi Auto Transfer",
        comodel_name="payment.report_bca_multi_auto_transfer",
        inverse_name="order_id",
    )
