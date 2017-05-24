# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import fields, models


class ProjectTask(models.Model):

    _inherit = 'project.task'

    timesheet_ids = fields.One2many(domain=[('is_timesheet', '=', True)])
