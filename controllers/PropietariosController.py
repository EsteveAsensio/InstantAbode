# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request, Response

class PropietariosController(http.Controller):
    #put
    @http.route('/InstantAbode/modificarPropietario', type='json', auth='user', methods=['PUT'])
    def modificarPropietario(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.propietario"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":"Error, no existe el propietario."
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
       
    #post
    @http.route('/InstantAbode/nuevoInmueble', type='json', auth='user', methods=['POST'], csrf=False)
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
        
    #put
    @http.route('/InstantAbode/modificarInmueble', type='json', auth='user', methods=['PUT'], csrf=False)
    def modificarInmueble(self, **kw):
        response = request.httprequest.json
        try:
            result = http.request.env["instant_abode.inmueble"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":"Error, no existe el inmueble."
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
        
    #put
    @http.route('/InstantAbode/modificarValoracionCliente', type='json', auth='public', methods=['PUT'])
    def modificarValoracionCliente(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.valoracioncliente"].sudo().search([("id","=",response["id"])])

            if not result.exists():
                data={
                "status":400,
                "message":"No existe la valoración"
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
                "message":str(error)
            }
            return data
       
    #delete
    @http.route('/InstantAbode/eliminarValoracionCliente/<int:valoracionid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def eliminarValoracionInmueble(self, valoracionid):
        valoracion = request.env['instant_abode.valoracioncliente'].sudo().browse(valoracionid)
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