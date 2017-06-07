# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/LGPL).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):

    _inherit = "hr.employee"

    product_id = fields.Many2one('product.product', string='Product')

    @api.constrains('product_id')
    def _check_product_id(self):
        for employee in self:
            if self.product_id and self.product_id.type != 'service':
                raise ValidationError(_(
                    'The product assigned to the employee should be empty'
                    ' or a service product.'))

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id and not self.product_id.standard_price:
            warning = {
                'title': _('Warning'),
                'message': _(
                    'The price of the product %s is not filled.' %
                    self.product_id.name)
            }

            return {'warning': warning}
