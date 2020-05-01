# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountTax(models.Model):
    _inherit = 'account.tax'

    adjust_amount = fields.Float(required=False, digits=(16, 4))
    cess_adjust_amount = fields.Float(required=False, digits=(16, 4))


    def _compute_amount(self, base_amount, price_unit, quantity=1.0, product=None, partner=None):
        res = super(AccountTax, self)._compute_amount(base_amount, price_unit, quantity, product, partner)
        self.ensure_one()
        if self.amount_type == 'percent' and self.price_include:

            if self.adjust_amount:
                return (base_amount*self.amount)/(100+self.adjust_amount)
            else:
                return base_amount - (base_amount / (1 + self.amount / 100))

        return res





