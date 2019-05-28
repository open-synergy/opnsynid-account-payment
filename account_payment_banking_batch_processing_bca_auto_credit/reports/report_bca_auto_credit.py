# -*- coding: utf-8 -*-
# Copyright 2018 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields
from openerp import tools


class ReportBcaAutoCredit(models.AbstractModel):
    _name = "payment.report_bca_auto_credit"
    _description = "BCA Auto-Credit Report"
    _auto = False

    transac_date = fields.Char(
        string="Transac. Date",
    )
    receiver_name = fields.Char(
        string="Receiver Name",
    )
    acc_no_to = fields.Char(
        string="Acc. No. To.",
    )
    bi_code = fields.Char(
        string="BI Code",
    )
    bank_name = fields.Char(
        string="Bank Name",
    )
    bank_branch_name = fields.Char(
        string="Bank Branch Name",
    )
    trans_amount = fields.Float(
        string="Trans. Amount"
    )
    jenis = fields.Char(
        string="Jenis",
    )
    remark1 = fields.Char(
        string="Remark 1",
    )
    remark2 = fields.Char(
        string="Remark 2",
    )
    customer_type = fields.Char(
        string="Customer Type",
    )
    customer_residence = fields.Char(
        string="Customer Residence",
    )
    order_id = fields.Many2one(
        string="# Order",
        comodel_name="payment.order",
    )

    def _select(self):
        select_str = """
             SELECT a.id AS id,
                    TO_CHAR(a.date, 'MM/DD/YYYY') AS transac_date,
                    f.acc_number AS acc_no_to,
                    a.amount_currency AS trans_amount,
                    a.communication AS remark1,
                    a.communication2 AS remark2,
                    'BCA' AS jenis,
                    f.bank_bic AS bi_code,
                    g.name AS bank_name,
                    f.bank_name AS bank_branch_name,
                    '1' AS customer_type,
                    'R' AS customer_residence,
                    f.owner_name AS receiver_name,
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
        """
        return join_str

    def init(self, cr):
        tools.drop_view_if_exists(cr, self._table)
        # pylint: disable=locally-disabled, sql-injection
        cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            FROM %s
            %s
            %s
        )""" % (
            self._table,
            self._select(),
            self._from(),
            self._join(),
            self._where()
        ))
