# -*- coding: utf-8 -*-

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    _name = 'product.template'

    hsn = fields.Char(string="HSN/SAC")

    @api.onchange('l10n_in_hsn_code')
    def _onchange_hsn(self):

        self.hsn = self.l10n_in_hsn_code


