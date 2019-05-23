# -*- coding: utf-8 -*-
# Copyright 2019 OpenSynergy Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "BCA Auto Transfer Banking Batch Processing",
    "version": "8.0.1.0.0",
    "website": "https://opensynergy-indonesia.com",
    "author": "OpenSynergy Indonesia",
    "license": "AGPL-3",
    "installable": True,
    "depends": [
        "account_payment_banking_batch_processing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizards/batch_processing_bca_auto_transfer.xml",
        "data/payment_banking_batch_processing_data.xml",
        "reports/report_bca_auto_transfer.xml",
    ],
}
