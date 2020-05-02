# -*- coding: utf-8 -*-
from odoo import http

# class KfcReport(http.Controller):
#     @http.route('/kfc_report/kfc_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kfc_report/kfc_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('kfc_report.listing', {
#             'root': '/kfc_report/kfc_report',
#             'objects': http.request.env['kfc_report.kfc_report'].search([]),
#         })

#     @http.route('/kfc_report/kfc_report/objects/<model("kfc_report.kfc_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kfc_report.object', {
#             'object': obj
#         })