# -*- coding: utf-8 -*-
# © 2016 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common


class TestAccountAnalyticLine(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountAnalyticLine, cls).setUpClass()

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

        cls.employee_3 = cls.env['hr.employee'].create({
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

        cls.user_3 = cls.env['res.users'].create({
            'name': 'User 3',
            'login': 'User 3',
            'employee_ids': [(4, cls.employee_2.id), (4, cls.employee_3.id)],
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

        cls.account_analytic_line_2 = cls.env['account.analytic.line'].create({
            'date': fields.Date.today(),
            'name': 'test',
            'user_id': cls.user_1.id,
            'project_id': cls.project.id,
            'is_timesheet': False,
        })

    def test_1_compute_employee_id_user_linked_to_1_employee(self):
        account_analytic_line_1 = self.account_analytic_line_1
        account_analytic_line_1.user_id = self.user_1
        self.assertEqual(
            account_analytic_line_1.employee_id, self.employee_1)

    def test_2_raise_exception_when_user_not_linked_to_an_employee(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id = self.user_2

    def test_3_raise_exception_when_user_linked_to_2_employees(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id = self.user_3

    def test_4_compute_employee_id_analytic_line_is_not_timesheet(self):
        account_analytic_line_2 = self.account_analytic_line_2
        self.assertFalse(account_analytic_line_2.employee_id)

    def test_5_raise_exception_when_user_not_filled(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id = False

    def test_6_compute_product_id_and_amount(self):
        account_analytic_line_1 = self.account_analytic_line_1
        self.assertEqual(
            account_analytic_line_1.product_id, self.product_1)
        amount = (
            -1 * self.product_1.standard_price *
            account_analytic_line_1.unit_amount)
        self.assertEqual(
            account_analytic_line_1.amount, amount)

    def test_7_raise_exception_when_product_is_not_service(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id.employee_ids.product_id = (
                self.product_2)

    def test_8_raise_exception_when_no_product_is_assigned_to_employee(self):
        account_analytic_line_1 = self.account_analytic_line_1
        with self.assertRaises(ValidationError):
            account_analytic_line_1.user_id = self.user_2

    def test_9_raise_exception_when_product_is_not_empty_or_service(self):
        employee_2 = self.employee_2
        with self.assertRaises(ValidationError):
            employee_2.product_id = self.product_2
