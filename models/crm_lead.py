from odoo import api, models


class Lead(models.Model):
    _inherit = "crm.lead"

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        res._set_last_crm_id_in_partner()
        return res

    def _set_last_crm_id_in_partner(self):
        for lead in self:
            if not lead.partner_id:
                continue
            lead.partner_id.last_crm_lead_id = lead.id
