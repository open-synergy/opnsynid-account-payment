# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    if not version:
        return

    cr.execute("""
        DELETE FROM ir_model_data
        WHERE   name = 'field_payment_line_tax_ids' AND
                module = 'account_payment_tax' AND
                model = 'ir.model.fields'
        """)

    cr.execute("""
        DELETE FROM ir_model_data
        WHERE   name = 'field_payment_line_amount_tax_currency' AND
                module = 'account_payment_tax' AND
                model = 'ir.model.fields'
        """)

    cr.execute("""
        DELETE FROM ir_model_data
        WHERE   name = 'field_payment_line_amount_total_currency' AND
                module = 'account_payment_tax' AND
                model = 'ir.model.fields'
        """)

    cr.execute("""
        DELETE FROM ir_model_fields AS a
        USING    ir_model AS b
        WHERE   a.name = 'can_read' AND
                b.name = 'hr.language' AND
                a.model_id = b.id
        """)

    cr.execute("""
        DELETE FROM ir_model_fields AS a
        USING    ir_model AS b
        WHERE   a.name = 'tax_ids' AND
                b.name = 'payment.line' AND
                a.model_id = b.id
        """)

    cr.execute("""
        DELETE FROM ir_model_fields AS a
        USING    ir_model AS b
        WHERE   a.name = 'amount_tax_currency' AND
                b.name = 'payment.line' AND
                a.model_id = b.id
        """)

    cr.execute("""
        DELETE FROM ir_model_fields AS a
        USING    ir_model AS b
        WHERE   a.name = 'amount_total_currency' AND
                b.name = 'payment.line' AND
                a.model_id = b.id
        """)

    cr.execute("""
        DROP TABLE IF EXISTS payment_line_tax_rel
        """)
