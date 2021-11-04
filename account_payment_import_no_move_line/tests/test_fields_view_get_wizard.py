# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from lxml import etree

from .base import BaseTest


class TestFieldsViewGet(BaseTest):
    def test_fields_view_get(self):
        line_ids = []
        # Create Payment With Entries
        # Using New Data

        # Invoice: state = open
        self.invoice.signal_workflow("invoice_open")
        # Payment Order: state = open
        self.payment_order.signal_workflow("open")
        # Create Payment
        move_line = self.invoice.move_id.line_id[0]

        create_payment = self.obj_create_payment.with_context(
            active_model="payment.order", active_id=self.payment_order.id
        )
        create_payment.create({"entries": [(6, 0, [move_line.id])]}).create_payment()

        # Create Payment Without Entries
        # Using old data demo
        data_payment_lines = {
            "order_id": self.data_payment.id,
            "name": "Test Payment Line - 1",
            "partner_id": self.partner.id,
            "communication": "-",
            "amount_currency": 75000,
        }
        data_payment_line = self.obj_payment_line.create(data_payment_lines)
        self.data_payment.signal_workflow("open")

        # GET LINE ID for Payment with Entries
        line_ids.append(self.payment_order.line_ids[0].id)
        # GET LINE ID for Payment without Entries
        line_ids.append(data_payment_line.id)

        # Create Bank Statement
        vals = {
            "name": "Test Statement",
            "journal_id": self.journal.id,
            "date": self.date,
            "balance_end_real": 0.0,
            "balance_start": 0.0,
            "currency": self.curr.id,
        }
        bank_stmt = self.obj_bank_statement.create(vals)

        wiz = self.wiz.with_context(active_id=bank_stmt.id)

        # Get Fields View Get
        view = wiz.fields_view_get()

        # Check Domain
        check_domain = [("id", "in", line_ids)]

        if "lines" in view["fields"]:
            arch = view["arch"]
            doc = etree.XML(arch)
            for node in doc.xpath("//field[@name='lines']"):
                domain = node.get("domain")
                self.assertEqual(domain, str(check_domain))
