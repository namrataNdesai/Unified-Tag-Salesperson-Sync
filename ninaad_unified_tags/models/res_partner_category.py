from odoo import models


class ResPartnerCategory(models.Model):
    _name = 'res.partner.category'
    _inherit = ['res.partner.category', 'tag.sync.mixin']

    _mirror_model = 'crm.tag'
