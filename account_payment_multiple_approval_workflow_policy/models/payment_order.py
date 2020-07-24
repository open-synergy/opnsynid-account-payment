# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentOrder(models.Model):
    _inherit = "payment.order"

    @api.multi
    @api.depends(
        "mode",
    )
    def _compute_policy(self):
        _super = super(PaymentOrder, self)
        _super._compute_policy()

    confirm_approval_ok = fields.Boolean(
        string="Can Confirm",
        compute="_compute_policy",
        store=False,
    )
    restart_approval_ok = fields.Boolean(
        string="Can Restart Approval",
        compute="_compute_policy",
        store=False,
    )
