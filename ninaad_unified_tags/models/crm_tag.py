from odoo import models

class CrmTag(models.Model):
    _name = 'crm.tag'
    _inherit = ['crm.tag', 'tag.sync.mixin']

    _mirror_model = 'res.partner.category'
