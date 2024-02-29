# -*- coding: utf-8 -*-
# from odoo import http


# class Investment(http.Controller):
#     @http.route('/investment/investment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/investment/investment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('investment.listing', {
#             'root': '/investment/investment',
#             'objects': http.request.env['investment.investment'].search([]),
#         })

#     @http.route('/investment/investment/objects/<model("investment.investment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('investment.object', {
#             'object': obj
#         })
