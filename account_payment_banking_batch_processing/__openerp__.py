# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Order To Banking Batch Processing",
    "version": "8.0.1.0.0",
    "website": "https://simetri-sinergi.id",
    "author": "OpenSynergy Indonesia, PT. Simetri Sinergi Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_payment",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/select_batch_processing.xml",
        "wizards/batch_processing.xml",
        "views/payment_banking_batch_processing_views.xml",
        "views/payment_order_views.xml",
    ],
}
