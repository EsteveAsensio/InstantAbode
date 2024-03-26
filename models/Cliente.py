from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class Cliente(models.Model):
    _name = 'instant_abode.cliente'
    _description = 'Información sobre los Clientes que inician sesión en la aplicación.'
    _sql_constraints= [
        ('cliente_dni_uniq', 'UNIQUE (dni)', 'No puede haber dos clientes con el mismo DNI.'),
        ('cliente_correo_uniq', 'UNIQUE (correo)', 'No puede haber dos clientes con el mismo correo.'),
        ('cliente_name_uniq', 'UNIQUE (name)', 'No puede haber dos clientes con el mismo nombre de usuario.'),
        ('cliente_contraseña_uniq', 'UNIQUE (contrasenya)', 'No puede haber dos clientes con la misma contraseña de usuario.'),
        ('cliente_telefono_uniq', 'UNIQUE (telefono)', 'No puede haber dos clientes con el mismo teléfono.')
    ]

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