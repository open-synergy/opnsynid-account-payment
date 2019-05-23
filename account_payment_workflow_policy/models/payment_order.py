# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentOrder(models.Model):
    _name = "payment.order"
    _inherit = [
        "payment.order",
        "base.workflow_policy_object",
    ]

    @api.multi
    @api.depends(
        "mode",
    )
    def _compute_policy(self):
        _super = super(PaymentOrder, self)
        _super._compute_policy()

    confirm_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
    )
    make_ok = fields.Boolean(
        string="Can Make Payment",
        compute="_compute_policy",
    )
    cancel_ok = fields.Boolean(
        string="Can Cancel",
        compute="_compute_policy",
    )
    restart_ok = fields.Boolean(
        string="Can Restart",
        compute="_compute_policy",
    )
