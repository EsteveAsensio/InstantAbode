# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request
import datetime

class ClientesController(http.Controller):
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
                return {'status': 200, 'result': 'Usuario encontrado'}
            else:
                return {'status': 400, 'message': 'Usuario no encontrado'}
        except Exception as error:
            data={
                "status":500,
                "error": str(error)
            }
            return data

    #post
    @http.route('/InstantAbode/registrarNuevoUsuario', type='json', auth='public', methods=['POST'], csrf=False)
    def registrarNuevoUsuario(self, **kw):
        response = request.httprequest.json
        try:
            username = response.get('name')

            cliente = request.env['instant_abode.cliente'].sudo().search([('name', '=', username)])
            if cliente.exists():
                return {"status": 400, "error": "Ya existe un usuario con ese nombre."}
            
            propietario = request.env['instant_abode.propietario'].sudo().search([('name', '=', username)])
            if propietario.exists():
                return {"status": 400, "error": "Ya existe un usuario con ese nombre."}
            
            result = http.request.env["instant_abode.cliente"].sudo().create(response)

            data={
                "status":200,
                "id":result.id
            }
            return data
        except Exception as error:
            data={
                "status":500,
                "error": str(error)
            }
            return data
        
    #get
    @http.route(['/InstantAbode/buscarInmuebles'], auth='public', type="json", methods=['GET'], csrf=False)
    def buscarInmuebles(self, **kw):
        try:
            response = request.httprequest.json

            provincia = response.get('provincia')
            fecha_inicio_str = response.get('fechaInicio')
            fecha_final_str = response.get('fechaFinal')

            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%d/%m/%Y").date()
            fecha_final = datetime.datetime.strptime(fecha_final_str, "%d/%m/%Y").date()

            inmuebles = request.env['instant_abode.inmueble'].sudo().search([
                ('provincia', '=', provincia),
                ('state', '=', 'Mostrar'),
            ])

            if not inmuebles:
                return {"status": 200, "error": "No hay inmuebles disponibles."}

            inmuebles_disponibles = []
            for inmueble in inmuebles:
                alquileres = request.env['instant_abode.alquiler'].sudo().search([
                    ('id', '!=', inmueble.id),
                    ('inmueble', '=', inmueble.id),
                    '|',
                    '&', ('fechaInicio', '<=', fecha_inicio), ('fechaFinal', '>=', fecha_inicio),
                    '&', ('fechaInicio', '<=', fecha_final), ('fechaFinal', '>=', fecha_final)
                ])
                if not alquileres:
                    inmuebles_disponibles.append({
                        'name': inmueble.name,
                        'localizacion': inmueble.localizacion,
                        # Agrega otros campos que desees devolver
                    })

            return {
                "status": 200,
                "inmuebles": inmuebles_disponibles
            }

        except Exception as error:
            data = {
                "status": 500,
                "error": str(error)
            }
            return data

    #put
    @http.route('/InstantAbode/modificarCliente', type='json', auth='public', methods=['PUT'])
    def modificarCliente(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.cliente"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":"Error, no existe el cliente."
                }   
                return data
            
            result.sudo().write(response)
            data={
                "status":200,
                "id":result.id
            }
            return data
       
       except Exception as error:
            data={
                "status":400,
                "error":str(error)
            }
            return data