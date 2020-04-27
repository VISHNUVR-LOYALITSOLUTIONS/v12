# -*- coding: utf-8 -*-
from odoo import http

# class AccountPurchaseExtend(http.Controller):
#     @http.route('/account_purchase_extend/account_purchase_extend/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_purchase_extend/account_purchase_extend/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_purchase_extend.listing', {
#             'root': '/account_purchase_extend/account_purchase_extend',
#             'objects': http.request.env['account_purchase_extend.account_purchase_extend'].search([]),
#         })

#     @http.route('/account_purchase_extend/account_purchase_extend/objects/<model("account_purchase_extend.account_purchase_extend"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_purchase_extend.object', {
#             'object': obj
#         })