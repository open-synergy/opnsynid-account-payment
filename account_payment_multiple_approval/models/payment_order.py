# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api


class PaymentOrder(models.Model):
    _name = "payment.order"
    _inherit = [
        "payment.order",
        "tier.validation",
    ]
    _state_from = [
        "draft",
        "confirm"
    ]
    _state_to = [
        "open",
    ]

    STATE_SELECTION = [
        ("draft", "Draft"),
        ("confirm", "Waiting for Approval"),
        ("cancel", "Cancelled"),
        ("open", 'Open'),
        ("done", "Done"),
    ]

    state = fields.Selection(
        string="State",
        selection=STATE_SELECTION,
        readonly=True,
        select=True,
        copy=False,
    )

    @api.multi
    def wkf_confirm(self):
        for document in self:
            document.write(document._prepare_confirm_data())
            document.request_validation()

    @api.multi
    def _prepare_confirm_data(self):
        self.ensure_one()
        return {
            "state": "confirm",
        }

    @api.multi
    def wkf_cancel(self):
        for document in self:
            document.write(document._prepare_cancel_data())
            document.restart_validation()

    @api.multi
    def _prepare_cancel_data(self):
        self.ensure_one()
        return {
            "state": "cancel",
        }

    @api.multi
    def validate_tier(self):
        _super = super(PaymentOrder, self)
        _super.validate_tier()
        for document in self:
            if document.validated:
                document.signal_workflow("open")

    @api.multi
    def restart_validation(self):
        _super = super(PaymentOrder, self)
        _super.restart_validation()
        for document in self:
            document.request_validation()
