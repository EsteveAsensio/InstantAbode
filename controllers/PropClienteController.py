# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import json
from odoo.http import request

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

    #put
    @http.route('/InstantAbode/modificarUser', type='json', auth='public', methods=['PUT'])
    def modificarUser(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["trufflesapp.order"].sudo().search([("id","=",response["id"])])
            if not result.exists():
                data={
                "status":400,
                "id":result.id
                }   
                return data
            
            if result.state == "Confirmed" or result.state == "Invoiced":
                data={
                "status":400,
                "error":"You cant modify this order because is alredy Confirmed or Invoiced"
                }   
                return data
            
            base = response.get('base')
            if base:
                return {"status": 400, "error": "You cant change the price"}
            
            totalIva = response.get('totalIva')
            if totalIva:
                return {"status": 400, "error": "You cant change the price"}
            
            active = response.get('active')
            if active:
                return {"status": 400, "error": "You dont have permissions to modify the active"}

            vendor = response.get('vendor')
            if not vendor:
                return {"status": 400, "error": "The vendor is required"}

            partner = request.env['res.partner'].sudo().browse(vendor)
            if not partner.exists():
                return {"status": 404, "error": "Vendor not found."}
            
            invoice = response.get('invoice')
            if invoice:
                return {"status": 400, "error": "You dont have permissions to modify the invoice"}

            state = response.get('state')
            if state:
                return {"status": 400, "error": "You cant change the state manually"}
            
            result.sudo().write(response)
            data={
                "status":200,
                "id":result.id
            }
            return data
       except Exception as error:
            data={
                "status":404,
                "error":error
            }
            return data
       
