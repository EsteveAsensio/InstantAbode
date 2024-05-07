from odoo import models, fields, api
from odoo.exceptions import ValidationError, AccessError

class ValoracionCliente(models.Model):
    _name = 'instant_abode.valoracioncliente'
    _description = 'Información de las valoraciones realizadas por un propietario a un cliente'
    _sql_constraints = [
        ('unique_valoracion_cliente', 'unique(propietario, cliente)', 'Solo se puede realizar una valoración por cliente.'),
        ('unique_name', 'unique(name)', 'Ese nombre ya está registrado')
    ]
    #Infomarción
    name = fields.Char(string='Nombre', compute='crearNombre', store=True)
    comentario = fields.Char(string="Comentario", help="Comentario sobre el cliente")
    puntuacion = fields.Integer(string="Valoración", help="Valoración del cliente", required=True)
    fecha = fields.Datetime(string="Fecha", help="Fecha de la reseña", default=fields.Datetime.now, readonly=True)
    #Propietario
    propietario = fields.Many2one("instant_abode.propietario", string="Propietario", ondelete="cascade", default=lambda self: self.default_propietario())
    #Cliente
    cliente = fields.Many2one("instant_abode.cliente", string="Cliente", ondelete="cascade", required=True)

    @api.model
    def default_propietario(self):
        # Aquí se busca el propietario relacionado al usuario que ha iniciado sesión
        propietario_id = self.env['instant_abode.propietario'].search([('user_id', '=', self.env.uid)], limit=1)
        return propietario_id
    
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

    @api.constrains('propietario', 'cliente')
    def alquilerPrevio(self):
        for valoracion in self:
            # Verificar si el cliente ha alquilado al menos un inmueble del propietario
            alquileres = self.env['instant_abode.alquiler'].search([
                ('cliente', '=', valoracion.cliente.id),
                ('inmueble.propietario', '=', valoracion.propietario.id)
            ])
            if not alquileres:
                raise ValidationError("El cliente debe haber alquilado al menos un inmueble del propietario para ser valorado.")
            
    @api.constrains('propietario', 'cliente')
    def alquilerPrevio(self):
        for valoracion in self:
            alquileres = self.env['instant_abode.alquiler'].search([
                ('cliente', '=', valoracion.cliente.id),
                ('inmueble.propietario', '=', valoracion.propietario.id)
            ])
            if not alquileres:
                raise ValidationError("El cliente debe haber alquilado al menos un inmueble del propietario para ser valorado.")

    @api.model
    def create(self, vals):
        # Verificar si el usuario pertenece al grupo de propietarios
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            propietario_id = self.env['instant_abode.propietario'].search([('user_id', '=', self.env.uid)], limit=1)
            if not propietario_id:
                raise AccessError("No tiene permisos para realizar esta acción.")
            
            # Verifica que el propietario ha alquilado al cliente
            cliente_id = vals.get('cliente')
            alquiler_count = self.env['instant_abode.alquiler'].search_count([
                ('cliente', '=', cliente_id),
                ('inmueble.propietario', '=', propietario_id.id)
            ])
            if alquiler_count == 0:
                raise AccessError("El cliente debe haber alquilado al menos un inmueble del propietario para ser valorado.")

        return super(ValoracionCliente, self).create(vals)

    def write(self, vals):
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            for record in self:
                if record.propietario.user_id != self.env.user:
                    raise AccessError("Solo puede modificar las valoraciones que usted mismo ha realizado.")
        return super(ValoracionCliente, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            for record in self:
                if record.propietario.user_id != self.env.user:
                    raise AccessError("Solo puede eliminar las valoraciones que usted mismo ha realizado.")
        return super(ValoracionCliente, self).unlink()