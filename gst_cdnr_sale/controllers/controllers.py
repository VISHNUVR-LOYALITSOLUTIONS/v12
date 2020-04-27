# -*- coding: utf-8 -*-
from odoo import http

# class GstCdnrSale(http.Controller):
#     @http.route('/gst_cdnr_sale/gst_cdnr_sale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gst_cdnr_sale/gst_cdnr_sale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gst_cdnr_sale.listing', {
#             'root': '/gst_cdnr_sale/gst_cdnr_sale',
#             'objects': http.request.env['gst_cdnr_sale.gst_cdnr_sale'].search([]),
#         })

#     @http.route('/gst_cdnr_sale/gst_cdnr_sale/objects/<model("gst_cdnr_sale.gst_cdnr_sale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gst_cdnr_sale.object', {
#             'object': obj
#         })