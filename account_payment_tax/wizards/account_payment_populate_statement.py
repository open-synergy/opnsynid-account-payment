# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, api


class AccountPaymentPopulateStatement(models.TransientModel):
    _inherit = "account.payment.populate.statement"

    @api.multi
    def populate_statement(self):
        """Replace the original amount column by aa_amount_currency"""

        statement_obj = self.env['account.bank.statement']
        statement_line_obj = self.env['account.bank.statement.line']

        line_ids = self.lines
        if not line_ids:
            return {'type': 'ir.actions.act_window_close'}

        statement = statement_obj.browse(
            self.env.context['active_id'])

        for line in line_ids:
            currency = statement.currency
            if line.amount_total_currency:
                amount = currency.round(
                    line.amount_total_currency)
            else:
                amount = currency.round(
                    line.amount_currency)

            st_line_vals = self._prepare_statement_line_vals(
                line, amount, statement)
            st_line_id = statement_line_obj.create(st_line_vals)

            line.write({'bank_statement_line_id': st_line_id.id})
        return {'type': 'ir.actions.act_window_close'}
