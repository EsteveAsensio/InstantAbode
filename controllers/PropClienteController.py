# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request, Response

class PropClienteController(http.Controller):

    #get                                        user
    @http.route(['/InstantAbode/login'], auth='public', type="json", methods=['POST'], csrf=False)
    def login(self, **kw):
        try:
            request_data = json.loads(request.httprequest.data)
            username = request_data.get('username')
            contrasenya = request_data.get('contrasenya')

            if not username or not contrasenya:
                return {'status': 400, 'message': 'Datos de usuario incompletos'}

            cliente = http.request.env["instant_abode.cliente"].sudo().search([("name","=",username)])

            propietario = http.request.env["instant_abode.propietario"].sudo().search([("name","=",username)])

            if cliente and cliente.contrasenya == contrasenya:
                return {'status': 200, 'message': 'Hola Cliente'}
            elif propietario and propietario.contrasenya == contrasenya:
                return {'status': 200, 'message': 'Hola Propietario'}
            else:
                return {'status': 400, 'message': 'Usuario no encontrado o contraseña incorrecta'}
        except Exception as error:
            data={
                "status": 500,
                "error": str(error)
            }
            return data
    


       
