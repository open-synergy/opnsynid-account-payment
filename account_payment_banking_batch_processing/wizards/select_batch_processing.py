# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class AccountBankingBatchProcessing(models.TransientModel):
    _name = "payment.select_batch_processing"
    _description = "Select Batch Payment Processing"

    @api.model
    def _default_order_id(self):
        return self._context.get("active_id", False)

    @api.multi
    @api.depends(
        "order_id",
    )
    def _compute_allowed_batch_processing_ids(self):
        obj_batch = self.env["payment.banking_batch_processing"]
        for wiz in self:
            bank = wiz.order_id.mode.bank_id.bank

            if not bank:
                continue

            criteria = [
                ("bank_id", "=", bank.id),
            ]
            batchs = obj_batch.search(criteria)
            wiz.allowed_batch_processing_ids = batchs.ids

    order_id = fields.Many2one(
        string="# Payment Order",
        comodel_name="payment.order",
        default=lambda self: self._default_order_id(),
    )
    batch_processing_id = fields.Many2one(
        string="Batch Processing",
        comodel_name="payment.banking_batch_processing",
        required=True,
    )
    allowed_batch_processing_ids = fields.Many2many(
        string="Allowed Batch Processing",
        comodel_name="payment.banking_batch_processing",
        compute="_compute_allowed_batch_processing_ids",
    )

    @api.multi
    def action_confirm(self):
        self.ensure_one()
        wiz = self.batch_processing_id.action_id.read()[0]
        wiz["context"] = {
            "default_order_id": self.order_id.id,
        }
        return wiz
