# -*- coding: utf-8 -*-
from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import json
from odoo.http import request, Response
import datetime
import re

class ClientesController(http.Controller):

    @http.route(['/InstantAbode/login'], auth='public', type="json", methods=['POST'], csrf=False)
    def login(self, **kw):
        try:
            request_data = json.loads(request.httprequest.data)
            username = request_data.get('username')
            contrasenya = request_data.get('contrasenya')

            if not username or not contrasenya:
                return {'status': 400, 'titulo' : 'Login Cliente', 'message': 'Datos de usuario incompletos'}

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
                    'imagen': 'http://localhost:8069/web/image?model=instant_abode.cliente&id={}&field=imagen'.format(cliente.id)
                }
                return {'status': 200, 'titulo' : 'Login Cliente', 'usuario': usuario}
            else:
                return {'status': 400, 'titulo' : 'Login Cliente', 'message': 'Usuario no encontrado o contraseña incorrecta'}
        except Exception as error:
            data = {
                "status": 500,
                'titulo' : 'Login Cliente',
                "message": str(error)
            }
            return data

                #GET
    @http.route(['/InstantAbode/getCliente/<int:idUser>'], auth='user', type="http", methods=['GET'])
    def getCliente(self, idUser):
        try:
            cliente = request.env['instant_abode.cliente'].sudo().search([('id', '=', idUser)])

            if not cliente:
                data = json.dumps({'status': 400, 'titulo' : 'Obtener Cliente', 'message' : 'El cliente ya no existe. Cierra la sesión lo antes posible.'})
                return Response(data, content_type='application/json', status=200)

            usuario = {
                'id': cliente.id,
                'dni': cliente.dni,
                'nombreCliente': cliente.nombreCliente,
                'apellidos': cliente.apellidos,
                'telefono': cliente.telefono,
                'name': cliente.name,
                'contrasenya': cliente.contrasenya,
                'correo': cliente.correo,
                'imagen': 'http://localhost:8069/web/image?model=instant_abode.cliente&id={}&field=imagen'.format(cliente.id)
            }

            data = json.dumps({'status': 200, 'titulo' : 'Obtener Cliente', 'cliente': usuario})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Obtener Cliente', 'message': str(error)})
            return Response(data, content_type='application/json', status=500)
        
        
    #post
    @http.route('/InstantAbode/registrarNuevoUsuario', type='json', auth='public', methods=['POST'], csrf=False)
    def registrarNuevoUsuario(self, **kw):
        response = request.httprequest.json
        try:
    
            http.request.env["instant_abode.cliente"].sudo().create(response)

            data={
                "status":200,
                'titulo' : 'Usuario Registrado',
                "message":"Nuevo usuario añadido."
            }
            return data
        except ValidationError as ve:
            return {"status": 400, 'titulo' : 'Registrar Usuario', "message": str(ve)}
        except Exception as error:
            return {"status": 500, 'titulo' : 'Registrar Usuario', "message": str(error)}

    #GET
    @http.route('/InstantAbode/provincias', type='http', auth='user', methods=['GET'])
    def get_provincias(self):
        try:
            provincias_data = request.env['instant_abode.inmueble'].sudo().read_group(
                [('state', '=', 'Mostrar')], 
                ['provincia'],  
                ['provincia']  
            )
            provincias = [prov['provincia'] for prov in provincias_data if prov['provincia']]
            data = json.dumps({'status': 200, 'titulo' : 'Obtener las Provincias', 'provincias': provincias})
            return Response(data, content_type='application/json', status=200)
        
        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Obtener las Provincias', 'message': str(error)})
            return Response(data, content_type='application/json', status=500)    
        
    #GET
    @http.route(['/InstantAbode/inmueblesAlquilados/<int:idUser>'], auth='user', type="http", methods=['GET'])
    def inmueblesAlquilados(self, idUser):
        try:
            alquileres = request.env['instant_abode.alquiler'].sudo().search([('cliente.id', '=', idUser)])

            if not alquileres:
                data = json.dumps({'status': 400, 'titulo' : 'Alquileres', 'message': 'Todavía no has alquilado ningún inmueble.'})
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
                
            data = json.dumps({'status': 200, 'titulo' : 'Nuevo Alquiler Realizado', 'inmuebles': alquileres_dispo})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Alquileres', 'message': str(error)})
            return Response(data, content_type='application/json', status=500)
        
        
    #post
    @http.route(['/InstantAbode/buscarInmuebles'], auth='user', type="json", methods=['POST'], csrf=False)
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
                return {"status": 400, 'titulo' : 'Buscar Inmuebles', "message": "No hay inmuebles disponibles."}

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
                        return {"status": 400, 'titulo' : 'Buscar Inmuebles', "message": "La fecha final debe ser posterior a la fecha de inicio."}

                    fecha_inicio_iso = fecha_inicio.isoformat()
                    fecha_final_iso = fecha_final.isoformat()
                    
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
                        'imagenes': ['http://localhost:8069/web/image?model=ir.attachment&id={}'.format(img.id) for img in inmueble.imagenes],
                        'fechaInicio' : fecha_inicio_iso,
                        "fechaFinal" : fecha_final_iso
                    })

            return {
                "status": 200,
                'titulo' : 'Buscar Inmuebles', 
                "inmuebles": inmuebles_disponibles
            }

        except Exception as error:
            data = {
                "status": 500,
                'titulo' : 'Buscar Inmuebles', 
                "message": str(error)
            }
            return data
        
    #GET
    @http.route(['/InstantAbode/infoInmueble/<int:idInmueble>'], auth='user', type="http", methods=['GET'])
    def infoInmueble(self, idInmueble):
        try:
            inmueble = request.env['instant_abode.inmueble'].sudo().search([('id', '=', idInmueble)])

            if not inmueble:
                data = json.dumps({'status': 400, 'titulo' : 'Información Inmueble', 'message': 'Ya no existe ese inmueble'})
                return Response(data, content_type='application/json', status=200)

            if inmueble.state == "Ocultar":
                data = json.dumps({'status': 400, 'titulo' : 'Información Inmueble', 'message': 'El inmueble ya no está cara al público'})
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


            data = json.dumps({'status': 200, 'titulo' : 'Información Inmueble', 'inmueble': inmuebleInfo})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Información Inmueble', 'message': str(error)})
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

    @http.route('/InstantAbode/realizarAlquiler', type='json', auth='user', methods=['POST'])
    def realizarAlquiler(self, **kw):
        response = request.httprequest.json
        try:
            cliente_id = response.get("cliente")
            inmueble_id = response.get("inmueble")
            fecha_inicio = response.get("fechaInicio")
            fecha_final = response.get("fechaFinal")

            existe_cliente = request.env['instant_abode.cliente'].sudo().search([("id", '=', cliente_id)])
            if not existe_cliente:
                return {"status": 400, 'titulo' : 'Realizar Alquiler', "message": "El usuario con el que está iniciado sesión no existe. Cerra sesión lo antes posible."}
            
            existe_inmueble = request.env['instant_abode.inmueble'].sudo().search([("id", '=', inmueble_id)])
            if not existe_inmueble:
                return {"status": 400, 'titulo' : 'Realizar Alquiler', "message": "El inmueble ya no existe."}

            if existe_inmueble.state == 'Ocultar':
                return {"status": 400, 'titulo' : 'Realizar Alquiler', "message": "El inmueble ya no está cara al público."}

            alquiler_data = {
                'cliente': cliente_id,
                'inmueble': inmueble_id,
                'fechaInicio': fecha_inicio,
                'fechaFinal': fecha_final
            }
            request.env['instant_abode.alquiler'].sudo().create(alquiler_data)

            return {"status": 200, 'titulo' : 'Realizar Alquiler', "message": "Alquiler realizado con éxito."}

        except Exception as error:
            return {"status": 500, 'titulo' : 'Realizar Alquiler', "message": str(error)}

        
    @http.route('/InstantAbode/modificarCliente', type='json', auth='user', methods=['PUT'])
    def modificarCliente(self, **kw):
        response = request.httprequest.json
        try:
            cliente_obj = request.env["instant_abode.cliente"]
            cliente_actual = cliente_obj.sudo().search([("id", "=", response["id"])])
            
            if not cliente_actual.exists():
                return {
                    "status": 400,
                    'titulo' : 'Modificar Perfil',
                    "message": "El usuario con el que está iniciado sesión no existe. Cerra sesión lo antes posible."
                }

            # Verificar la unicidad en los campos críticos del usuario asociado
            campos_unicos = {
                'vat': 'DNI',
                'email': 'correo electrónico',
                'phone': 'teléfono',
                'login': 'nombre de usuario (login)'
            }

            for campo, descripcion in campos_unicos.items():
                if campo in response and getattr(cliente_actual, campo, None) != response[campo]:
                    dominio = [(campo, '=', response[campo])]
                    if campo == 'name':
                        dominio.append(('id', '!=', cliente_actual.user_id.id))
                    else:
                        dominio.append(('partner_id', '!=', cliente_actual.user_id.partner_id.id))
                    
                    if request.env['res.users'].sudo().search(dominio).exists():
                        return {
                            "status": 400,
                            'titulo' : 'Modificar Perfil',
                            "message": f"El {descripcion} {response[campo]} ya está registrado en otro usuario."
                        }
                    
            cliente_actual.sudo().write(response)

            #antes de devolver 200 comprobar respuesta del .write
            return {
                "status": 200,
                'titulo' : 'Modificar Perfil',
                "message": 'Modificaciones realizadas con éxito.'
            }

        except Exception as error:
            return {
                "status": 500,
                'titulo' : 'Modificar Perfil',
                "message": str(error)
            }


    #GET
    @http.route(['/InstantAbode/valoracionesUsuario/<int:idUser>'], auth='user', type="http", methods=['GET'])
    def valoracionesUsuario(self, idUser):
        try:
            valoraciones = request.env['instant_abode.valoracioninmueble'].sudo().search([('cliente.id', '=', idUser)])

            if not valoraciones:
                data = json.dumps({'status': 400, 'titulo' : 'Obtener Valoraciones', 'message': 'El usuario no ha realizado ninguna valoración.'})
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

            data = json.dumps({'status': 200, 'titulo' : 'Obtener Valoraciones', 'valoraciones': lista_valoraciones})
            return Response(data, content_type='application/json', status=200)

        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Obtener Valoraciones', 'message': str(error)})
            return Response(data, content_type='application/json', status=500)


    #delete
    @http.route('/InstantAbode/eliminarValoracionInmueble/<int:valoracionid>', type='http', auth='user', methods=['DELETE'], csrf=False)
    def eliminarValoracionInmueble(self, valoracionid):
        try:
            valoracion = request.env['instant_abode.valoracioninmueble'].sudo().browse(valoracionid)
            if not valoracion.exists():
                data = json.dumps({'status': 400, 'titulo' : 'Eliminar Valoración', 'message': 'Valoración no encontrada.'})
                return Response(data, content_type='application/json', status=400)

            valoracion.unlink()

            data = json.dumps({'status': 200, 'titulo' : 'Eliminar Valoración', 'message': 'Valoración eliminada correctamente.'})
            return Response(data, content_type='application/json', status=200)
    
        except Exception as error:
            data = json.dumps({'status': 500, 'titulo' : 'Eliminar Valoración', 'message': error})
            return Response(data, content_type='application/json', status=400)
        
        
    #put
    @http.route('/InstantAbode/addValoracionInmueble', type='json', auth='user', methods=['POST'])
    def addValoracionInmueble(self, **kw):
        response = request.httprequest.json
        try:

            alquiler = request.env['instant_abode.alquiler'].sudo().search([('id', '=', response.get('idAlquiler'))])

            if not alquiler:
                return {
                    "status": 400,
                    'titulo' : 'Añadir Valoración',
                    "message": "No se encontró el alquiler especificado."
                }
            
            if response.get('puntuacion') < 1 or response.get('puntuacion') > 10:
                return {
                    "status": 400,
                    'titulo': 'Añadir Valoración',
                    "message": "La puntuación debe estar entre 1 y 10."
                }

            # Crear la nueva valoración (mal)
            request.env['instant_abode.valoracioninmueble'].sudo().create({
                'name': response.get('name'),
                'comentario': response.get('comentario'),
                'puntuacion': response.get('puntuacion'),
                'fecha': response.get('fecha'),
                'alquiler': alquiler.id
            })

            return {
                "status": 200,
                'titulo' : 'Añadir Valoración',
                "message": "Valoración creada y añadida correctamente."
            }
       
        except Exception as error:
            return {
                "status": 500,
                'titulo' : 'Añadir Valoración',
                "message":str(error)
            }
       
    #put
    @http.route('/InstantAbode/modificarValoracionInmueble', type='json', auth='user', methods=['PUT'])
    def modificarValoracionInmueble(self, **kw):
       response = request.httprequest.json
       try:
            result = http.request.env["instant_abode.valoracioninmueble"].sudo().search([("id","=",response["id"])])

            if not result.exists():
                data={
                "status":400,
                'titulo' : 'Modificar Valoración',
                "message":"No existe la valoración que intenta modificar."
                }   
                return data
            
            if response.get('puntuacion') < 1 or response.get('puntuacion') > 10:
                return {
                    "status": 400,
                    'titulo': 'Añadir Valoración',
                    "message": "La puntuación debe estar entre 1 y 10."
                }
            
            result.sudo().write(response)
            data={
                "status":200,
                'titulo' : 'Modificar Valoración',
                "message":"Valoración modificada con éxito"
            }
            return data
       except Exception as error:
            data={
                "status":500,
                'titulo' : 'Modificar Valoración',
                "message":str(error)
            }
            return data

    @http.route(['/registro_propietario'], type='http', auth="public", website=True)
    def registro_propietario(self, **kw):
        return request.render("instant_abode.form_registro_propietario")
    

    @http.route('/create_propietario', type='http', auth='public', methods=['POST'], website=True)
    def create_propietario(self, **post):
        # Preparar los datos para la creación del registro Propietario
        propietario_vals = {
            'dni': post.get('vat'), 
            'correo': post.get('email'), 
            'telefono': post.get('phone'),
            'nombreCliente': post.get('nombreCliente'), 
            'apellidos': post.get('apellidos'),
            'name': post.get('name'),
            'contrasenya': post.get('contrasenya')
        }

        # Verificación de unicidad en el modelo res.partner y res.users
        campos_partner = {'dni': 'vat', 'correo': 'email', 'telefono': 'phone'}
        for campo, partner_field in campos_partner.items():
            valor = propietario_vals[campo]
            if valor:
                dominio = [(partner_field, '=', valor)]
                existe = request.env['res.partner'].sudo().search(dominio, limit=1)
                if existe:
                    descripcion = {'dni': 'DNI', 'correo': 'correo electrónico', 'telefono': 'teléfono'}[campo]
                    return request.render("instant_abode.error_template", {
                        'message': f"El {descripcion} {valor} ya está registrado en otro usuario."
                    })

        # Verificar la unicidad del nombre de usuario en res.users
        if propietario_vals['name']:
            user_exist = request.env['res.users'].sudo().search([('login', '=', propietario_vals['name'])], limit=1)
            if user_exist:
                return request.render("instant_abode.error_template", {
                    'message': "El nombre de usuario ya está registrado."
                })

        # Verificación de formato
        if not self.validar_correo(propietario_vals['correo']):
            return request.render("instant_abode.error_template", {'message': "El formato del correo es invalido."})
        
        if not self.validar_telefono(propietario_vals['telefono']):
            return request.render("instant_abode.error_template", {'message': "El teléfono debe ser de 9 dígitos."})

        if not self.validar_dni(propietario_vals['dni']):
            return request.render("instant_abode.error_template", {'message': "El formato del DNI es incorrecto."})

        # Crear el propietario
        Propietario = request.env['instant_abode.propietario'].sudo()
        Propietario.create(propietario_vals)

        return request.redirect('/contactus-thank-you')

    def validar_correo(self, correo):
        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            return False
        return True

    def validar_telefono(self, telefono):
        if telefono and len(str(telefono)) != 9:
            return False
        return True

    def validar_dni(self, dni):
        if not dni:
            return False
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        if len(dni) != 9:
            return False
        else:
            numero = dni[:-1]
            letra = dni[-1]
            if not numero.isdigit():
                return False
            numero = int(numero)
            correcto = letras[numero % 23]
            if letra != correcto:
                return False
        return True

