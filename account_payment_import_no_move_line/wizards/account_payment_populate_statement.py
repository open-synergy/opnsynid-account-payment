# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree
from openerp import models, api
from openerp.tools.safe_eval import safe_eval


class AccountPaymentPopulateStatement(models.TransientModel):
    _inherit = 'account.payment.populate.statement'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(AccountPaymentPopulateStatement, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        list_mode = []
        context = self.env.context
        obj_bank_statement = self.env['account.bank.statement']
        obj_payment_mode = self.env['payment.mode']
        obj_payment_line = self.env['payment.line']

        bank_statement_id = context.get('active_id')
        bank_statement = obj_bank_statement.browse(bank_statement_id)

        criteria = [
            ('journal', '=', bank_statement.journal_id.id)
        ]
        mode_ids = obj_payment_mode.search(criteria)

        if mode_ids:
            for mode in mode_ids:
                list_mode.append(mode.id)

        criteria_line = [
            ('order_id.state', '=', 'open'),
            ('order_id.mode', 'in', list_mode),
            ('bank_statement_line_id', '=', False),
            ('move_line_id', '=', False)
        ]

        payment_line_ids = obj_payment_line.search(
            criteria_line)

        if 'arch' in res:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='lines']"):
                domain = node.get('domain')
                if domain:
                    domain = safe_eval(domain)
                    for n, crit in enumerate(domain):
                        if crit[0] == 'id' and crit[1] == 'in':
                            id_domain = list(crit[2])
                            for payment_line in payment_line_ids:
                                id_domain.append(payment_line.id)
                            domain[n] = ("id", "in", id_domain)
                node.set('domain', str(domain))
            res['arch'] = etree.tostring(doc)
        return res
