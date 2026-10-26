from odoo import api, models, _
from odoo.exceptions import ValidationError


class TagSyncMixin(models.AbstractModel):
    _name = 'tag.sync.mixin'
    _description = 'Tag Sync Mixin'

    _mirror_model = None  # set in child

    def _unified_enabled(self):
        return bool(self.env.company.unified_tags) and not self.env.context.get('skip_tag_sync')

    def _find_by_name(self, model, name, exclude=None):
        domain = [('name', '=ilike', name.strip())]
        recs = self.env[model].with_context(active_test=False).sudo().search(domain)
        return recs - exclude if exclude else recs

    def _check_unique_name(self, name, exclude=None):
        """exclude: dict {model_name: recordset} of records allowed to have this name."""
        exclude = exclude or {}
        for model in (self._name, self._mirror_model):
            if self._find_by_name(model, name, exclude.get(model)):
                raise ValidationError(_(
                    "A tag named '%s' already exists (in leads or contacts). "
                    "Tag names must be unique across both.", name))

    @api.model_create_multi
    def create(self, vals_list):
        if not self._unified_enabled():
            return super().create(vals_list)
        seen = set()
        for vals in vals_list:
            name = (vals.get('name') or '').strip()
            if not name:
                continue
            if name.lower() in seen:
                raise ValidationError(_("Duplicate tag name '%s'.", name))
            seen.add(name.lower())
            self._check_unique_name(name)
        records = super().create(vals_list)
        Mirror = self.env[self._mirror_model].sudo().with_context(skip_tag_sync=True)
        Mirror.create([{'name': r.name, 'color': r.color} for r in records])
        return records

    def write(self, vals):
        if 'name' not in vals or not self._unified_enabled():
            return super().write(vals)
        new_name = (vals['name'] or '').strip()
        mirrors = self.env[self._mirror_model].sudo()
        for rec in self:
            mirrors |= self._find_by_name(self._mirror_model, rec.name)
        if new_name:
            self._check_unique_name(new_name, {self._name: self, self._mirror_model: mirrors})
        res = super().write(vals)
        mirrors.with_context(skip_tag_sync=True).write({'name': vals['name']})
        return res

    @api.model
    def _sync_all_tags(self):
        """Create missing counterparts so both models have the same names."""
        Lead = self.env['crm.tag'].sudo().with_context(skip_tag_sync=True)
        Partner = self.env['res.partner.category'].sudo().with_context(skip_tag_sync=True, active_test=False)
        lead_names = {t.name.strip().lower(): t for t in Lead.search([])}
        partner_names = {t.name.strip().lower(): t for t in Partner.search([])}
        Partner.create([{'name': t.name, 'color': t.color}
                        for k, t in lead_names.items() if k not in partner_names])
        Lead.create([{'name': t.name, 'color': t.color}
                     for k, t in partner_names.items() if k not in lead_names])
