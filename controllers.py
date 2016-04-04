# -*- coding: utf-8 -*-
from openerp import http


class MroModule(http.Controller):

#        @http.route('/mro_module/mro_module/', auth='public')
#        def index(self, **kw):
#            return "Hello, world"

        @http.route('/mro_module/mro_module/objects/', auth='public')
        def list(self, **kw):
            return http.request.render('mro_module.listing', {
                'root': '/mro_module/mro_module',
                'objects': http.request.env['mro_module.mro_module'].search([]),
            })

        @http.route('/mro_module/mro_module/objects/<model("mro_module.mro_module"):obj>/', auth='public')
        def object(self, obj, **kw):
            return http.request.render('mro_module.object', {
                'object': obj
            })
