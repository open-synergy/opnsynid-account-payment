# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
import openerp.addons.decimal_precision as dp

class PaymentOrderTax(models.Model):
    _name = "payment.order.tax"
    _description = "Payment Order Tax"
    _order = 'sequence'

    @api.one
    @api.depends(
        'base',
        'base_amount',
        'amount',
        'tax_amount'
    )
    def _compute_factors(self):
        self.factor_base =\
            self.base_amount / self.base if self.base else 1.0
        self.factor_tax =\
            self.tax_amount / self.amount if self.amount else 1.0

    payment_id = fields.Many2one(
        comodel_name='payment.order',
        string='#PO',
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
        required=True,
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
    def base_change(self, base, currency_id=False, company_id=False, date_created=False):
        factor = self.factor_base if self else 1
        company = self.env['res.company'].browse(company_id)
        if currency_id and company.currency_id:
            currency = self.env['res.currency'].browse(currency_id)
            currency = currency.with_context(date=date_created or fields.Date.context_today(self))
            base = currency.compute(base * factor, company.currency_id, round=False)
        return {'value': {'base_amount': base}}

    @api.multi
    def amount_change(self, amount, currency_id=False, company_id=False, date_created=False):
        company = self.env['res.company'].browse(company_id)
        if currency_id and company.currency_id:
            currency = self.env['res.currency'].browse(currency_id)
            currency = currency.with_context(date=date_created or fields.Date.context_today(self))
            amount = currency.compute(amount, company.currency_id, round=False)
        tax_sign = (self.tax_amount / self.amount) if self.amount else 1
        return {'value': {'tax_amount': amount * tax_sign}}

    @api.multi
    def compute(self, payment):
        tax_grouped = {}
        for line in payment.line_ids:
            currency = line.currency.with_context(
                date=payment.date_created or fields.Date.context_today(payment)
            )
            company_currency = line.company_currency
            taxes = line.payment_line_tax_id.compute_all(
                price_unit=line.amount_currency,
                quantity=1.0,
                partner=line.partner_id
            )['taxes']
            for tax in taxes:
                val = {
                    'payment_id': payment.id,
                    'name': tax['name'],
                    'amount': tax['amount'],
                    'manual': False,
                    'sequence': tax['sequence'],
                    'base': currency.round(tax['price_unit'] * 1),
                }
                val['base_code_id'] = tax['base_code_id']
                val['tax_code_id'] = tax['tax_code_id']
                val['base_amount'] = currency.compute(val['base'] * tax['base_sign'], company_currency, round=False)
                val['tax_amount'] = currency.compute(val['amount'] * tax['tax_sign'], company_currency, round=False)
                val['account_id'] = tax['account_collected_id'] or line.move_line_id.account_id.id
                val['account_analytic_id'] = tax['account_analytic_collected_id']

                # If the taxes generate moves on the same financial account as the payment line
                # and no default analytic account is defined at the tax level, propagate the
                # analytic account from the payment line to the tax line. This is necessary
                # in situations were (part of) the taxes cannot be reclaimed,
                # to ensure the tax move is allocated to the proper analytic account.
                if not val.get('account_analytic_id') and line.move_line_id.analytic_account_id and val['account_id'] == line.move_line_id.account_id.id:
                    val['account_analytic_id'] = line.move_line_id.analytic_account_id.id

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
