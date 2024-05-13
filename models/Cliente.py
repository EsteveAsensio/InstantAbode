from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Cliente(models.Model):
    _name = 'instant_abode.cliente'
    _description = 'Información sobre los Clientes que inician sesión en la aplicación.'

    #Infomarción Personal
    dni = fields.Char(string="DNI", help="DNI del cliente", required=True) #No repetidos y formato
    nombreCliente = fields.Char(string="Nombre", help="Nombre del cliente", required=True)
    apellidos = fields.Char(string="Apellidos", help="Apellidos del cliente")
    correo = fields.Char(string="Correo", help="Correo del cliente", required=True) #No repetidos y formato
    telefono = fields.Char(string="Teléfono", help="Teléfono del cliente") #No repetidos y numeros
    #Información Cuenta Usuario
    name = fields.Char(string="Nombre de Usuario", help="Nombre del usuario", required=True) #No repetidos
    contrasenya = fields.Char(string="Contraseña", help="Contraseña del usuario", required=True) #No repetidos y formato
    imagen = fields.Binary(string="Imagen", help="Foto del cliente", store=True)
    #Valoraciones Recibidas
    valoraciones = fields.One2many("instant_abode.valoracioncliente", "cliente", readonly=True)
    #Alquileres
    alquileres = fields.One2many("instant_abode.alquiler", "cliente")

    user_id = fields.Many2one("res.users", string="Usuario Asociado", readonly=True)

        
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
        partner = self.env['res.partner'].create({
            'name': vals.get('nombreCliente'),
            'email': vals.get('correo'),
            'phone': vals.get('telefono'),
            'vat': vals.get('dni'),
            'image_1920': vals.get('imagen'),
        })

        cliente = super(Cliente, self).create(vals)

        # Creación del usuario con los grupos adecuados
        new_user = self.env['res.users'].create({
            'name': cliente.nombreCliente,
            'login': cliente.name,
            'partner_id': partner.id,
            'password': cliente.contrasenya,
            'image_1920': cliente.imagen
        })

        cliente.user_id = new_user.id

        #Buscar los grupos necesarios
        grupo_clientes = self.env['res.groups'].search([('name', '=', 'Clientes')], limit=1)
        grupo_permisos_extra = self.env['res.groups'].search([('name', '=', 'Creación de contactos')], limit=1)

        # Lista para mantener los ids de los grupos
        groups_ids = []
        if grupo_clientes:
            groups_ids.append(grupo_clientes.id)
        if grupo_permisos_extra:
            groups_ids.append(grupo_permisos_extra.id)

        # Asignar los grupos al usuario
        if groups_ids:
            new_user.groups_id = [(6, 0, groups_ids)]

        return cliente


    def unlink(self):
        for cliente in self:
            if cliente.user_id:
                # Obtener el partner asociado al usuario
                partner = cliente.user_id.partner_id
                # Eliminar el usuario
                cliente.user_id.unlink() 
                if partner:
                    partner.unlink()

        return super(Cliente, self).unlink()

    
    def write(self, vals):
        self.validar_unicidad(vals)

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
            
        return super(Cliente, self).write(vals)


    def validar_unicidad(self, vals):
        # Validar que el campo no sea None antes de hacer la búsqueda
        if 'dni' in vals and vals.get('dni') and vals.get('dni') != self.dni:
            existing_dni = self.env['res.partner'].search([('vat', '=', vals['dni']), ('id', '!=', self.user_id.partner_id.id)])
            if existing_dni:
                raise ValidationError(f"El DNI {vals['dni']} ya está registrado.")

        if 'correo' in vals and vals.get('correo') and vals.get('correo') != self.correo:
            existing_correo = self.env['res.partner'].search([('email', '=', vals['correo']), ('id', '!=', self.user_id.partner_id.id)])
            if existing_correo:
                raise ValidationError(f"El correo {vals['correo']} ya está registrado.")

        if 'telefono' in vals and vals.get('telefono') and vals.get('telefono') != self.telefono:
            existing_telefono = self.env['res.partner'].search([('phone', '=', vals['telefono']), ('id', '!=', self.user_id.partner_id.id)])
            if existing_telefono:
                raise ValidationError(f"El teléfono {vals['telefono']} ya está registrado.")

        if 'name' in vals and vals.get('name') and vals.get('name') != self.name:
            existing_login = self.env['res.users'].search([('login', '=', vals['name']), ('id', '!=', self.user_id.id)])
            if existing_login:
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

