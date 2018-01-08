# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    is_timesheet = fields.Boolean(string="Is Timesheet")
    employee_id = fields.Many2one('hr.employee', 'Employee')

    @api.depends(
        'date', 'user_id', 'project_id',
        'sheet_id_computed.date_to', 'sheet_id_computed.date_from',
        'sheet_id_computed.employee_id', 'is_timesheet')
    def _compute_sheet(self):
        # Override the original method to allow affecting any timesheet
        # to an analytic line
        for line in self.filtered(lambda l: l.is_timesheet):
            if not line.project_id:
                continue
            sheets = self.env['hr_timesheet_sheet.sheet'].search(
                [('date_to', '>=', line.date), ('date_from', '<=', line.date),
                 ('employee_id.user_id.id', '=', line.user_id.id)])
            if sheets:
                line.sheet_id_computed = sheets[0]
                line.sheet_id = sheets[0]

        for line in self.filtered(lambda l: not l.is_timesheet):
            line.sheet_id = None

    def _check_employees_length(self, employees):
        if len(employees) == 0:
            raise ValidationError(_(
                'No employee attached to the '
                'user %s was found.') % self.user_id.name)

        if len(employees) != 1:
            raise ValidationError(_(
                'The user %(user)s is attached to more than one '
                'employee. These employees are : %(employee)s.') % {
                'user': self.user_id.name,
                'employee': [e.name for e in employees],
            })

    def _check_employee_product(self, employee):
        if not employee.product_id:
            raise ValidationError(_(
                'No product was assigned to the employee %s.')
                % employee.name)

        if employee.product_id.type != 'service':
            raise ValidationError(_(
                'The product %s assigned to the employee is not a '
                'service product.') % employee.product_id.name)

    def _compute_timesheet_values(self):
        if not self.user_id:
            raise ValidationError(_('The User field must be filled.'))

        employees = self.user_id.employee_ids
        self._check_employees_length(employees)
        self._check_employee_product(employees)
        product_id = employees.product_id

        return {
            'employee_id': employees.id,
            'product_id': product_id.id,
            'amount': -1 * self.unit_amount * product_id.standard_price,
        }

    @api.model
    def create(self, vals):
        line = super(AccountAnalyticLine, self).create(vals)
        if not line.is_timesheet:
            return line

        if not line.user_id:
            raise ValidationError(_(
                'No user was linked to this timesheet entry.'))

        timesheet_values = line._compute_timesheet_values()
        if timesheet_values:
            line.write(timesheet_values)

        return line

    @api.multi
    def write(self, vals):
        super(AccountAnalyticLine, self).write(vals)
        if 'is_timesheet' not in vals and 'user_id' not in vals:
            return

        for line in self:
            timesheet_values = line._compute_timesheet_values()
            if timesheet_values:
                line.write(timesheet_values)
