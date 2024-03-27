# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request, Response

class PropClienteController(http.Controller):

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


       
