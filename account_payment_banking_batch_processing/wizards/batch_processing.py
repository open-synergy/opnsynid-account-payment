# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, models, fields
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class BatchProcessing(models.AbstractModel):
    _name = "payment.batch_processing"
    _description = "Batch Processing"

    order_id = fields.Many2one(
        string="# Order",
        comodel_name="payment.order",
    )
    output_format = fields.Selection(
        string="Output Format",
        required=True,
        selection=[
            ("screen", "On-Screen"),
            ("ods", "ODS"),
            ("xls", "XLS")
        ],
        default="screen",
    )

    @api.multi
    def action_print_sreen(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_ods(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_print_xls(self):
        raise UserError(
            _("This feature hasn't been implemented yet"))

    @api.multi
    def action_confirm(self):
        self.ensure_one()

        if self.output_format == "screen":
            result = self.action_print_sreen()
        elif self.output_format == "ods":
            result = self.action_print_ods()
        elif self.output_format == "xls":
            result = self.action_print_xls()
        else:
            raise UserError(_("No Output Format Selected"))

        return result
