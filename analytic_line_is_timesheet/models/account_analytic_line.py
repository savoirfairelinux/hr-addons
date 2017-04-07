# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    is_timesheet = fields.Boolean(string="Is Timesheet")

    @api.multi
    def compute_timesheet_values(self):
        return True

    @api.model
    def create(self, vals):
        line = super(AccountAnalyticLine, self).create(vals)
        if line.is_timesheet:
            if not line.user_id:
                raise ValidationError(_(
                    'No user was linked to this timesheet entry.'))
            line.compute_timesheet_values()

        return line

    @api.multi
    def write(self, vals):
        super(AccountAnalyticLine, self).write(vals)
        if 'is_timesheet' in vals or 'user_id' in vals:
            self.filtered(lambda l: l.is_timesheet).compute_timesheet_values()
