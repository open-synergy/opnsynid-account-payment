# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from lxml import etree

from openerp import models, api


class AccountPaymentPopulateStatement(models.TransientModel):
    _inherit = 'account.payment.populate.statement'

    @api.model
    def fields_view_get(self, view_id=None, view_type='form',
                        toolbar=False, submenu=False):
        res = super(AccountPaymentPopulateStatement, self).fields_view_get(
            view_id=view_id, view_type=view_type,
            toolbar=toolbar, submenu=submenu)
        context = self.env.context
        obj_bank_statement = self.env['account.bank.statement']
        obj_payment_mode = self.env['payment.mode']
        bank_statement_id = context.get('active_id')
        bank_statement = obj_bank_statement.browse(bank_statement_id)
        criteria = [
            ('journal', '=', bank_statement.journal_id.id)
        ]
        payment_mode = obj_payment_mode.search(criteria)
        if 'arch' in res:
            doc = etree.XML(res['arch'])
            for node in doc.xpath("//field[@name='lines']"):
                domain = node.get('domain')
                domain = [
                    ('order_id.state', '=', 'open'),
                    ('order_id.mode', '=', payment_mode.id),
                    ('bank_statement_line_id', '=', False)
                ]
                node.set('domain', str(domain))
            res['arch'] = etree.tostring(doc)
        return res
