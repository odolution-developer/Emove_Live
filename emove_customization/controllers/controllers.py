# -*- coding: utf-8 -*-
# from odoo import http


# class EmoveCustomization(http.Controller):
#     @http.route('/emove_customization/emove_customization', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emove_customization/emove_customization/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('emove_customization.listing', {
#             'root': '/emove_customization/emove_customization',
#             'objects': http.request.env['emove_customization.emove_customization'].search([]),
#         })

#     @http.route('/emove_customization/emove_customization/objects/<model("emove_customization.emove_customization"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emove_customization.object', {
#             'object': obj
#         })

