# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountAnalyticLine(models.Model):

    _inherit = 'account.analytic.line'

    is_timesheet = fields.Boolean(string="Is Timesheet")

    def compute_timesheet_values(self):
        return {}

    @api.model
    def create(self, vals):
        line = super(AccountAnalyticLine, self).create(vals)
        if line.is_timesheet:
            if not line.user_id:
                raise ValidationError(_(
                    'No user was linked to this timesheet entry.'))
            timesheet_values = line.compute_timesheet_values()
            if timesheet_values:
                line.write(timesheet_values)

        return line

    @api.multi
    def write(self, vals):
        super(AccountAnalyticLine, self).write(vals)
        if 'is_timesheet' in vals or 'user_id' in vals:
            for line in self:
                timesheet_values = line.compute_timesheet_values()
                if timesheet_values:
                    line.write(timesheet_values)

    @api.depends(
        'date', 'user_id', 'project_id',
        'sheet_id_computed.date_to', 'sheet_id_computed.date_from',
        'sheet_id_computed.employee_id', 'is_timesheet')
    def _compute_sheet(self):
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
