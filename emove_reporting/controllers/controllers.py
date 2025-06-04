# -*- coding: utf-8 -*-
# from odoo import http


# class EmoveReporting(http.Controller):
#     @http.route('/emove_reporting/emove_reporting', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/emove_reporting/emove_reporting/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('emove_reporting.listing', {
#             'root': '/emove_reporting/emove_reporting',
#             'objects': http.request.env['emove_reporting.emove_reporting'].search([]),
#         })

#     @http.route('/emove_reporting/emove_reporting/objects/<model("emove_reporting.emove_reporting"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('emove_reporting.object', {
#             'object': obj
#         })

