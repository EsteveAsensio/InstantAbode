from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re
import random
import string
import smtplib
from email.message import EmailMessage
import ssl

class Propietario(models.Model):
    _name = 'instant_abode.propietario'
    _description = 'Información sobre los Propietarios que inician sesión en la aplicación.'

    #Infomarción Personal
    dni = fields.Char(string="DNI", help="DNI del propietario", required=True) #No repetidos y formato
    nombreCliente = fields.Char(string="Nombre", help="Nombre del propietario", required=True)
    apellidos = fields.Char(string="Apellidos", help="Apellidos del propietario")
    correo = fields.Char(string="Correo", help="Correo del propietario", required=True) #No repetidos y formato
    telefono = fields.Char(string="Teléfono", help="Teléfono del propietario") #No repetidos y numeros

    #Notificación
    concepto = fields.Char(string="Concepto", help="Experiencia o información del trabajador") #No repetidos y numeros
    notificado = fields.Boolean(string= "Notificado", help="Saber si el propietario ha sido informado o no.", readonly=True, default=False)
    #Información Cuenta Usuario
    name = fields.Char(string="Nombre de Usuario", help="Nombre del usuario", required=True) #No repetidos
    contrasenya = fields.Char(string="Contraseña", help="Contraseña del usuario", required=True) #No repetidos y formato
    imagen = fields.Binary(string="Imagen", help="Foto del propietario", store=True)
    #Valoraciones hacia Clientes
    valoracionesClientes = fields.One2many("instant_abode.valoracioncliente", "propietario")
    #Inmuebles Propietario
    inmuebles = fields.One2many("instant_abode.inmueble", "propietario")

    user_id = fields.Many2one("res.users", string="Usuario Asociado", readonly=True)

    @api.constrains("name")
    def comprobarNombre(self):
        if self.env['instant_abode.cliente'].search([('name', '=', self.name)]):
                raise ValidationError("Este nombre de usuario ya está registrado.")
        
    @api.constrains("correo")
    def comprobarCorreo(self):
        if self.correo and not re.match(r"[^@]+@[^@]+\.[^@]+", self.correo):
            raise ValidationError("El formato del correo es invalido.")
        
    @api.constrains("telefono")
    def comprobarTelefono(self):
        if self.telefono:
            if len(str(self.telefono)) != 9:
                raise ValidationError("El teléfono debe ser de 9 dígitos.")

    @api.constrains("dni")
    def comprobarDNI(self):
        letras = "TRWAGMYFPDXBNJZSQVHLCKE"
        if(len(self.dni) != 9):
             raise ValidationError("El DNI necesita 8 dígitos y una letra.")
        else:
            numero = self.dni[:-1]
            letra = self.dni[-1]
            if not numero.isdigit():
                raise ValidationError("La primera parte del DNI solo debe contener dígitos.")

            numero = int(numero)

            correcto = letras[numero % 23]
            if letra != correcto:
                 raise ValidationError("La letra del DNI es incorrecta.") 
            
            
    @api.constrains("contrasenya")      
    def comrpobarContrasenya(self):
        # Menos 5 letras
        if len(re.findall(r'[a-zA-Z]', self.contrasenya)) < 5:
            raise ValidationError("La contraseña debe tener como mínimo 5 letras.")
        
        # Carácter especial
        if not re.search(r'[!@#$%^&*()_+{}\|:"<>?~\[\];\',./]', self.contrasenya):
            raise ValidationError("La contraseña debe tener como mínimo 1 carácter especial.")
        
        # Un número
        if not re.search(r'\d', self.contrasenya):
            raise ValidationError("La contraseña debe tener como mínimo 1 dígito")
        
    @api.model
    def create(self, vals):
        self.validar_unicidad(vals)
        cliente = super(Propietario, self).create(vals)
        return cliente
    
    def unlink(self):
        grupo_propietarios = 'instant_abode.grupo_propietarios'
        if self.env.user.has_group(grupo_propietarios):
            if not all(self.mapped(lambda x: x.user_id.id == self.env.user.id)):
                raise ValidationError("No tiene permiso para eliminar otros propietarios.")
        for cliente in self:
            if cliente.user_id:
                partner = cliente.user_id.partner_id
                # Eliminar el usuario
                cliente.user_id.unlink() 
                
                if partner:
                    partner.unlink()

        return super(Propietario, self).unlink()

    
    def write(self, vals):
        grupo_propietarios = 'instant_abode.grupo_propietarios'
        if self.env.user.has_group(grupo_propietarios):
            if not all(self.mapped(lambda x: x.user_id.id == self.env.user.id)):
                raise ValidationError("No está autorizado para modificar el perfil de otro propietario.")

        campos_clave = ['dni', 'correo', 'telefono', 'name']
        campos_validos = {key: vals.get(key) for key in campos_clave if key in vals and vals[key]}

        if campos_validos:
            self.validar_unicidad(campos_validos)

        # Lógica para desactivar el usuario y aplicar cambios
        desactivar_usuario = False
        if 'name' in vals and vals['name'] != self.name:
            desactivar_usuario = True
        if 'dni' in vals and vals['dni'] != self.dni:
            desactivar_usuario = True
        if 'correo' in vals and vals['correo'] != self.correo:
            desactivar_usuario = True
        if 'telefono' in vals and vals['telefono'] != self.telefono:
            desactivar_usuario = True
            
        # Desactivar el usuario antes de realizar cambios si es necesario
        for cliente in self:
            if desactivar_usuario and cliente.user_id:
                cliente.user_id.active = False  # Desactivar antes de aplicar cambios

            # Actualizar el partner y el usuario asociado
            partner_vals = {}
            if 'nombreCliente' in vals:
                partner_vals['name'] = vals['nombreCliente']
            if 'correo' in vals:
                partner_vals['email'] = vals['correo']
            if 'telefono' in vals:
                partner_vals['phone'] = vals['telefono']
            if 'dni' in vals:
                partner_vals['vat'] = vals['dni']
            if 'imagen' in vals:
                partner_vals['image_1920'] = vals['imagen']
            if partner_vals and cliente.user_id.partner_id:
                cliente.user_id.partner_id.write(partner_vals)

            user_vals = {}
            if 'name' in vals:
                user_vals['login'] = vals['name']
            if 'contrasenya' in vals:
                user_vals['password'] = vals['contrasenya']
            if 'imagen' in vals:
                user_vals['image_1920'] = vals['imagen']
            if user_vals and cliente.user_id:
                cliente.user_id.write(user_vals)

            if desactivar_usuario and cliente.user_id:
                cliente.user_id.active = True  # Reactivar después de aplicar cambios
            
        return super(Propietario, self).write(vals)


    def validar_unicidad(self, vals):
        # Validar que el campo no sea None antes de hacer la búsqueda
        if 'dni' in vals and vals.get('dni'):
            existing_dni = self.env['res.partner'].search([('vat', '=', vals['dni'])])
            if len(existing_dni) > 1 or (existing_dni and existing_dni.id != self.id):
                raise ValidationError(f"El DNI {vals['dni']} ya está registrado.")

        if 'correo' in vals and vals.get('correo'):
            existing_correo = self.env['res.partner'].search([('email', '=', vals['correo'])])
            if len(existing_correo) > 1 or (existing_correo and existing_correo.id != self.id):
                raise ValidationError(f"El correo {vals['correo']} ya está registrado.")

        if 'telefono' in vals and vals.get('telefono'):
            existing_telefono = self.env['res.partner'].search([('phone', '=', vals['telefono'])])
            if len(existing_telefono) > 1 or (existing_telefono and existing_telefono.id != self.id):
                raise ValidationError(f"El teléfono {vals['telefono']} ya está registrado.")

        if 'name' in vals and vals.get('name'):
            existing_login = self.env['res.users'].search([('login', '=', vals['name'])])
            if len(existing_login) > 1 or (existing_login and existing_login.id != self.id):
                raise ValidationError(f"El nombre de usuario {vals['name']} ya está registrado.")
            
    # Comprobar si el DNI está presente y si ya está registrado en otro propietario
        if 'dni' in vals:
            dni_provided = vals.get('dni')
            if dni_provided:
                propietario = self.env['instant_abode.propietario'].search([('dni', '=', dni_provided)], limit=1)
                if propietario and propietario.id != self.id:
                    raise ValidationError(f"El dni {dni_provided} ya está registrado en otro propietario.")

        # Comprobar si el nombre de usuario está presente y si ya está registrado en otro propietario
        if 'name' in vals:
            name_provided = vals.get('name')
            if name_provided:
                propietario = self.env['instant_abode.propietario'].search([('name', '=', name_provided)], limit=1)
                if propietario and propietario.id != self.id:
                    raise ValidationError(f"El nombre de usuario {name_provided} ya está registrado en otro propietario.")

        # Comprobar si el correo está presente y si ya está registrado en otro propietario
        if 'correo' in vals:
            correo_provided = vals.get('correo')
            if correo_provided:
                propietario = self.env['instant_abode.propietario'].search([('correo', '=', correo_provided)], limit=1)
                if propietario and propietario.id != self.id:
                    raise ValidationError(f"El correo {correo_provided} ya está registrado en otro propietario.")

        # Comprobar si el teléfono está presente y si ya está registrado en otro propietario
        if 'telefono' in vals:
            telefono_provided = vals.get('telefono')
            if telefono_provided:
                propietario = self.env['instant_abode.propietario'].search([('telefono', '=', telefono_provided)], limit=1)
                if propietario and propietario.id != self.id:
                    raise ValidationError(f"El teléfono {telefono_provided} ya está registrado en otro propietario.")  
    
    def notificarPropietario(self):        
        partner = self.env['res.partner'].create({
            'name': self.nombreCliente,
            'email': self.correo,
            'phone': self.telefono,
            'vat': self.dni,
            'image_1920' : self.imagen,
        })

        new_user = self.env['res.users'].create({
            'name': self.nombreCliente,
            'login': self.name,
            'password': self.contrasenya,
            'partner_id': partner.id,
            'image_1920' : self.imagen,
        })

        self.user_id = new_user.id

        # Buscar los grupos necesarios
        grup_propietarios = self.env['res.groups'].search([('name', '=', 'Propietarios')], limit=1)
        grupo_permisos_extra = self.env['res.groups'].search([('name', '=', 'Creación de contactos')], limit=1)

        # Lista para mantener los ids de los grupos
        groups_ids = []
        if grup_propietarios:
            groups_ids.append(grup_propietarios.id)
        if grupo_permisos_extra:
            groups_ids.append(grupo_permisos_extra.id)

        # Asignar los grupos al usuario
        if groups_ids:
            new_user.groups_id = [(6, 0, groups_ids)]

        # Enviar notificación por correo electrónico
        correo_emisor = 'esteve.ase2004@gmail.com'
        contrasenya_emisor = 'zzuq smod izrq mgpu'  # clave
        correo_receptor = self.correo
        asunto = "¡Bienvenido/a a InstantAbode!"
        mensaje = f"Hola {self.nombreCliente} {self.apellidos}.\n Tu cuenta en nuestra aplicación InstantAbode ha sido creada.\n Usuario: {self.name}\n Contraseña: {self.contrasenya}\n\n Puedes cambiar la contraseña al iniciar sesión en el servidor."

        # Crear el objeto mensaje
        msg = EmailMessage()
        msg['From'] = correo_emisor
        msg['To'] = correo_receptor
        msg['Subject'] = asunto
        msg.set_content(mensaje)

        # Enviar el correo
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(correo_emisor, contrasenya_emisor)
            smtp.sendmail(correo_emisor, correo_receptor, msg.as_string())

        self.notificado = True
