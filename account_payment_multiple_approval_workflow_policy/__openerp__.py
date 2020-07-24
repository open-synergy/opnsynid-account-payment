# -*- coding: utf-8 -*-
# Copyright 2020 OpenSynergy Indonesia
# Copyright 2020 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Payment Order Multiple Approval Workflow Policy",
    "version": "8.0.1.0.0",
    "category": "Accounting & Finance",
    "website": "https://simetri-sinergi.id",
    "author": "PT. Simetri Sinergi Indonesia, OpenSynergy Indonesia",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "auto_install": True,
    "depends": [
        "account_payment_multiple_approval",
        "account_payment_workflow_policy",
    ],
    "data": [
        "data/base_workflow_policy_data.xml",
        "views/payment_order_views.xml",
        "views/payment_mode_views.xml",
    ],
    "images": [
        "static/description/banner.png",
    ],
}
