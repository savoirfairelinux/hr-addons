# -*- coding: utf-8 -*-
# Copyright 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Analytic Line is Timesheet',
    'version': '10.0.1.0.0',
    'category': 'Human Resources',
    'website': 'https://www.savoirfairelinux.com/',
    'author': 'Savoir-Faire Linux',
    'license': 'LGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'hr_timesheet_sheet',
    ],
    'data': [
        'views/hr_employee.xml',
        'views/hr_timesheet_sheet.xml',
        'views/project_task.xml',
    ],
}
