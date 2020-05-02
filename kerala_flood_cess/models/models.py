# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountFiscalposition(models.Model):
    _inherit = 'account.fiscal.position'

    kfc_fiscal = fields.Boolean(string = 'KFC', default=False)

class ResPartner(models.Model):
    _inherit = 'res.partner'


    @api.model
    def create_from_ui(self, partner):

        res = super(ResPartner, self).create_from_ui(partner)
        partner_id = self.browse(res)
        if partner_id.state_id==partner_id.company_id.state_id and not partner_id.x_gstin and partner_id.state_id.code =='KL':
            fiscal_id = self.env['account.fiscal.position'].search([('kfc_fiscal','=',True)],limit=1)
            partner_id.property_account_position_id = fiscal_id
        return res

    @api.onchange('state_id','x_gstin',)
    def kfc_fiscal_partner(self):
        if self.state_id==self.company_id.state_id and not self.x_gstin and self.state_id.code =='KL':
            fiscal_id = self.env['account.fiscal.position'].search([('kfc_fiscal','=',True)],limit=1)
            self.property_account_position_id = fiscal_id
        else:
            if self.property_account_position_id and self.property_account_position_id.kfc_fiscal:
                self.property_account_position_id = False

    @api.onchange('property_account_position_id')
    def kfc_fiscal_checking(self):

        if self.property_account_position_id.kfc_fiscal:
            if not(self.state_id == self.company_id.state_id and not self.x_gstin and self.state_id.code == 'KL'):
                self.property_account_position_id = False


class AccountTax(models.Model):
    _inherit = 'account.tax'

    kfc = fields.Boolean(string='KFC', default=False)


