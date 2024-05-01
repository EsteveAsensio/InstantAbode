# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request, Response

class PropClienteController(http.Controller):

    @http.route(['/InstantAbode/login'], auth='public', type="json", methods=['POST'], csrf=False)
    def login(self, **kw):
        try:
            request_data = json.loads(request.httprequest.data)
            username = request_data.get('username')
            contrasenya = request_data.get('contrasenya')

            if not username or not contrasenya:
                return {'status': 400, 'message': 'Datos de usuario incompletos'}

            cliente = http.request.env["instant_abode.cliente"].sudo().search([("name","=",username)])

            if cliente and cliente.contrasenya == contrasenya:
                usuario = {
                    'id': cliente.id,
                    'dni': cliente.dni,
                    'nombreCliente': cliente.nombreCliente,
                    'apellidos': cliente.apellidos,
                    'telefono': cliente.telefono,
                    'name': cliente.name,
                    'contrasenya': cliente.contrasenya,
                    'correo': cliente.correo,
                    'imagen': cliente.imagen,
                    'rol': 'Cliente',
                }
                return {'status': 200, 'usuario': usuario}
            else:
                return {'status': 400, 'message': 'Usuario no encontrado o contraseña incorrecta'}
        except Exception as error:
            data = {
                "status": 500,
                "message": str(error)
            }
            return data

    


       
