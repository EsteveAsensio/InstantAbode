from odoo import models, fields, api

class Inmueble(models.Model):
    _name = 'instant_abode.inmueble'
    _description = 'Información sobre los Inmuebles introducios por los propietarios.'

    name = fields.Char(string="Nombre", help="Características básicas del inmueble", required=True) 
    provincia = fields.Char(string="Provincia", help="Provincia donde se localiza el inmueble", required=True)
    localizacion = fields.Char(string="Localización", help="Localización del inmueble", required=True)
    habitaciones = fields.Integer(string="Habitaciones", help="Habitaciones del inmueble", required=True)
    banyos = fields.Integer(string="Baños", help="Baños del inmueble", required=True)
    metrosCuadrados = fields.Integer(string="Metros Cuadrados", help="Metros cuadrados del inmueble", required=True)
    descripcion = fields.Html(string="Descripción", help="Descripción del inmueble")
    adicionales = fields.Char(string="Adicionales", help="Datos adicionales del inmueble")
    #Propietario
    propietario = fields.Many2one("instant_abode.propietario", string="Propietario", ondelete="cascade", required=True)
    #Alquileres
    alquileres = fields.One2many("instant_abode.alquiler", "inmueble")
    #Dar de alta
    state=fields.Selection(string="Cara al Público", selection=[('Mostrar', 'Activo'), ('Ocultar', 'Desactivo')], default="Ocultar", readonly=True)

    def mostrarPublico(self):
        self.state = 'Mostrar'

    def ocultarPublico(self):
        self.state = 'Ocultar'