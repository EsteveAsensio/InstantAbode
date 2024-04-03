# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request, Response
import datetime

class ClientesController(http.Controller):

    #post
    @http.route('/InstantAbode/registrarNuevoUsuario', type='json', auth='public', methods=['POST'], csrf=False)
    def registrarNuevoUsuario(self, **kw):
        response = request.httprequest.json
        try:
            username = response.get('name')
            contrasenya = response.get('contrasenya')
            propietario = request.env['instant_abode.propietario'].sudo().search([('name', '=', username)])
            if propietario.exists():
                return {"status": 400, "error": "Ya existe un usuario con ese nombre."}
            
            propietario = request.env['instant_abode.propietario'].sudo().search([('contrasenya', '=', contrasenya)])
            if propietario.exists():
                return {"status": 400, "error": "La contraseña introducida ya existe."}
            
            result = http.request.env["instant_abode.cliente"].sudo().create(response)

            data={
                "status":200,
                "result":"Nuevo usuario añadido."
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
                "status":500,
                "error":str(error)
            }
            return data
       
    #delete
    @http.route('/InstantAbode/eliminarValoracionInmueble/<int:valoracionid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def eliminarValoracionInmueble(self, valoracionid):
        valoracion = request.env['instant_abode.valoracioninmueble'].sudo().browse(valoracionid)
        try:
            if not valoracion.exists():
                data = json.dumps({'status': 400, 'message': 'Valoración no encontrada.'})
                return Response(data, content_type='application/json', status=400)

            valoracion.unlink()

            data = json.dumps({'status': 200, 'message': 'Valoración eliminada correctamente.'})
            return Response(data, content_type='application/json', status=200)
    
        except Exception as error:
            data = json.dumps({'status': 500, 'message': error})
            return Response(data, content_type='application/json', status=400)
        
    #put
    @http.route('/InstantAbode/modificarValoracionInmueble', type='json', auth='public', methods=['PUT'])
    def modificarValoracionInmueble(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.valoracioninmueble"].sudo().search([("id","=",response["id"])])

            if not result.exists():
                data={
                "status":400,
                "error":"No existe la valoración"
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
                "status":500,
                "error":str(error)
            }
            return data