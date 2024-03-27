from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ValoracionCliente(models.Model):
    _name = 'instant_abode.valoracioncliente'
    _description = 'Información de las valoraciones realizadas por un propietario a un cliente'

    #Infomarción
    name = fields.Char(string='Nombre', compute='crearNombre', store=True)
    comentario = fields.Html(string="Comentario", help="Comentario sobre el cliente")
    puntuacion = fields.Integer(string="Valoración", help="Valoración del cliente", required=True)
    fecha = fields.Datetime(string="Fecha", help="Fecha de la reseña", default=fields.Datetime.now, readonly=True)
    #Propietario
    propietario = fields.Many2one("instant_abode.propietario", string="Propietario", ondelete="cascade", required=True)
    #Cliente
    cliente = fields.Many2one("instant_abode.cliente", string="Cliente", ondelete="cascade", required=True)

    @api.depends('fecha', 'propietario', 'cliente')
    def crearNombre(self):
        for valoracion in self:
            fecha_valoracion = valoracion.fecha.strftime("%d/%m/%Y")
            valoracion.name = f'Valoración de {valoracion.propietario.name} a {valoracion.cliente.name} el {fecha_valoracion}'

    @api.constrains("puntuacion")
    def comprobarPuntuacion(self):
        if self.puntuacion < 1:
            raise ValidationError("La valoración debe de tener como mínimo un 1 de puntuación i como máximo un 10")
        if self.puntuacion > 10:
            raise ValidationError("La valoración debe de tener como mínimo un 1 de puntuación i como máximo un 10")