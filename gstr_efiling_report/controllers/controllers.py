# -*- coding: utf-8 -*-
from odoo import http

# class GstrEfilingReport(http.Controller):
#     @http.route('/gstr_efiling_report/gstr_efiling_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gstr_efiling_report/gstr_efiling_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gstr_efiling_report.listing', {
#             'root': '/gstr_efiling_report/gstr_efiling_report',
#             'objects': http.request.env['gstr_efiling_report.gstr_efiling_report'].search([]),
#         })

#     @http.route('/gstr_efiling_report/gstr_efiling_report/objects/<model("gstr_efiling_report.gstr_efiling_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gstr_efiling_report.object', {
#             'object': obj
#         })