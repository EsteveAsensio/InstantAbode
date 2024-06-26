from odoo import models, fields, api

class Inmueble(models.Model):
    _name = 'instant_abode.inmueble'
    _description = 'Información sobre los Inmuebles introducios por los propietarios.'
    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Ese nombre ya está registrado')
    ]

    name = fields.Char(string="Nombre", help="Características básicas del inmueble", required=True) 
    provincia = fields.Char(string="Provincia", help="Provincia donde se localiza el inmueble", required=True)
    localizacion = fields.Char(string="Localización", help="Localización del inmueble", required=True)
    habitaciones = fields.Integer(string="Habitaciones", help="Habitaciones del inmueble", required=True)
    banyos = fields.Integer(string="Baños", help="Baños del inmueble", required=True)
    metrosCuadrados = fields.Integer(string="Metros Cuadrados", help="Metros cuadrados del inmueble", required=True)
    descripcion = fields.Char(string="Descripción", help="Descripción del inmueble")
    adicionales = fields.Char(string="Adicionales", help="Datos adicionales del inmueble")
    imagenPrincipal = fields.Binary(string="Imagen Principal", help="Foto principal del inmueble, será la primera imagen que se mostrará al cliente", store=True, required=True)
    imagenes = fields.One2many('ir.attachment', 'inmueble_id', string='Imágenes')
    precio = fields.Float(string="Precio", help="Precio del inmueble, puede variar dependiendo de la instancia en el", required=True)
    #Propietario
    propietario = fields.Many2one("instant_abode.propietario", string="Propietario", ondelete="cascade", default=lambda self: self.default_propietario(), required=True)
    #Alquileres
    alquileres = fields.One2many("instant_abode.alquiler", "inmueble")
    #Dar de alta
    state=fields.Selection(string="Cara al Público", selection=[('Mostrar', 'Activo'), ('Ocultar', 'Inactivo')], default="Ocultar", readonly=True)

    @api.model
    def default_propietario(self):
        # Aquí se busca el propietario relacionado al usuario que ha iniciado sesión
        propietario_id = self.env['instant_abode.propietario'].search([('user_id', '=', self.env.uid)], limit=1)
        return propietario_id

    def mostrarPublico(self):
        self.state = 'Mostrar'

    def ocultarPublico(self):
        self.state = 'Ocultar'