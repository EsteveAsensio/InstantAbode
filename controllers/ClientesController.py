# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import json
from odoo.http import request, Response
import datetime

class ClientesController(http.Controller):

    #post
    @http.route('/InstantAbode/registrarNuevoUsuario', type='json', auth='public', methods=['POST'], csrf=False)
    def registrarNuevoUsuario(self, **kw):
        response = request.httprequest.json
        try:
    
            result = http.request.env["instant_abode.cliente"].sudo().create(response)

            data={
                "status":200,
                "message":"Nuevo usuario añadido."
            }
            return data
        except ValidationError as ve:
            return {"status": 400, "message": str(ve)}
        except Exception as error:
            return {"status": 500, "message": str(error)}

    #GET
    @http.route('/InstantAbode/provincias', type='http', auth='public', methods=['GET'])
    def get_provincias(self):
        provincias_data = request.env['instant_abode.inmueble'].sudo().read_group(
            [('state', '=', 'Mostrar')], 
            ['provincia'],  
            ['provincia']  
        )
        provincias = [prov['provincia'] for prov in provincias_data if prov['provincia']]
        response = json.dumps(provincias)
        return request.make_response(response, [('Content-Type', 'application/json')])
        
    #GET
    @http.route(['/InstantAbode/inmueblesAlquilados/<int:idUser>'], auth='public', type="http", methods=['GET'])
    def inmueblesAlquilados(self, idUser):
        try:
            alquileres = request.env['instant_abode.alquiler'].sudo().search([('cliente.id', '=', idUser)])

            if not alquileres:
                data = json.dumps({'status': 400, 'message': 'Todavía no has alquilado ningún inmueble.'})
                return Response(data, content_type='application/json', status=200)

            alquileres_dispo = []


            for alquiler in alquileres:
                fechaIn_formateada = alquiler.fechaInicio.strftime("%Y-%m-%d")
                fechaFin_formateada = alquiler.fechaFinal.strftime("%Y-%m-%d")

                valoracion_data = {}
                valoracion = request.env['instant_abode.valoracioninmueble'].sudo().search([('alquiler.id', '=', alquiler.id)])

                if valoracion:
                    valoracion_data = {
                    'id': valoracion.id,
                    'name': valoracion.name,
                    'comentario': valoracion.comentario,
                    'puntuacion': valoracion.puntuacion,
                    'fecha': valoracion.fecha.strftime("%Y-%m-%d") if valoracion.fecha else None
                    }
                else:
                    valoracion_data = None
                    
                alquileres_dispo.append({
                        'id' : alquiler.id,
                        'name': alquiler.name,
                        'fechaInicio': fechaIn_formateada,
                        'fechaFinal': fechaFin_formateada,
                        'precio': alquiler.precio,
                        'inmueble': {
                            'id' : alquiler.inmueble.id,
                            'name' : alquiler.inmueble.name,
                            'imagenPrincipal': 'http://localhost:8069/web/image?model=instant_abode.inmueble&id={}&field=imagenPrincipal'.format(alquiler.inmueble.id),
                            'localizacion' : alquiler.inmueble.localizacion,
                            'provincia' : alquiler.inmueble.provincia
                        },
                        'valoracionInmueble': valoracion_data
                    })
                
            data = json.dumps({'status': 200, 'inmuebles': alquileres_dispo})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'message': str(error)})
            return Response(data, content_type='application/json', status=500)
        
        
    #post
    @http.route(['/InstantAbode/buscarInmuebles'], auth='public', type="json", methods=['POST'], csrf=False)
    def buscarInmuebles(self, **kw):
        try:
            response = request.httprequest.json

            provincia = response.get('provincia')
            fecha_inicio_str = response.get('fechaInicio')
            fecha_final_str = response.get('fechaFinal')

            fecha_inicio = datetime.datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
            fecha_final = datetime.datetime.strptime(fecha_final_str, "%Y-%m-%d").date()

            inmuebles = request.env['instant_abode.inmueble'].sudo().search([
                ('provincia', '=', provincia),
                ('state', '=', 'Mostrar'),
            ])

            if not inmuebles:
                return {"status": 400, "message": "No hay inmuebles disponibles."}

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
                    diferencia_dias = (fecha_final - fecha_inicio).days

                    if diferencia_dias <= 0:
                        return {"status": 400, "message": "La fecha final debe ser posterior a la fecha de inicio."}
                    
                    precioAlquiler = diferencia_dias * inmueble.precio
                    inmuebles_disponibles.append({
                        'id' : inmueble.id,
                        'name': inmueble.name,
                        'provincia': inmueble.provincia,
                        'localizacion': inmueble.localizacion,
                        'habitaciones': inmueble.habitaciones,
                        'banyos' : inmueble.banyos,
                        'metrosCuadrados' : inmueble.metrosCuadrados,
                        'descripcion' : inmueble.descripcion,
                        'adicionales' : inmueble.adicionales,
                        'precio' : inmueble.precio,
                        'precioAlquiler' : precioAlquiler,
                        'imagenPrincipal': 'http://localhost:8069/web/image?model=instant_abode.inmueble&id={}&field=imagenPrincipal'.format(inmueble.id),
                        'imagenes': ['http://localhost:8069/web/image?model=ir.attachment&id={}'.format(img.id) for img in inmueble.imagenes]
                    })

            return {
                "status": 200,
                "inmuebles": inmuebles_disponibles
            }

        except Exception as error:
            data = {
                "status": 500,
                "message": str(error)
            }
            return data
        
    #GET
    @http.route(['/InstantAbode/infoInmueble/<int:idInmueble>'], auth='public', type="http", methods=['GET'])
    def infoInmueble(self, idInmueble):
        try:
            inmueble = request.env['instant_abode.inmueble'].sudo().search([('id', '=', idInmueble)])

            if not inmueble:
                data = json.dumps({'status': 400, 'message': 'Ya no existe ese inmueble'})
                return Response(data, content_type='application/json', status=200)

            lista_valoraciones = self.valoracionesInmueble(inmueble.id)

            inmuebleInfo = {
                'id' : inmueble.id,
                'name': inmueble.name,
                'provincia': inmueble.provincia,
                'localizacion': inmueble.localizacion,
                'habitaciones': inmueble.habitaciones,
                'banyos' : inmueble.banyos,
                'metrosCuadrados' : inmueble.metrosCuadrados,
                'descripcion' : inmueble.descripcion,
                'adicionales' : inmueble.adicionales,
                'precio' : inmueble.precio,
                'imagenPrincipal': 'http://localhost:8069/web/image?model=instant_abode.inmueble&id={}&field=imagenPrincipal'.format(inmueble.id),
                'imagenes': ['http://localhost:8069/web/image?model=ir.attachment&id={}'.format(img.id) for img in inmueble.imagenes],
                'valoraciones' : lista_valoraciones
            }


            data = json.dumps({'status': 200, 'inmueble': inmuebleInfo})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'message': str(error)})
            return Response(data, content_type='application/json', status=500)
        
    #GET
    def valoracionesInmueble(self, idInmueble):
        try:
            valoraciones = request.env['instant_abode.valoracioninmueble'].sudo().search([('alquiler.inmueble.id', '=', idInmueble)])

            lista_valoraciones = []

            for valoracion in valoraciones:
                # Convertir la fecha a una cadena en el formato deseado, por ejemplo 'YYYY-MM-DD'
                fecha_formateada = valoracion.fecha.strftime("%Y-%m-%d") if valoracion.fecha else None

                clienteInfo = self.clienteValoracion(valoracion.cliente.id)
                lista_valoraciones.append({
                    'id': valoracion.id,
                    'name': valoracion.name,
                    'comentario': valoracion.comentario,
                    'puntuacion': valoracion.puntuacion,
                    'fecha': fecha_formateada,
                    'cliente': clienteInfo
                })

            return lista_valoraciones
        except Exception as error:
            return str(error)
        

    def clienteValoracion(self, idCliente):
        try:
            cliente = request.env['instant_abode.cliente'].sudo().search([('id', '=', idCliente)])

            clienteInfo = {
                'id' : cliente.id,
                'name' : cliente.name,
                'imagen' : 'http://localhost:8069/web/image?model=instant_abode.cliente&id={}&field=imagen'.format(cliente.id),
            }

            return clienteInfo
        except Exception as error:
            return str(error)
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
                "message":str(error)
            }
            return data
       

    #GET
    @http.route(['/InstantAbode/valoracionesUsuario/<int:idUser>'], auth='public', type="http", methods=['GET'])
    def valoracionesUsuario(self, idUser):
        try:
            valoraciones = request.env['instant_abode.valoracioninmueble'].sudo().search([('cliente.id', '=', idUser)])

            if not valoraciones:
                data = json.dumps({'status': 400, 'message': 'El usuario no ha realizado ninguna valoración.'})
                return Response(data, content_type='application/json', status=200)

            lista_valoraciones = []

            for valoracion in valoraciones:
                # Convertir la fecha a una cadena en el formato deseado, por ejemplo 'YYYY-MM-DD'
                fecha_formateada = valoracion.fecha.strftime("%Y-%m-%d") if valoracion.fecha else None

                lista_valoraciones.append({
                    'id': valoracion.id,
                    'name': valoracion.name,
                    'comentario': valoracion.comentario,
                    'puntuacion': valoracion.puntuacion,
                    'fecha': fecha_formateada,
                    'alquiler': {
                        'id': valoracion.alquiler.id, 
                        'name': valoracion.alquiler.name,
                        'inmueble' : {
                            'id': valoracion.alquiler.inmueble.id,
                            'imagenPrincipal': 'http://localhost:8069/web/image?model=instant_abode.inmueble&id={}&field=imagenPrincipal'.format(valoracion.alquiler.inmueble.id),
                        }
                    }
                })

            data = json.dumps({'status': 200, 'valoraciones': lista_valoraciones})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'message': str(error)})
            return Response(data, content_type='application/json', status=500)


    #delete
    @http.route('/InstantAbode/eliminarValoracionInmueble/<int:valoracionid>', type='http', auth='public', methods=['DELETE'], csrf=False)
    def eliminarValoracionInmueble(self, valoracionid):
        try:
            valoracion = request.env['instant_abode.valoracioninmueble'].sudo().browse(valoracionid)
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
    @http.route('/InstantAbode/addValoracionInmueble', type='json', auth='public', methods=['POST'])
    def addValoracionInmueble(self, **kw):
        response = request.httprequest.json
        try:

            alquiler = request.env['instant_abode.alquiler'].sudo().search([('id', '=', response.get('idAlquiler'))])

            if not alquiler:
                return {
                    "status": 400,
                    "message": "No se encontró el alquiler especificado."
                }

            # Crear la nueva valoración
            nueva_valoracion = request.env['instant_abode.valoracioninmueble'].sudo().create({
                'name': response.get('name'),
                'comentario': response.get('comentario'),
                'puntuacion': response.get('puntuacion'),
                'fecha': response.get('fecha'),
                'alquiler': alquiler.id
            })

            return {
                "status": 200,
                "message": "Valoración creada correctamente."
            }
       
        except Exception as error:
            return {
                "status": 500,
                "message":str(error)
            }
       
    #put
    @http.route('/InstantAbode/modificarValoracionInmueble', type='json', auth='public', methods=['PUT'])
    def modificarValoracionInmueble(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.valoracioninmueble"].sudo().search([("id","=",response["id"])])

            if not result.exists():
                data={
                "status":400,
                "message":"No existe la valoración"
                }   
                return data
            
            result.sudo().write(response)
            data={
                "status":200,
                "message":"Valoración modificada"
            }
            return data
       except Exception as error:
            data={
                "status":500,
                "message":str(error)
            }
            return data