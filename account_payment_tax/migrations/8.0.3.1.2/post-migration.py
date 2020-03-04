# -*- coding: utf-8 -*-
# Copyright 2017 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import SUPERUSER_ID
from openerp.api import Environment


def migrate(cr, version):
    if not version:
        return

    env = Environment(cr, SUPERUSER_ID, {})
    obj_order = env['payment.order']
    order_ids = obj_order.search([])
    for order in order_ids:
        for line in order.line_ids:
            line.button_reset_taxes()
