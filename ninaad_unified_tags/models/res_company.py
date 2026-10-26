from odoo import fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    unified_tags = fields.Boolean(
        string="Unify Lead & Contact Tags",
        help="If enabled, lead tags and contact tags are shared (same names in both) "
             "and duplicate names are not allowed.",
    )

    contact_salesperson_sync = fields.Boolean(
        string="Use Contact Salesperson on Leads",
        help="If enabled, selecting a contact on a lead or opportunity sets "
             "the lead's Salesperson to the contact's Salesperson.",
    )

    def write(self, vals):
        res = super().write(vals)
        if vals.get('unified_tags'):
            self.env['crm.tag']._sync_all_tags()
        return res
