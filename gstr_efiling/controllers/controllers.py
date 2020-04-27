# -*- coding: utf-8 -*-
from odoo import http

# class GstrEfiling(http.Controller):
#     @http.route('/gstr_efiling/gstr_efiling/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gstr_efiling/gstr_efiling/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gstr_efiling.listing', {
#             'root': '/gstr_efiling/gstr_efiling',
#             'objects': http.request.env['gstr_efiling.gstr_efiling'].search([]),
#         })

#     @http.route('/gstr_efiling/gstr_efiling/objects/<model("gstr_efiling.gstr_efiling"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gstr_efiling.object', {
#             'object': obj
#         })