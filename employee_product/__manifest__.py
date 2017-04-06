# -*- coding: utf-8 -*-
# Copyright 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    "name": "Employee Product",
    "summary": "Add product_id field to hr_employee",
    "version": "10.0.1.0.0",
    "category": "",
    "website": "https://www.savoirfairelinux.com/",
    "author": "Savoir-Faire Linux, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "hr",
        "hr_timesheet_employee",
    ],
    "data": [
        "views/hr_employee.xml",
    ],
}
