from odoo import models, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def _get_contact_salesperson(self, partner, company):
        if partner and company.contact_salesperson_sync and partner.user_id:
            return partner.user_id
        return self.env['res.users']

    @api.model
    def _get_crm_tags_for_partners(self, partners):
        """{partner_id: [crm.tag ids]} using one search and one batch create."""
        names = set(partners.category_id.mapped('name'))
        if not names:
            return {}
        CrmTag = self.env['crm.tag'].sudo()
        found = {t.name: t.id for t in CrmTag.search([('name', 'in', list(names))])}
        missing = [n for n in names if n not in found]
        if missing:
            for tag in CrmTag.create([{'name': n} for n in missing]):
                found[tag.name] = tag.id
        return {
            p.id: [found[c.name] for c in p.category_id if c.name in found]
            for p in partners
        }

    def _apply_contact_tags(self):
        leads = self.filtered(
            lambda l: l.partner_id
            and (l.company_id or self.env.company).unified_tags
        )
        if not leads:
            return
        tag_map = self._get_crm_tags_for_partners(leads.partner_id)
        for lead in leads:
            new_ids = set(tag_map.get(lead.partner_id.id, [])) - set(lead.tag_ids.ids)
            if new_ids:  # write only when something actually changes
                lead.tag_ids = [(4, i) for i in new_ids]

    @api.onchange('partner_id')
    def _onchange_partner_id_set_contact_tags(self):
        for lead in self.filtered('partner_id'):
            company = lead.company_id or self.env.company
            if company.unified_tags:
                ids = self._get_crm_tags_for_partners(lead.partner_id).get(
                    lead.partner_id.id)
                if ids:
                    lead.tag_ids |= self.env['crm.tag'].browse(ids)
            user = lead._get_contact_salesperson(lead.partner_id, company)
            if user:
                lead.user_id = user

    @api.model_create_multi
    def create(self, vals_list):
        requests = []
        for vals in vals_list:
            if not vals.get('partner_id'):
                continue
            partner = self.env['res.partner'].browse(vals['partner_id'])
            company = (
                self.env['res.company'].browse(vals['company_id'])
                if vals.get('company_id') else self.env.company
            )
            user = self._get_contact_salesperson(partner, company)
            if user:
                vals['user_id'] = user.id
            if company.unified_tags and partner.category_id:
                requests.append((vals, partner))
        if requests:
            partners = self.env['res.partner'].concat(*[p for _, p in requests])
            tag_map = self._get_crm_tags_for_partners(partners)
            for vals, partner in requests:
                ids = tag_map.get(partner.id)
                if ids:
                    vals['tag_ids'] = list(vals.get('tag_ids') or []) + [
                        (4, i) for i in ids]
        return super().create(vals_list)  # single create, no second write

    def write(self, vals):
        if vals.get('partner_id') and 'user_id' not in vals:
            partner = self.env['res.partner'].browse(vals['partner_id'])
            groups = {}
            for lead in self:
                user = lead._get_contact_salesperson(
                    partner, lead.company_id or self.env.company)
                groups[user.id] = groups.get(user.id, self.browse()) | lead
            for user_id, leads in groups.items():
                super(CrmLead, leads).write(
                    dict(vals, user_id=user_id) if user_id else vals)
            res = True
        else:
            res = super().write(vals)
        if vals.get('partner_id'):
            self._apply_contact_tags()
        return res