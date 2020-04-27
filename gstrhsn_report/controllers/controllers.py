# -*- coding: utf-8 -*-
from odoo import http

# class GstrhsnReport(http.Controller):
#     @http.route('/gstrhsn_report/gstrhsn_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gstrhsn_report/gstrhsn_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gstrhsn_report.listing', {
#             'root': '/gstrhsn_report/gstrhsn_report',
#             'objects': http.request.env['gstrhsn_report.gstrhsn_report'].search([]),
#         })

#     @http.route('/gstrhsn_report/gstrhsn_report/objects/<model("gstrhsn_report.gstrhsn_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gstrhsn_report.object', {
#             'object': obj
#         })