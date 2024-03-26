# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request
import datetime

class InstantAbode(http.Controller):

    #
    #Cliente
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
                return {"status": 400, "error": "Ya existe un cliente con ese nombre de usuario."}
            
            propietario = request.env['instant_abode.propietario'].sudo().search([('name', '=', username)])
            if propietario.exists():
                return {"status": 400, "error": "Ya existe un propietario con ese nombre de usuario."}
            
            result = http.request.env["instant_abode.cliente"].sudo().create(response)

            data={
                "status":201,
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
                alquileres = inmueble.alquileres.filtered(lambda a: a.fechaInicio <= fecha_final and a.fechaFinal >= fecha_inicio)
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
        #
        #Propietario
        #

    #post
    @http.route('/InstantAbode/nuevoInmueble', type='json', auth='public', methods=['POST'], csrf=False)
    def nuevoInmueble(self, **kw):
        response = request.httprequest.json
        try:
            propietario = response.get('propietario')
            existe = request.env['instant_abode.propietario'].sudo().browse(propietario)
            if existe:
                result = http.request.env["instant_abode.inmueble"].sudo().create(response)

                data={
                    "status":201,
                    "id":result.id
                }
                return data
            else:
                return {"status": 400, "error": "No existe el propietario."}
            
        except Exception as error:
            data={
                "status":500,
                "error": str(error)
            }
            return data
