# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common


class EmployeeProduct(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(EmployeeProduct, cls).setUpClass()
        cls.create_account_analytic_line()

    @classmethod
    def create_account_analytic_line(cls):
        cls.product_1 = cls.env['product.product'].create({
            'name': 'Product 1',
            'type': 'service',
            'standard_price': 20,
        })

        cls.product_2 = cls.env['product.product'].create({
            'name': 'Product 2',
            'type': 'consu',
            'standard_price': 20,
        })

        cls.employee_1 = cls.env['hr.employee'].create({
            'name': 'Employee 1',
            'product_id': cls.product_1.id,
        })

        cls.employee_2 = cls.env['hr.employee'].create({
            'name': 'Employee 2',
        })

        cls.user_1 = cls.env['res.users'].create({
            'name': 'User 1',
            'login': 'User 1',
            'employee_ids': [(4, cls.employee_1.id)],
        })

        cls.user_2 = cls.env['res.users'].create({
            'name': 'User 2',
            'login': 'User 2',
            'employee_ids': [(4, cls.employee_2.id)],
        })

        cls.project = cls.env['project.project'].create({
            'name': 'Project 1',
        })

        cls.account_analytic_line_1 = cls.env['account.analytic.line'].create({
            'date': fields.Date.today(),
            'name': 'test',
            'user_id': cls.user_1.id,
            'unit_amount': 4,
            'project_id': cls.project.id,
            'is_timesheet': True,
        })

    def test_1_compute_product_id_and_amount(self):
        account_analytic_line_1 = self.account_analytic_line_1
        self.assertEqual(
            account_analytic_line_1.product_id, self.product_1)
        amount = (
            -1 * self.product_1.standard_price *
            account_analytic_line_1.unit_amount)
        self.assertEqual(
            account_analytic_line_1.amount, amount)

    def test_2_raise_exception_when_product_is_not_service(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id.employee_ids.product_id = (
                self.product_2)

    def test_3_raise_exception_when_no_product_is_assigned_to_employee(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id = self.user_2

    def test_4_raise_exception_when_product_is_not_empty_or_service(self):
        employee_2 = self.employee_2
        with self.assertRaises(ValidationError):
            employee_2.product_id = self.product_2
