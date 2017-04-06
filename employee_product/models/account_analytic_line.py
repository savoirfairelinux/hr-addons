# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import api, models


class AccountAnalyticLine(models.Model):

    _inherit = "account.analytic.line"

    @api.multi
    def compute_timesheet_values(self):
        super(AccountAnalyticLine, self).compute_timesheet_values()

        for line in self:
            line.product_id = line.employee_id.product_id
            line.amount = (
                -1 * line.unit_amount * line.product_id.standard_price)
