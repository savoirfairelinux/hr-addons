# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    @api.multi
    def compute_timesheet_values(self):
        super(AccountAnalyticLine, self).compute_timesheet_values()

        for line in self:
            if not line.employee_id.product_id:
                raise ValidationError(_(
                    'No product was assigned to the employee %s.')
                    % line.employee_id.name)

            if line.employee_id.product_id.type == 'service':
                line.product_id = line.employee_id.product_id
                line.amount = (
                    -1 * line.unit_amount * line.product_id.standard_price)
            else:
                raise ValidationError(_(
                    'The product %s assigned to the employee is not a '
                    'service product.') % line.product_id.name)
