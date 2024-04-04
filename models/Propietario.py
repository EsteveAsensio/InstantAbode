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
    _sql_constraints= [
        ('propietario_dni_uniq', 'UNIQUE (dni)', 'No puede haber dos propietario con el mismo DNI.'),
        ('propietario_correo_uniq', 'UNIQUE (correo)', 'No puede haber dos propietario con el mismo correo.'),
        ('propietario_name_uniq', 'UNIQUE (name)', 'No puede haber dos propietario con el mismo nombre de usuario.'),
        ('propietario_contraseña_uniq', 'UNIQUE (contrasenya)', 'No puede haber dos propietario con la misma contraseña de usuario.'),
        ('propietario_telefono_uniq', 'UNIQUE (telefono)', 'No puede haber dos propietario con el mismo teléfono.')
    ]

    #Infomarción Personal
    dni = fields.Char(string="DNI", help="DNI del propietario", required=True) #No repetidos y formato
    nombreCliente = fields.Char(string="Nombre", help="Nombre del propietario", required=True)
    apellidos = fields.Char(string="Apellidos", help="Apellidos del propietario")
    correo = fields.Char(string="Correo", help="Correo del propietario", required=True) #No repetidos y formato
    telefono = fields.Char(string="Teléfono", help="Teléfono del propietario") #No repetidos y numeros
    #Información Cuenta Usuario
    name = fields.Char(string="Nombre de Usuario", help="Nombre del usuario", required=True) #No repetidos
    contrasenya = fields.Char(string="Contraseña", help="Contraseña del usuario", required=True) #No repetidos y formato
    imagen = fields.Binary(string="Imagen", help="Foto del propietario", store=True)
    #Valoraciones hacia Clientes
    valoracionesClientes = fields.One2many("instant_abode.valoracioncliente", "propietario")
    #Inmuebles Propietario
    inmuebles = fields.One2many("instant_abode.inmueble", "propietario")

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
        
    def nuevoUsuarioNotificacion(self):
        nombre = self.usuarioAleatorio()
        contrasenya = self.contrasenyAleatoria()

        # Verificar
        while self.env['instant_abode.propietario'].search([('name', '=', nombre)]) or \
                self.env['instant_abode.propietario'].search([('contrasenya', '=', contrasenya)]):
            nombre = self.usuarioAleatorio()
            contrasenya = self.contrasenyAleatoria()

        while self.env['instant_abode.cliente'].search([('name', '=', nombre)]) or \
            self.env['instant_abode.cliente'].search([('contrasenya', '=', contrasenya)]):
            nombre = self.usuarioAleatorio()
            contrasenya = self.contrasenyAleatoria()

        self.name = nombre
        self.contrasenya = contrasenya

    def contrasenyAleatoria(self):
        especiales = string.punctuation
        digitos = string.digits
        letras = string.ascii_letters

        longitud = random.randint(5, 15)  # Longitud aleatoria entre 5 y 15 caracteres

        # Al menos un carácter especial, un dígito y cinco letras
        contrasenya = ''.join(random.choice(especiales) +
                              random.choice(digitos) +
                              ''.join(random.choice(letras) for _ in range(5)) +
                              ''.join(random.choice(especiales + digitos + letras) for _ in range(longitud - 7)))

        # Mezcla los caracteres de la contraseña
        contrasenya = ''.join(random.sample(contrasenya, len(contrasenya)))
        return contrasenya

    def usuarioAleatorio(self):
        nombre_usuario = ''.join(random.choices(string.ascii_lowercase, k=6))  # Genera un nombre de usuario de 8 caracteres
        return nombre_usuario
    
    def notificarPropietario(self):
        # Configuración del servidor SMTP
        correo_emisor = 'esteve.ase2004@gmail.com'
        contrasenya_emisor = 'zzuq smod izrq mgpu'  # clave
        correo_receptor = self.correo

        asunto = "¡Bienvenido/a a InstantAbode!"
        mensaje = (
            f'Hola {self.nombreCliente} {self.apellidos}.\n La petición para hacerte propietario/a en nuestra aplicación InstantAbode ha sido aceptada.\n'
            f'Tu nuevo usuario y contraseña son los siguientes:\n\nUsuario: {self.name}\nContraseña: {self.contrasenya}\n\n'
            f'Estos datos pueden ser modificados al entrar dentro de la aplicación > Perfil.\nMuchas gracias por confiar en nosotros.'
        )

        # Crear el objeto mensaje
        msg = EmailMessage()
        msg['From'] = correo_emisor
        msg['To'] = correo_receptor
        msg['Subject'] = asunto
        msg.set_content(mensaje)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context= context) as smtp:
            smtp.login(correo_emisor, contrasenya_emisor)
            smtp.sendmail(correo_emisor, correo_receptor, msg.as_string())
