from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class ValoracionInmueble(models.Model):
    _name = 'instant_abode.valoracioninmueble'
    _description = 'Información de las valoraciones realizadas por un cliente a un inmueble'

    #Infomarción
    name = fields.Char(string='Nombre', compute='crearNombre', store=True)
    comentario = fields.Char(string="Comentario", help="Comentario sobre el inmueble")
    puntuacion = fields.Integer(string="Valoración", help="Valoración del inmueble", required=True)
    fecha = fields.Date(string="Fecha", help="Fecha de la reseña", default=fields.Date.today, readonly=True)
    #Alquiler
    alquiler = fields.Many2one("instant_abode.alquiler", string="Alquiler", required=True, ondelete="cascade")
    #Cliente
    cliente = fields.Many2one("instant_abode.cliente", string="Cliente", readonly=True, ondelete="cascade")
    #Inmueble
    inmueble = fields.Many2one("instant_abode.inmueble", string="Inmueble", readonly=True, ondelete="cascade")

    @api.depends('fecha', 'inmueble', 'cliente', 'alquiler')
    def crearNombre(self):
        for valoracion in self:
            fecha_valoracion = valoracion.fecha.strftime("%d/%m/%Y")
            valoracion.name = f'Valoración de {valoracion.cliente.name} a {valoracion.inmueble.name} el {fecha_valoracion}'
    @api.constrains("puntuacion")
    def comprobarPuntuacion(self):
        if self.puntuacion < 1:
            raise ValidationError("La valoración debe de tener como mínimo un 1 de puntuación i como máximo un 10")
        if self.puntuacion > 10:
            raise ValidationError("La valoración debe de tener como mínimo un 1 de puntuación i como máximo un 10")

    @api.constrains("alquiler")
    def modificarClienteInmueble(self):
        self.cliente = self.alquiler.cliente
        self.inmueble = self.alquiler.inmueble
