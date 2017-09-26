# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    def compute_timesheet_values(self):
        vals = super(AccountAnalyticLine, self).compute_timesheet_values()

        if 'employee_id' in vals:
            employee = self.env['hr.employee'].browse(vals['employee_id'])
        else:
            employee = self.employee_id

        if not employee.product_id:
            raise ValidationError(_(
                'No product was assigned to the employee %s.')
                % employee.name)

        if employee.product_id.type == 'service':
            vals['product_id'] = employee.product_id.id
            vals['amount'] = (
                -1 * self.unit_amount * employee.product_id.standard_price)
        else:
            raise ValidationError(_(
                'The product %s assigned to the employee is not a '
                'service product.') % employee.product_id.name)

        return vals
