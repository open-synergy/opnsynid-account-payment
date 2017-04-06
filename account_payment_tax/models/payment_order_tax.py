# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class PaymentOrderTax(models.Model):
    _name = "payment.order.tax"
    _description = "Payment Order Tax"
    _order = 'sequence'

    @api.multi
    @api.depends(
        'base',
        'base_amount',
        'amount',
        'tax_amount'
    )
    def _compute_factors(self):
        for rec in self:
            rec.factor_base =\
                rec.base_amount / rec.base if rec.base else 1.0
            rec.factor_tax =\
                rec.tax_amount / rec.amount if rec.amount else 1.0

    payment_line_id = fields.Many2one(
        comodel_name='payment.line',
        string='Payment Line',
        ondelete='cascade',
        index=True
    )
    name = fields.Char(
        string='Tax Description',
        required=True
    )
    account_id = fields.Many2one(
        comodel_name='account.account',
        string='Tax Account',
        domain=[
            ('type', 'not in', ['view', 'income', 'closed'])
        ]
    )
    account_analytic_id = fields.Many2one(
        comodel_name='account.analytic.account',
        string='Analytic account'
    )
    base = fields.Float(
        string='Base',
        digits=dp.get_precision('Account')
    )
    amount = fields.Float(
        string='Amount',
        digits=dp.get_precision('Account')
    )
    manual = fields.Boolean(
        string='Manual',
        default=True
    )
    sequence = fields.Integer(
        string='Sequence'
    )
    base_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string='Base Code',
        help="The account basis of the tax declaration."
    )
    base_amount = fields.Float(
        string='Base Code Amount',
        digits=dp.get_precision('Account'),
        default=0.0
    )
    tax_code_id = fields.Many2one(
        comodel_name='account.tax.code',
        string='Tax Code',
        help="The tax basis of the tax declaration."
    )
    tax_amount = fields.Float(
        string='Tax Code Amount',
        digits=dp.get_precision('Account'),
        default=0.0
    )
    company_id = fields.Many2one(
        company='res.company',
        string='Company',
        related='account_id.company_id',
        store=True,
        readonly=True
    )
    factor_base = fields.Float(
        string='Multipication factor for Base code',
        compute='_compute_factors'
    )
    factor_tax = fields.Float(
        string='Multipication factor Tax code',
        compute='_compute_factors'
    )

    @api.multi
    def compute(self, payment_line):
        tax_grouped = {}
        date_created = payment_line.order_id.date_created
        date_context =\
            fields.Date.context_today(payment_line)
        currency = payment_line.currency.with_context(
            date=date_created or date_context
        )
        company_currency = payment_line.company_currency
        taxes = payment_line.tax_ids.compute_all(
            price_unit=payment_line.amount_currency,
            quantity=1.0,
            partner=payment_line.partner_id
        )['taxes']
        for tax in taxes:
            val = {
                'payment_line_id': payment_line.id,
                'name': tax['name'],
                'amount': tax['amount'],
                'manual': False,
                'sequence': tax['sequence'],
                'base': currency.round(tax['price_unit'] * 1),
            }
            val['base_code_id'] = tax['base_code_id']
            val['tax_code_id'] = tax['tax_code_id']
            val['base_amount'] =\
                currency.compute(
                    val['base'] * tax['base_sign'],
                    company_currency,
                    round=False
                )
            val['tax_amount'] =\
                currency.compute(
                    val['amount'] * tax['tax_sign'],
                    company_currency,
                    round=False
                )
            account_id = payment_line.move_line_id.account_id.id
            analytic_id = payment_line.move_line_id.analytic_account_id
            val['account_id'] =\
                tax['account_collected_id'] or account_id
            val['account_analytic_id'] = tax['account_analytic_collected_id']

            if (
                not val.get('account_analytic_id') and
                analytic_id and val['account_id'] == account_id
            ):
                val['account_analytic_id'] = account_id

            key = (val['tax_code_id'], val['base_code_id'], val['account_id'])
            if not key in tax_grouped:
                tax_grouped[key] = val
            else:
                tax_grouped[key]['base'] += val['base']
                tax_grouped[key]['amount'] += val['amount']
                tax_grouped[key]['base_amount'] += val['base_amount']
                tax_grouped[key]['tax_amount'] += val['tax_amount']

        for t in tax_grouped.values():
            t['base'] = currency.round(t['base'])
            t['amount'] = currency.round(t['amount'])
            t['base_amount'] = currency.round(t['base_amount'])
            t['tax_amount'] = currency.round(t['tax_amount'])

        return tax_grouped
