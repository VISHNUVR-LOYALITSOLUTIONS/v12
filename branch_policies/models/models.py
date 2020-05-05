# -*- coding: utf-8 -*-

from odoo import models, fields, api

class company_privilege_policies(models.Model):
    _inherit = 'operating.unit'

    select_rule = fields.Many2one('branch_policies.branch_policies')
    branch_limit = fields.Float()

#     def _value_pc(self):
#         self.value2 = float(self.value) / 100