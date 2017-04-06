# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import fields, models


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    product_id = fields.Many2one('product.product')
