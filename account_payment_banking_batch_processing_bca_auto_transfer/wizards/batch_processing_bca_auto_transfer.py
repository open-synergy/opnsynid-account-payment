# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models


class BatchProcessingBcaAutoTransfer(models.TransientModel):
    _name = "payment.batch_processing_bca_auto_transfer"
    _inherit = "payment.batch_processing"
    _description = "BCA Auto-Transfer Batch Processing"

    @api.multi
    def action_print_sreen(self):
        self.ensure_one()
        xml = (
            "account_payment_banking_batch_processing_bca_auto_transfer."
            + "payment_report_bca_auto_transfer_action"
        )
        report = self.env.ref(xml).read()[0]
        report["domain"] = [("order_id", "=", self.order_id.id)]
        return report
