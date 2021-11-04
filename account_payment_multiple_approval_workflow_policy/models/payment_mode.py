# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class PaymentMode(models.Model):
    _inherit = "payment.mode"

    payment_order_confirm_approval_grp_ids = fields.Many2many(
        string="Allowed to Confirm",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_confirm_approval",
        column1="mode_id",
        column2="group_id",
    )
    payment_order_restart_approval_grp_ids = fields.Many2many(
        string="Allow To Restart Approval",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_restart_approval",
        column1="mode_id",
        column2="group_id",
    )
