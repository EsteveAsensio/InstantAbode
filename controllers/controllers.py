# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import json
from odoo.http import request

class InstantAbode(http.Controller):

    #
    #Product
    #

    #get
    @http.route(['/InstantAbode/login'], auth='public', type="json", methods=['GET'], csrf=False)
    def login(self, **kw):
        response = request.jsonrequest
        try:
            username = response.get('username')
            contrasenya = response.get('contrasenya')

            domain=[("name","=",username), ("contrasenya","=",contrasenya)]                                                                                                                         
            cliente = http.request.env["instant_abode.cliente"].sudo().search_read(domain,["dni", "nombreCliente", "apellidos", "correo", "telefono", "name", "contrasenya", "imagen", "valoraciones", "alquileres"])

            if cliente:
                return {'status': 200, 'result': 'Usuario enconstrado'}
            else:
                return {'status': 404, 'message': 'Usuario no encontrado'}
        except Exception as error:
            data={
                "status":500,
                "error":error
            }
            return data
