# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp.tests.common import TransactionCase
from lxml import etree
from datetime import datetime


class TestFieldsViewGet(TransactionCase):
    def setUp(self, *args, **kwargs):
        result = super(TestFieldsViewGet, self).setUp(*args, **kwargs)
        # Object
        self.wiz =\
            self.env['account.payment.populate.statement']
        self.obj_bank_statement = self.env['account.bank.statement']

        # Data
        self.date = datetime.now().strftime("%Y-%m-%d")
        self.journal = self.env.ref('account.bank_journal')
        self.curr = self.env.ref("base.IDR")
        self.mode = self.env.ref('account_payment.payment_mode_1')

        return result

    def test_fields_view_get(self):
        vals = {
            'name': 'Test Statement',
            'journal_id': self.journal.id,
            'date': self.date,
            'balance_end_real': 0.0,
            'balance_start': 0.0,
            'currency': self.curr.id
        }
        bank_stmt = self.obj_bank_statement.create(vals)

        wiz = self.wiz.with_context(active_id=bank_stmt.id)

        view = wiz.fields_view_get()

        check_domain = [
            ('order_id.state', '=', 'open'),
            ('order_id.mode', '=', self.mode.id),
            ('bank_statement_line_id', '=', False)
        ]

        if 'lines' in view['fields']:
            arch = view['arch']
            doc = etree.XML(arch)
            for node in doc.xpath("//field[@name='lines']"):
                domain = node.get('domain')
                self.assertEquals(
                    domain,
                    str(check_domain)
                )
        return True
