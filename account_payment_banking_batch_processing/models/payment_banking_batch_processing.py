# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields


class AccountBankingBatchProcessing(models.Model):
    _name = "payment.banking_batch_processing"
    _description = "Banking Batch Payment Processing"

    name = fields.Char(
        string="Batch Processing",
        required=True,
    )
    bank_id = fields.Many2one(
        string="Bank",
        comodel_name="res.bank",
        required=False,
    )
    action_id = fields.Many2one(
        string="Window Action",
        comodel_name="ir.actions.act_window",
        required=True,
    )
    active = fields.Boolean(
        string="Active",
        default=True,
    )
    note = fields.Text(
        string="Note",
    )
