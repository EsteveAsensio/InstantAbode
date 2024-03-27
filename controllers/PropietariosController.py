# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request

class PropietariosController(http.Controller):
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
        
    #put
    @http.route('/InstantAbode/modificarPropietario', type='json', auth='public', methods=['PUT'])
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