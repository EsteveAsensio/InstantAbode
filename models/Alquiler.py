from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime

class Alquiler(models.Model):
    _name = 'instant_abode.alquiler'
    _description = 'Información sobre los Alquileres realizados de un cliente a un inmueble'

    name = fields.Char(string='Nombre', compute='crearNombre', store=True)
    fechaInicio = fields.Date(string="Fecha Inicial", help="Fecha inicio instancia", required=True)
    fechaFinal = fields.Date(string="Fecha Final", help="Fecha final instancia", required=True)
    precio = fields.Float(string='Precio Total', compute='modificarPrecio', store=True, readonly=True)
    inmueble = fields.Many2one("instant_abode.inmueble", string="Inmueble", required=True, ondelete="cascade")
    cliente = fields.Many2one("instant_abode.cliente", string="Cliente", required=True)
    valoracionInmueble = fields.Many2one("instant_abode.valoracioninmueble", string="Valoración", readonly=True)

    @api.depends('fechaInicio', 'fechaFinal', 'inmueble')
    def modificarPrecio(self):
        for alquiler in self:
            if alquiler.fechaInicio and alquiler.fechaFinal:
                dias = alquiler.fechaFinal - alquiler.fechaInicio
                dias_alquilados = dias.days + 1  # Se suma 1 para incluir también el último día
                alquiler.precio = dias_alquilados * alquiler.inmueble.precio  # Calcula el precio total

    @api.depends('fechaInicio', 'fechaFinal', 'inmueble')
    def crearNombre(self):
        for alquiler in self:
            alquiler.name = f'Alquiler de {alquiler.inmueble.name} del {alquiler.fechaInicio} al {alquiler.fechaFinal}'

    @api.constrains('fechaInicio', 'fechaFinal', 'inmueble')
    def comprobarFechas(self):
        for alquiler in self:
            if alquiler.fechaInicio > alquiler.fechaFinal:
                raise ValidationError("La fecha de inicio debe ser anterior a la fecha final.")
            
            domain = [
                ('id', '!=', alquiler.id),
                ('inmueble', '=', alquiler.inmueble.id),
                '|',
                '&', ('fechaInicio', '<=', alquiler.fechaInicio), ('fechaFinal', '>=', alquiler.fechaInicio),
                '&', ('fechaInicio', '<=', alquiler.fechaFinal), ('fechaFinal', '>=', alquiler.fechaFinal)
            ]
            overlapped_alquiler = self.env['instant_abode.alquiler'].search_count(domain)
            if overlapped_alquiler:
                raise ValidationError("El inmueble ya está alquilado para este rango de fechas.")