from odoo import models, api
from odoo.exceptions import AccessError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            raise AccessError("No tienes permiso para crear contactos.")
        return super(ResPartner, self).create(vals)

    def write(self, vals):
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            if any(partner.id != self.env.user.partner_id.id for partner in self):
                raise AccessError("No tienes permiso para modificar este contacto.")
        return super(ResPartner, self).write(vals)

    def unlink(self):
        if self.env.user.has_group('instant_abode.grupo_propietarios'):
            if any(partner.id != self.env.user.partner_id.id for partner in self):
                raise AccessError("No tienes permiso para eliminar este contacto.")
        return super(ResPartner, self).unlink()
