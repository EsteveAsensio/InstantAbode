from odoo import models, fields

class AttachmentInmueble(models.Model):
    _inherit = 'ir.attachment'

    inmueble_id = fields.Many2one(
        'instant_abode.inmueble',
        string='Inmueble Asociado',
        help='Inmueble al que está vinculado este adjunto.',
        ondelete='cascade'
    )
