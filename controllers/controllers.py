# -*- coding: utf-8 -*-
# from odoo import http


# class InstantAbode(http.Controller):
#     @http.route('/instant_abode/instant_abode', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/instant_abode/instant_abode/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('instant_abode.listing', {
#             'root': '/instant_abode/instant_abode',
#             'objects': http.request.env['instant_abode.instant_abode'].search([]),
#         })

#     @http.route('/instant_abode/instant_abode/objects/<model("instant_abode.instant_abode"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('instant_abode.object', {
#             'object': obj
#         })
