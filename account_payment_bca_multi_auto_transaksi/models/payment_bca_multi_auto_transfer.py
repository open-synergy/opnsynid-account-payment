# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, tools


class PaymentBcaMultiAutoTransfer(models.AbstractModel):
    _name = "payment.report_bca_multi_auto_transfer"
    _description = "BCA Multi Auto Transfer"
    _auto = False

    no = fields.Integer(
        string="No",
    )
    transaction_id = fields.Char(
        string="Transaction ID",
    )
    transaction_type = fields.Char(
        string="Transaction Type",
    )
    debited_acc = fields.Char(
        string="Debited Acc.",
    )
    credited_acc = fields.Char(
        string="Credited Acc.",
    )
    amount = fields.Float(
        string="Amount",
    )
    effective_date = fields.Date(
        string="Eff. Date",
    )
    currency = fields.Char(
        string="Currency",
    )
    charges_type = fields.Char(
        string="Charges Type",
    )
    charges_acc = fields.Char(
        string="Charges Acc",
    )
    receiver_name = fields.Char(
        string="Receiver Name",
    )
    beneficiary_email = fields.Char(
        string="Beneficiary Email",
    )
    order_id = fields.Many2one(
        string="# Payment Order",
        comodel_name="payment.order",
    )

    def _select(self):
        select_str = """
             SELECT ROW_NUMBER() OVER(
                        ORDER BY    a.order_id,
                                    a.id
                        ) AS id,
                    ROW_NUMBER() OVER(
                        PARTITION BY  a.order_id
                        ORDER BY    a.order_id,
                                    a.id
                        ) AS no,
                    CONCAT(b.reference,a.name) AS transaction_id,
                    'BCA' AS transaction_type,
                    d.acc_number AS debited_acc,
                    f.acc_number AS credited_acc,
                    a.amount_currency AS amount,
                    a.date AS effective_date,
                    'IDR' AS currency,
                    'OUR' AS charges_type,
                    d.acc_number AS charges_acc,
                    f.owner_name AS receiver_name,
                    h.email AS beneficiary_email,
                    b.id AS order_id
        """
        return select_str

    def _from(self):
        from_str = """
                payment_line AS a
        """
        return from_str

    def _where(self):
        where_str = """
        WHERE 1 = 1
        """
        return where_str

    def _join(self):
        join_str = """
        JOIN payment_order AS b
            ON a.order_id = b.id
        JOIN payment_mode AS c
            ON b.mode = c.id
        JOIN res_partner_bank AS d
            ON c.bank_id = d.id
        JOIN res_bank AS e
            ON d.bank = e.id
        JOIN res_partner_bank AS f
            ON a.bank_id = f.id
        JOIN res_bank AS g
            ON f.bank = g.id
        JOIN res_partner AS h
            ON a.partner_id = h.id
        """
        return join_str

    def _order_by(self):
        order_str = """
            ORDER BY    a.order_id,
                        a.id
        """
        return order_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute(
            """CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
            %s
        )"""
            % (
                self._table,
                self._select(),
                self._from(),
                self._join(),
                self._where(),
                self._order_by(),
            )
        )
