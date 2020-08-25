# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "BCA Auto Credit Banking Batch Processing",
    "version": "8.0.2.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_payment_banking_batch_processing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/base_xlsx_template.xml",
        "views/payment_order_view.xml",
        "views/report_bca_auto_credit.xml",
    ],
}
