# -*- coding: utf-8 -*-

from odoo import models, fields, api

class branch_policies(models.Model):
    _name = 'branch_policies.branch_policies'

    name = fields.Char(string="Based On")
    short_code = fields.Char(string="Short Code")
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100