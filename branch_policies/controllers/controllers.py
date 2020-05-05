# -*- coding: utf-8 -*-
from odoo import http

# class BranchPolicies(http.Controller):
#     @http.route('/branch_policies/branch_policies/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/branch_policies/branch_policies/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('branch_policies.listing', {
#             'root': '/branch_policies/branch_policies',
#             'objects': http.request.env['branch_policies.branch_policies'].search([]),
#         })

#     @http.route('/branch_policies/branch_policies/objects/<model("branch_policies.branch_policies"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('branch_policies.object', {
#             'object': obj
#         })