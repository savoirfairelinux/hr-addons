# -*- coding: utf-8 -*-
# Copyright 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import _, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    employee_id = fields.Many2one('hr.employee', 'Employee')

    def compute_timesheet_values(self):
        vals = super(AccountAnalyticLine, self).compute_timesheet_values()

        if 'user_id' in vals:
            user = self.env['res.users'].browse(vals['user_id'])
        else:
            user = self.user_id

        if user:
            employees = user.employee_ids
            if len(employees) == 1:
                vals['employee_id'] = employees.id
            elif len(employees) == 0:
                raise ValidationError(_(
                    'No employee attached to the '
                    'user %s was found.') % user.name)
            else:
                raise ValidationError(_(
                    'The user %(user)s is attached to more than one '
                    'employee. These employees are : %(employee)s.') % {
                    'user': user.name,
                    'employee': [e.name for e in employees],
                })
        else:
            raise ValidationError(_('The User field must be filled.'))

        return vals
