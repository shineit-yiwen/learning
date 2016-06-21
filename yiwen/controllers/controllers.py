# -*- coding: utf-8 -*-
from openerp import http

# class Yiwen(http.Controller):
#     @http.route('/yiwen/yiwen/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/yiwen/yiwen/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('yiwen.listing', {
#             'root': '/yiwen/yiwen',
#             'objects': http.request.env['yiwen.yiwen'].search([]),
#         })

#     @http.route('/yiwen/yiwen/objects/<model("yiwen.yiwen"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('yiwen.object', {
#             'object': obj
#         })