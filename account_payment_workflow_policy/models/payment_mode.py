# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class PaymentMode(models.Model):
    _name = "payment.mode"
    _inherit = [
        "payment.mode",
    ]

    payment_order_confirm_grp_ids = fields.Many2many(
        string="Allowed To Confirm Payment Order",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_confirm",
        column1="mode_id",
        column2="group_id",
    )
    payment_order_make_grp_ids = fields.Many2many(
        string="Allowed To Make Payment Order",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_make",
        column1="mode_id",
        column2="group_id",
    )
    payment_order_cancel_grp_ids = fields.Many2many(
        string="Allowed To Cancel Payment Order",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_cancel",
        column1="mode_id",
        column2="group_id",
    )
    payment_order_restart_grp_ids = fields.Many2many(
        string="Allowed To Restart Payment Order",
        comodel_name="res.groups",
        relation="rel_payment_mode_2_grp_payment_order_restart",
        column1="mode_id",
        column2="group_id",
    )
