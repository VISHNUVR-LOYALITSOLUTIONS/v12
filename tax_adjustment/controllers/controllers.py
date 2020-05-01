# -*- coding: utf-8 -*-
from odoo import http

# class TaxAdjustment(http.Controller):
#     @http.route('/tax_adjustment/tax_adjustment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tax_adjustment/tax_adjustment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tax_adjustment.listing', {
#             'root': '/tax_adjustment/tax_adjustment',
#             'objects': http.request.env['tax_adjustment.tax_adjustment'].search([]),
#         })

#     @http.route('/tax_adjustment/tax_adjustment/objects/<model("tax_adjustment.tax_adjustment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tax_adjustment.object', {
#             'object': obj
#         })